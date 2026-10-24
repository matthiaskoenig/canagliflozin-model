"""Simulation experiment of the study Tamborlane2018."""

from typing import ClassVar, NamedTuple, override

from pkpdsim.metadata import (
    ApplicationForm,
    Coadministration,
    Dosing,
    Fasting,
    Health,
    PKPDMappingMetaData,
    Route,
    Tissue,
)
from sbmlsim import Q
from sbmlsim.data import DataSet
from sbmlsim.fit import FitData, FitMapping
from sbmlsim.plot import Axis, Figure
from sbmlsim.simulation import Change, Simulation
from sbmlsim.units import Quantity

from pkdb_models.models.canagliflozin import MODEL
from pkdb_models.models.canagliflozin.experiments.base_experiment import (
    CanagliflozinSimulationExperiment,
)


class Group(NamedTuple):
    """A group of Tamborlane2018 (Table 1, the mean plasma glucose of Fig 5)."""

    bodyweight: float  # [kg]
    fpg: float  # fasting plasma glucose [mg/dl]
    gfr: float  # eGFR (Schwartz) [ml/min/1.73 m^2]
    mpg: float  # 24-hr mean plasma glucose of day -1 [mg/dl]
    mpg_d14: float  # 24-hr mean plasma glucose of day 14 [mg/dl]


class Tamborlane2018(CanagliflozinSimulationExperiment):
    """Simulation experiment of Tamborlane2018.

    Children and adolescents (10 - 17 years, obese) with type 2 diabetes on a
    stable dose of metformin (>= 1000 mg/day), a placebo tablet on day -1, then
    canagliflozin 100 or 300 mg once daily in the morning on days 1 - 14; food
    not reported. Plasma canagliflozin of day 14 for 72 hr, the urinary glucose
    (UGE) of 0 - 12 and 0 - 24 hr of day -1 and day 14, the mean renal
    threshold of glucose (RTG) of 0 - 12 and 12 - 24 hr of day 14.

    The simulation starts with day -1 (the first dose at 24 hr) and is shifted
    so that the dose of day 14 is at 0 hr.
    """

    groups: ClassVar[dict[int, Group]] = {
        100: Group(116.8, 134.0, 135.8, 147, 115),
        300: Group(98.6, 106.3, 161.3, 110, 96),
    }

    #: the first dose (day 1) after day -1 [hr]
    time_first = 24
    #: the dose of day 14 [hr]
    time_last = 24 * 14
    #: mg/dl of glucose per mM
    mgdl_per_mM = 18.016

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1", "Fig3", "Fig4"]:
            df = self.load_dataframe(fig_id)
            if fig_id == "Fig4":
                # the urine of day -1 and of day 14, two collections
                df["label"] = df["label"] + df["time"].map(
                    lambda t: "_baseline" if t < 0 else ""
                )
            for label, df_label in df.groupby("label"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)
                # unit conversion to mole/l
                if label.startswith("canagliflozin_"):
                    dset.unit_conversion("mean", 1 / self.Mr.can)
                elif label.startswith("renal_threshold"):
                    dset.unit_conversion("mean", 1 / self.Mr.glc)

                dsets[label] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}
        resets: dict[str, Quantity] = {
            "KI__glc_urine": Q(0, "mmole"),
            "KI__RTG_int": Q(0, "mM*min"),
            "KI__RTG_time": Q(0, "min"),
        }
        for dose, group in self.groups.items():
            fpg = group.fpg / self.mgdl_per_mM
            # the filtered glucose is the 24-hr mean plasma glucose of day -1
            # before and of day 14 after the first dose, the FPG of day -1 (the
            # shift of the RTG in diabetes) is kept; the urine is collected
            # from dose to dose, the RTG of day 14 over 0 - 12 and 12 - 24 hr
            tcsims[f"po_can{dose}"] = Simulation(
                time_unit="hr",
                end=self.time_last + 72,
                preinit_changes={
                    **self.default_changes(),
                    "BW": Q(group.bodyweight, "kg"),
                    "[KI__fpg]": Q(fpg, "mM"),
                    "KI__PG_delta": Q(group.mpg / self.mgdl_per_mM - fpg, "mM"),
                    "KI__f_renal_function": Q(group.gfr / 101, "dimensionless"),
                },
                changes=[
                    Change(
                        self.time_first,
                        {
                            "KI__PG_delta": Q(
                                group.mpg_d14 / self.mgdl_per_mM - fpg, "mM"
                            ),
                        },
                    ),
                    Change(
                        list(range(self.time_first, self.time_last + 1, 24)), resets
                    ),
                    self.add_doses(
                        list(range(self.time_first, self.time_last + 1, 24)),
                        {"PODOSE_can": Q(dose, "mg")},
                    ),
                    Change(
                        self.time_last + 12,
                        {"KI__RTG_int": Q(0, "mM*min"), "KI__RTG_time": Q(0, "min")},
                    ),
                ],
                time_shift=-self.time_last,
            )

        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}

        for key, (dataset, sid, tissue) in {
            "plasma": ("canagliflozin", "[Cve_can]", Tissue.PLASMA),
            "uge_baseline": ("glucose_cumulative_amount", "KI__UGE", Tissue.URINE),
            "uge": ("glucose_cumulative_amount", "KI__UGE", Tissue.URINE),
            "rtg": ("renal_threshold", "KI__RTG_mean", Tissue.PLASMA),
        }.items():
            suffix = "_baseline" if key.endswith("_baseline") else ""
            for dose in self.groups:
                mappings[f"fm_can{dose}_{key}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=f"{dataset}_CAN{dose}{suffix}",
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                    ),
                    observable=FitData(
                        self, task=f"task_po_can{dose}", xid="time", yid=sid
                    ),
                    metadata=PKPDMappingMetaData(
                        tissue=tissue,
                        route=Route.PO,
                        application_form=ApplicationForm.TABLET,
                        dosing=Dosing.MULTIPLE,
                        health=Health.T2DM,
                        fasting=Fasting.NR,
                        coadministration=Coadministration.METFORMIN,
                    ),
                )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        return {**self.figure_plasma(), **self.figure_pd()}

    def figure_plasma(self) -> dict[str, Figure]:
        """Canagliflozin in plasma of day 14."""
        fig = Figure(
            experiment=self,
            sid="Fig_plasma",
            num_cols=2,
            name=f"{self.__class__.__name__} (T2DM, pediatric)",
        )
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit=self.unit_time, min=-2, max=74),
            legend=True,
        )
        plots[0].set_yaxis(self.label_can, unit=self.unit_can)
        plots[1].set_yaxis(self.label_can, unit=self.unit_can, scale="log")
        for plot in plots:
            for dose in self.groups:
                plot.add_data(
                    task=f"task_po_can{dose}",
                    xid="time",
                    yid="[Cve_can]",
                    label=f"{dose} mg PO",
                    color=self.dose_colors[dose],
                )
                plot.add_data(
                    dataset=f"canagliflozin_CAN{dose}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=f"{dose} mg PO",
                    color=self.dose_colors[dose],
                )

        return self.figures_by_sid(fig)

    def figure_pd(self) -> dict[str, Figure]:
        """Urinary glucose of day -1 and day 14, mean RTG of day 14."""
        fig = Figure(
            experiment=self,
            sid="Fig_pd",
            num_cols=3,
            name=f"{self.__class__.__name__} (T2DM, pediatric)",
        )
        # the legends inside the panels cover data
        fig.settings = {**fig.settings, "legend_position": "outside"}
        plots = fig.create_plots(legend=True)
        plots[0].set_xaxis(
            f"{self.label_time} (day -1)", unit=self.unit_time, min=-337, max=-311
        )
        for plot in plots[1:]:
            plot.set_xaxis(
                f"{self.label_time} (day 14)", unit=self.unit_time, min=-1, max=25
            )
        plots[0].set_yaxis(self.label_uge, unit=self.unit_uge, min=-2, max=30)
        plots[1].set_yaxis(self.label_uge, unit=self.unit_uge, min=-2, max=120)
        plots[2].set_yaxis(self.label_rtg_mean, unit=self.unit_rtg, min=2, max=8)

        for k, (sid, dataset, suffix) in enumerate(
            [
                ("KI__UGE", "glucose_cumulative_amount", "_baseline"),
                ("KI__UGE", "glucose_cumulative_amount", ""),
                ("KI__RTG_mean", "renal_threshold", ""),
            ]
        ):
            for dose in self.groups:
                plots[k].add_data(
                    task=f"task_po_can{dose}",
                    xid="time",
                    yid=sid,
                    label=f"{dose} mg PO",
                    color=self.dose_colors[dose],
                )
                plots[k].add_data(
                    dataset=f"{dataset}_CAN{dose}{suffix}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=f"{dose} mg PO",
                    color=self.dose_colors[dose],
                )
        # the 24-hr mean RTG of the same patients (not mapped)
        for dose in self.groups:
            plots[2].add_data(
                dataset=f"renal_threshold_mean24_CAN{dose}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"{dose} mg PO (24-hr mean)",
                color=self.dose_colors[dose],
                marker="D",
                markerfacecolor="white",
                markeredgecolor=self.dose_colors[dose],
            )

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(Tamborlane2018, output_dir=Tamborlane2018.__name__)

"""Simulation experiment of the study Devineni2013."""

from typing import ClassVar, override

from pkpdsim.metadata import (
    ApplicationForm,
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


class Devineni2013(CanagliflozinSimulationExperiment):
    """Simulation experiment of Devineni2013."""

    bodyweights: ClassVar[dict[int, float]] = {0: 84.2, 50: 82.9, 100: 82.2, 300: 83.2}
    #: FPG on day -2 [mg/dl]
    fpg: ClassVar[dict[int, float]] = {0: 182, 50: 189, 100: 182, 300: 185}
    #: mean plasma glucose of 0-24 hr (MPG0-24) on day -1 (baseline), day 1 and
    #: day 7 [mg/dl] (Table 3), the glucose which is filtered
    mpg: ClassVar[dict[int, dict[str, float]]] = {
        0: {"d0": 207, "d1": 214, "d7": 215},
        50: {"d0": 217, "d1": 190, "d7": 185},
        100: {"d0": 195, "d1": 169, "d7": 158},
        300: {"d0": 197, "d1": 164, "d7": 151},
    }
    #: eGFR on day 1 [ml/min/1.73 m^2]
    gfr: ClassVar[dict[int, float]] = {0: 117.9, 50: 110.1, 100: 106.3, 300: 121.8}

    doses: ClassVar[list[int]] = [0, 50, 100, 300]

    info: ClassVar[dict[str, str]] = {
        "can": "canagliflozin",
        "m5": "M5",
        "m7": "M7",
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1", "Tab2A", "Tab3A"]:
            df = self.load_dataframe(fig_id)
            # the zero amounts at the start of the urine collection of day 7 lie
            # at the reset of the collection of day 6 and carry no information
            if fig_id == "Tab2A":
                df = df[~(df.label.str.endswith("_d7") & (df.time == 0))]
            for label, df_label in df.groupby("label"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)
                # unit conversion to mole/l; the amounts of the metabolites in
                # the urine are canagliflozin equivalents (% of the dose with
                # the molecular weight of canagliflozin, Table 2)
                if label.startswith(
                    ("canagliflozin_", "M5_cumulative_amount", "M7_cumulative_amount")
                ):
                    dset.unit_conversion("mean", 1 / self.Mr.can)
                elif label.startswith("M5_"):
                    dset.unit_conversion("mean", 1 / self.Mr.m5)
                elif label.startswith("M7_"):
                    dset.unit_conversion("mean", 1 / self.Mr.m7)
                elif label.startswith("glucose_renal_threshold"):
                    dset.unit_conversion("mean", 1 / self.Mr.glc)
                dsets[label] = dset
        return dsets

    def _group_changes(self, dose: int, day: str) -> dict[str, Quantity]:
        """Get the characteristics of a group.

        Args:
            dose: the dose of the group [mg].
            day: the day of the mean plasma glucose (`d0`, `d1`, `d7`).

        Returns:
            The body weight, FPG, mean plasma glucose and renal function.
        """
        fpg = (Q(self.fpg[dose], "mg/dl") / self.Mr.glc).to("mM")
        mpg = (Q(self.mpg[dose][day], "mg/dl") / self.Mr.glc).to("mM")
        return {
            "BW": Q(self.bodyweights[dose], "kg"),
            "[KI__fpg]": fpg,
            "KI__PG_delta": mpg - fpg,
            "KI__f_renal_function": Q(self.gfr[dose] / 101, "dimensionless"),
        }

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}

        # single dose
        for dose in self.doses:
            tcsims[f"po_can{dose}_single"] = Simulation(
                time_unit="hr",
                end=25,
                preinit_changes={
                    **self.default_changes(),
                    **self._group_changes(dose, "d1"),
                    "PODOSE_can": Q(dose, "mg"),
                },
            )

        # multiple dose: the placebo baseline day -1, then doses every 24 hr from
        # 24 to 168 hr (days 1 to 7); the urine and the RTG are collected from
        # dose to dose, the data at the end of a collection is compared with
        # the state before the reset. The mean plasma glucose of day 7 holds
        # from day 2 on.
        resets = {
            "KI__glc_urine": Q(0, "mmole"),  # reset UGE
            "KI__RTG_int": Q(0, "mM*min"),  # reset RTG
            "KI__RTG_time": Q(0, "min"),
            "Aurine_can": Q(0, "mmole"),  # reset canagliflozin
            "Aurine_m5": Q(0, "mmole"),  # reset M5
            "Aurine_m7": Q(0, "mmole"),  # reset M7
        }
        for dose in self.doses:
            tcsims[f"po_can{dose}_multi"] = Simulation(
                time_unit="hr",
                end=193,
                preinit_changes={
                    **self.default_changes(),
                    **self._group_changes(dose, "d0"),
                    "PODOSE_can": Q(0, "mg"),
                },
                changes=[
                    Change(
                        24,
                        {
                            **resets,
                            "KI__PG_delta": self._group_changes(dose, "d1")[
                                "KI__PG_delta"
                            ],
                        },
                    ),
                    Change(
                        [24 * k for k in range(2, 8)],
                        {
                            **resets,
                            "KI__PG_delta": self._group_changes(dose, "d7")[
                                "KI__PG_delta"
                            ],
                        },
                    ),
                    self.add_doses(
                        [24 * k for k in range(1, 8)], {"PODOSE_can": Q(dose, "mg")}
                    ),
                ],
                time_shift=-7 * 24,
            )

        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}

        for name, sid in [
            ("canagliflozin", "[Cve_can]"),
            ("canagliflozin_cumulative_amount", "Aurine_can"),
            ("M5_cumulative_amount", "Aurine_m5"),
            ("M7_cumulative_amount", "Aurine_m7"),
        ]:
            for day in ["d1", "d7"]:
                type_dosing = "single" if day == "d1" else "multi"
                for dose in self.doses[1:]:
                    mappings[f"fm_po_can{dose}_{name}_{day}"] = FitMapping(
                        self,
                        reference=FitData(
                            self,
                            dataset=f"{name}_CAN{dose}_{day}",
                            xid="time",
                            yid="mean",
                            yid_sd="mean_sd",
                            count="count",
                        ),
                        observable=FitData(
                            self,
                            task=f"task_po_can{dose}_{type_dosing}",
                            xid="time",
                            yid=sid,
                        ),
                        # dosed 10 min before a standardized breakfast, the
                        # convention of the studies is fasted
                        metadata=PKPDMappingMetaData(
                            tissue=Tissue.URINE
                            if "cumulative" in name
                            else Tissue.PLASMA,
                            route=Route.PO,
                            application_form=ApplicationForm.TABLET,
                            dosing=Dosing.SINGLE if day == "d1" else Dosing.MULTIPLE,
                            health=Health.T2DM,
                            fasting=Fasting.FASTED,
                        ),
                    )

        # the baseline day, day 1 and day 7 of the multiple dose simulation
        for name, sid, tissue in [
            ("glucose_cumulative_amount", "KI__UGE", Tissue.URINE),
            # the 24-hr mean RTG
            ("glucose_renal_threshold", "KI__RTG_mean", Tissue.PLASMA),
        ]:
            for dose in self.doses:
                mappings[f"fm_po_can{dose}_{name}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=f"{name}_CAN{dose}",
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                    ),
                    observable=FitData(
                        self,
                        task=f"task_po_can{dose}_multi",
                        xid="time",
                        yid=sid,
                    ),
                    metadata=PKPDMappingMetaData(
                        tissue=tissue,
                        route=Route.PO,
                        application_form=ApplicationForm.TABLET,
                        dosing=Dosing.MULTIPLE,
                        health=Health.T2DM,
                        fasting=Fasting.FASTED,
                    ),
                )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        return self.figures_by_sid(
            self._figure_single_multi(),
            *self._figures_urine(),
            self._figure_uge(),
            self._figure_rtg(),
        )

    def _figure_single_multi(self) -> Figure:
        """Plasma concentrations of canagliflozin after the first and last dose."""
        fig = Figure(
            experiment=self,
            sid="Fig_plasma",
            num_rows=1,
            num_cols=2,
            name=f"{self.__class__.__name__} (T2DM)",
        )
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit=self.unit_time), legend=True
        )
        plots[0].set_yaxis(self.label_can, unit=self.unit_can)
        plots[1].set_yaxis(self.label_can, unit=self.unit_can)
        # the day before and day 7, the data of day 7 cover 0-24 hr
        plots[1].set_xaxis(self.label_time, unit=self.unit_time, min=-24, max=25)

        for dose in self.doses[1:]:
            for k, day in enumerate(["d1", "d7"]):
                type_dosing = "single" if day == "d1" else "multi"

                # simulation
                plots[k].add_data(
                    task=f"task_po_can{dose}_{type_dosing}",
                    xid="time",
                    yid="[Cve_can]",
                    label=f"{dose} mg PO",
                    color=self.dose_colors[dose],
                )

                # data
                plots[k].add_data(
                    dataset=f"canagliflozin_CAN{dose}_{day}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=f"{dose} mg PO",
                    color=self.dose_colors[dose],
                )

        return fig

    def _figures_urine(self) -> list[Figure]:
        """Cumulative amounts in the urine after the first and the last dose."""
        figures = []
        for dosing in ["single", "multi"]:
            day = "d1" if dosing == "single" else "d7"

            fig = Figure(
                experiment=self,
                sid=f"Fig_urine_{dosing}",
                num_rows=1,
                num_cols=3,
                name=f"{self.__class__.__name__} (T2DM)",
            )
            # the legends inside the panels cover data
            fig.settings = {**fig.settings, "legend_position": "outside"}
            # the day before and day 7 of the multiple dose
            plots = fig.create_plots(
                xaxis=Axis(
                    self.label_time,
                    unit=self.unit_time,
                    min=-24 if dosing == "multi" else None,
                    max=25,
                ),
                legend=True,
            )
            plots[0].set_yaxis(self.label_can_urine, unit=self.unit_can_urine)
            plots[1].set_yaxis(self.label_m5_urine, unit=self.unit_m5_urine)
            plots[2].set_yaxis(self.label_m7_urine, unit=self.unit_m7_urine)

            for dose in self.doses[1:]:
                for k, (sid, did) in enumerate(self.info.items()):
                    # simulation
                    plots[k].add_data(
                        task=f"task_po_can{dose}_{dosing}",
                        xid="time",
                        yid=f"Aurine_{sid}",
                        label=f"{dose} mg PO",
                        color=self.dose_colors[dose],
                    )

                    # data
                    plots[k].add_data(
                        dataset=f"{did}_cumulative_amount_CAN{dose}_{day}",
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                        label=f"{dose} mg PO",
                        color=self.dose_colors[dose],
                        linestyle="",
                    )
            figures.append(fig)

        return figures

    def _figure_uge(self) -> Figure:
        """Urinary glucose excretion."""
        fig = Figure(
            experiment=self,
            sid="Fig_uge",
            name=f"{self.__class__.__name__} (T2DM)",
        )
        # the legends inside the panel cover data
        fig.settings = {**fig.settings, "legend_position": "outside"}
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="day"), legend=True)
        plots[0].set_yaxis(self.label_uge, unit=self.unit_uge)

        for dose in self.doses:
            # simulation
            plots[0].add_data(
                task=f"task_po_can{dose}_multi",
                xid="time",
                yid="KI__UGE",
                label=f"{dose} mg PO",
                color=self.dose_colors[dose],
            )
            # data
            plots[0].add_data(
                dataset=f"glucose_cumulative_amount_CAN{dose}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"{dose} mg PO",
                color=self.dose_colors[dose],
                linestyle="",
            )

        return fig

    def _figure_rtg(self) -> Figure:
        """Renal threshold of glucose."""
        fig = Figure(
            experiment=self,
            sid="Fig_rtg",
            name=f"{self.__class__.__name__} (T2DM)",
        )
        # the legends inside the panel cover data
        fig.settings = {**fig.settings, "legend_position": "outside"}
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit=self.unit_time), legend=True
        )
        plots[0].set_yaxis(self.label_rtg_mean, unit=self.unit_rtg)

        for dose in self.doses:
            # simulation
            plots[0].add_data(
                task=f"task_po_can{dose}_multi",
                xid="time",
                yid="KI__RTG_mean",
                label=f"{dose} mg PO",
                color=self.dose_colors[dose],
            )

            # data
            plots[0].add_data(
                dataset=f"glucose_renal_threshold_CAN{dose}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"{dose} mg PO",
                color=self.dose_colors[dose],
                linestyle="",
            )

        return fig


if __name__ == "__main__":
    MODEL.run_experiments(Devineni2013, output_dir=Devineni2013.__name__)

"""Simulation experiment of the study Devineni2014."""

from typing import ClassVar, override

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

from pkdb_models.models.canagliflozin import MODEL
from pkdb_models.models.canagliflozin.experiments.base_experiment import (
    CanagliflozinSimulationExperiment,
)


class Devineni2014(CanagliflozinSimulationExperiment):
    """Simulation experiment of Devineni2014."""

    bodyweight = 75.6  # [kg]
    fpg = 5  # [mM] (healthy, not reported)

    info: ClassVar[dict[str, str]] = {
        "can300": "CAN300",
        "can300_hctz25": "CAN300_HCTZ25",
    }
    #: the geometric least squares mean of the mean plasma glucose of 0-24 hr
    #: (MPG0-24) on day 7 of canagliflozin alone and with HCTZ [mM] (Table II),
    #: the glucose which is filtered. HCTZ raises the glucose; it changes no
    #: enzyme or transporter of canagliflozin (AUC 1.12, Cmax 1.15 with HCTZ,
    #: mechanism unknown), so the model has no interaction factors and the arm
    #: with HCTZ is validation data
    mpg: ClassVar[dict[str, float]] = {"can300": 5.16, "can300_hctz25": 5.46}

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig2", "Tab2A"]:
            df = self.load_dataframe(fig_id)
            # the zero amounts at the start of the urine collection of day 7
            # lie at the reset of the collection of day 6 and carry no
            # information
            df = df[~((df.measurement_type == "cumulative amount") & (df.time == 0))]
            for label, df_label in df.groupby("label"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)

                # unit conversion to mole/l
                if label.startswith("canagliflozin_"):
                    dset.unit_conversion("mean", 1 / self.Mr.can)

                dsets[label] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}

        # multiple dose: doses every 24 hr from 0 to 144 hr (days 1 to 7), the
        # urine and the RTG are collected from dose to dose, the data at the end
        # of a collection is compared with the state before the reset. The arm
        # with HCTZ is days 29-35 of period 2, 7 doses of canagliflozin as well.
        for sim in self.info:
            tcsims[f"po_{sim}_multi"] = Simulation(
                time_unit="hr",
                end=169,
                preinit_changes={
                    **self.default_changes(),
                    "PODOSE_can": Q(300, "mg"),
                    "BW": Q(self.bodyweight, "kg"),
                    "[KI__fpg]": Q(self.fpg, "mM"),
                    "KI__PG_delta": Q(self.mpg[sim] - self.fpg, "mM"),
                },
                changes=[
                    Change(
                        [24 * k for k in range(1, 7)],
                        {
                            "KI__glc_urine": Q(0, "mmole"),  # reset UGE
                            "KI__RTG_int": Q(0, "mM*min"),  # reset RTG
                            "KI__RTG_time": Q(0, "min"),
                        },
                    ),
                    self.add_doses(
                        [24 * k for k in range(1, 7)], {"PODOSE_can": Q(300, "mg")}
                    ),
                ],
                time_shift=-6 * 24,
            )

        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}

        for name, sid, tissue in [
            ("canagliflozin", "[Cve_can]", Tissue.PLASMA),
            ("glucose_cumulative_amount", "KI__UGE", Tissue.URINE),
            # the 24-hr mean RTG
            ("glucose_renal_threshold", "KI__RTG_mean", Tissue.PLASMA),
        ]:
            for sim, group in self.info.items():
                coadministration = (
                    Coadministration.HCTZ
                    if "HCTZ25" in group
                    else Coadministration.NONE
                )

                mappings[f"fm_po_{sim}_{name}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=f"{name}_{group}",
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                    ),
                    observable=FitData(
                        self,
                        task=f"task_po_{sim}_multi",
                        xid="time",
                        yid=sid,
                    ),
                    # standardized meals, the time of the dose to the meal is
                    # not reported
                    metadata=PKPDMappingMetaData(
                        tissue=tissue,
                        route=Route.PO,
                        application_form=ApplicationForm.TABLET,
                        dosing=Dosing.MULTIPLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.FASTED,
                        coadministration=coadministration,
                    ),
                )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        return self.figures_by_sid(
            self._figure_multi(), self._figure_uge(), self._figure_rtg()
        )

    def _figure_multi(self) -> Figure:
        """Plasma concentrations of canagliflozin."""
        fig = Figure(
            experiment=self,
            sid="Fig_plasma",
            name=f"{self.__class__.__name__} (Healthy)",
        )
        # the legend inside the panel covers data
        fig.settings = {**fig.settings, "legend_position": "outside"}
        # the day before and day 7, the data of day 7 cover 0-24 hr
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit=self.unit_time, min=-24, max=25),
            legend=True,
        )
        plots[0].set_yaxis(self.label_can, unit=self.unit_can)

        for sim, group in self.info.items():
            color = "black" if group == "CAN300" else "tab:blue"
            label = "300 mg PO" if group == "CAN300" else "300 mg PO + HCTZ"
            # simulation
            plots[0].add_data(
                task=f"task_po_{sim}_multi",
                xid="time",
                yid="[Cve_can]",
                label=label,
                color=color,
                # the curves of both arms are close
                linestyle="-" if sim == "can300" else "--",
            )
            # data
            plots[0].add_data(
                dataset=f"canagliflozin_{group}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=label,
                color=color,
            )

        return fig

    def _figure_uge(self) -> Figure:
        """Urinary glucose excretion."""
        fig = Figure(
            experiment=self,
            sid="Fig_uge",
            name=f"{self.__class__.__name__} (Healthy)",
        )
        # the legends inside the panels cover data
        fig.settings = {**fig.settings, "legend_position": "outside"}
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="day"), legend=True)
        plots[0].set_yaxis(self.label_uge, unit=self.unit_uge)

        for sim, group in self.info.items():
            color = "black" if group == "CAN300" else "tab:blue"
            label = "300 mg PO" if group == "CAN300" else "300 mg PO + HCTZ"
            # simulation
            plots[0].add_data(
                task=f"task_po_{sim}_multi",
                xid="time",
                yid="KI__UGE",
                label=label,
                color=color,
                # the curves of both arms are close
                linestyle="-" if sim == "can300" else "--",
            )
            # data
            plots[0].add_data(
                dataset=f"glucose_cumulative_amount_{group}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=label,
                color=color,
            )

        return fig

    def _figure_rtg(self) -> Figure:
        """Renal threshold of glucose."""
        fig = Figure(
            experiment=self,
            sid="Fig_rtg",
            name=f"{self.__class__.__name__} (Healthy)",
        )
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit=self.unit_time), legend=True
        )
        plots[0].set_yaxis(self.label_rtg_mean, unit=self.unit_rtg)

        for sim, group in self.info.items():
            color = "black" if group == "CAN300" else "tab:blue"
            label = "300 mg PO" if group == "CAN300" else "300 mg PO + HCTZ"
            # simulation
            plots[0].add_data(
                task=f"task_po_{sim}_multi",
                xid="time",
                yid="KI__RTG_mean",
                label=label,
                color=color,
                # the curves of both arms are close
                linestyle="-" if sim == "can300" else "--",
            )
            # data
            plots[0].add_data(
                dataset=f"glucose_renal_threshold_{group}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=label,
                color=color,
            )

        return fig


if __name__ == "__main__":
    MODEL.run_experiments(Devineni2014, output_dir=Devineni2014.__name__)

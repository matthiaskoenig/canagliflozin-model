"""Simulation experiment of the study Devineni2012."""

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

from pkdb_models.models.canagliflozin import MODEL
from pkdb_models.models.canagliflozin.experiments.base_experiment import (
    CanagliflozinSimulationExperiment,
)


class Devineni2012(CanagliflozinSimulationExperiment):
    """Simulation experiment of Devineni2012."""

    bodyweights: ClassVar[dict[int, float]] = {0: 95.1, 100: 107.8, 300: 94.1}
    #: FPG on day 1 before the dose [mM]
    fpg: ClassVar[dict[int, float]] = {0: 8.7, 100: 9, 300: 9.6}
    #: mean 24-hr plasma glucose [mM] at baseline (day -1) and the change on
    #: day 27 (Table 3), the glucose which is filtered
    mpg_baseline: ClassVar[dict[int, float]] = {0: 9.82, 100: 9.30, 300: 11.29}
    mpg_change: ClassVar[dict[int, float]] = {0: 0.07, 100: -1.64, 300: -2.46}

    interventions: ClassVar[dict[str, int]] = {"CAN0": 0, "QD100": 100, "BID300": 300}
    #: the times of the doses of a day [hr]: before the morning meal, the
    #: second dose of 300 mg BID before the evening meal at 10.5 hr (the meal
    #: of the urine and glucose sampling, the second rise of Fig1 starts
    #: between 10.5 and 11 hr)
    dose_times: ClassVar[dict[int, list[float]]] = {
        0: [0.0],
        100: [0.0],
        300: [0.0, 10.5],
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1", "Fig3", "Tab3A"]:
            df = self.load_dataframe(fig_id)
            # the zero amounts at the start of the urine collection of day 27
            # lie at the reset of the collection of the day before and carry
            # no information
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
        """Placebo, 100 mg QD and 300 mg BID on days 1 to 27.

        The urine and the RTG are collected over the 24 hr from the morning
        dose: they are reset with every morning dose, the data at the end of a
        collection is compared with the state before the reset. The mean plasma
        glucose is the one of baseline on day 1 and the one of day 27 from day
        2 on (the glucose falls within the first days of the treatment).
        """
        tcsims = {}
        for intervention, dose in self.interventions.items():
            pg_baseline = Q(self.mpg_baseline[dose] - self.fpg[dose], "mM")
            pg_treatment = Q(
                self.mpg_baseline[dose] + self.mpg_change[dose] - self.fpg[dose], "mM"
            )
            # the evening doses of 300 mg BID on days 1 to 27
            evening = [
                24 * k + t for k in range(27) for t in self.dose_times[dose] if t > 0
            ]
            changes = [
                Change(
                    [24 * k for k in range(1, 27)],
                    {
                        "KI__PG_delta": pg_treatment,
                        "KI__glc_urine": Q(0, "mmole"),  # reset UGE
                        "KI__RTG_int": Q(0, "mM*min"),  # reset RTG
                        "KI__RTG_time": Q(0, "min"),
                    },
                ),
                self.add_doses(
                    [24 * k for k in range(1, 27)] + evening,
                    {"PODOSE_can": Q(dose, "mg")},
                ),
            ]
            tcsims[f"po_{intervention}_multi"] = Simulation(
                time_unit="hr",
                end=28 * 24,
                preinit_changes={
                    **self.default_changes(),
                    "BW": Q(self.bodyweights[dose], "kg"),
                    "[KI__fpg]": Q(self.fpg[dose], "mM"),
                    "KI__PG_delta": pg_baseline,
                    "PODOSE_can": Q(dose, "mg"),
                },
                changes=changes,
                time_shift=-26 * 24,
            )

        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for name, sid, tissue in [
            ("canagliflozin", "[Cve_can]", Tissue.PLASMA),
            ("glucose_cumulative_amount", "KI__UGE", Tissue.URINE),
            # the 24-hr mean RTG
            ("glucose_RT", "KI__RTG_mean", Tissue.PLASMA),
        ]:
            for intervention in self.interventions:
                # the placebo has no pharmacokinetics
                if name == "canagliflozin" and intervention == "CAN0":
                    continue
                mappings[f"fm_po_{intervention}_{name}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=f"{name}_{intervention}_d27",
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                    ),
                    observable=FitData(
                        self,
                        task=f"task_po_{intervention}_multi",
                        xid="time",
                        yid=sid,
                    ),
                    # dosed before the meals, the convention of the studies is
                    # fasted
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
            self._figure_multi(),
            self._figure_uge(),
            self._figure_rtg(),
        )

    def _figure_multi(self) -> Figure:
        """Plasma concentrations of canagliflozin after the last dose."""
        fig = Figure(
            experiment=self,
            sid="Fig_plasma",
            name=f"{self.__class__.__name__} (T2DM)",
        )
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit=self.unit_time, min=-48, max=50),
            legend=True,
        )
        plots[0].set_yaxis(self.label_can, unit=self.unit_can)
        for intervention, dose in {"QD100": 100, "BID300": 300}.items():
            # simulation
            plots[0].add_data(
                task=f"task_po_{intervention}_multi",
                xid="time",
                yid="[Cve_can]",
                label=f"{dose} mg PO",
                color=self.dose_colors[dose],
            )

            # data
            plots[0].add_data(
                dataset=f"canagliflozin_{intervention}_d27",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"{dose} mg PO",
                color=self.dose_colors[dose],
            )

        return fig

    def _figure_uge(self) -> Figure:
        """Urinary glucose excretion."""
        fig = Figure(
            experiment=self,
            sid="Fig_uge",
            name=f"{self.__class__.__name__} (T2DM)",
        )
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit=self.unit_time, min=-48, max=50),
            legend=True,
        )
        plots[0].set_yaxis(self.label_uge, unit=self.unit_uge)

        for intervention, dose in self.interventions.items():
            # simulation
            plots[0].add_data(
                task=f"task_po_{intervention}_multi",
                xid="time",
                yid="KI__UGE",
                label=f"{dose} mg PO",
                color=self.dose_colors[dose],
            )

            # data
            plots[0].add_data(
                dataset=f"glucose_cumulative_amount_{intervention}_d27",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"{dose} mg PO",
                color=self.dose_colors[dose],
            )
        return fig

    def _figure_rtg(self) -> Figure:
        """Renal threshold of glucose."""
        fig = Figure(
            experiment=self,
            sid="Fig_rtg",
            name=f"{self.__class__.__name__} (T2DM)",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="day"), legend=True)
        plots[0].set_yaxis(self.label_rtg_mean, unit=self.unit_rtg)

        for intervention, dose in self.interventions.items():
            # simulation
            plots[0].add_data(
                task=f"task_po_{intervention}_multi",
                xid="time",
                yid="KI__RTG_mean",
                label=f"{dose} mg PO",
                color=self.dose_colors[dose],
            )

            # data
            plots[0].add_data(
                dataset=f"glucose_RT_{intervention}_d27",
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
    MODEL.run_experiments(Devineni2012, output_dir=Devineni2012.__name__)

"""Simulation experiment of the study Devineni2016."""

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
from sbmlsim.simulation import Simulation

from pkdb_models.models.canagliflozin import MODEL
from pkdb_models.models.canagliflozin.experiments.base_experiment import (
    CanagliflozinSimulationExperiment,
)


class Devineni2016(CanagliflozinSimulationExperiment):
    """Simulation experiment of Devineni2016.

    Single doses of canagliflozin (200 mg and 300 mg) in healthy Indian
    subjects (crossover), after a 10 hr fast and 10 min before a standard
    breakfast (the model has no food effect, Devineni2015e).
    """

    doses: ClassVar[list[int]] = [200, 300]
    bodyweight = 59.7  # [kg]
    fpg = 5  # [mM] (healthy, not reported)
    #: the mean plasma glucose 0-4 hr after the dose on day 1 [mg/dl] (Tab3);
    #: the filtered glucose is the MPG, i.e. `PG_delta` = MPG - FPG
    mpg: ClassVar[dict[int, float]] = {200: 89.8, 300: 89.7}
    #: eGFR (MDRD) [ml/min/1.73 m^2]; the renal function is eGFR/101
    egfr = 111

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig2", "Fig3", "Tab3A"]:
            df = self.load_dataframe(fig_id)
            for label, df_label in df.groupby("label"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)
                # unit conversion to mole/l
                if label.startswith("canagliflozin_"):
                    dset.unit_conversion("mean", 1 / self.Mr.can)
                elif label.startswith("glucose_renal_threshold"):
                    dset.unit_conversion("mean", 1 / self.Mr.glc)

                dsets[label] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}

        # single dose
        for dose in self.doses:
            tcsims[f"po_can{dose}_single"] = Simulation(
                time_unit="hr",
                end=80,
                preinit_changes={
                    **self.default_changes(),
                    "BW": Q(self.bodyweight, "kg"),
                    "[KI__fpg]": Q(self.fpg, "mM"),
                    "KI__PG_delta": (
                        Q(self.mpg[dose], "mg/dl") / self.Mr.glc - Q(self.fpg, "mM")
                    ).to("mM"),
                    "KI__f_renal_function": Q(self.egfr / 101, "dimensionless"),
                    "PODOSE_can": Q(dose, "mg"),
                },
            )

        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}

        for name, sid in [
            ("canagliflozin", "[Cve_can]"),
            # change from baseline, the baseline UGE is 0.04-0.05 g/day
            ("glucose_cumulative_amount", "KI__UGE"),
            # mean RTG over 0-4 hr
            ("glucose_renal_threshold", "KI__RTG_mean"),
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
                        task=f"task_po_can{dose}_single",
                        xid="time",
                        yid=sid,
                    ),
                    metadata=PKPDMappingMetaData(
                        tissue=Tissue.URINE if "cumulative" in name else Tissue.PLASMA,
                        route=Route.PO,
                        application_form=ApplicationForm.TABLET,
                        dosing=Dosing.SINGLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.FASTED,
                    ),
                )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        return self.figures_by_sid(
            self._figure_plasma(), self._figure_uge(), self._figure_rtg()
        )

    def _figure_plasma(self) -> Figure:
        """Plasma concentrations of canagliflozin."""
        fig = Figure(
            experiment=self,
            sid="Fig_plasma",
            name=f"{self.__class__.__name__} (Healthy)",
        )
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit=self.unit_time), legend=True
        )
        plots[0].set_yaxis(self.label_can, unit=self.unit_can)

        for dose in self.doses:
            # simulation
            plots[0].add_data(
                task=f"task_po_can{dose}_single",
                xid="time",
                yid="[Cve_can]",
                label=f"{dose} mg PO",
                color=self.dose_colors[dose],
            )

            # data
            plots[0].add_data(
                dataset=f"canagliflozin_CAN{dose}",
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
            name=f"{self.__class__.__name__} (Healthy)",
        )
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit=self.unit_time), legend=True
        )
        plots[0].set_yaxis(self.label_uge, unit=self.unit_uge)

        for dose in self.doses:
            # simulation
            plots[0].add_data(
                task=f"task_po_can{dose}_single",
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
            )

        return fig

    def _figure_rtg(self) -> Figure:
        """Mean renal threshold of glucose over 0-4 hr."""
        fig = Figure(
            experiment=self,
            sid="Fig_rtg",
            name=f"{self.__class__.__name__} (Healthy)",
        )
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit=self.unit_time, min=0, max=12),
            legend=True,
        )
        plots[0].set_yaxis(self.label_rtg_mean, unit=self.unit_rtg)

        for dose in self.doses:
            # simulation
            plots[0].add_data(
                task=f"task_po_can{dose}_single",
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
            )

        return fig


if __name__ == "__main__":
    MODEL.run_experiments(Devineni2016, output_dir=Devineni2016.__name__)

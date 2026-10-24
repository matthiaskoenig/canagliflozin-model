"""Simulation experiment of the study Devineni2015e."""

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


class Devineni2015e(CanagliflozinSimulationExperiment):
    """Simulation experiment of Devineni2015e.

    Study 1: single doses of canagliflozin 300 mg fasted and 30 min after the
    start of a high fat breakfast (crossover, 73.4 kg). Study 2: single doses
    of 50 (a developmental formulation), 100 and 300 mg fasted (crossover,
    72.6 kg). The model has no food effect (AUC +8 %, Cmax +0.5 %): both arms
    of study 1 are one simulation, the fed arm is validation of it.
    """

    conditions: ClassVar[list[str]] = ["fasted", "fed"]
    bodyweight_s1 = 73.4  # [kg]

    doses: ClassVar[list[int]] = [50, 100, 300]
    bodyweight_s2 = 72.6  # [kg]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1", "Fig2"]:
            df = self.load_dataframe(fig_id)
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

        # study 1
        tcsims["po_can300_s1"] = Simulation(
            time_unit="hr",
            end=80,
            preinit_changes={
                **self.default_changes(),
                "BW": Q(self.bodyweight_s1, "kg"),
                "[KI__fpg]": Q(5, "mM"),  # healthy
                "PODOSE_can": Q(300, "mg"),
            },
        )

        # study 2
        for dose in self.doses:
            tcsims[f"po_can{dose}_fasted"] = Simulation(
                time_unit="hr",
                end=80,
                preinit_changes={
                    **self.default_changes(),
                    "BW": Q(self.bodyweight_s2, "kg"),
                    "[KI__fpg]": Q(5, "mM"),  # healthy
                    "PODOSE_can": Q(dose, "mg"),
                },
            )

        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for condition in self.conditions:
            mappings[f"fm_po_can300_{condition}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"canagliflozin_CAN300_{condition}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task="task_po_can300_s1",
                    xid="time",
                    yid="[Cve_can]",
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.PLASMA,
                    route=Route.PO,
                    application_form=ApplicationForm.TABLET,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED if condition == "fasted" else Fasting.FED,
                ),
            )

        for dose in self.doses:
            mappings[f"fm_po_can{dose}_single_fasted"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"canagliflozin_CAN{dose}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task=f"task_po_can{dose}_fasted",
                    xid="time",
                    yid="[Cve_can]",
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.PLASMA,
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
            self._figure_fastvsfed(),
            self._figure_dose(),
        )

    def _figure_fastvsfed(self) -> Figure:
        """Plasma concentrations fasted and fed."""
        fig = Figure(
            experiment=self,
            sid="Fig_fastvsfed",
            num_rows=1,
            num_cols=1,
            name=f"{self.__class__.__name__} (Healthy)",
        )

        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit=self.unit_time),
            legend=True,
        )
        plots[0].set_yaxis(self.label_can, unit=self.unit_can)

        # simulation: the model has no food effect
        plots[0].add_data(
            task="task_po_can300_s1",
            xid="time",
            yid="[Cve_can]",
            label="300 mg PO",
            color=self.fasting_colors["fasted"],
        )

        # fasted vs fed at 300 mg
        for condition in self.conditions:
            label = f"300 mg PO ({condition})"

            # data
            plots[0].add_data(
                dataset=f"canagliflozin_CAN300_{condition}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=label,
                color=self.fasting_colors[condition],
            )

        return fig

    def _figure_dose(self) -> Figure:
        """Plasma concentrations of the doses."""
        fig = Figure(
            experiment=self,
            sid="Fig_dose",
            num_rows=1,
            num_cols=1,
            name=f"{self.__class__.__name__} (Healthy)",
        )

        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit=self.unit_time),
            legend=True,
        )
        plots[0].set_yaxis(self.label_can, unit=self.unit_can)

        # Dose dependency under fasted conditions
        for dose in self.doses:
            label = f"{dose} mg PO"

            # simulation
            plots[0].add_data(
                task=f"task_po_can{dose}_fasted",
                xid="time",
                yid="[Cve_can]",
                label=label,
                color=self.dose_colors[dose],
            )

            # data
            plots[0].add_data(
                dataset=f"canagliflozin_CAN{dose}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=label,
                color=self.dose_colors[dose],
            )

        return fig


if __name__ == "__main__":
    MODEL.run_experiments(Devineni2015e, output_dir=Devineni2015e.__name__)

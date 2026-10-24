"""Simulation experiment of the study Murphy2015."""

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
from sbmlsim.simulation import Simulation

from pkdb_models.models.canagliflozin import MODEL
from pkdb_models.models.canagliflozin.experiments.base_experiment import (
    CanagliflozinSimulationExperiment,
)


class Murphy2015(CanagliflozinSimulationExperiment):
    """Simulation experiment of Murphy2015.

    24 healthy subjects (15 men, 9 women, BW 76.3 kg), randomized open-label
    two-period crossover (washout 10-14 days) of a single tablet of the
    fixed-dose combination of canagliflozin 150 mg and metformin 1000 mg
    (immediate release), fasted (overnight >= 10 h) and fed (30 min after the
    start of a standardized high-fat breakfast), no food until 4 h after the
    dose. Canagliflozin in plasma to 72 h (Fig 1A).

    The model has no food effect (high fat breakfast: AUC +11.5 %, Cmax
    -9.4 %, tmax 1.5 -> 3.5 h, bioequivalent): the fed arm is the same
    simulation as the fasted arm.
    """

    conditions: ClassVar[list[str]] = ["fasted", "fed"]

    bodyweight = 76.3  # [kg]
    fpg = 5  # mM (healthy)

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1"]:
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
        for condition in self.conditions:
            tcsims[f"po_can150_{condition}"] = Simulation(
                time_unit="hr",
                end=80,
                preinit_changes={
                    **self.default_changes(),
                    "BW": Q(self.bodyweight, "kg"),
                    "[KI__fpg]": Q(self.fpg, "mM"),
                    "PODOSE_can": Q(150, "mg"),
                },
            )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for condition in self.conditions:
            mappings[f"fm_po_can150_{condition}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"canagliflozin_{condition}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task=f"task_po_can150_{condition}",
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
                    coadministration=Coadministration.METFORMIN,
                ),
            )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig1",
            name=f"{self.__class__.__name__} (Healthy)",
        )
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit=self.unit_time), legend=True
        )
        plots[0].set_yaxis(self.label_can, unit=self.unit_can)

        for condition in self.conditions:
            label = "150 mg PO (fasted)" if condition == "fasted" else "150 mg PO (fed)"

            # simulation
            plots[0].add_data(
                task=f"task_po_can150_{condition}",
                xid="time",
                yid="[Cve_can]",
                label=label,
                color=self.fasting_colors[condition],
            )
            # data
            plots[0].add_data(
                dataset=f"canagliflozin_{condition}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=label,
                color=self.fasting_colors[condition],
            )

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(Murphy2015, output_dir=Murphy2015.__name__)

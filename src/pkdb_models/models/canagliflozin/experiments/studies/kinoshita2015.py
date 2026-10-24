"""Simulation experiment of the study Kinoshita2015."""

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


class Kinoshita2015(CanagliflozinSimulationExperiment):
    """Simulation experiment of Kinoshita2015.

    Japanese healthy men, open-label one-way crossover (group 1, n=25, BW
    61.57 kg): a single oral dose of canagliflozin 200 mg (tablet) alone, and
    after a washout of >= 14 days a single dose of canagliflozin 200 mg on day
    7 of teneligliptin 40 mg once daily (days 1-9). Overnight fast >= 10 h,
    the dose 30 min before breakfast. Canagliflozin in plasma to 72 h (Fig 2).

    Teneligliptin does not change the pharmacokinetics of canagliflozin (GMR
    AUC0-72 0.982, Cmax 0.982), the model has no interaction: both arms are
    the single dose of canagliflozin.
    """

    #: the arms by dataset: the coadministration
    groups: ClassVar[dict[str, Coadministration]] = {
        "CAN200": Coadministration.NONE,
        # teneligliptin is no member of the vocabulary of pkpdsim yet
        "CAN200_TNL40": Coadministration.COMEDICATION,
    }

    bodyweight = 61.57  # [kg]
    fpg = 5  # [mM] healthy

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig2"]:
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
        return {
            "po_can200": Simulation(
                time_unit="hr",
                end=80,
                preinit_changes={
                    **self.default_changes(),
                    "BW": Q(self.bodyweight, "kg"),
                    "[KI__fpg]": Q(self.fpg, "mM"),
                    "PODOSE_can": Q(200, "mg"),
                },
            )
        }

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}

        for group, coadministration in self.groups.items():
            mappings[self.to_sid(f"fm_po_{group.lower()}")] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"canagliflozin_{group}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task="task_po_can200",
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
                    coadministration=coadministration,
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
            xaxis=Axis(self.label_time, unit=self.unit_time, min=-1, max=80),
            legend=True,
        )
        plots[0].set_yaxis(self.label_can, unit=self.unit_can)

        # simulation
        plots[0].add_data(
            task="task_po_can200",
            xid="time",
            yid="[Cve_can]",
            label="200 mg PO",
            color="black",
        )

        # data
        for group in self.groups:
            color = "black" if group == "CAN200" else "tab:blue"
            label = "200 mg PO" if group == "CAN200" else "200 mg PO + TNL"

            plots[0].add_data(
                dataset=f"canagliflozin_{group}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=label,
                color=color,
            )

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(Kinoshita2015, output_dir=Kinoshita2015.__name__)

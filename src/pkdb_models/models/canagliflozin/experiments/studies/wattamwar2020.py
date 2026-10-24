"""Simulation experiment of the study Wattamwar2020."""

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


class Wattamwar2020(CanagliflozinSimulationExperiment):
    """Simulation experiment of Wattamwar2020.

    Healthy Indian men, parallel groups, a single immediate release tablet of
    the fixed-dose combination canagliflozin/metformin 150/1000 mg after an
    overnight fast (24 analysed) or 30 min after a high-fat breakfast (32
    analysed). Plasma canagliflozin up to 48 hr (mean, no SD). The fasted tmax
    of 5.16 hr is atypical for canagliflozin (1 - 2 hr elsewhere), and the
    model has no food effect (Devineni2015e): the curves are validation data.
    """

    conditions: ClassVar[list[str]] = ["fasted", "fed"]

    #: not reported, healthy men
    bodyweight = 75  # [kg]
    fpg = 5  # [mM] (healthy)

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig4"]:
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
                end=50,
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
            mappings[f"fm_can150_fdc_{condition}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"canagliflozin_CAN150_{condition}",
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
                    # fixed-dose combination with metformin, no interaction
                    # expected (Devineni2015, Mohamed2019)
                    coadministration=Coadministration.METFORMIN,
                ),
            )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig_plasma",
            name=f"{self.__class__.__name__} (Healthy)",
        )
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit=self.unit_time), legend=True
        )
        plots[0].set_yaxis(self.label_can, unit=self.unit_can)

        for condition in self.conditions:
            # simulation
            plots[0].add_data(
                task=f"task_po_can150_{condition}",
                xid="time",
                yid="[Cve_can]",
                label=f"150 mg PO ({condition})",
                color=self.fasting_colors[condition],
                # no food effect: the simulations are the same
                linestyle="-" if condition == "fasted" else "--",
            )
            # data
            plots[0].add_data(
                dataset=f"canagliflozin_CAN150_{condition}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"150 mg PO ({condition})",
                color=self.fasting_colors[condition],
            )

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(Wattamwar2020, output_dir=Wattamwar2020.__name__)

"""Simulation experiment of the study Mohamed2019."""

from typing import override

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


class Mohamed2019(CanagliflozinSimulationExperiment):
    """Simulation experiment of Mohamed2019.

    Bioanalytical method paper: 2 healthy Egyptian volunteers (sex, age and BW
    not reported), fasting, one tablet of the fixed-dose combination of
    canagliflozin 50 mg and metformin 850 mg (Vokanamet). Canagliflozin in
    plasma to 72 h (Fig 4b, LLOQ 10 ng/ml); the points at 48 and 72 h are
    below the LLOQ and are not used.
    """

    fpg = 5  # [mM]
    bodyweight = 75  # [kg] reference (no bodyweight given)

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
        tcsims["po_can50"] = Simulation(
            time_unit="hr",
            end=80,
            preinit_changes={
                **self.default_changes(),
                "BW": Q(self.bodyweight, "kg"),
                "PODOSE_can": Q(50, "mg"),
                "[KI__fpg]": Q(self.fpg, "mM"),
            },
        )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        mappings["fm_po_can50"] = FitMapping(
            self,
            reference=FitData(
                self,
                dataset="canagliflozin_CAN50",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
            ),
            observable=FitData(
                self,
                task="task_po_can50",
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
                coadministration=Coadministration.METFORMIN,
            ),
        )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig4",
            name=f"{self.__class__.__name__} (Healthy)",
        )
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit=self.unit_time), legend=True
        )
        plots[0].set_yaxis(self.label_can, unit=self.unit_can)

        # simulation
        plots[0].add_data(
            task="task_po_can50",
            xid="time",
            yid="[Cve_can]",
            label="50 mg PO",
            color="black",
        )
        # data
        plots[0].add_data(
            dataset="canagliflozin_CAN50",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label="50 mg PO",
            color="black",
        )

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(Mohamed2019, output_dir=Mohamed2019.__name__)

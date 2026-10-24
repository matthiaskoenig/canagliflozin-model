"""Simulation experiment of the study Devineni2015."""

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


class Devineni2015(CanagliflozinSimulationExperiment):
    """Simulation experiment of Devineni2015."""

    info: ClassVar[dict[str, str]] = {
        "can300": "CAN300",
        "can300_met2000": "CAN300_MET2000",
    }
    #: the doses of canagliflozin 300 mg QD (days 4 to 8) up to the profile:
    #: alone the 4th dose (day 7, sampled 0-24 hr), with metformin 2000 mg the
    #: 5th dose (day 8, sampled 0-72 hr). Metformin changes no enzyme or
    #: transporter of canagliflozin (AUC 1.10, Cmax 1.05), so the model has no
    #: interaction factors and the arm with metformin is validation data
    n_doses: ClassVar[dict[str, int]] = {"can300": 4, "can300_met2000": 5}

    bodyweight = 75.6  # [kg] (study 2)
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

        # multiple dose: doses every 24 hr, the profile after the last dose
        for sim, n in self.n_doses.items():
            tcsims[f"po_{sim}_multi"] = Simulation(
                time_unit="hr",
                end=24 * (n - 1) + 73,
                preinit_changes={
                    **self.default_changes(),
                    "BW": Q(self.bodyweight, "kg"),
                    "[KI__fpg]": Q(self.fpg, "mM"),
                    "PODOSE_can": Q(300, "mg"),
                },
                changes=[
                    self.add_doses(
                        [24 * k for k in range(1, n)],
                        {"PODOSE_can": Q(300, "mg")},
                    )
                ],
                time_shift=-24 * (n - 1),
            )

        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}

        for sim, group in self.info.items():
            coadministration = (
                Coadministration.METFORMIN
                if "MET2000" in group
                else Coadministration.NONE
            )

            mappings[f"fm_po_{sim}_canagliflozin"] = FitMapping(
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
                    task=f"task_po_{sim}_multi",
                    xid="time",
                    yid="[Cve_can]",
                ),
                # dosed 10 min before a standardized breakfast, the convention
                # of the studies is fasted
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.PLASMA,
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
        fig = Figure(
            experiment=self,
            sid="Fig4",
            name=f"{self.__class__.__name__} (Healthy)",
        )
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit=self.unit_time, min=-24, max=73),
            legend=True,
        )
        plots[0].set_yaxis(self.label_can, unit=self.unit_can)

        for sim, group in self.info.items():
            color = "black" if group == "CAN300" else "tab:blue"
            label = "300 mg PO" if group == "CAN300" else "300 mg PO + MET"
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

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(Devineni2015, output_dir=Devineni2015.__name__)

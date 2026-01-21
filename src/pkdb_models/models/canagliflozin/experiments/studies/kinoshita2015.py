from typing import Dict

from sbmlsim.data import DataSet, load_pkdb_dataframe
from sbmlsim.fit import FitMapping, FitData
from sbmlutils.console import console

from pkdb_models.models.canagliflozin.experiments.base_experiment import (
    CanagliflozinSimulationExperiment,
)
from pkdb_models.models.canagliflozin.experiments.metadata import Tissue, Route, Dosing, ApplicationForm, Health, \
    Fasting, CanagliflozinMappingMetaData

from sbmlsim.plot import Axis, Figure
from sbmlsim.simulation import Timecourse, TimecourseSim

from pkdb_models.models.canagliflozin.helpers import run_experiments


class Kinoshita2015(CanagliflozinSimulationExperiment):
    """Simulation experiment of Kinoshita2015."""

    groups = {"CAN200": "single", "CAN200_TNL40": "multi"}

    info = {"CAN200": "can200", "CAN200_TNL40": "can200_tnl40"}

    bodyweight = 61.57  # [kg]
    fpg = 5  # [mM] healthy

    def datasets(self) -> Dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig2"]:
            df = load_pkdb_dataframe(f"{self.sid}_{fig_id}", data_path=self.data_path)
            for label, df_label in df.groupby("label"):
                dset = DataSet.from_df(df_label, self.ureg)

                # unit conversion to mole/l
                if label.startswith("canagliflozin_"):
                    dset.unit_conversion("mean", 1 / self.Mr.can)

                dsets[f"{label}"] = dset

        # console.print(dsets)
        # console.print(dsets.keys())
        return dsets

    def simulations(self) -> Dict[str, TimecourseSim]:
        Q_ = self.Q_
        tcsims = {}

        # single dose
        tcsims[f"po_can200_single"] = TimecourseSim(
            Timecourse(
                start=0,
                end=80 * 60,  # [min]
                steps=500,
                changes={
                    **self.default_changes(),
                    "BW": Q_(self.bodyweight, "kg"),
                    "[KI__fpg]": Q_(self.fpg, "mM"),
                    "PODOSE_can": Q_(200, "mg"),
                },
            )
        )

        # multiple dose
        tc0 = Timecourse(
            start=0,
            end=72 * 60,  # [min]
            steps=500,
            changes={
                **self.default_changes(),
                "BW": Q_(self.bodyweight, "kg"),
                "[KI__fpg]": Q_(self.fpg, "mM"),
                "PODOSE_can": Q_(0, "mg"),
            },
        )
        tc1 = Timecourse(
            start=0,
            end=72 * 60,  # [min]
            steps=500,
            changes={
                "BW": Q_(self.bodyweight, "kg"),
                "[KI__fpg]": Q_(self.fpg, "mM"),
                "PODOSE_can": Q_(200, "mg")
            },
        )
        tc2 = Timecourse(
            start=0,
            end=73 * 60,  # [min]
            steps=500,
            changes={
                "BW": Q_(self.bodyweight, "kg"),
                "[KI__fpg]": Q_(self.fpg, "mM"),
                "PODOSE_can": Q_(200, "mg")
            },
        )

        tcsims[f"po_can200_tnl40_multi"] = TimecourseSim(
            [tc0] + [tc1 for _ in range(7)] + [tc2],
            time_offset=-8 * 72 * 60,
        )

        return tcsims

    def fit_mappings(self) -> Dict[str, FitMapping]:

        mappings = {}

        for group, dosing in self.groups.items():

            sim = self.info[group]

            mappings[f"task_po_{sim}"] = FitMapping(
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
                    self, task=f"task_po_{sim}_{dosing}", xid="time", yid="[Cve_can]",
                ),
                metadata=CanagliflozinMappingMetaData(
                    tissue=Tissue.PLASMA,
                    route=Route.PO,
                    application_form=ApplicationForm.TABLET,
                    dosing=Dosing.SINGLE if dosing == "single" else Dosing.MULTIPLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                ),
            )

        # console.print(mappings)
        return mappings

    def figures(self) -> Dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig1",
            name=f"{self.__class__.__name__} (Healthy)",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit=self.unit_time, min=-1, max=80), legend=True)
        plots[0].set_yaxis(self.label_can, unit=self.unit_can)

        # simulation
        plots[0].add_data(
            task=f"task_po_can200_single",
            xid="time",
            yid=f"[Cve_can]",
            label=f"200 mg PO",
            color="black",
        )

        # data
        for group, dosing in self.groups.items():
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

        return {
            fig.sid: fig,
        }

if __name__ == "__main__":
    run_experiments(Kinoshita2015, output_dir=Kinoshita2015.__name__)

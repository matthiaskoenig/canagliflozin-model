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


class Murphy2015(CanagliflozinSimulationExperiment):
    """Simulation experiment of Murphy2015."""

    conditions = ["fasted", "fed"]

    bodyweight = 76.3  # [kg]
    fpg = 5  # mM (healthy)

    def datasets(self) -> Dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1"]:
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
        for condition in self.conditions:
            tcsims[f"po_can150_{condition}"] = TimecourseSim(
                [Timecourse(
                    start=0,
                    end=80 * 60,  # [min]
                    steps=500,
                    changes={
                        **self.default_changes(),
                        "BW": Q_(self.bodyweight, "kg"),
                        "[KI__fpg]": Q_(self.fpg, "mM"),
                        "PODOSE_can": Q_(150, "mg"),
                        "GU__f_absorption": Q_(self.fasting_map[condition], "dimensionless"),
                    },
                )]
            )
        return tcsims

    def fit_mappings(self) -> Dict[str, FitMapping]:
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
                        self, task=f"task_po_can150_{condition}", xid="time", yid=f"[Cve_can]",
                    ),
                    metadata=CanagliflozinMappingMetaData(
                        tissue=Tissue.PLASMA,
                        route=Route.PO,
                        application_form=ApplicationForm.TABLET,
                        dosing=Dosing.SINGLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.FASTED if condition == "fasted" else Fasting.FED,
                    ),
                )
        return mappings

    def figures(self) -> Dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig1",
            name=f"{self.__class__.__name__} (Healthy)",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit=self.unit_time), legend=True)
        plots[0].set_yaxis(self.label_can, unit=self.unit_can)

        for condition in self.conditions:
            label = "150 mg PO (fasted)" if condition == "fasted" else "150 mg PO (fed)"

            # simulation
            plots[0].add_data(
                task=f"task_po_can150_{condition}",
                xid="time",
                yid=f"[Cve_can]",
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

        return {
            fig.sid: fig,
        }


if __name__ == "__main__":
    run_experiments(Murphy2015, output_dir=Murphy2015.__name__)

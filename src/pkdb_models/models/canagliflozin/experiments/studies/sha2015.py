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


class Sha2015(CanagliflozinSimulationExperiment):
    """Simulation experiment of Sha2015."""

    colors = {300: "tab:green"}

    bodyweight = 78.9  # [kg]
    fpg = 5  # mM (healthy)
    gfr = 96.8  # [ml/min/1.73*m^2]

    def datasets(self) -> Dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig2", "Fig3"]:
            df = load_pkdb_dataframe(f"{self.sid}_{fig_id}", data_path=self.data_path)
            for label, df_label in df.groupby("label"):
                dset = DataSet.from_df(df_label, self.ureg)

                dsets[f"{label}"] = dset

        # console.print(dsets)
        # console.print(dsets.keys())
        return dsets

    def simulations(self) -> Dict[str, TimecourseSim]:
        Q_ = self.Q_
        tcsims = {}

        # single dose
        tcsims[f"po_can300_single"] = TimecourseSim(
            Timecourse(
                start=0,
                end=25 * 60,  # [min]
                steps=500,
                changes={
                    **self.default_changes(),
                    "BW": Q_(self.bodyweight, "kg"),
                    "[KI__fpg]": Q_(self.fpg, "mM"),
                    "KI__f_renal_function": Q_(self.gfr / 100, "dimensionless"),  # [0, 1]  <=> [0, 100] gfr
                    "PODOSE_can": Q_(300, "mg"),
                },
            )
        )

        return tcsims

    def fit_mappings(self) -> Dict[str, FitMapping]:

        mappings = {}

        for name, sid in [
            ('canagliflozin', '[Cve_can]'),
            ('glucose_cumulative_amount', 'KI__UGE'),
            ('renal_threshold', 'KI__RTG'),
        ]:

            mappings[f"task_po_can300_{name}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"{name}_CAN300",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self, task=f"task_po_can300_single", xid="time", yid=sid,
                ),
                metadata=CanagliflozinMappingMetaData(
                    tissue=Tissue.URINE if "cumulative" in name else Tissue.PLASMA,
                    route=Route.PO,
                    application_form=ApplicationForm.TABLET,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                ),
            )

        # console.print(mappings)
        return mappings

    def figures(self) -> Dict[str, Figure]:
        return {
            **self.figure_plasma(),
            **self.figure_uge(),
            **self.figure_rtg()
        }

    def figure_plasma(self) -> Dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="canagliflozin plasma",
            name=f"{self.__class__.__name__} (Healthy)",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit=self.unit_time), legend=True)
        plots[0].set_yaxis(self.label_can, unit=self.unit_can)

        # simulation
        plots[0].add_data(
            task=f"task_po_can300_single",
            xid="time",
            yid=f"[Cve_can]",
            label=f"300 mg PO",
            color="black",
        )

        # data
        plots[0].add_data(
            dataset=f"canagliflozin_CAN300",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label=f"300 mg PO",
            color="black",
        )

        return {
            fig.sid: fig,
        }

    def figure_uge(self) -> Dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig_uge",
            name=f"{self.__class__.__name__} (Healthy)",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit=self.unit_time), legend=True)
        plots[0].set_yaxis(self.label_uge, unit=self.unit_uge)

        # simulation
        plots[0].add_data(
            task=f"task_po_can300_single",
            xid="time",
            yid=f"KI__UGE",
            label=f"300 mg PO",
            color="black",
        )
        # data
        plots[0].add_data(
            dataset=f"glucose_cumulative_amount_CAN300",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label=f"300 mg PO",
            color="black",
        )

        return {
            fig.sid: fig,
        }

    def figure_rtg(self) -> Dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig_rtg",
            name=f"{self.__class__.__name__} (Healthy)",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit=self.unit_time), legend=True)
        plots[0].set_yaxis(self.label_rtg, unit=self.unit_rtg)

        # simulation
        plots[0].add_data(
            task=f"task_po_can300_single",
            xid="time",
            yid=f"KI__RTG",
            label=f"300 mg PO",
            color="black",
        )

        # data
        plots[0].add_data(
            dataset=f"renal_threshold_CAN300",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label=f"300 mg PO",
            color="black",
        )

        return {
            fig.sid: fig,
        }

if __name__ == "__main__":
    run_experiments(Sha2015, output_dir=Sha2015.__name__)
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


class Mamidi2014(CanagliflozinSimulationExperiment):
    """Simulation experiment of Mamidi2014."""

    bodyweight = 62  # [kg]
    fpg = 5  # mM (healthy)

    info = {
        "cantot": "canagliflozin_total",
        "can": "canagliflozin",
        "m5": "M5",
        "m7": "M7",
    }

    info_urine = {
        "m5": "M5",
        "m7": "M7",
        "cantot": "canagliflozin_total",
    }

    info_feces = {
        "cantot": "canagliflozin_total",
        "can": "canagliflozin",
        "m9": "M9",
        "m7": "M7",
    }

    colors = {"cantot": "black", "can": "tab:red", "m5": "tab:blue", "m7": "tab:green", "m9": "purple"}

    def datasets(self) -> Dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig3", "Tab5A", "Tab6A"]:
            df = load_pkdb_dataframe(f"{self.sid}_{fig_id}", data_path=self.data_path)
            for label, df_label in df.groupby("label"):
                dset = DataSet.from_df(df_label, self.ureg)

                # unit conversion to mole/l
                if label.startswith("canagliflozin_"):
                    dset.unit_conversion("mean", 1 / self.Mr.can)
                elif label.startswith("M7_"):
                    dset.unit_conversion("mean", 1 / self.Mr.m7)
                elif label.startswith("M5_"):
                    dset.unit_conversion("mean", 1 / self.Mr.m5)
                elif label.startswith("M9_"):
                    dset.unit_conversion("mean", 1 / self.Mr.m9)

                dsets[f"{label}"] = dset

        # console.print(dsets)
        # console.print(dsets.keys())
        return dsets

    def simulations(self) -> Dict[str, TimecourseSim]:
        Q_ = self.Q_
        tcsims = {}

        tcsims[f"po_can_CAN188"] = TimecourseSim(
            [Timecourse(
                start=0,
                end=50 * 60,  # [min]
                steps=500,
                changes={
                    **self.default_changes(),
                    "BW": Q_(self.bodyweight, "kg"),
                    "[KI__fpg]": Q_(self.fpg, "mM"),
                    "PODOSE_can": Q_(188, "mg"),
                },
            )]
        )

        return tcsims

    def fit_mappings(self) -> Dict[str, FitMapping]:

        mappings = {}
        for name, sid in [
            ('canagliflozin_total_CAN188', '[Cve_cantot]'),
            ('canagliflozin_CAN188', '[Cve_can]'),
            ('M5_CAN188', '[Cve_m5]'),
            ('M7_CAN188', '[Cve_m7]'),

        ]:

            mappings[f"fm_CAN188_{name}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"{name}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self, task=f"task_po_can_CAN188", xid="time", yid=f"{sid}",
                ),
                metadata=CanagliflozinMappingMetaData(
                    tissue=Tissue.PLASMA,
                    route=Route.PO,
                    application_form=ApplicationForm.SOLUTION,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED
                ),
            )

            for name, sid in [
                ('canagliflozin_total_cumulative amount_urine', 'Aurine_cantot'),
                ('M5_cumulative amount_urine', 'Aurine_m5'),
                ('M7_cumulative amount_urine', 'Aurine_m7'),
                ('canagliflozin_total_cumulative amount_feces', 'Afeces_cantot'),
                ('canagliflozin_cumulative amount_feces', 'Afeces_can'),
                ('M7_cumulative amount_feces', 'Afeces_m7'),
                ('M9_cumulative amount_feces', 'Afeces_m9'),

            ]:
                tissue = Tissue.URINE if "urine" in name else Tissue.FECES
                mappings[f"fm_CAN188_{name}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=f"{name}",
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                    ),
                    observable=FitData(
                        self, task=f"task_po_can_CAN188", xid="time", yid=f"{sid}",
                    ),
                    metadata=CanagliflozinMappingMetaData(
                        tissue=tissue,
                        route=Route.PO,
                        application_form=ApplicationForm.SOLUTION,
                        dosing=Dosing.SINGLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.FASTED
                    ),
                )

        # console.print(mappings)
        return mappings

    def figures(self) -> Dict[str, Figure]:
        return {
            **self.figure_conc(),
            **self.figure_urine(),
            **self.figure_feces(),
        }

    def figure_conc(self) -> Dict[str, Figure]:

        fig = Figure(
            experiment=self,
            sid="Fig2",
            num_rows=2,
            num_cols=2,
            name=f"{self.__class__.__name__} (Healthy)",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit=self.unit_time), legend=True)
        plots[0].set_yaxis(self.label_cantot, unit=self.unit_cantot)
        plots[1].set_yaxis(self.label_can, unit=self.unit_can)
        plots[2].set_yaxis(self.label_m5, unit=self.unit_m5)
        plots[3].set_yaxis(self.label_m7, unit=self.unit_m7)

        for k, sid in enumerate(self.info):
            # simulation
            plots[k].add_data(
                task=f"task_po_can_CAN188",
                xid="time",
                yid=f"[Cve_{sid}]",
                label=f"188 mg PO",
                color="black",
            )

            # data
            did = self.info[sid]
            plots[k].add_data(
                dataset=f"{did}_CAN188",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"188 mg PO",
                color="black",
            )

        return {
            fig.sid: fig,
        }

    def figure_urine(self):

        fig = Figure(
            experiment=self,
            sid="urine",
            num_rows=1,
            num_cols=3,
            name=f"{self.__class__.__name__} (Healthy)",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit=self.unit_time), legend=True)
        plots[0].set_yaxis(self.label_cantot_urine, unit=self.unit_cantot_urine)
        plots[1].set_yaxis(self.label_m5_urine, unit=self.unit_m5_urine)
        plots[2].set_yaxis(self.label_m7_urine, unit=self.unit_m7_urine)

        for k, sid in enumerate(self.info_urine):
            # simulation
            plots[k].add_data(
                task=f"task_po_can_CAN188",
                xid="time",
                yid=f"Aurine_{sid}",
                label=f"188 mg PO",
                color="black",
            )
            # data
            did = self.info[sid]
            plots[k].add_data(
                dataset=f"{did}_cumulative amount_urine",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"188 mg PO",
                color="black",
                linestyle=""
            )
        return {
            fig.sid: fig,
        }

    def figure_feces(self):

        fig = Figure(
            experiment=self,
            sid="feces",
            num_rows=2,
            num_cols=2,
            name=f"{self.__class__.__name__} (Healthy)",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit=self.unit_time), legend=True)
        plots[0].set_yaxis(self.label_cantot_feces, unit=self.unit_cantot_urine)
        plots[1].set_yaxis(self.label_can_feces, unit=self.unit_can_urine)
        plots[2].set_yaxis(self.label_m7_feces, unit=self.unit_m7_feces)
        plots[3].set_yaxis(self.label_m9_feces, unit=self.unit_m9_feces)

        for k, sid in enumerate(self.info_feces):
            # simulation
            plots[k].add_data(
                task=f"task_po_can_CAN188",
                xid="time",
                yid=f"Afeces_{sid}",
                label=f"188 mg PO",
                color="black",
            )
            # data
            did = self.info_feces[sid]
            plots[k].add_data(
                dataset=f"{did}_cumulative amount_feces",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"188 mg PO",
                color="black",
                linestyle=""
            )
        return {
            fig.sid: fig,
        }


if __name__ == "__main__":
    run_experiments(Mamidi2014, output_dir=Mamidi2014.__name__)

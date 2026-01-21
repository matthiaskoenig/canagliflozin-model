from typing import Dict
from sbmlsim.data import DataSet, load_pkdb_dataframe
from sbmlsim.fit import FitMapping, FitData
from sbmlsim.plot import Axis, Figure
from sbmlsim.simulation import Timecourse, TimecourseSim
from sbmlutils.console import console
from pkdb_models.models.canagliflozin.experiments.base_experiment import CanagliflozinSimulationExperiment
from pkdb_models.models.canagliflozin.experiments.metadata import Tissue, Route, Dosing, ApplicationForm, Health, \
    Fasting, CanagliflozinMappingMetaData
from pkdb_models.models.canagliflozin.helpers import run_experiments


class Chen2015(CanagliflozinSimulationExperiment):
    """Simulation experiment of Chen2015."""

    bodyweight = 63   # [kg]
    fpg = 5  # mM (healthy)
    gfr = 103  # [ml/min/1.73*m^2]

    interventions = {"CAN100": 100,
                     "CAN300": 300}

    interventions_uge = {"CAN0": 0,
                         "CAN100": 100,
                         "CAN300": 300,}

    info = {
        "can": "canagliflozin",
        "m5": "M5",
        "m7": "M7",
    }

    doses = [0, 100, 300]

    def datasets(self) -> Dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1", "Tab2A", "Tab3"]:
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
                elif label.startswith("glucose_RT"):
                    dset.unit_conversion("mean", 1 / self.Mr.glc)
                dsets[f"{label}"] = dset
        # console.print(dsets)
        # console.print(dsets.keys())
        return dsets

    def simulations(self) -> Dict[str, TimecourseSim]:
        Q_ = self.Q_
        tcsims = {}

        for dose in self.doses:
            tcsims[f"po_can_CAN{dose}"] = TimecourseSim(
                [Timecourse(
                    start=0,
                    end=80 * 60,  # [min]
                    steps=500,
                    changes={
                        **self.default_changes(),
                        "BW": Q_(self.bodyweight, "kg"),
                        "[KI__fpg]": Q_(self.fpg, "mM"),
                        "KI__f_renal_function": Q_(self.gfr/100, "dimensionless"),   # [0, 1]  <=> [0, 100] gfr
                        "PODOSE_can": Q_(dose, "mg"),
                    },
                )]
            )

        return tcsims

    def fit_mappings(self) -> Dict[str, FitMapping]:

        mappings = {}
        for name, sid in [
            ('canagliflozin', '[Cve_can]'),
            ('M5', '[Cve_m5]'),
            ('M7', '[Cve_m7]'),
            ('canagliflozin_cumulative_amount', 'Aurine_can'),
            ('M5_cumulative_amount', 'Aurine_m5'),
            ('M7_cumulative_amount', 'Aurine_m7'),
            ('glucose_cumulative_amount', 'KI__UGE'),
            ('glucose_RT_MDRD', 'KI__RTG'),
            ('glucose_RT_McrCl', 'KI__RTG'),
        ]:
            tissue = Tissue.URINE if "cumulative" in name else Tissue.PLASMA
            for intervention in self.interventions_uge:
                if (intervention != "CAN0") or (intervention == "CAN0" and sid == "KI__UGE"):
                    mappings[f"fm_po_can_{intervention}_{name}"] = FitMapping(
                        self,
                        reference=FitData(
                            self,
                            dataset=f"{name}_{intervention}",
                            xid="time",
                            yid="mean",
                            yid_sd="mean_sd",
                            count="count",
                        ),
                        observable=FitData(
                            self, task=f"task_po_can_{intervention}", xid="time", yid=f"{sid}",
                        ),
                        metadata=CanagliflozinMappingMetaData(
                            tissue=tissue,
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
            **self.figure_single(),
            **self.figure_urine(),
            **self.figure_uge()
        }

    def figure_single(self) -> Dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig1",
            num_rows=1,
            num_cols=3,
            name=f"{self.__class__.__name__} (Healthy)",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit=self.unit_time), legend=True)
        plots[0].set_yaxis(self.label_can, unit=self.unit_can)
        plots[1].set_yaxis(self.label_m5, unit=self.unit_m5)
        plots[2].set_yaxis(self.label_m7, unit=self.unit_m7)

        for intervention, key in self.interventions.items():
            for k, sid in enumerate(self.info):
                # simulation
                plots[k].add_data(
                    task=f"task_po_can_{intervention}",
                    xid="time",
                    yid=f"[Cve_{sid}]",
                    label=f"{key} mg PO",
                    color=self.dose_colors[key],
                )
                # data
                did = self.info[sid]
                plots[k].add_data(
                    dataset=f"{did}_{intervention}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=f"{key} mg PO",
                    color=self.dose_colors[key],
                )

        return {fig.sid: fig}

    def figure_urine(self) -> Dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig2",
            num_rows=1,
            num_cols=3,
            name=f"{self.__class__.__name__} (Healthy)",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit=self.unit_time), legend=True)
        plots[0].set_yaxis(self.label_can_urine, unit=self.unit_can_urine)
        plots[1].set_yaxis(self.label_m5_urine, unit=self.unit_m5_urine)
        plots[2].set_yaxis(self.label_m7_urine, unit=self.unit_m7_urine)

        for intervention, key in self.interventions.items():
            for k, sid in enumerate(self.info):
                # simulation
                plots[k].add_data(
                    task=f"task_po_can_{intervention}",
                    xid="time",
                    yid=f"Aurine_{sid}",
                    label=f"{key} mg PO",
                    color=self.dose_colors[key],
                )
                # data
                did = self.info[sid]
                plots[k].add_data(
                    dataset=f"{did}_cumulative_amount_{intervention}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=f"{key} mg PO",
                    color=self.dose_colors[key],
                    linestyle = ""
                )

        return {fig.sid: fig}

    def figure_uge(self) -> Dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig3",
            num_rows=1,
            num_cols=2,
            name=f"{self.__class__.__name__} (healthy)",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit=self.unit_time), legend=True)
        plots[0].set_yaxis(self.label_uge, unit=self.unit_uge)
        plots[1].set_yaxis(self.label_rtg, unit=self.unit_rtg)

        for intervention in self.interventions_uge:
            dose = self.interventions_uge[intervention]
            # simulation
            for k, sid in enumerate(["UGE", "RTG"]):
                plots[k].add_data(
                    task=f"task_po_can_{intervention}",
                    xid="time",
                    yid=f"KI__{sid}",
                    label=f"{dose} mg PO",
                    color=self.dose_colors[dose],
                )
            # data
            plots[0].add_data(
                dataset=f"glucose_cumulative_amount_{intervention}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"{dose} mg PO",
                color=self.dose_colors[dose],
            )
            if intervention != "CAN0":
                for method in ["MDRD", "McrCl"]:
                    plots[1].add_data(
                        dataset=f"glucose_RT_{method}_{intervention}",
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                        label=f"{dose} mg PO ({method})",
                        color=self.dose_colors[dose],
                    )

        return {fig.sid: fig}


if __name__ == "__main__":
    run_experiments(Chen2015, output_dir=Chen2015.__name__)

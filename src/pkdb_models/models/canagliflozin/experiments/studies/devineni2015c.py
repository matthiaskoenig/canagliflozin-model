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


class Devineni2015c(CanagliflozinSimulationExperiment):
    """Simulation experiment of Devineni2015c.

    Hepatic and renal impairment
    """

    conditions_hepatic = {
        "normal_hepatic": "Control",
        "mild_hepatic": "Mild cirrhosis",
        "moderate_hepatic": "Moderate cirrhosis"
    }

    conditions_renal = {
        "normal_renal": "Normal renal function",
        "mild_renal": "Mild renal impairment",
        "moderate_renal": "Moderate renal impairment",
        "severe_renal": "Severe renal impairment",
        # "esrd_pre_renal": "End stage renal disease",
        # "esrd_post_renal": "End stage renal disease"
    }

    conditions_rtg = {
        "normal_renal": "Normal renal function",
        "mild_renal": "Mild renal impairment",
        "moderate_renal": "Moderate renal impairment",
        "severe_renal": "Severe renal impairment"
    }

    info = {
        "can": "canagliflozin",
        "m5": "M5",
        "m7": "M7",
    }

    bodyweights_renal = {
        "normal_hepatic": 78.3,
        "mild_hepatic": 79,
        "moderate_hepatic": 74.7,
        "normal_renal": 92.5,
        "mild_renal": 70.1,
        "moderate_renal": 77.7,
        "severe_renal": 72.7,
        "esrd_pre_renal": 104,
        "esrd_post_renal": 104
    }

    bodyweights_hepatic = {
        "normal_hepatic": 78.3,
        "mild_hepatic": 79,
        "moderate_hepatic": 74.7
    }

    # fpg
    fpg = 5  # [mM] (nondiabetic, could be higher, no inclusion criteria given)
    def datasets(self) -> Dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig2", "Fig3", "Fig5", "Tab2A", "Tab3A", "Tab5A"]:
            df = load_pkdb_dataframe(f"{self.sid}_{fig_id}", data_path=self.data_path)
            for label, df_label in df.groupby("label"):
                dset = DataSet.from_df(df_label, self.ureg)

                # unit conversion to mole/l
                if label.startswith("canagliflozin"):
                    dset.unit_conversion("mean", 1 / self.Mr.can)
                elif label.startswith("M5"):
                    dset.unit_conversion("mean", 1 / self.Mr.m5)
                elif label.startswith("M7"):
                    dset.unit_conversion("mean", 1 / self.Mr.m7)
                elif label.startswith("glucose_RT"):
                    dset.unit_conversion("mean", 1 / self.Mr.glc)
                dsets[f"{label}"] = dset

        # console.print(dsets)
        # console.print(dsets.keys())
        return dsets

    def simulations(self) -> Dict[str, TimecourseSim]:
        Q_ = self.Q_
        tcsims = {}

        # renal
        for condition, renal_class in self.conditions_renal.items():
            tcsims[f"po_can200_{condition}"] = TimecourseSim(
                Timecourse(
                    start=0,
                    end=30 * 60,  # [min]
                    steps=500,
                    changes={
                        **self.default_changes(),
                        "BW": Q_(self.bodyweights_renal[condition], "kg"),
                        "PODOSE_can": Q_(200, "mg"),
                        "[KI__fpg]": Q_(self.fpg, "mM"),
                        "KI__f_renal_function": Q_(self.renal_map[renal_class], "dimensionless")
                    },
                )
            )

        # hepatic
        for condition, hepatic_class in self.conditions_hepatic.items():
            tcsims[f"po_can300_{condition}"] = TimecourseSim(
                Timecourse(
                    start=0,
                    end=30 * 60,  # [min]
                    steps=500,
                    changes={
                        **self.default_changes(),
                        "BW": Q_(self.bodyweights_hepatic[condition], "kg"),
                        "PODOSE_can": Q_(300, "mg"),
                        "[KI__fpg]": Q_(self.fpg, "mM"),
                        "f_cirrhosis": Q_(self.cirrhosis_map[hepatic_class], "dimensionless")
                    },
                )
            )

        return tcsims

    def fit_mappings(self) -> Dict[str, FitMapping]:
        mappings = {}

        #renal
        for condition in self.conditions_renal.keys():
            for name, sid in [
                ('canagliflozin', '[Cve_can]'),
                ('M5', '[Cve_m5]'),
                ('M7', '[Cve_m7]'),
                ('canagliflozin_cumulative_amount', 'Aurine_can'),
                ('M5_cumulative_amount', 'Aurine_m5'),
                ('M7_cumulative_amount', 'Aurine_m7'),
                ('glucose_cumulative_amount', 'KI__UGE'),
                ('glucose_RT', 'KI__RTG'),
                ('glucose_RT_mean', 'KI__RTG'),
            ]:

                tissue = Tissue.URINE if "cumulative" in name else Tissue.PLASMA
                health = Health.HEALTHY if condition == "normal_renal" else Health.RENAL_IMPAIRMENT

                if name == 'glucose_cumulative_amount' or name == 'glucose_RT' or name == 'glucose_RT_mean' and 'esrd' in condition:
                    continue
                else:
                    mappings[f"fm_po_can200_{condition}_{name}"] = FitMapping(
                        self,
                        reference=FitData(
                            self,
                            dataset=f"{name}_CAN200_{condition}",
                            xid="time",
                            yid="mean",
                            yid_sd="mean_sd",
                            count="count",
                        ),
                        observable=FitData(
                            self, task=f"task_po_can200_{condition}", xid="time", yid=f"{sid}",
                        ),
                        metadata=CanagliflozinMappingMetaData(
                            tissue=tissue,
                            route=Route.PO,
                            application_form=ApplicationForm.TABLET,
                            dosing=Dosing.SINGLE,
                            health=health,
                            fasting=Fasting.FASTED,
                        ),
                    )

        #hepatic
        for condition in self.conditions_hepatic:
            for name, sid in [('canagliflozin', '[Cve_can]'), ('canagliflozin_cumulative_amount', 'Aurine_can'),
                              ('M5_cumulative_amount', 'Aurine_m5'), ('M7_cumulative_amount', 'Aurine_m7')]:

                tissue = Tissue.URINE if "cumulative" in name else Tissue.PLASMA
                health = Health.HEALTHY if condition == "normal_hepatic" else Health.HEPATIC_IMPAIRMENT
                mappings[f"fm_po_can300_{condition}_{sid}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=f"{name}_CAN300_{condition}",
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                    ),
                    observable=FitData(
                        self, task=f"task_po_can300_{condition}", xid="time", yid=f"{sid}",
                    ),
                    metadata=CanagliflozinMappingMetaData(
                        tissue=tissue,
                        route=Route.PO,
                        application_form=ApplicationForm.TABLET,
                        dosing=Dosing.MULTIPLE,
                        health=health,
                        fasting=Fasting.FASTED,
                    ),
                )

        return mappings

    def figures(self) -> Dict[str, Figure]:
        return {
            **self.figure_renal(),
            **self.figure_hepatic(),
            **self.urine_renal(),
            **self.urine_hepatic(),
            **self.figure_rtg(),
            **self.figure_uge()
        }

    def figure_renal(self) -> Dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig_renal",
            num_rows=1,
            num_cols=3,
            name=f"{self.__class__.__name__} (Nondiabetic)",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit=self.unit_time), legend=True)
        plots[0].set_yaxis(self.label_can, unit=self.unit_can)
        plots[1].set_yaxis(self.label_m5, unit=self.unit_m5)
        plots[2].set_yaxis(self.label_m7, unit=self.unit_m7)

        # simulation
        for condition, impairment in self.conditions_renal.items():
            label_short = impairment.split()[0]
            for k, sid in enumerate(self.info):
                plots[k].add_data(
                    task=f"task_po_can200_{condition}",
                    xid="time",
                    yid=f"[Cve_{sid}]",
                    label=f"200 mg PO ({label_short})",
                    color=self.renal_colors[impairment],
                )

                # data
                did = self.info[sid]
                plots[k].add_data(
                    dataset=f"{did}_CAN200_{condition}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=f"200 mg PO ({label_short})",
                    color=self.renal_colors[impairment],
                )

        return {
            fig.sid: fig,
        }

    def figure_hepatic(self) -> Dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig_hepatic",
            num_rows=1,
            num_cols=3,
            name=f"{self.__class__.__name__} (Nondiabetic)",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit=self.unit_time), legend=True)
        plots[0].set_yaxis(self.label_can, unit=self.unit_can)
        plots[1].set_yaxis(self.label_m5, unit=self.unit_m5)
        plots[2].set_yaxis(self.label_m7, unit=self.unit_m7)

        # simulation
        for condition, hepatic_class in self.conditions_hepatic.items():
            label_short = hepatic_class.split()[0] if hepatic_class != "Control" else "Normal"
            for k, sid in enumerate(self.info):
                plots[k].add_data(
                    task=f"task_po_can300_{condition}",
                    xid="time",
                    yid=f"[Cve_{sid}]",
                    label=f"300 mg PO ({label_short})",
                    color=self.cirrhosis_colors[hepatic_class],
                )

                # data
                did = self.info[sid]
                plots[k].add_data(
                    dataset=f"{did}_CAN300_{condition}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=f"300 mg PO ({label_short})",
                    color=self.cirrhosis_colors[hepatic_class],
                )

        return {
            fig.sid: fig,
        }

    def urine_renal(self) -> Dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig_urine_renal",
            num_rows=1,
            num_cols=3,
            name=f"{self.__class__.__name__} (Nondiabetic)",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit=self.unit_time), legend=True)
        plots[0].set_yaxis(self.label_can_urine, unit=self.unit_can_urine)
        plots[1].set_yaxis(self.label_m5_urine, unit=self.unit_m5_urine)
        plots[2].set_yaxis(self.label_m7_urine, unit=self.unit_m7_urine)

        for condition, impairment in self.conditions_renal.items():
            label_short = impairment.split()[0]
            for k, sid in enumerate(self.info):
                # simulation
                plots[k].add_data(
                    task=f"task_po_can200_{condition}",
                    xid="time",
                    yid=f"Aurine_{sid}",
                    label=f"200 mg PO ({label_short})",
                    color=self.renal_colors[impairment],
                )

                # data
                did = self.info[sid]
                plots[k].add_data(
                    dataset=f"{did}_cumulative_amount_CAN200_{condition}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=f"200 mg PO ({label_short})",
                    color=self.renal_colors[impairment],
                )

        return {
            fig.sid: fig,
        }

    def urine_hepatic(self) -> Dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig_urine_hepatic",
            num_rows=1,
            num_cols=3,
            name=f"{self.__class__.__name__} (Nondiabetic)",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit=self.unit_time), legend=True)
        plots[0].set_yaxis(self.label_can_urine, unit=self.unit_can_urine)
        plots[1].set_yaxis(self.label_m5_urine, unit=self.unit_m5_urine)
        plots[2].set_yaxis(self.label_m7_urine, unit=self.unit_m7_urine)

        for condition, hepatic_class in self.conditions_hepatic.items():
            label_short = hepatic_class.split()[0] if hepatic_class != "Control" else "Normal"
            for k, sid in enumerate(self.info):
                # simulation
                plots[k].add_data(
                    task=f"task_po_can300_{condition}",
                    xid="time",
                    yid=f"Aurine_{sid}",
                    label=f"300 mg PO ({label_short})",
                    color=self.cirrhosis_colors[hepatic_class],
                )

                # data
                did = self.info[sid]
                plots[k].add_data(
                    dataset=f"{did}_cumulative_amount_CAN300_{condition}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=f"300 mg PO ({label_short})",
                    color=self.cirrhosis_colors[hepatic_class],
                )

        return {
            fig.sid: fig,
        }

    def figure_rtg(self) -> Dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig_rtg",
            num_rows=1,
            num_cols=1,
            name=f"{self.__class__.__name__} (Nondiabetic)",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit=self.unit_time), legend=True)
        plots[0].set_yaxis(self.label_rtg, unit=self.unit_rtg)

        for condition, impairment in self.conditions_rtg.items():
            label_short = impairment.split()[0]

            # simulation
            plots[0].add_data(
                task=f"task_po_can200_{condition}",
                xid="time",
                yid=f"KI__RTG",
                label=f"200 mg PO ({label_short})",
                color=self.renal_colors[impairment],
            )

            # data
            plots[0].add_data(
                dataset=f"glucose_RT_CAN200_{condition}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"200 mg PO ({label_short})",
                color=self.renal_colors[impairment],
            )

        return {
            fig.sid: fig,
        }

    def figure_uge(self) -> Dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig_uge",
            num_rows=1,
            num_cols=2,
            name=f"{self.__class__.__name__} (Nondiabetic)",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit=self.unit_time), legend=True)
        plots[0].set_yaxis(self.label_uge, unit=self.unit_uge)
        plots[1].set_yaxis(self.label_rtg, unit=self.unit_rtg)

        for condition, impairment in self.conditions_rtg.items():
            label_short = impairment.split()[0]

            # simulation
            plots[0].add_data(
                task=f"task_po_can200_{condition}",
                xid="time",
                yid=f"KI__UGE",
                label=f"200 mg PO ({label_short})",
                color=self.renal_colors[impairment],
            )

            plots[1].add_data(
                task=f"task_po_can200_{condition}",
                xid="time",
                yid=f"KI__RTG",
                label=f"200 mg PO ({label_short})",
                color=self.renal_colors[impairment],
            )

            # data
            plots[0].add_data(
                dataset=f"glucose_cumulative_amount_CAN200_{condition}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"200 mg PO ({label_short})",
                color=self.renal_colors[impairment],
            )

            plots[1].add_data(
                dataset=f"glucose_RT_mean_CAN200_{condition}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"200 mg PO ({label_short})",
                color=self.renal_colors[impairment],
            )

        return {
            fig.sid: fig,
        }


if __name__ == "__main__":
    run_experiments(Devineni2015c, output_dir=Devineni2015c.__name__)

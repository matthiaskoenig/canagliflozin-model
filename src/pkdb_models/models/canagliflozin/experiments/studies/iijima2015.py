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


class Iijima2015(CanagliflozinSimulationExperiment):
    """Simulation experiment of Iijima2015."""

    doses = [25, 100, 200, 400]
    doses_uge = [25, 100, 200, 400]
    interventions = ["CAN0", "CAN25", "CAN100", "CAN200", "CAN400"]
    colors = {0: "black", 25: "blue", 100: "orange", 200: "green", 400: "red"}

    info = [
        ("[Cve_can]", "canagliflozin"),
        ("KI__UGE", "glucose_cumulative_amount")
    ]

    bodyweights = {0: 69.73, 25: 74.24, 100: 73.44, 200: 63.67, 400: 73.88}
    fpg = {0: 184.9, 25: 172.2, 100: 162.5, 200: 163.4, 400: 170.9}

    def datasets(self) -> Dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig2", "Fig3", "Tab2A"]:
            df = load_pkdb_dataframe(f"{self.sid}_{fig_id}", data_path=self.data_path)
            for label, df_label in df.groupby("label"):
                dset = DataSet.from_df(df_label, self.ureg)

                # unit conversion to mole/l
                if label.startswith("canagliflozin_"):
                    dset.unit_conversion("mean", 1 / self.Mr.can)
                elif label.startswith("glucose_renal"):
                    dset.unit_conversion("mean", 1 / self.Mr.glc)

                dsets[f"{label}"] = dset

        # console.print(dsets)
        # console.print(dsets.keys())
        return dsets

    def simulations(self) -> Dict[str, TimecourseSim]:
        Q_ = self.Q_
        tcsims = {}

        # single dose
        for dose in self.doses:
            tcsims[f"po_can{dose}_single"] = TimecourseSim(
                Timecourse(
                    start=0,
                    end=30 * 60,  # [min]
                    steps=500,
                    changes={
                        **self.default_changes(),
                        "BW": Q_(self.bodyweights[dose], "kg"),
                        "[KI__fpg]": Q_(self.fpg[dose] / 18, "mM"),
                        "PODOSE_can": Q_(dose, "mg"),
                    },
                )
            )

        # multiple dose
        for dose in self.doses_uge:
            tc0 = Timecourse(
                start=0,
                end=48 * 60,  # [min]
                steps=500,
                changes={
                    **self.default_changes(),
                    "BW": Q_(self.bodyweights[dose], "kg"),
                    "[KI__fpg]": Q_(self.fpg[dose] / 18, "mM"),
                    "PODOSE_can": Q_(dose, "mg"),
                },
            )
            tc1 = Timecourse(
                start=0,
                end=24 * 60,  # [min]
                steps=500,
                changes={
                    "BW": Q_(self.bodyweights[dose], "kg"),
                    "[KI__fpg]": Q_(self.fpg[dose] / 18, "mM"),
                    "KI__glc_urine": Q_(0, "mmole"),  # reset UGE
                    "PODOSE_can": Q_(dose, "mg"),
                    "Aurine_can": Q_(0, "mmole"),  # reset the urinary amount for collection
                },
            )
            tc2 = Timecourse(
                start=0,
                end=72 * 60,  # [min]
                steps=500,
                changes={
                    "BW": Q_(self.bodyweights[dose], "kg"),
                    "[KI__fpg]": Q_(self.fpg[dose] / 18, "mM"),
                    "KI__glc_urine": Q_(0, "mmole"),  # reset UGE
                    "PODOSE_can": Q_(dose, "mg"),
                    "Aurine_can": Q_(0, "mmole"),  # reset the urinary amount for collection
                },
            )

            tcsims[f"po_can{dose}_multi"] = TimecourseSim(
                [tc0] + [tc1 for _ in range(14)] + [tc2],
                time_offset=-16 * 24 * 60,
            )

        return tcsims

    def fit_mappings(self) -> Dict[str, FitMapping]:

        mappings = {}

        for day in ['d1', 'd16']:

            dosing = Dosing.SINGLE if day == 'd1' else Dosing.MULTIPLE
            type_dosing = 'single' if day == 'd1' else 'multi'

            for name, sid in [
                ('canagliflozin', '[Cve_can]'),
                ('glucose_cumulative_amount', 'KI__UGE'),
                ('glucose_renal_threshold', 'KI__RTG'),
                ('canagliflozin_urine', 'Aurine_can')
            ]:

                if name == 'glucose_renal_threshold' or name == 'glucose_cumulative_amount' and day == 'd1':
                    continue

                else:
                    for dose in self.doses:
                        tissue = Tissue.URINE if "cumulative" in name else Tissue.PLASMA
                        mappings[f"task_po_can{dose}_{name}"] = FitMapping(
                            self,
                            reference=FitData(
                                self,
                                dataset=f"{name}_CAN{dose}_{day}",
                                xid="time",
                                yid="mean",
                                yid_sd="mean_sd",
                                count="count",
                            ),
                            observable=FitData(
                                self, task=f"task_po_can{dose}_{type_dosing}", xid="time", yid=sid,
                            ),
                            metadata=CanagliflozinMappingMetaData(
                                tissue=tissue,
                                route=Route.PO,
                                application_form=ApplicationForm.TABLET,
                                dosing=dosing,
                                health=Health.T2DM,
                                fasting=Fasting.FASTED,
                            ),
                        )

        # console.print(mappings)
        return mappings

    def figures(self) -> Dict[str, Figure]:
        return {
            **self.figure_single_multi(),
            **self.figure_uge(),
            **self.figure_urine(),
            **self.figure_rtg()
        }

    def figure_single_multi(self) -> Dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="urine single and multi",
            num_rows=1,
            num_cols=2,
            name=f"{self.__class__.__name__} (T2DM)",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit=self.unit_time), legend=True)
        plots[0].set_yaxis(self.label_can, unit=self.unit_can)
        plots[1].set_yaxis(self.label_can, unit=self.unit_can)

        for dose in self.doses:
            for k, day in enumerate(['d1', 'd16']):
                type_dosing = 'single' if day == 'd1' else 'multi'
                # simulation
                plots[k].add_data(
                    task=f"task_po_can{dose}_{type_dosing}",
                    xid="time",
                    yid=f"[Cve_can]",
                    label=f"{dose} mg PO",
                    color=self.dose_colors[dose],
                )

                # data
                plots[k].add_data(
                    dataset=f"canagliflozin_CAN{dose}_{day}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=f"{dose} mg PO",
                    color=self.dose_colors[dose],
                )

        return {
            fig.sid: fig,
        }

    def figure_uge(self) -> Dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig_uge",
            num_rows=1,
            num_cols=1,
            name=f"{self.__class__.__name__} (T2DM)",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="day"), legend=True)
        plots[0].set_yaxis(self.label_uge, unit=self.unit_uge)

        for dose in self.doses_uge:
            # simulation
            plots[0].add_data(
                task=f"task_po_can{dose}_multi",
                xid="time",
                yid=f"KI__UGE",
                label=f"{dose} mg PO",
                color=self.dose_colors[dose],
            )
            # data
            plots[0].add_data(
                dataset=f"glucose_cumulative_amount_CAN{dose}_d16",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"{dose} mg PO",
                color=self.dose_colors[dose],
                linestyle=""
            )

        return {
            fig.sid: fig,
        }

    def figure_urine(self) -> Dict[str, Figure]:

        fig = Figure(
            experiment=self,
            sid="Fig_urine",
            num_rows=1,
            num_cols=2,
            name=f"{self.__class__.__name__} (T2DM)",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit=self.unit_time), legend=True)
        plots[0].set_yaxis(self.label_can_urine, unit=self.unit_can_urine)
        plots[1].set_yaxis(self.label_can_urine, unit=self.unit_can_urine)

        for dose in self.doses:
            for k, day in enumerate(['d1', 'd16']):
                type_dosing = 'single' if day == 'd1' else 'multi'
                # simulation
                plots[k].add_data(
                    task=f"task_po_can{dose}_{type_dosing}",
                    xid="time",
                    yid=f"Aurine_can",
                    label=f"{dose} mg PO",
                    color=self.dose_colors[dose],
                )

                # data
                plots[k].add_data(
                    dataset=f"canagliflozin_urine_CAN{dose}_{day}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=f"{dose} mg PO",
                    color=self.dose_colors[dose],
                    linestyle=""
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
            name=f"{self.__class__.__name__} (T2DM)",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit=self.unit_time), legend=True)
        plots[0].set_yaxis(self.label_rtg, unit=self.unit_rtg)

        for dose in self.doses:
            # simulation
            plots[0].add_data(
                task=f"task_po_can{dose}_multi",
                xid="time",
                yid=f"KI__RTG",
                label=f"{dose} mg PO",
                color=self.dose_colors[dose],
            )

            # data
            plots[0].add_data(
                dataset=f"glucose_renal_threshold_CAN{dose}_d16",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"{dose} mg PO",
                color=self.dose_colors[dose],
                linestyle=""
            )

        return {
            fig.sid: fig,
        }


if __name__ == "__main__":
    run_experiments(Iijima2015, output_dir=Iijima2015.__name__)
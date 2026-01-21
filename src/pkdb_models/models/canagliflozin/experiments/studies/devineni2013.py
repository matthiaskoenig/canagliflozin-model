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


class Devineni2013(CanagliflozinSimulationExperiment):
    """Simulation experiment of Devineni2013."""

    bodyweights = {0: 84.2, 50: 82.9,  100: 82.2, 300: 83.2}
    fpg = {0: 182, 50: 189, 100: 182, 300: 185}  # [mg/dl]
    gfr = {0: 117.9, 50: 110.1, 100: 106.3, 300: 121.8}  # [ml/min]

    doses = [0, 50, 100, 300]
    interventions = ["CAN0", "CAN50", "CAN100", "CAN300"]

    info = {
        "can": "canagliflozin",
        "m5": "M5",
        "m7": "M7",
    }

    def datasets(self) -> Dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1", "Tab2A", "Tab3A"]:
            df = load_pkdb_dataframe(f"{self.sid}_{fig_id}", data_path=self.data_path)
            for label, df_label in df.groupby("label"):
                dset = DataSet.from_df(df_label, self.ureg)
                # unit conversion to mole/l
                if label.startswith("canagliflozin_"):
                    dset.unit_conversion("mean", 1 / self.Mr.can)
                elif label.startswith("M5_"):
                    dset.unit_conversion("mean", 1 / self.Mr.m5)
                elif label.startswith("M7_"):
                    dset.unit_conversion("mean", 1 / self.Mr.m7)
                elif label.startswith("glucose_renal_threshold"):
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
                    end=25 * 60,  # [min]
                    steps=500,
                    changes={
                        **self.default_changes(),
                        "BW": Q_(self.bodyweights[dose], "kg"),
                        "[KI__fpg]": Q_(self.fpg[dose] / 18, "mM"),
                        "KI__f_renal_function": Q_(self.gfr[dose] / 100, "dimensionless"),  # [0, 1]  <=> [0, 100] gfr
                        "PODOSE_can": Q_(dose, "mg"),
                    },
                )
            )

        # multiple dose
        for dose in self.doses:
            tc0 = Timecourse(
                start=0,
                end=24 * 60,  # [min]
                steps=500,
                changes={
                    **self.default_changes(),
                    "PODOSE_can": Q_(0, "mg"),
                },
            )
            changes_multi = {
                "BW": Q_(self.bodyweights[dose], "kg"),
                "[KI__fpg]": Q_(self.fpg[dose] / 18, "mM"),
                "KI__f_renal_function": Q_(self.gfr[dose] / 100, "dimensionless"),  # [0, 1]  <=> [0, 100] gfr
                "KI__glc_urine": Q_(0, "mmole"),  # reset UGE
                "Aurine_can": Q_(0, "mmole"),  # reset canagliflozin
                "Aurine_m5": Q_(0, "mmole"),  # reset M5
                "Aurine_m7": Q_(0, "mmole"),  # reset M7
                "PODOSE_can": Q_(dose, "mg"),
            }
            tc1 = Timecourse(
                start=0,
                end=24 * 60,  # [min]
                steps=500,
                changes=changes_multi
            )
            tc2 = Timecourse(
                start=0,
                end=25 * 60,  # [min]
                steps=500,
                changes=changes_multi
            )

            tcsims[f"po_can{dose}_multi"] = TimecourseSim(
                [tc0] + [tc1 for _ in range(6)] + [tc2],
                time_offset=-7 * 24 * 60,
            )

        return tcsims

    def fit_mappings(self) -> Dict[str, FitMapping]:

        mappings = {}

        for name, sid in [
            ('canagliflozin', '[Cve_can]'),
            ('canagliflozin_cumulative_amount', 'Aurine_can'),
            ('M5_cumulative_amount', 'Aurine_m5'),
            ('M7_cumulative_amount', 'Aurine_m7')
        ]:
            for day in ['d1', 'd7']:
                dosing = Dosing.SINGLE if day == 'd1' else Dosing.MULTIPLE
                type_dosing = 'single' if day == 'd1' else 'multi'

                for dose in self.doses[1:]:
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
                            tissue=Tissue.URINE if "cumulative" in name else Tissue.PLASMA,
                            route=Route.PO,
                            application_form=ApplicationForm.TABLET,
                            dosing=dosing,
                            health=Health.T2DM,
                            fasting=Fasting.FASTED,
                        ),
                    )
        for name, sid in [
            ('glucose_cumulative_amount', 'KI__UGE'),
            ('glucose_renal_threshold', 'KI__RTG'),
        ]:
            for dose in self.doses:
                mappings[f"task_po_can{dose}_{name}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=f"{name}_CAN{dose}",
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                    ),
                    observable=FitData(
                        self, task=f"task_po_can{dose}_{type_dosing}", xid="time", yid=sid,
                    ),
                    metadata=CanagliflozinMappingMetaData(
                        tissue=Tissue.URINE,
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
            **self.figures_urine(),
            **self.figure_uge(),
            **self.figure_rtg()
        }

    def figure_single_multi(self) -> Dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="urine single",
            num_rows=1,
            num_cols=2,
            name=f"{self.__class__.__name__} (T2DM)",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit=self.unit_time), legend=True)
        plots[0].set_yaxis(self.label_can, unit=self.unit_can)
        plots[1].set_yaxis(self.label_can, unit=self.unit_can)

        for dose in self.doses[1:]:
            for k, day in enumerate(['d1', 'd7']):
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

    def figures_urine(self) -> Dict[str, Figure]:
        figures = {}
        for dosing in ["single", "multi"]:
            day = "d1" if dosing == "single" else "d7"

            fig = Figure(
                experiment=self,
                sid=f"Fig_urine_{dosing}",
                num_rows=1,
                num_cols=3,
                name=f"{self.__class__.__name__} (T2DM)",
            )
            plots = fig.create_plots(xaxis=Axis(self.label_time, unit=self.unit_time), legend=True)
            plots[0].set_yaxis(self.label_can_urine, unit=self.unit_can_urine)
            plots[1].set_yaxis(self.label_m5_urine, unit=self.unit_m5_urine)
            plots[2].set_yaxis(self.label_m7_urine, unit=self.unit_m7_urine)

            for dose in self.doses[1:]:
                for k, sid in enumerate(self.info):
                    # simulation
                    plots[k].add_data(
                        task=f"task_po_can{dose}_{dosing}",
                        xid="time",
                        yid=f"Aurine_{sid}",
                        label=f"{dose} mg PO",
                        color=self.dose_colors[dose],
                    )

                    # data
                    did = self.info[sid]
                    plots[k].add_data(
                        dataset=f"{did}_cumulative_amount_CAN{dose}_{day}",
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                        label=f"{dose} mg PO",
                        color=self.dose_colors[dose],
                        linestyle="",
                    )
            figures[fig.sid] = fig

        return figures

    def figure_uge(self) -> Dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig_uge",
            name=f"{self.__class__.__name__} (T2DM)",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="day"), legend=True)
        plots[0].set_yaxis(self.label_uge, unit=self.unit_uge)

        for dose in self.doses:
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
                dataset=f"glucose_cumulative_amount_CAN{dose}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"{dose} mg PO",
                color=self.dose_colors[dose],
                linestyle="",
            )

        return {
            fig.sid: fig,
        }

    def figure_rtg(self) -> Dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig_rtg",
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
                dataset=f"glucose_renal_threshold_CAN{dose}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"{dose} mg PO",
                color=self.dose_colors[dose],
                linestyle="",
            )

        return {
            fig.sid: fig,
        }


if __name__ == "__main__":
    run_experiments(Devineni2013, output_dir=Devineni2013.__name__)
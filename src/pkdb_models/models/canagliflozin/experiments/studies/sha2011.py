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


class Sha2011(CanagliflozinSimulationExperiment):
    """Simulation experiment of Sha2011."""

    doses = [0, 10, 30, 100, 200, 400, 600, 800]

    colors = {0: "black", 10: "#191970", 30: "#0000FF", 100: "#6495ED",
              200: "#87CEEB", 400: "#00CED1", 600: "#00FFFF", 800: "#66CDAA", "400_BID": "#00FA9A"}

    fpg = 5  # mM (healthy)
    gfr = 97.1  # [ml/min/1.73*m^2]
    bodyweight = 75 # [kg] (no data given, but BMI=24)

    def datasets(self) -> Dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1"]:
            df = load_pkdb_dataframe(f"{self.sid}_{fig_id}", data_path=self.data_path)
            for label, df_label in df.groupby("label"):
                dset = DataSet.from_df(df_label, self.ureg)
                # unit conversion to mole/l
                if label.startswith("renal_threshold"):
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
                    end=24 * 60,  # [min]
                    steps=500,
                    changes={
                        **self.default_changes(),
                        "BW": Q_(self.bodyweight, "kg"),
                        "[KI__fpg]": Q_(self.fpg, "mM"),
                        "KI__f_renal_function": Q_(self.gfr / 100, "dimensionless"),  # [0, 1]  <=> [0, 100] gfr
                        "PODOSE_can": Q_(dose, "mg"),
                    },
                )
            )

            # multiple dose (twice daily)
            dose = 400  # [mg]
            tc0 = Timecourse(
                start=0,
                end=12 * 60,  # [min]
                steps=500,
                changes={
                    **self.default_changes(),
                    "BW": Q_(self.bodyweight, "kg"),
                    "[KI__fpg]": Q_(self.fpg, "mM"),
                    "KI__f_renal_function": Q_(self.gfr / 100, "dimensionless"),  # [0, 1]  <=> [0, 100] gfr
                    "PODOSE_can": Q_(dose, "mg"),
                },
            )
            tc1 = Timecourse(
                start=0,
                end=12 * 60,  # [min]
                steps=500,
                changes={
                    "BW": Q_(self.bodyweight, "kg"),
                    "[KI__fpg]": Q_(self.fpg, "mM"),
                    "KI__f_renal_function": Q_(self.gfr / 100, "dimensionless"),  # [0, 1]  <=> [0, 100] gfr
                    # "KI__glc_urine": Q_(0, "mmole"),  # reset UGE
                    "PODOSE_can": Q_(dose, "mg"),
                },
            )
            tcsims[f"po_can{dose}_multi"] = TimecourseSim(
                [tc0] + [tc1]
            )

        return tcsims

    def fit_mappings(self) -> Dict[str, FitMapping]:

        mappings = {}

        for name, sid in [
            ('cumulative_amount', 'KI__UGE'),
            ('renal_threshold', 'KI__RTG'),
        ]:

            for dose in self.doses:

                if dose == 0 and name == 'renal_threshold':
                    continue

                else:
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
                            self, task=f"task_po_can{dose}_single", xid="time", yid=sid,
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

        for name, sid in [
            ('cumulative_amount', 'KI__UGE'),
            ('renal_threshold', 'KI__RTG'),
        ]:

            dose = 400
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
                    self, task=f"task_po_can{dose}_multi", xid="time", yid=sid,
                ),
                metadata=CanagliflozinMappingMetaData(
                    tissue=Tissue.URINE if "cumulative" in name else Tissue.PLASMA,
                    route=Route.PO,
                    application_form=ApplicationForm.SOLUTION,
                    dosing=Dosing.MULTIPLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                ),
            )

        # console.print(mappings)
        return mappings

    def figures(self) -> Dict[str, Figure]:
        return {
            **self.figure_uge(),
            **self.figure_rtg()
        }

    def figure_uge(self) -> Dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig_uge",
            name=f"{self.__class__.__name__} (Healthy)",
        )
        Figure.legend_fontsize = 9
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit=self.unit_time), legend=True)
        plots[0].set_yaxis(self.label_uge, unit=self.unit_uge)

        for dose in self.doses:
            # simulation
            plots[0].add_data(
                task=f"task_po_can{dose}_single",
                xid="time",
                yid=f"KI__UGE",
                label=f"{dose} mg PO",
                color=self.dose_colors[dose],
            )

        # 400 mg BID (twice daily)
        plots[0].add_data(
            task=f"task_po_can400_multi",
            xid="time",
            yid=f"KI__UGE",
            label=f"400 mg PO BID",
            color=self.dose_colors[400],
            linestyle="--",
        )

        for dose in self.doses:
            # data
            plots[0].add_data(
                dataset=f"cumulative_amount_CAN{dose}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"{dose} mg PO",
                color=self.dose_colors[dose],
            )

        plots[0].add_data(
            dataset=f"cumulative_amount_CAN400_BID",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label=f"400 mg PO BID",
            color=self.dose_colors[400],
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
        Figure.legend_fontsize=9
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit=self.unit_time), legend=True)
        plots[0].set_yaxis(self.label_rtg, unit=self.unit_rtg)

        for dose in self.doses[1:]:  # Skip 0 mg dose
            # simulation
            plots[0].add_data(
                task=f"task_po_can{dose}_single",
                xid="time",
                yid=f"KI__RTG",
                label=f"{dose} mg PO",
                color=self.dose_colors[dose],
            )

        # 400 mg BID (twice daily)
        plots[0].add_data(
            task=f"task_po_can400_multi",
            xid="time",
            yid=f"KI__RTG",
            label=f"400 mg PO BID",
            color=self.dose_colors[400],
            linestyle="--",
        )

        for dose in self.doses[1:]:  # Skip 0 mg dose
            # data
            plots[0].add_data(
                dataset=f"renal_threshold_CAN{dose}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"{dose} mg PO",
                color=self.dose_colors[dose],
            )

        plots[0].add_data(
            dataset=f"renal_threshold_CAN400",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label=f"400 mg PO BID",
            color=self.dose_colors[400],
        )

        return {
            fig.sid: fig,
        }


if __name__ == "__main__":
    run_experiments(Sha2011, output_dir=Sha2011.__name__)

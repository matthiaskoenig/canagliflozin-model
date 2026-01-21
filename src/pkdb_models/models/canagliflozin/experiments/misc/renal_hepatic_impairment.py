from typing import Dict
from sbmlsim.plot import Axis, Figure
from sbmlsim.simulation import Timecourse, TimecourseSim
from pkdb_models.models.canagliflozin.experiments.base_experiment import CanagliflozinSimulationExperiment
from pkdb_models.models.canagliflozin.helpers import run_experiments


class HepaticRenalImpairment(CanagliflozinSimulationExperiment):
    """Hepatic and renal impairment."""

    maps = {
        "hepatic": CanagliflozinSimulationExperiment.cirrhosis_map,
        "renal": CanagliflozinSimulationExperiment.renal_map,
    }
    colors = {
        "hepatic": CanagliflozinSimulationExperiment.cirrhosis_colors,
        "renal": CanagliflozinSimulationExperiment.renal_colors,
    }
    parameters = {
        "hepatic": "f_cirrhosis",
        "renal": "KI__f_renal_function",
    }

    dose_mg = 100
    dpi = 300
    legend_font_size = 10

    def simulations(self) -> Dict[str, TimecourseSim]:
        Q_ = self.Q_
        tcsims: Dict[str, TimecourseSim] = {}

        for impairment in ["hepatic", "renal"]:
            map_ = self.maps[impairment]
            parameter = self.parameters[impairment]

            for group, value in map_.items():
                key = f"can_{impairment}_{group.replace(' ', '_').replace('/', '_').lower()}"
                tcsims[key] = TimecourseSim(
                    Timecourse(
                        start=0,
                        end=24 * 60,  # minutes
                        steps=6000,
                        changes={
                            **self.default_changes(),
                            "PODOSE_can": Q_(self.dose_mg, "mg"),
                            parameter: Q_(value, "dimensionless"),
                        },
                    )
                )

        return tcsims

    def figures(self) -> Dict[str, Figure]:
        return {
            **self.figure_pk(),
            **self.figure_pd(),
        }

    def figure_pk(self) -> Dict[str, Figure]:
        figures: Dict[str, Figure] = {}
        Figure.legend_fontsize = self.legend_font_size
        Figure.fig_dpi = self.dpi

        sids = [
            # plasma
            "[Cve_can]",
            "[Cve_m5]",
            "[Cve_m7]",
            "[Cve_cantot]",
            # urine
            "Aurine_can",
            "Aurine_m5",
            "Aurine_m7",
            "Aurine_cantot",
            # feces
            "Afeces_can",
            "Afeces_m9",
            "Afeces_m7",
            "Afeces_cantot",
        ]

        for impairment in ["hepatic", "renal"]:
            map_ = self.maps[impairment]
            parameter = self.parameters[impairment]
            colors = self.colors[impairment]

            fig = Figure(
                experiment=self,
                sid=f"Fig_{parameter}_pk",
                num_rows=3,
                num_cols=4,
                name=f"Pharmacokinetics: {impairment.title()} impairment",
            )
            plots = fig.create_plots(xaxis=Axis(self.label_time, unit=self.unit_time), legend=True)

            for ksid, sid in enumerate(sids):
                plots[ksid].set_yaxis(label=self.labels[sid], unit=self.units[sid])

                for group, _ in map_.items():
                    task_id = f"task_can_{impairment}_{group.replace(' ', '_').replace('/', '_').lower()}"
                    plots[ksid].add_data(
                        task=task_id,
                        xid="time",
                        yid=sid,
                        label=group,
                        color=colors[group],
                    )

            figures[fig.sid] = fig

        return figures

    def figure_pd(self) -> Dict[str, Figure]:
        figures: Dict[str, Figure] = {}
        Figure.legend_fontsize = self.legend_font_size
        Figure.fig_dpi = self.dpi

        time_sids = ["KI__UGE", "KI__RTG", "[KI__fpg]"]
        xid_plasma = "[Cve_can]"

        for impairment in ["hepatic", "renal"]:
            map_ = self.maps[impairment]
            parameter = self.parameters[impairment]
            colors = self.colors[impairment]

            fig = Figure(
                experiment=self,
                sid=f"Fig_{parameter}_pd",
                num_rows=2,
                num_cols=3,
                name=f"Pharmacodynamics: {impairment.title()} impairment",
            )
            plots = fig.create_plots(xaxis=Axis(self.label_time, unit=self.unit_time), legend=True)

            plots[3].set_xaxis(label=self.label_can, unit=self.unit_can)
            plots[3].set_yaxis(label="Rate glucose excretion", unit="mmole/min")
            plots[4].set_xaxis(label=self.label_can, unit=self.unit_can)
            plots[4].set_yaxis(label=self.label_rtg, unit=self.unit_rtg)
            plots[5].set_xaxis(label=self.label_can, unit=self.unit_can)
            plots[5].set_yaxis(label=self.label_uge, unit=self.unit_uge)

            for ksid, sid in enumerate(time_sids):
                plots[ksid].set_yaxis(label=self.labels[sid], unit=self.units[sid])

            for group, _ in map_.items():
                task_id = f"task_can_{impairment}_{group.replace(' ', '_').replace('/', '_').lower()}"
                color = colors[group]

                for ksid, sid in enumerate(time_sids):
                    plots[ksid].add_data(
                        task=task_id,
                        xid="time",
                        yid=sid,
                        label=group,
                        color=color,
                    )

                plots[3].add_data(task=task_id, xid=xid_plasma, yid="KI__GLCEX", label=group, color=color)
                plots[4].add_data(task=task_id, xid=xid_plasma, yid="KI__RTG",   label=group, color=color)
                plots[5].add_data(task=task_id, xid=xid_plasma, yid="KI__UGE",   label=group, color=color)

            figures[fig.sid] = fig

        return figures


if __name__ == "__main__":
    run_experiments(HepaticRenalImpairment, output_dir=HepaticRenalImpairment.__name__)

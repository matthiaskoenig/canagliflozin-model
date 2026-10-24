"""Pharmacokinetics and pharmacodynamics in hepatic and renal impairment."""

from collections.abc import Mapping
from typing import ClassVar, override

from sbmlsim import Q
from sbmlsim.plot import Axis, Figure
from sbmlsim.simulation import Simulation

from pkdb_models.models.canagliflozin import MODEL
from pkdb_models.models.canagliflozin.experiments.base_experiment import (
    CanagliflozinSimulationExperiment,
)


class HepaticRenalImpairment(CanagliflozinSimulationExperiment):
    """Hepatic and renal impairment."""

    maps: ClassVar[dict[str, Mapping[str, float]]] = {
        "hepatic": CanagliflozinSimulationExperiment.cirrhosis_map,
        "renal": CanagliflozinSimulationExperiment.renal_map,
    }
    colors: ClassVar[dict[str, Mapping[str, str]]] = {
        "hepatic": CanagliflozinSimulationExperiment.cirrhosis_colors,
        "renal": CanagliflozinSimulationExperiment.renal_colors,
    }
    parameters: ClassVar[dict[str, str]] = {
        "hepatic": "f_cirrhosis",
        "renal": "KI__f_renal_function",
    }

    dose_mg = 100

    @staticmethod
    def _key(impairment: str, group: str) -> str:
        """Key of the simulation of a group of the impairment."""
        return f"can_{impairment}_{group.replace(' ', '_').replace('/', '_').lower()}"

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims: dict[str, Simulation] = {}

        for impairment in ["hepatic", "renal"]:
            map_ = self.maps[impairment]
            parameter = self.parameters[impairment]

            for group, value in map_.items():
                tcsims[self._key(impairment, group)] = Simulation(
                    time_unit="min",
                    end=24 * 60,
                    preinit_changes={
                        **self.default_changes(),
                        "PODOSE_can": Q(self.dose_mg, "mg"),
                        parameter: Q(value, "dimensionless"),
                    },
                )

        return tcsims

    @override
    def figures(self) -> dict[str, Figure]:
        return {
            **self.figure_pk(),
            **self.figure_pd(),
        }

    def figure_pk(self) -> dict[str, Figure]:
        """Timecourses of canagliflozin and its metabolites in plasma, urine and feces."""
        figures: list[Figure] = []

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
            plots = fig.create_plots(
                xaxis=Axis(self.label_time, unit=self.unit_time), legend=True
            )

            for ksid, sid in enumerate(sids):
                plots[ksid].set_yaxis(label=self.labels[sid], unit=self.units[sid])

                for group in map_:
                    task_id = f"task_{self._key(impairment, group)}"
                    plots[ksid].add_data(
                        task=task_id,
                        xid="time",
                        yid=sid,
                        label=group,
                        color=colors[group],
                    )

            figures.append(fig)

        return self.figures_by_sid(*figures)

    def figure_pd(self) -> dict[str, Figure]:
        """Timecourses of the glucose excretion and its dependency on canagliflozin."""
        figures: list[Figure] = []

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
            plots = fig.create_plots(
                xaxis=Axis(self.label_time, unit=self.unit_time), legend=True
            )

            plots[3].set_xaxis(label=self.label_can, unit=self.unit_can)
            plots[3].set_yaxis(label="Rate glucose excretion", unit="mmole/min")
            plots[4].set_xaxis(label=self.label_can, unit=self.unit_can)
            plots[4].set_yaxis(label=self.label_rtg, unit=self.unit_rtg)
            plots[5].set_xaxis(label=self.label_can, unit=self.unit_can)
            plots[5].set_yaxis(label=self.label_uge, unit=self.unit_uge)

            for ksid, sid in enumerate(time_sids):
                plots[ksid].set_yaxis(label=self.labels[sid], unit=self.units[sid])

            for group in map_:
                task_id = f"task_{self._key(impairment, group)}"
                color = colors[group]

                for ksid, sid in enumerate(time_sids):
                    plots[ksid].add_data(
                        task=task_id,
                        xid="time",
                        yid=sid,
                        label=group,
                        color=color,
                    )

                plots[3].add_data(
                    task=task_id,
                    xid=xid_plasma,
                    yid="KI__GLCEX",
                    label=group,
                    color=color,
                )
                plots[4].add_data(
                    task=task_id,
                    xid=xid_plasma,
                    yid="KI__RTG",
                    label=group,
                    color=color,
                )
                plots[5].add_data(
                    task=task_id,
                    xid=xid_plasma,
                    yid="KI__UGE",
                    label=group,
                    color=color,
                )

            figures.append(fig)

        return self.figures_by_sid(*figures)


if __name__ == "__main__":
    MODEL.run_experiments(
        HepaticRenalImpairment, output_dir=HepaticRenalImpairment.__name__
    )

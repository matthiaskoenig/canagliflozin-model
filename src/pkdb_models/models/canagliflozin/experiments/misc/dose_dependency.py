"""Dependency of the pharmacokinetics and pharmacodynamics on the dose and glucose."""

from typing import ClassVar, override

from sbmlsim import Q
from sbmlsim.plot import Axis, Figure
from sbmlsim.simulation import Simulation

from pkdb_models.models.canagliflozin import MODEL
from pkdb_models.models.canagliflozin.experiments.base_experiment import (
    CanagliflozinSimulationExperiment,
)


class DoseDependencyExperiment(CanagliflozinSimulationExperiment):
    """Dose and glucose dependency experiment."""

    doses: ClassVar[list[int]] = [0, 10, 50, 100, 300, 600, 800]  # [mg]
    glucoses: ClassVar[list[int]] = [5, 6, 7, 8, 9, 10, 11]  # [mM]

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims: dict[str, Simulation] = {}

        # Dose dependency
        for dose in self.doses:
            tcsims[f"can_dose_{dose}"] = Simulation(
                time_unit="min",
                end=24 * 60,
                preinit_changes={
                    **self.default_changes(),
                    "PODOSE_can": Q(dose, "mg"),
                },
            )

        # Glucose dependency
        for glc in self.glucoses:
            tcsims[f"can_glucose_{glc}"] = Simulation(
                time_unit="min",
                end=24 * 60,
                preinit_changes={
                    **self.default_changes(),
                    "PODOSE_can": Q(100, "mg"),
                    "[KI__fpg]": Q(glc, "mM"),
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

        for key in ["dose", "glucose"]:
            if key == "dose":
                values = self.doses
                color_map = self.dose_colors
                title = "Dose Dependency of Pharmacokinetics"
            else:
                values = self.glucoses
                color_map = self.glucose_colors
                title = "Glucose Dependency of Pharmacokinetics"

            fig = Figure(
                experiment=self,
                sid=f"Fig_{key}_dependency_pk",
                num_rows=3,
                num_cols=4,
                name=title,
                settings={"legend_scope": "row"},
            )

            plots = fig.create_plots(
                xaxis=Axis(self.label_time, unit=self.unit_time),
                legend=True,
            )

            for ksid, sid in enumerate(sids):
                plots[ksid].set_yaxis(
                    label=self.labels[sid],
                    unit=self.units[sid],
                )

            for ksid, sid in enumerate(sids):
                for value in values:
                    label = f"{value} mg" if key == "dose" else f"{value} mM"
                    plots[ksid].add_data(
                        task=f"task_can_{key}_{value}",
                        xid="time",
                        yid=sid,
                        label=label,
                        color=color_map.get(value, "black"),
                    )

            figures.append(fig)

        return self.figures_by_sid(*figures)

    def figure_pd(self) -> dict[str, Figure]:
        """Timecourses of the glucose excretion and its dependency on canagliflozin."""
        figures: list[Figure] = []

        for key in ["dose", "glucose"]:
            if key == "dose":
                values = self.doses
                color_map = self.dose_colors
                title = "Dose Dependency of Pharmacodynamics"
            else:
                values = self.glucoses
                color_map = self.glucose_colors
                title = "Glucose Dependency of Pharmacodynamics"

            fig = Figure(
                experiment=self,
                sid=f"Fig_{key}_dependency_pd",
                num_rows=2,
                num_cols=3,
                name=title,
                settings={"legend_scope": "row"},
            )

            plots = fig.create_plots(
                xaxis=Axis(self.label_time, unit=self.unit_time),
                legend=True,
            )

            time_sids = ["KI__UGE", "KI__RTG", "[KI__fpg]"]
            for ksid, sid in enumerate(time_sids):
                plots[ksid].set_yaxis(
                    label=self.labels[sid],
                    unit=self.units[sid],
                )
                for value in values:
                    label = f"{value} mg" if key == "dose" else f"{value} mM"
                    plots[ksid].add_data(
                        task=f"task_can_{key}_{value}",
                        xid="time",
                        yid=sid,
                        label=label,
                        color=color_map.get(value, "black"),
                    )

            plots[3].set_xaxis(label=self.label_can, unit=self.unit_can)
            plots[3].set_yaxis(label="Rate glucose excretion", unit="mmole/min")

            plots[4].set_xaxis(label=self.label_can, unit=self.unit_can)
            plots[4].set_yaxis(label=self.label_rtg, unit=self.unit_rtg)

            plots[5].set_xaxis(label=self.label_can, unit=self.unit_can)
            plots[5].set_yaxis(label=self.label_uge, unit=self.unit_uge)

            for value in values:
                label = f"{value} mg" if key == "dose" else f"{value} mM"
                plots[3].add_data(
                    task=f"task_can_{key}_{value}",
                    xid="[Cve_can]",
                    yid="KI__GLCEX",
                    label=label,
                    color=color_map.get(value, "black"),
                )
                plots[4].add_data(
                    task=f"task_can_{key}_{value}",
                    xid="[Cve_can]",
                    yid="KI__RTG",
                    label=label,
                    color=color_map.get(value, "black"),
                )
                plots[5].add_data(
                    task=f"task_can_{key}_{value}",
                    xid="[Cve_can]",
                    yid="KI__UGE",
                    label=label,
                    color=color_map.get(value, "black"),
                )

            figures.append(fig)

        return self.figures_by_sid(*figures)


if __name__ == "__main__":
    MODEL.run_experiments(
        DoseDependencyExperiment, output_dir=DoseDependencyExperiment.__name__
    )

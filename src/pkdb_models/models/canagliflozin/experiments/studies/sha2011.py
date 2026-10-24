"""Simulation experiment of the study Sha2011."""

from typing import ClassVar, override

from pkpdsim.metadata import (
    ApplicationForm,
    Dosing,
    Fasting,
    Health,
    PKPDMappingMetaData,
    Route,
    Tissue,
)
from sbmlsim import Q
from sbmlsim.data import DataSet
from sbmlsim.fit import FitData, FitMapping
from sbmlsim.plot import Axis, Figure, Plot
from sbmlsim.simulation import Simulation
from sbmlsim.units import Quantity

from pkdb_models.models.canagliflozin import MODEL
from pkdb_models.models.canagliflozin.experiments.base_experiment import (
    CanagliflozinSimulationExperiment,
)


class Sha2011(CanagliflozinSimulationExperiment):
    """Simulation experiment of Sha2011.

    Healthy men, a single oral dose of a suspension of 10 to 800 mg or 400 mg
    twice daily (one cohort per dose, placebo pooled), after an overnight fast
    with standardized meals 0.5, 4.5 and 10.5 hr after the morning dose. The
    urinary glucose of 0 - 24 hr (UGE) and the 24-hr mean renal threshold of
    glucose (RTG) of day 1; no pharmacokinetics.
    """

    doses: ClassVar[list[int]] = [0, 10, 30, 100, 200, 400, 600, 800]  # [mg]
    dose_bid = 400  # [mg]
    #: the evening dose of the twice daily dose (assumed): the paper gives "the
    #: evening" with the evening meal 0.5 hr after it, the evening meal of the
    #: other cohorts is 10.5 hr after the morning dose
    time_evening = 10  # [hr]

    #: healthy: the fasting plasma glucose of the model and its default of the
    #: mean plasma glucose of the day (`KI__PG_delta`)
    fpg = 5  # [mM]
    #: 24-hr creatinine clearance 97.1 (69.7 - 138) ml/min/1.73 m^2
    gfr = 97.1  # [ml/min]
    #: not reported, men with a BMI of 24 (20.4 - 29.8) kg/m^2
    bodyweight = 75  # [kg]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1"]:
            df = self.load_dataframe(fig_id)
            for label, df_label in df.groupby("label"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)
                # unit conversion to mole/l
                if label.startswith("renal_threshold"):
                    dset.unit_conversion("mean", 1 / self.Mr.glc)

                dsets[label] = dset

        return dsets

    def changes_subjects(self) -> dict[str, Quantity]:
        """Get the changes of the subjects of the study."""
        return {
            "BW": Q(self.bodyweight, "kg"),
            "[KI__fpg]": Q(self.fpg, "mM"),
            "KI__f_renal_function": Q(self.gfr / 101, "dimensionless"),
        }

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}

        # single dose, the urine of 0 - 24 hr
        for dose in self.doses:
            tcsims[f"po_can{dose}"] = Simulation(
                time_unit="hr",
                end=24,
                preinit_changes={
                    **self.default_changes(),
                    **self.changes_subjects(),
                    "PODOSE_can": Q(dose, "mg"),
                },
            )

        # twice daily: the morning and the evening dose of day 1
        tcsims[f"po_can{self.dose_bid}_bid"] = Simulation(
            time_unit="hr",
            end=24,
            preinit_changes={
                **self.default_changes(),
                **self.changes_subjects(),
                "PODOSE_can": Q(self.dose_bid, "mg"),
            },
            changes=[
                self.add_doses(
                    self.time_evening, {"PODOSE_can": Q(self.dose_bid, "mg")}
                )
            ],
        )

        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}

        # the 24-hr mean RTG is the mean of the RTG over 0 - 24 hr, the RTG of
        # placebo is not reported
        observables = {
            "cumulative_amount": ("uge", "KI__UGE", Tissue.URINE),
            "renal_threshold": ("rtg", "KI__RTG_mean", Tissue.PLASMA),
        }
        for name, (key, sid, tissue) in observables.items():
            groups: list[tuple[str, str, str, Dosing]] = [
                (f"CAN{dose}", f"can{dose}", f"task_po_can{dose}", Dosing.SINGLE)
                for dose in self.doses
                if not (dose == 0 and key == "rtg")
            ]
            groups.append(
                (
                    f"CAN{self.dose_bid}_BID",
                    f"can{self.dose_bid}bid",
                    f"task_po_can{self.dose_bid}_bid",
                    Dosing.MULTIPLE,
                )
            )
            for group, prefix, task, dosing in groups:
                mappings[f"fm_{prefix}_{key}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=f"{name}_{group}",
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                    ),
                    observable=FitData(self, task=task, xid="time", yid=sid),
                    metadata=PKPDMappingMetaData(
                        tissue=tissue,
                        route=Route.PO,
                        application_form=ApplicationForm.SUSPENSION,
                        dosing=dosing,
                        health=Health.HEALTHY,
                        fasting=Fasting.FASTED,
                    ),
                )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        return {**self.figure_uge(), **self.figure_rtg()}

    def plot_doses(self, plot: Plot, sid: str, dataset: str, doses: list[int]) -> None:
        """Add the simulations and the data of the doses to a plot.

        Args:
            plot: the plot.
            sid: the observable of the simulations.
            dataset: the prefix of the datasets.
            doses: the doses of the single doses.
        """
        for dose in doses:
            plot.add_data(
                task=f"task_po_can{dose}",
                xid="time",
                yid=sid,
                label=f"{dose} mg PO",
                color=self.dose_colors[dose],
            )
        plot.add_data(
            task=f"task_po_can{self.dose_bid}_bid",
            xid="time",
            yid=sid,
            label=f"{self.dose_bid} mg PO BID",
            color=self.dose_colors[self.dose_bid],
            linestyle="--",
        )
        for dose in doses:
            plot.add_data(
                dataset=f"{dataset}_CAN{dose}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"{dose} mg PO",
                color=self.dose_colors[dose],
            )
        plot.add_data(
            dataset=f"{dataset}_CAN{self.dose_bid}_BID",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label=f"{self.dose_bid} mg PO BID",
            color=self.dose_colors[self.dose_bid],
            marker="s",
        )

    def figure_uge(self) -> dict[str, Figure]:
        """Cumulative urinary glucose excretion after single and twice daily doses."""
        fig = Figure(
            experiment=self,
            sid="Fig_uge",
            name=f"{self.__class__.__name__} (Healthy)",
        )
        # the legends inside the panel cover data
        fig.settings = {**fig.settings, "legend_position": "outside"}
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit=self.unit_time), legend=True
        )
        plots[0].set_yaxis(self.label_uge, unit=self.unit_uge)
        self.plot_doses(plots[0], "KI__UGE", "cumulative_amount", self.doses)

        return self.figures_by_sid(fig)

    def figure_rtg(self) -> dict[str, Figure]:
        """Mean renal threshold of glucose since the dose (24-hr mean at 24 hr)."""
        fig = Figure(
            experiment=self,
            sid="Fig_rtg",
            name=f"{self.__class__.__name__} (Healthy)",
        )
        # the legends inside the panel cover data
        fig.settings = {**fig.settings, "legend_position": "outside"}
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit=self.unit_time), legend=True
        )
        plots[0].set_yaxis(self.label_rtg_mean, unit=self.unit_rtg)
        # the RTG of placebo is not reported
        self.plot_doses(plots[0], "KI__RTG_mean", "renal_threshold", self.doses[1:])

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(Sha2011, output_dir=Sha2011.__name__)

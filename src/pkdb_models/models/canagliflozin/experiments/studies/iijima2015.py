"""Simulation experiment of the study Iijima2015."""

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
from sbmlsim.plot import Axis, Figure
from sbmlsim.simulation import Change, Simulation
from sbmlsim.units import Quantity

from pkdb_models.models.canagliflozin import MODEL
from pkdb_models.models.canagliflozin.experiments.base_experiment import (
    CanagliflozinSimulationExperiment,
)


class Iijima2015(CanagliflozinSimulationExperiment):
    """Simulation experiment of Iijima2015.

    Japanese patients with T2DM: placebo on day 0, canagliflozin (25, 100,
    200, 400 mg) or placebo on day 1, no dose on day 2 and QD on days 3-16
    (15 doses); the dose is taken at 8-9 a.m. and followed by a standard
    breakfast within 10 min (the model has no food effect, Devineni2015e).
    The urine is collected per day (UGE on days 0-6 and 15-18, the 24-hr mean
    RTG on days 1 and 16). The multiple dose simulations start on day 0, the
    dose of day 16 is at time 0; the day d ends at d - 15 days.
    """

    doses: ClassVar[list[int]] = [25, 100, 200, 400]
    #: the arms of the multiple dose simulations, with placebo (0)
    doses_multi: ClassVar[list[int]] = [0, 25, 100, 200, 400]

    # [kg]
    bodyweights: ClassVar[dict[int, float]] = {
        0: 69.73,
        25: 74.24,
        100: 73.44,
        200: 63.67,
        400: 73.88,
    }
    # [mg/dl]
    fpg: ClassVar[dict[int, float]] = {
        0: 184.9,
        25: 172.2,
        100: 162.5,
        200: 163.4,
        400: 170.9,
    }

    #: the dose times of the multiple dose simulations [hr] from the start of
    #: day 0: day 1 and days 3-16
    dose_times: ClassVar[list[int]] = [24] + [24 * day for day in range(3, 17)]
    #: the end of the days 0-17 [hr], the daily reset of the urine collection
    day_ends: ClassVar[list[int]] = [24 * day for day in range(1, 19)]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig2", "Fig3", "Tab2A"]:
            df = self.load_dataframe(fig_id)
            if fig_id == "Tab2A":
                # the start of the collection on day 16 is compared with the
                # state before the reset, i.e. the urine of day 15
                df = df[~(df["label"].str.endswith("_d16") & (df["time"] == 0))]
            for label, df_label in df.groupby("label"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)

                # unit conversion to mole/l
                if label.startswith("canagliflozin_"):
                    dset.unit_conversion("mean", 1 / self.Mr.can)
                elif label.startswith("glucose_renal"):
                    dset.unit_conversion("mean", 1 / self.Mr.glc)

                dsets[label] = dset

        return dsets

    def _patient_changes(self, dose: int) -> dict[str, Quantity | float]:
        """Get the body weight and FPG of the arm of a dose.

        Args:
            dose: the dose [mg], 0 for placebo.

        Returns:
            The changes by id.
        """
        return {
            **self.default_changes(),
            "BW": Q(self.bodyweights[dose], "kg"),
            # mg/dl to mM with the molecular weight of glucose (180.16 g/mole)
            "[KI__fpg]": Q(self.fpg[dose] / 18.016, "mM"),
        }

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}

        # single dose (day 1)
        for dose in self.doses:
            tcsims[f"po_can{dose}_d1"] = Simulation(
                time_unit="hr",
                end=26,
                preinit_changes={
                    **self._patient_changes(dose),
                    "PODOSE_can": Q(dose, "mg"),
                },
            )

        # multiple doses from day 0; the urine, the UGE and the mean RTG are
        # collected per day
        day_reset = {
            "KI__glc_urine": Q(0, "mmole"),
            "KI__RTG_int": Q(0, "mM*min"),
            "KI__RTG_time": Q(0, "min"),
            "Aurine_can": Q(0, "mmole"),
        }
        for dose in self.doses_multi:
            changes = [
                Change(self.day_ends, day_reset),
                self.add_doses(self.dose_times, {"PODOSE_can": Q(dose, "mg")}),
            ]
            tcsims[f"po_can{dose}_multi"] = Simulation(
                time_unit="hr",
                end=19 * 24 + 1,
                preinit_changes=self._patient_changes(dose),
                changes=changes,
                time_shift=-16 * 24,
            )

        return tcsims

    def _metadata(self, tissue: Tissue, dosing: Dosing) -> PKPDMappingMetaData:
        """Metadata of the mappings."""
        return PKPDMappingMetaData(
            tissue=tissue,
            route=Route.PO,
            application_form=ApplicationForm.TABLET,
            dosing=dosing,
            health=Health.T2DM,
            fasting=Fasting.FASTED,
        )

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}

        def mapping(dataset: str, task: str, yid: str) -> tuple[FitData, FitData]:
            return (
                FitData(
                    self,
                    dataset=dataset,
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                FitData(self, task=task, xid="time", yid=yid),
            )

        # pharmacokinetics on day 1 and day 16
        for dose in self.doses:
            for day, task, dosing in [
                ("d1", f"task_po_can{dose}_d1", Dosing.SINGLE),
                ("d16", f"task_po_can{dose}_multi", Dosing.MULTIPLE),
            ]:
                for name, sid, tissue in [
                    ("canagliflozin", "[Cve_can]", Tissue.PLASMA),
                    ("canagliflozin_urine", "Aurine_can", Tissue.URINE),
                ]:
                    reference, observable = mapping(
                        f"{name}_CAN{dose}_{day}", task, sid
                    )
                    mappings[f"fm_po_can{dose}_{day}_{name}"] = FitMapping(
                        self,
                        reference=reference,
                        observable=observable,
                        metadata=self._metadata(tissue, dosing),
                    )

        # change of the 24-hr UGE from day 0 on days 1-6 and 15-18, compared
        # with the UGE of the day: the baseline UGE of day 0 (14-24 g/day) is
        # not in the data
        for dose in self.doses:
            reference, observable = mapping(
                f"glucose_uge_change_CAN{dose}_d16",
                f"task_po_can{dose}_multi",
                "KI__UGE",
            )
            mappings[f"fm_po_can{dose}_uge_change"] = FitMapping(
                self,
                reference=reference,
                observable=observable,
                metadata=self._metadata(Tissue.URINE, Dosing.MULTIPLE),
            )

        # 24-hr mean RTG on days 1 and 16, with placebo
        for dose in self.doses_multi:
            reference, observable = mapping(
                f"glucose_renal_threshold_CAN{dose}_d16",
                f"task_po_can{dose}_multi",
                "KI__RTG_mean",
            )
            mappings[f"fm_po_can{dose}_rtg_mean"] = FitMapping(
                self,
                reference=reference,
                observable=observable,
                metadata=self._metadata(Tissue.PLASMA, Dosing.MULTIPLE),
            )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        return self.figures_by_sid(
            self._figure_plasma(),
            self._figure_urine(),
            self._figure_uge(),
            self._figure_rtg(),
        )

    def _label(self, dose: int) -> str:
        """Label of an arm."""
        return f"{dose} mg PO" if dose else "placebo"

    def _figure_plasma(self) -> Figure:
        """Plasma concentrations on day 1 and day 16."""
        fig = Figure(
            experiment=self,
            sid="Fig_plasma",
            num_rows=1,
            num_cols=2,
            name=f"{self.__class__.__name__} (T2DM)",
        )
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit=self.unit_time, min=0, max=25),
            legend=True,
        )
        plots[0].set_title("Day 1")
        plots[1].set_title("Day 16")
        for k, day in enumerate(["d1", "d16"]):
            plots[k].set_yaxis(self.label_can, unit=self.unit_can)
            for dose in self.doses:
                task = (
                    f"task_po_can{dose}_d1"
                    if day == "d1"
                    else f"task_po_can{dose}_multi"
                )
                # simulation
                plots[k].add_data(
                    task=task,
                    xid="time",
                    yid="[Cve_can]",
                    label=self._label(dose),
                    color=self.dose_colors[dose],
                )
                # data
                plots[k].add_data(
                    dataset=f"canagliflozin_CAN{dose}_{day}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=self._label(dose),
                    color=self.dose_colors[dose],
                )

        return fig

    def _figure_urine(self) -> Figure:
        """Urinary canagliflozin over 0-24 hr on day 1 and day 16."""
        fig = Figure(
            experiment=self,
            sid="Fig_urine",
            num_rows=1,
            num_cols=2,
            name=f"{self.__class__.__name__} (T2DM)",
        )
        # the legends inside the panels cover data
        fig.settings = {**fig.settings, "legend_position": "outside"}
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit=self.unit_time, min=0, max=25),
            legend=True,
        )
        plots[0].set_title("Day 1")
        plots[1].set_title("Day 16")
        for k, day in enumerate(["d1", "d16"]):
            plots[k].set_yaxis(self.label_can_urine, unit=self.unit_can_urine)
            for dose in self.doses:
                task = (
                    f"task_po_can{dose}_d1"
                    if day == "d1"
                    else f"task_po_can{dose}_multi"
                )
                # simulation
                plots[k].add_data(
                    task=task,
                    xid="time",
                    yid="Aurine_can",
                    label=self._label(dose),
                    color=self.dose_colors[dose],
                )
                # data
                plots[k].add_data(
                    dataset=f"canagliflozin_urine_CAN{dose}_{day}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=self._label(dose),
                    color=self.dose_colors[dose],
                    linestyle="",
                )

        return fig

    def _figure_uge(self) -> Figure:
        """UGE per day (change from day 0 in the data) on days 1-6 and 15-18."""
        fig = Figure(
            experiment=self,
            sid="Fig_uge",
            num_rows=1,
            num_cols=1,
            name=f"{self.__class__.__name__} (T2DM)",
        )
        # the legends inside the panel cover data
        fig.settings = {**fig.settings, "legend_position": "outside"}
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="day"), legend=True)
        plots[0].set_yaxis(self.label_uge, unit=self.unit_uge)

        for dose in self.doses:
            # simulation
            plots[0].add_data(
                task=f"task_po_can{dose}_multi",
                xid="time",
                yid="KI__UGE",
                label=self._label(dose),
                color=self.dose_colors[dose],
            )
            # data
            plots[0].add_data(
                dataset=f"glucose_uge_change_CAN{dose}_d16",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=self._label(dose),
                color=self.dose_colors[dose],
                linestyle="",
            )

        return fig

    def _figure_rtg(self) -> Figure:
        """24-hr mean renal threshold of glucose on days 1 and 16."""
        fig = Figure(
            experiment=self,
            sid="Fig_rtg",
            num_rows=1,
            num_cols=1,
            name=f"{self.__class__.__name__} (T2DM)",
        )
        # the legends inside the panel cover data
        fig.settings = {**fig.settings, "legend_position": "outside"}
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="day"), legend=True)
        plots[0].set_yaxis(self.label_rtg_mean, unit=self.unit_rtg)

        for dose in self.doses_multi:
            # simulation
            plots[0].add_data(
                task=f"task_po_can{dose}_multi",
                xid="time",
                yid="KI__RTG_mean",
                label=self._label(dose),
                color=self.dose_colors[dose],
            )
            # data
            plots[0].add_data(
                dataset=f"glucose_renal_threshold_CAN{dose}_d16",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=self._label(dose),
                color=self.dose_colors[dose],
                linestyle="",
            )

        return fig


if __name__ == "__main__":
    MODEL.run_experiments(Iijima2015, output_dir=Iijima2015.__name__)

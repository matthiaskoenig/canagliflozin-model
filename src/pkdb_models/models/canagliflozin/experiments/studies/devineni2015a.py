"""Simulation experiment of the study Devineni2015a."""

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


class Devineni2015a(CanagliflozinSimulationExperiment):
    """Simulation experiment of Devineni2015a."""

    doses: ClassVar[list[int]] = [50, 100, 300]
    info: ClassVar[dict[str, str]] = {
        "can": "canagliflozin",
        "m5": "M5",
        "m7": "M7",
    }

    bodyweight = 74.4  # [kg]
    fpg = 5  # [mM] (healthy, not reported)
    #: the mean plasma glucose of 0-24 hr (MPG0-24) on day 1, day 9 and day 10
    #: [mg/dl] (Table 2), the glucose which is filtered
    mpg: ClassVar[dict[int, dict[str, float]]] = {
        50: {"d1": 100.0, "d9": 99.8, "d10": 102.0},
        100: {"d1": 92.8, "d9": 94.5, "d10": 95.6},
        300: {"d1": 93.3, "d9": 93.9, "d10": 95.7},
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1", "Tab1A", "Tab2A"]:
            df = self.load_dataframe(fig_id)
            # the zero amounts at the start of the urine collection of day 9 lie
            # at the reset of the collection of day 8 and carry no information
            if fig_id == "Tab1A":
                df = df[~(df.label.str.contains("_d9") & (df.time == 0))]
            for label, df_label in df.groupby("label"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)
                # unit conversion to mole/l; the amounts of the metabolites in
                # the urine are canagliflozin equivalents (% of the dose)
                if label.startswith(
                    ("canagliflozin_", "M5_cumulative_amount", "M7_cumulative_amount")
                ):
                    dset.unit_conversion("mean", 1 / self.Mr.can)
                elif label.startswith("M7_"):
                    dset.unit_conversion("mean", 1 / self.Mr.m7)
                elif label.startswith("M5_"):
                    dset.unit_conversion("mean", 1 / self.Mr.m5)
                elif label.startswith("glucose_renal"):
                    dset.unit_conversion("mean", 1 / self.Mr.glc)

                dsets[label] = dset

        return dsets

    def _pg_delta(self, dose: int, day: str) -> Quantity:
        """Get the mean plasma glucose of a day above the FPG.

        Args:
            dose: the dose of the group [mg].
            day: the day (`d1`, `d9`, `d10`).

        Returns:
            The mean plasma glucose minus the FPG.
        """
        mpg = (Q(self.mpg[dose][day], "mg/dl") / self.Mr.glc).to("mM")
        return mpg - Q(self.fpg, "mM")

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}

        # single dose (day 1)
        for dose in self.doses:
            tcsims[f"po_can_{dose}_single"] = Simulation(
                time_unit="hr",
                end=50,  # (urine sample after 48 [hr])
                preinit_changes={
                    **self.default_changes(),
                    "BW": Q(self.bodyweight, "kg"),
                    "[KI__fpg]": Q(self.fpg, "mM"),
                    "KI__PG_delta": self._pg_delta(dose, "d1"),
                    "PODOSE_can": Q(dose, "mg"),
                },
            )

        # a single dose on day 1 (0 hr), multiple doses on days 4 to 9 (72 to
        # 192 hr) and no dose on day 10. The urine and the RTG are collected
        # over 24 hr from the dose, the data at the end of a collection is
        # compared with the state before the reset; the urine of day 9 is
        # collected over 48 hr (no reset of the urine at 216 hr), the UGE of
        # day 10 is the sum of days 9 and 10 in the data
        resets_rtg = {
            "KI__RTG_int": Q(0, "mM*min"),  # reset RTG
            "KI__RTG_time": Q(0, "min"),
        }
        resets = {
            **resets_rtg,
            "KI__glc_urine": Q(0, "mmole"),  # reset UGE
            "Aurine_can": Q(0, "mmole"),  # reset canagliflozin
            "Aurine_m5": Q(0, "mmole"),  # reset M5
            "Aurine_m7": Q(0, "mmole"),  # reset M7
        }
        for dose in self.doses:
            tcsims[f"po_can_{dose}_multi"] = Simulation(
                time_unit="hr",
                end=241,
                preinit_changes={
                    **self.default_changes(),
                    "BW": Q(self.bodyweight, "kg"),
                    "[KI__fpg]": Q(self.fpg, "mM"),
                    "KI__PG_delta": self._pg_delta(dose, "d1"),
                    "PODOSE_can": Q(dose, "mg"),
                },
                changes=[
                    # days 2 and 3 without dose
                    Change([24, 48], resets),
                    Change(
                        [24 * k for k in range(3, 9)],
                        {
                            **resets,
                            "KI__PG_delta": self._pg_delta(dose, "d9"),
                        },
                    ),
                    self.add_doses(
                        [24 * k for k in range(3, 9)], {"PODOSE_can": Q(dose, "mg")}
                    ),
                    # day 10 without dose
                    Change(
                        216,
                        {**resets_rtg, "KI__PG_delta": self._pg_delta(dose, "d10")},
                    ),
                ],
                time_shift=-8 * 24,
            )

        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}

        # pharmacokinetics
        for name, sid in [
            ("canagliflozin", "[Cve_can]"),
            ("M5", "[Cve_m5]"),
            ("M7", "[Cve_m7]"),
            ("canagliflozin_cumulative_amount", "Aurine_can"),
            ("M5_cumulative_amount", "Aurine_m5"),
            ("M7_cumulative_amount", "Aurine_m7"),
        ]:
            for dosing in ["single", "multi"]:
                day = "d1" if dosing == "single" else "d9"
                for dose in self.doses:
                    mappings[f"fm_po_can_{dose}_{name}_{dosing}"] = FitMapping(
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
                            self,
                            task=f"task_po_can_{dose}_{dosing}",
                            xid="time",
                            yid=sid,
                        ),
                        metadata=PKPDMappingMetaData(
                            tissue=Tissue.URINE
                            if "_cumulative" in name
                            else Tissue.PLASMA,
                            route=Route.PO,
                            application_form=ApplicationForm.TABLET,
                            dosing=Dosing.SINGLE
                            if dosing == "single"
                            else Dosing.MULTIPLE,
                            health=Health.HEALTHY,
                            fasting=Fasting.FASTED,
                        ),
                    )

        # UGE, RTG
        for name, sid, tissue in [
            ("glucose_cumulative_amount", "KI__UGE", Tissue.URINE),
            # the 24-hr mean RTG
            ("glucose_renal_threshold", "KI__RTG_mean", Tissue.PLASMA),
        ]:
            for dose in self.doses:
                mappings[f"fm_po_can_{dose}_{name}_multi"] = FitMapping(
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
                        self,
                        task=f"task_po_can_{dose}_multi",
                        xid="time",
                        yid=sid,
                    ),
                    metadata=PKPDMappingMetaData(
                        tissue=tissue,
                        route=Route.PO,
                        application_form=ApplicationForm.TABLET,
                        dosing=Dosing.MULTIPLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.FASTED,
                    ),
                )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        return self.figures_by_sid(
            *self._figures_plasma(),
            *self._figures_urine(),
            self._figure_uge(),
            self._figure_rtg(),
        )

    def _figures_plasma(self) -> list[Figure]:
        """Plasma concentrations after the first and the last dose."""
        figures = []

        for dosing in ["single", "multi"]:
            day = "d1" if dosing == "single" else "d9"
            fig = Figure(
                experiment=self,
                sid=f"Fig_{dosing}",
                num_rows=1,
                num_cols=3,
                name=f"{self.__class__.__name__} (Healthy)",
            )
            # the day before and day 9 of the multiple dose
            plots = fig.create_plots(
                xaxis=Axis(
                    self.label_time,
                    unit=self.unit_time,
                    min=-24 if dosing == "multi" else None,
                    max=30,
                ),
                legend=True,
            )
            plots[0].set_yaxis(self.label_can, unit=self.unit_can)
            plots[1].set_yaxis(self.label_m5, unit=self.unit_m5)
            plots[2].set_yaxis(self.label_m7, unit=self.unit_m7)

            for dose in self.doses:
                for k, (sid, did) in enumerate(self.info.items()):
                    # simulation
                    plots[k].add_data(
                        task=f"task_po_can_{dose}_{dosing}",
                        xid="time",
                        yid=f"[Cve_{sid}]",
                        label=f"{dose} mg PO",
                        color=self.dose_colors[dose],
                    )

                    # data
                    plots[k].add_data(
                        dataset=f"{did}_CAN{dose}_{day}",
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                        label=f"{dose} mg PO",
                        color=self.dose_colors[dose],
                    )

            figures.append(fig)

        return figures

    def _figures_urine(self) -> list[Figure]:
        """Cumulative amounts in the urine after the first and the last dose."""
        figures = []

        for dosing in ["single", "multi"]:
            day = "d1" if dosing == "single" else "d9"
            fig = Figure(
                experiment=self,
                sid=f"Fig_urine_{dosing}",
                num_rows=1,
                num_cols=3,
                name=f"{self.__class__.__name__} (Healthy)",
            )
            # the legends inside the panels cover data
            fig.settings = {**fig.settings, "legend_position": "outside"}
            # the day before and days 9 and 10 of the multiple dose
            plots = fig.create_plots(
                xaxis=Axis(
                    self.label_time,
                    unit=self.unit_time,
                    min=-24 if dosing == "multi" else None,
                    max=50,
                ),
                legend=True,
            )
            plots[0].set_yaxis(self.label_can_urine, unit=self.unit_can_urine)
            plots[1].set_yaxis(self.label_m5_urine, unit=self.unit_m5_urine)
            plots[2].set_yaxis(self.label_m7_urine, unit=self.unit_m7_urine)

            for dose in self.doses:
                for k, (sid, did) in enumerate(self.info.items()):
                    # simulation
                    plots[k].add_data(
                        task=f"task_po_can_{dose}_{dosing}",
                        xid="time",
                        yid=f"Aurine_{sid}",
                        label=f"{dose} mg PO",
                        color=self.dose_colors[dose],
                    )
                    # data
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

            figures.append(fig)

        return figures

    def _figure_uge(self) -> Figure:
        """Urinary glucose excretion."""
        fig = Figure(
            experiment=self,
            sid="Fig_uge",
            name=f"{self.__class__.__name__} (Healthy)",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="day"), legend=True)
        plots[0].set_yaxis(self.label_uge, unit=self.unit_uge)

        for dose in self.doses:
            # simulation
            plots[0].add_data(
                task=f"task_po_can_{dose}_multi",
                xid="time",
                yid="KI__UGE",
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

        return fig

    def _figure_rtg(self) -> Figure:
        """Renal threshold of glucose."""
        fig = Figure(
            experiment=self,
            sid="Fig_rtg",
            name=f"{self.__class__.__name__} (Healthy)",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="day"), legend=True)
        plots[0].set_yaxis(self.label_rtg_mean, unit=self.unit_rtg)

        for dose in self.doses:
            # simulation
            plots[0].add_data(
                task=f"task_po_can_{dose}_multi",
                xid="time",
                yid="KI__RTG_mean",
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

        return fig


if __name__ == "__main__":
    MODEL.run_experiments(Devineni2015a, output_dir=Devineni2015a.__name__)

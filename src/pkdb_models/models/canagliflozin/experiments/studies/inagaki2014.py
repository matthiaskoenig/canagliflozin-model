"""Simulation experiment of the study Inagaki2014."""

from collections.abc import Mapping
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

from pkdb_models.models.canagliflozin import MODEL
from pkdb_models.models.canagliflozin.experiments.base_experiment import (
    CanagliflozinSimulationExperiment,
)


class Inagaki2014(CanagliflozinSimulationExperiment):
    """Simulation experiment of Inagaki2014.

    Japanese men with T2DM, open-label randomized two-way crossover of single
    oral doses of canagliflozin 100 mg and 200 mg (tablet, washout >= 14 days),
    in two groups of 12: normal renal function or mild renal impairment (eGFR
    92.7 ml/min/1.73 m2, BW 75.33 kg, FPG 183.1 mg/dl) and moderate renal
    impairment (eGFR 39.7, BW 74.85 kg, FPG 167.5 mg/dl). Overnight fast, the
    dose 10 min before breakfast (meals at 10 min, 4.5 h and 10.5 h).
    Canagliflozin, M5 and M7 in plasma (LC-MS/MS, ng/ml of the metabolites)
    to 72 h, canagliflozin in urine 0-72 h (Table 3), the change of the daily
    urinary glucose excretion from the baseline day (Fig 2).

    The baseline UGE of the subjects is not reported; the model excretes no
    glucose at the FPG of the groups without canagliflozin, so the change from
    baseline is compared with the UGE of the model. The UGE is collected per
    day (reset at 24 and 48 h). The renal function is the eGFR over 101 ml/min.
    """

    conditions_renal: ClassVar[dict[str, str]] = {
        "normal": "Normal renal function",
        "moderate": "Moderate renal impairment",
    }
    labels: ClassVar[Mapping[str, str]] = {
        "normal": "NRF",
        "moderate": "MRI",
    }
    markers: ClassVar[dict[int, str]] = {
        100: "s",
        200: "D",
    }

    doses: ClassVar[list[int]] = [100, 200]

    info: ClassVar[dict[str, str]] = {
        "can": "canagliflozin",
        "m5": "M5",
        "m7": "M7",
    }

    bodyweights: ClassVar[dict[str, float]] = {"moderate": 74.85, "normal": 75.33}

    #: fasting plasma glucose [mM] from mg/dl (glucose 180.16 g/mol)
    fpg: ClassVar[dict[str, float]] = {
        "moderate": 167.5 / 18.016,
        "normal": 183.1 / 18.016,
    }

    gfr: ClassVar[dict[str, float]] = {"moderate": 39.7, "normal": 92.7}

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1", "Fig2", "Tab3A"]:
            df = self.load_dataframe(fig_id)
            # the recovery (percent of the dose) repeats the amount in urine;
            # the cumulative UGE is the sum of the daily changes (Fig 2), which
            # are the data
            df = df[
                ~df.label.str.contains("recovery")
                & ~df.label.str.startswith("glucose_cumulative_amount")
            ]
            for label, df_label in df.groupby("label"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)

                if label.startswith("glucose_excretion_daily"):
                    # the change of the UGE per day [g/day] is the amount of
                    # the 24 h collection interval
                    dset.unit_conversion("mean", Q(1, "day"))
                elif label.startswith("canagliflozin_"):
                    dset.unit_conversion("mean", 1 / self.Mr.can)
                elif label.startswith("M7_"):
                    dset.unit_conversion("mean", 1 / self.Mr.m7)
                elif label.startswith("M5_"):
                    dset.unit_conversion("mean", 1 / self.Mr.m5)

                dsets[label] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}
        for dose in self.doses:
            for condition in self.conditions_renal:
                tcsims[f"po_can{dose}_{condition}"] = Simulation(
                    time_unit="hr",
                    end=73,
                    preinit_changes={
                        **self.default_changes(),
                        "BW": Q(self.bodyweights[condition], "kg"),
                        "[KI__fpg]": Q(self.fpg[condition], "mM"),
                        # eGFR over the GFR_base of 101 ml/min
                        "KI__f_renal_function": Q(
                            self.gfr[condition] / 101, "dimensionless"
                        ),
                        "PODOSE_can": Q(dose, "mg"),
                    },
                    # the urinary glucose is collected per day
                    changes=[Change([24, 48], {"KI__glc_urine": Q(0, "mmole")})],
                )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for name, sid in [
            ("canagliflozin", "[Cve_can]"),
            ("M5", "[Cve_m5]"),
            ("M7", "[Cve_m7]"),
            ("glucose_excretion_daily", "KI__UGE"),
            ("canagliflozin_urine", "Aurine_can"),
        ]:
            if name in {"canagliflozin", "M5", "M7"}:
                tissue = Tissue.PLASMA
            else:
                tissue = Tissue.URINE

            for condition in self.conditions_renal:
                for dose in self.doses:
                    mappings[f"fm_po_can_{name}_{dose}_{condition}"] = FitMapping(
                        self,
                        reference=FitData(
                            self,
                            dataset=f"{name}_CAN{dose}_{condition}",
                            xid="time",
                            yid="mean",
                            yid_sd="mean_sd",
                            count="count",
                        ),
                        observable=FitData(
                            self,
                            task=f"task_po_can{dose}_{condition}",
                            xid="time",
                            yid=sid,
                        ),
                        metadata=PKPDMappingMetaData(
                            tissue=tissue,
                            route=Route.PO,
                            application_form=ApplicationForm.TABLET,
                            dosing=Dosing.SINGLE,
                            health=Health.T2DM
                            if condition == "normal"
                            else Health.T2DM_RENAL_IMPAIRMENT,
                            # dose after an overnight fast, 10 min before
                            # breakfast, as in the other studies of the label
                            fasting=Fasting.FASTED,
                        ),
                    )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        return self.figures_by_sid(
            self._figure_single(),
            self._figure_urine(),
            self._figure_uge(),
        )

    def _figure_single(self) -> Figure:
        """Plasma concentrations of canagliflozin, M5 and M7."""
        fig = Figure(
            experiment=self,
            sid="Fig_single",
            num_rows=1,
            num_cols=3,
            name=f"{self.__class__.__name__} (T2DM)",
            # the legend inside the panels covers data: right of the grid
            settings={"legend_scope": "row"},
        )
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit=self.unit_time), legend=True
        )
        plots[0].set_yaxis(self.label_can, unit=self.unit_can)
        plots[1].set_yaxis(self.label_m5, unit=self.unit_m5)
        plots[2].set_yaxis(self.label_m7, unit=self.unit_m7)

        for condition, renal_class in self.conditions_renal.items():
            for dose in self.doses:
                for k, sid in enumerate(self.info):
                    # simulation
                    plots[k].add_data(
                        task=f"task_po_can{dose}_{condition}",
                        xid="time",
                        yid=f"[Cve_{sid}]",
                        label=f"{dose} mg PO ({self.labels[condition]})",
                        color=self.renal_colors[renal_class],
                        linewidth=3 if dose == 200 else 2,
                    )

                    # data
                    did = self.info[sid]
                    plots[k].add_data(
                        dataset=f"{did}_CAN{dose}_{condition}",
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                        label=f"{dose} mg PO ({self.labels[condition]})",
                        color=self.renal_colors[renal_class],
                        marker=self.markers[dose],
                    )

        return fig

    def _figure_urine(self) -> Figure:
        """Urinary canagliflozin."""
        fig = Figure(
            experiment=self,
            sid="Fig_urine",
            name=f"{self.__class__.__name__} (T2DM)",
            # the legend inside the panels covers data: right of the grid
            settings={"legend_scope": "row"},
        )
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit=self.unit_time), legend=True
        )
        plots[0].set_yaxis(self.label_can_urine, unit=self.unit_can_urine)

        for dose in self.doses:
            for condition, renal_class in self.conditions_renal.items():
                # simulation
                plots[0].add_data(
                    task=f"task_po_can{dose}_{condition}",
                    xid="time",
                    yid="Aurine_can",
                    label=f"{dose} mg PO ({self.labels[condition]})",
                    color=self.renal_colors[renal_class],
                    linewidth=3 if dose == 200 else 2,
                )

                # data
                plots[0].add_data(
                    dataset=f"canagliflozin_urine_CAN{dose}_{condition}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=f"{dose} mg PO ({self.labels[condition]})",
                    color=self.renal_colors[renal_class],
                    marker=self.markers[dose],
                    linestyle="",
                )

        return fig

    def _figure_uge(self) -> Figure:
        """Urinary glucose excretion per day (change from the baseline day)."""
        fig = Figure(
            experiment=self,
            sid="Fig_uge",
            name=f"{self.__class__.__name__} (T2DM)",
            # the legend inside the panels covers data: right of the grid
            settings={"legend_scope": "row"},
        )
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit=self.unit_time), legend=True
        )
        plots[0].set_yaxis(self.label_uge, unit=self.unit_uge)

        for condition, renal_class in self.conditions_renal.items():
            for dose in self.doses:
                # simulation
                plots[0].add_data(
                    task=f"task_po_can{dose}_{condition}",
                    xid="time",
                    yid="KI__UGE",
                    label=f"{dose} mg PO ({self.labels[condition]})",
                    color=self.renal_colors[renal_class],
                    linewidth=3 if dose == 200 else 2,
                )
                # data
                plots[0].add_data(
                    dataset=f"glucose_excretion_daily_CAN{dose}_{condition}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=f"{dose} mg PO ({self.labels[condition]})",
                    color=self.renal_colors[renal_class],
                    marker=self.markers[dose],
                    linestyle="",
                )

        return fig


if __name__ == "__main__":
    MODEL.run_experiments(Inagaki2014, output_dir=Inagaki2014.__name__)

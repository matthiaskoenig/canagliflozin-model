"""Simulation experiment of the study Chen2015."""

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
from sbmlsim.simulation import Simulation

from pkdb_models.models.canagliflozin import MODEL
from pkdb_models.models.canagliflozin.experiments.base_experiment import (
    CanagliflozinSimulationExperiment,
)


class Chen2015(CanagliflozinSimulationExperiment):
    """Simulation experiment of Chen2015."""

    bodyweight = 63  # [kg]
    fpg = 5  # [mM] (healthy, not reported)
    #: the eGFR (MDRD) [ml/min/1.73 m^2]
    gfr = 103
    #: the mean plasma glucose of 0-24 hr (MPG0-24) of the arms (Table III)
    #: [mg/dl], the glucose which is filtered
    mpg: ClassVar[dict[int, float]] = {0: 99.4, 100: 98.2, 300: 96.9}

    interventions: ClassVar[dict[str, int]] = {"CAN100": 100, "CAN300": 300}

    interventions_uge: ClassVar[dict[str, int]] = {
        "CAN0": 0,
        "CAN100": 100,
        "CAN300": 300,
    }

    info: ClassVar[dict[str, str]] = {
        "can": "canagliflozin",
        "m5": "M5",
        "m7": "M7",
    }

    doses: ClassVar[list[int]] = [0, 100, 300]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1", "Tab2A", "Tab3"]:
            df = self.load_dataframe(fig_id)
            for label, df_label in df.groupby("label"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)
                # unit conversion to mole/l; the amounts of the metabolites in
                # the urine are canagliflozin equivalents (% of the dose,
                # "corrected for molecular weight only for metabolites")
                if label.startswith(
                    ("canagliflozin_", "M5_cumulative_amount", "M7_cumulative_amount")
                ):
                    dset.unit_conversion("mean", 1 / self.Mr.can)
                elif label.startswith("M7_"):
                    dset.unit_conversion("mean", 1 / self.Mr.m7)
                elif label.startswith("M5_"):
                    dset.unit_conversion("mean", 1 / self.Mr.m5)
                elif label.startswith("glucose_RT"):
                    dset.unit_conversion("mean", 1 / self.Mr.glc)
                dsets[label] = dset
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}
        for dose in self.doses:
            tcsims[f"po_can_CAN{dose}"] = Simulation(
                time_unit="hr",
                end=80,
                preinit_changes={
                    **self.default_changes(),
                    "BW": Q(self.bodyweight, "kg"),
                    "[KI__fpg]": Q(self.fpg, "mM"),
                    "KI__PG_delta": (Q(self.mpg[dose], "mg/dl") / self.Mr.glc).to("mM")
                    - Q(self.fpg, "mM"),
                    "KI__f_renal_function": Q(self.gfr / 101, "dimensionless"),
                    "PODOSE_can": Q(dose, "mg"),
                },
            )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for name, sid in [
            ("canagliflozin", "[Cve_can]"),
            ("M5", "[Cve_m5]"),
            ("M7", "[Cve_m7]"),
            ("canagliflozin_cumulative_amount", "Aurine_can"),
            ("M5_cumulative_amount", "Aurine_m5"),
            ("M7_cumulative_amount", "Aurine_m7"),
            ("glucose_cumulative_amount", "KI__UGE"),
            # the 24-hr mean RTG, calculated with the GFR of the MDRD equation
            # and of the measured creatinine clearance
            ("glucose_RT_MDRD", "KI__RTG_mean"),
            ("glucose_RT_McrCl", "KI__RTG_mean"),
        ]:
            tissue = Tissue.URINE if "cumulative" in name else Tissue.PLASMA
            for intervention in self.interventions_uge:
                # the placebo has only data of the urinary glucose excretion
                if intervention != "CAN0" or sid == "KI__UGE":
                    mappings[f"fm_po_can_{intervention}_{name}"] = FitMapping(
                        self,
                        reference=FitData(
                            self,
                            dataset=f"{name}_{intervention}",
                            xid="time",
                            yid="mean",
                            yid_sd="mean_sd",
                            count="count",
                        ),
                        observable=FitData(
                            self,
                            task=f"task_po_can_{intervention}",
                            xid="time",
                            yid=sid,
                        ),
                        # dosed 10 min before a standardized breakfast, the
                        # convention of the studies is fasted
                        metadata=PKPDMappingMetaData(
                            tissue=tissue,
                            route=Route.PO,
                            application_form=ApplicationForm.TABLET,
                            dosing=Dosing.SINGLE,
                            health=Health.HEALTHY,
                            fasting=Fasting.FASTED,
                        ),
                    )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        return self.figures_by_sid(
            self._figure_plasma(), self._figure_urine(), self._figure_uge()
        )

    def _figure_plasma(self) -> Figure:
        """Plasma concentrations of canagliflozin, M5 and M7."""
        fig = Figure(
            experiment=self,
            sid="Fig1",
            num_rows=1,
            num_cols=3,
            name=f"{self.__class__.__name__} (Healthy)",
        )
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit=self.unit_time), legend=True
        )
        plots[0].set_yaxis(self.label_can, unit=self.unit_can)
        plots[1].set_yaxis(self.label_m5, unit=self.unit_m5)
        plots[2].set_yaxis(self.label_m7, unit=self.unit_m7)

        for intervention, dose in self.interventions.items():
            for k, (sid, did) in enumerate(self.info.items()):
                # simulation
                plots[k].add_data(
                    task=f"task_po_can_{intervention}",
                    xid="time",
                    yid=f"[Cve_{sid}]",
                    label=f"{dose} mg PO",
                    color=self.dose_colors[dose],
                )
                # data
                plots[k].add_data(
                    dataset=f"{did}_{intervention}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=f"{dose} mg PO",
                    color=self.dose_colors[dose],
                )

        return fig

    def _figure_urine(self) -> Figure:
        """Cumulative amounts of canagliflozin, M5 and M7 in the urine."""
        fig = Figure(
            experiment=self,
            sid="Fig2",
            num_rows=1,
            num_cols=3,
            name=f"{self.__class__.__name__} (Healthy)",
        )
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit=self.unit_time), legend=True
        )
        plots[0].set_yaxis(self.label_can_urine, unit=self.unit_can_urine)
        plots[1].set_yaxis(self.label_m5_urine, unit=self.unit_m5_urine)
        plots[2].set_yaxis(self.label_m7_urine, unit=self.unit_m7_urine)

        for intervention, dose in self.interventions.items():
            for k, (sid, did) in enumerate(self.info.items()):
                # simulation
                plots[k].add_data(
                    task=f"task_po_can_{intervention}",
                    xid="time",
                    yid=f"Aurine_{sid}",
                    label=f"{dose} mg PO",
                    color=self.dose_colors[dose],
                )
                # data
                plots[k].add_data(
                    dataset=f"{did}_cumulative_amount_{intervention}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=f"{dose} mg PO",
                    color=self.dose_colors[dose],
                    linestyle="",
                )

        return fig

    def _figure_uge(self) -> Figure:
        """Urinary glucose excretion and the mean renal threshold of glucose."""
        fig = Figure(
            experiment=self,
            sid="Fig3",
            num_rows=1,
            num_cols=2,
            name=f"{self.__class__.__name__} (Healthy)",
        )
        # the legends inside the panels cover data
        fig.settings = {**fig.settings, "legend_position": "outside"}
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit=self.unit_time), legend=True
        )
        plots[0].set_yaxis(self.label_uge, unit=self.unit_uge)
        plots[1].set_yaxis(self.label_rtg_mean, unit=self.unit_rtg)

        for intervention, dose in self.interventions_uge.items():
            # simulation
            for k, sid in enumerate(["UGE", "RTG_mean"]):
                plots[k].add_data(
                    task=f"task_po_can_{intervention}",
                    xid="time",
                    yid=f"KI__{sid}",
                    label=f"{dose} mg PO",
                    color=self.dose_colors[dose],
                )
            # data
            plots[0].add_data(
                dataset=f"glucose_cumulative_amount_{intervention}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"{dose} mg PO",
                color=self.dose_colors[dose],
            )
            if intervention != "CAN0":
                for method, marker in [("MDRD", "s"), ("McrCl", "^")]:
                    plots[1].add_data(
                        dataset=f"glucose_RT_{method}_{intervention}",
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                        label=f"{dose} mg PO ({method})",
                        color=self.dose_colors[dose],
                        linestyle="",
                        marker=marker,
                    )

        return fig


if __name__ == "__main__":
    MODEL.run_experiments(Chen2015, output_dir=Chen2015.__name__)

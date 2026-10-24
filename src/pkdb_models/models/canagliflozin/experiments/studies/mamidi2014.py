"""Simulation experiment of the study Mamidi2014."""

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


class Mamidi2014(CanagliflozinSimulationExperiment):
    """Simulation experiment of Mamidi2014.

    Mass balance of a single oral dose of 188 mg [14C]canagliflozin (0.5 %
    hypromellose suspension) in 6 healthy men (19-45 years, BW 62-87 kg),
    overnight fast >= 8 h, lunch at 4 h, dinner at 10 h. Plasma radioactivity
    and the radio-HPLC profiles of canagliflozin, M5, M7 and M9 in pooled
    samples to 24 h (Fig 3), urine and feces pooled 0-48 h by metabolite
    (Tables 5 and 6) and the total radioactivity in urine and feces 0-168 h
    (Table 1).

    All data are radioactivity in canagliflozin equivalents (ng-eq/ml,
    percent of the dose), converted with the molecular weight of
    canagliflozin. The total of the model in plasma and urine is
    canagliflozin + M5 + M7, in feces canagliflozin + M7 + M9.
    """

    bodyweight = 75  # [kg] reference, the range 62-87 kg is reported
    fpg = 5  # mM (healthy)

    info: ClassVar[dict[str, str]] = {
        "cantot": "canagliflozin_total",
        "can": "canagliflozin",
        "m5": "M5",
        "m7": "M7",
    }

    info_urine: ClassVar[dict[str, str]] = {
        "cantot": "canagliflozin_total",
        "m5": "M5",
        "m7": "M7",
    }

    info_feces: ClassVar[dict[str, str]] = {
        "cantot": "canagliflozin_total",
        "can": "canagliflozin",
        "m9": "M9",
        "m7": "M7",
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig3", "Tab5A", "Tab6A", "Tab1A"]:
            df = self.load_dataframe(fig_id)
            # the amounts (the recovery in percent of the dose repeats them);
            # no observable for M9 in plasma and the sum of urine and feces
            df = df[
                df.measurement_type.isin(["concentration", "cumulative amount"])
                & (df.label != "M9_CAN188")
                & (df.tissue != "feces_urine")
            ]
            for label, df_label in df.groupby("label"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)

                # radioactivity in canagliflozin equivalents to mole/l and mole
                dset.unit_conversion("mean", 1 / self.Mr.can)

                dsets[self.to_sid(label)] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}

        tcsims["po_can_CAN188"] = Simulation(
            time_unit="hr",
            end=170,
            preinit_changes={
                **self.default_changes(),
                "BW": Q(self.bodyweight, "kg"),
                "[KI__fpg]": Q(self.fpg, "mM"),
                "PODOSE_can": Q(188, "mg"),
            },
        )

        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for name, sid in [
            ("canagliflozin_total_CAN188", "[Cve_cantot]"),
            ("canagliflozin_CAN188", "[Cve_can]"),
            ("M5_CAN188", "[Cve_m5]"),
            ("M7_CAN188", "[Cve_m7]"),
        ]:
            mappings[self.to_sid(f"fm_CAN188_{name}")] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(name),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task="task_po_can_CAN188",
                    xid="time",
                    yid=sid,
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.PLASMA,
                    route=Route.PO,
                    application_form=ApplicationForm.SUSPENSION,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                ),
            )

        # the cumulative amounts in the urine and feces
        for name_excreta, sid_excreta in [
            ("canagliflozin_total_cumulative amount_urine", "Aurine_cantot"),
            ("M5_cumulative amount_urine", "Aurine_m5"),
            ("M7_cumulative amount_urine", "Aurine_m7"),
            ("canagliflozin_total_cumulative amount_feces", "Afeces_cantot"),
            # the total radioactivity 0-168 h (Table 1)
            ("canagliflozin_total_cumulative amount_168h_urine", "Aurine_cantot"),
            ("canagliflozin_total_cumulative amount_168h_feces", "Afeces_cantot"),
            ("canagliflozin_cumulative amount_feces", "Afeces_can"),
            ("M7_cumulative amount_feces", "Afeces_m7"),
            ("M9_cumulative amount_feces", "Afeces_m9"),
        ]:
            tissue = Tissue.URINE if "urine" in name_excreta else Tissue.FECES
            mappings[self.to_sid(f"fm_CAN188_{name_excreta}")] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(name_excreta),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task="task_po_can_CAN188",
                    xid="time",
                    yid=sid_excreta,
                ),
                metadata=PKPDMappingMetaData(
                    tissue=tissue,
                    route=Route.PO,
                    application_form=ApplicationForm.SUSPENSION,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                ),
            )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        return self.figures_by_sid(
            self._figure_conc(),
            self._figure_urine(),
            self._figure_feces(),
        )

    def _figure_conc(self) -> Figure:
        """Plasma concentrations."""
        fig = Figure(
            experiment=self,
            sid="Fig2",
            num_rows=2,
            num_cols=2,
            name=f"{self.__class__.__name__} (Healthy)",
        )
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit=self.unit_time, min=0, max=26),
            legend=True,
        )
        plots[0].set_yaxis(self.label_cantot, unit=self.unit_cantot)
        plots[1].set_yaxis(self.label_can, unit=self.unit_can)
        plots[2].set_yaxis(self.label_m5, unit=self.unit_m5)
        plots[3].set_yaxis(self.label_m7, unit=self.unit_m7)

        for k, sid in enumerate(self.info):
            # simulation
            plots[k].add_data(
                task="task_po_can_CAN188",
                xid="time",
                yid=f"[Cve_{sid}]",
                label="188 mg PO",
                color="black",
            )

            # data
            did = self.info[sid]
            plots[k].add_data(
                dataset=self.to_sid(f"{did}_CAN188"),
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label="188 mg PO",
                color="black",
            )

        return fig

    def _figure_urine(self) -> Figure:
        """Urinary excretion."""
        fig = Figure(
            experiment=self,
            sid="urine",
            num_rows=1,
            num_cols=3,
            name=f"{self.__class__.__name__} (Healthy)",
        )
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit=self.unit_time), legend=True
        )
        plots[0].set_yaxis(self.label_cantot_urine, unit=self.unit_cantot_urine)
        plots[1].set_yaxis(self.label_m5_urine, unit=self.unit_m5_urine)
        plots[2].set_yaxis(self.label_m7_urine, unit=self.unit_m7_urine)

        for k, sid in enumerate(self.info_urine):
            # simulation
            plots[k].add_data(
                task="task_po_can_CAN188",
                xid="time",
                yid=f"Aurine_{sid}",
                label="188 mg PO",
                color="black",
            )
            # data
            did = self.info[sid]
            plots[k].add_data(
                dataset=self.to_sid(f"{did}_cumulative amount_urine"),
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label="188 mg PO (0-48 h)",
                color="black",
                linestyle="",
            )
        plots[0].add_data(
            dataset=self.to_sid("canagliflozin_total_cumulative amount_168h_urine"),
            xid="time",
            yid="mean",
            count="count",
            label="188 mg PO (0-168 h)",
            color="tab:blue",
            linestyle="",
        )
        return fig

    def _figure_feces(self) -> Figure:
        """Fecal excretion."""
        fig = Figure(
            experiment=self,
            sid="feces",
            num_rows=2,
            num_cols=2,
            name=f"{self.__class__.__name__} (Healthy)",
        )
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit=self.unit_time), legend=True
        )
        plots[0].set_yaxis(self.label_cantot_feces, unit=self.unit_cantot_feces)
        plots[1].set_yaxis(self.label_can_feces, unit=self.unit_can_feces)
        plots[2].set_yaxis(self.label_m9_feces, unit=self.unit_m9_feces)
        plots[3].set_yaxis(self.label_m7_feces, unit=self.unit_m7_feces)

        for k, sid in enumerate(self.info_feces):
            # simulation
            plots[k].add_data(
                task="task_po_can_CAN188",
                xid="time",
                yid=f"Afeces_{sid}",
                label="188 mg PO",
                color="black",
            )
            # data
            did = self.info_feces[sid]
            plots[k].add_data(
                dataset=self.to_sid(f"{did}_cumulative amount_feces"),
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label="188 mg PO (0-48 h)",
                color="black",
                linestyle="",
            )
        plots[0].add_data(
            dataset=self.to_sid("canagliflozin_total_cumulative amount_168h_feces"),
            xid="time",
            yid="mean",
            count="count",
            label="188 mg PO (0-168 h)",
            color="tab:blue",
            linestyle="",
        )
        return fig


if __name__ == "__main__":
    MODEL.run_experiments(Mamidi2014, output_dir=Mamidi2014.__name__)

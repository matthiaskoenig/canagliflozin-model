"""Simulation experiment of the study Devineni2015b."""

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


class Devineni2015b(CanagliflozinSimulationExperiment):
    """Simulation experiment of Devineni2015b."""

    bodyweight = 78.2  # [kg]
    fpg = 5  # mM (healthy)

    #: the datasets of the plasma: the intervention, the simulation, the
    #: observable; the unchanged [14C]-canagliflozin (AMS, n=5) is
    #: canagliflozin, the total 14C (n=9) is canagliflozin, M5 and M7 in
    #: canagliflozin equivalents (the radioactivity of M9 and of the other
    #: oxidative metabolites in the plasma is not in the model)
    plasma: ClassVar[list[tuple[str, str, str]]] = [
        ("CAN300", "po_iv", "[Cve_can]"),
        ("unchanged_C14CAN10", "iv", "[Cve_can]"),
        ("total_C14CAN10", "iv", "[Cve_cantot]"),
    ]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig2", "Tab1A"]:
            df = self.load_dataframe(fig_id)
            for label, df_label in df.groupby("label"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)

                # unit conversion to mole/l
                if label.startswith("canagliflozin_"):
                    dset.unit_conversion("mean", 1 / self.Mr.can)

                dsets[label] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}

        # 10 µg [14C]-canagliflozin intravenous over 15 min, 105 min after
        # the oral dose; the model is linear at these concentrations, the tracer
        # is simulated without the oral dose (`iv`): the difference of 300 mg +
        # 10 µg and 300 mg deviates < 5 % from 10 µg alone
        changes_iv = [
            Change(105, {"Ri_can": Q(10 / 15, "µg/min")}),
            Change(120, {"Ri_can": Q(0, "µg/min")}),
        ]
        for key, po_dose in [
            # 300 mg PO followed by the tracer iv
            ("po_iv", 300),
            # only the tracer iv
            ("iv", 0),
        ]:
            tcsims[key] = Simulation(
                time_unit="min",
                end=120 + 80 * 60,
                preinit_changes={
                    **self.default_changes(),
                    "BW": Q(self.bodyweight, "kg"),
                    "[KI__fpg]": Q(self.fpg, "mM"),
                    "PODOSE_can": Q(po_dose, "mg"),
                },
                changes=changes_iv,
            )

        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}

        for intervention, sim_key, sid in self.plasma:
            mappings[f"fm_{intervention}_canagliflozin"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"canagliflozin_{intervention}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task=f"task_{sim_key}",
                    xid="time",
                    yid=sid,
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.PLASMA,
                    route=Route.PO if intervention == "CAN300" else Route.IV,
                    application_form=ApplicationForm.TABLET
                    if intervention == "CAN300"
                    else ApplicationForm.SOLUTION,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                ),
            )

        # total 14C (canagliflozin equivalents) excreted 0-70 hr after the iv
        # start (71.75 hr); the radioactivity of the feces is mostly
        # canagliflozin of the hydrolysed glucuronides of the bile
        for name, sid in [
            ("urine", "Aurine_cantot"),
            ("feces", "Afeces_cantot"),
        ]:
            tissue = Tissue.URINE if "urine" in name else Tissue.FECES
            mappings[f"fm_{name}_canagliflozin_total"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"canagliflozin_14C_CAN10_cumulative_amount_{name}_total",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task="task_iv",
                    xid="time",
                    yid=sid,
                ),
                metadata=PKPDMappingMetaData(
                    tissue=tissue,
                    route=Route.IV,
                    application_form=ApplicationForm.SOLUTION,
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
            self._figure_urine_feces(),
        )

    def _figure_conc(self) -> Figure:
        """Plasma concentrations of canagliflozin."""
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
        plots[0].set_yaxis(self.label_can, unit=self.unit_can)
        plots[1].set_yaxis(self.label_can, unit="nM")  # very small IV dose
        plots[2].set_yaxis(self.label_cantot, unit="nM")  # very small IV dose

        labels = [
            "300 mg PO + 10 µg 14C IV",
            "10 µg 14C IV (unchanged)",
            "10 µg 14C IV (total)",
        ]

        for k, ((intervention, sim_key, sid), label) in enumerate(
            zip(self.plasma, labels, strict=True)
        ):
            # simulation
            plots[k].add_data(
                task=f"task_{sim_key}",
                xid="time",
                yid=sid,
                label=label,
                color="black",
            )
            # data
            plots[k].add_data(
                dataset=f"canagliflozin_{intervention}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=label,
                color="black",
            )

        return fig

    def _figure_urine_feces(self) -> Figure:
        """Cumulative amounts of total canagliflozin in the urine and feces."""
        fig = Figure(
            experiment=self,
            sid="Fig_urine_feces",
            num_rows=1,
            num_cols=2,
            name=f"{self.__class__.__name__} (Healthy)",
        )
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit=self.unit_time), legend=True
        )
        plots[0].set_yaxis(self.label_cantot_urine, unit="nmole")  # very small IV dose
        plots[1].set_yaxis(self.label_cantot_feces, unit="nmole")  # very small IV dose

        for k, (sid, tissue) in enumerate(
            [("Aurine_cantot", "urine"), ("Afeces_cantot", "feces")]
        ):
            label = "10 µg 14C IV"

            # simulation
            plots[k].add_data(
                task="task_iv",
                xid="time",
                yid=sid,
                label=label,
                color="black",
            )
            # data
            plots[k].add_data(
                dataset=f"canagliflozin_14C_CAN10_cumulative_amount_{tissue}_total",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=label,
                color="black",
            )

        return fig


if __name__ == "__main__":
    MODEL.run_experiments(Devineni2015b, output_dir=Devineni2015b.__name__)

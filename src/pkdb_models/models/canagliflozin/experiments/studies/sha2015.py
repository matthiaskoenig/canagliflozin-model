"""Simulation experiment of the study Sha2015."""

from typing import override

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


class Sha2015(CanagliflozinSimulationExperiment):
    """Simulation experiment of Sha2015.

    Healthy subjects, crossover with dapagliflozin (not simulated):
    canagliflozin 300 mg (over-encapsulated tablet) once daily for 4 days after
    an overnight fast, on day 4 20 min before a mixed meal tolerance test
    (MMTT, t = 0 of the paper). Plasma canagliflozin, the cumulative urinary
    glucose (UGE, urine of 0 - 2, 2 - 4, 4 - 10, 10 - 14 and 14 - 24 hr from
    the start of the MMTT, Table 2) and the mean renal threshold of glucose
    (RTG) of 0 - 4, 4 - 10, 10 - 14 and 14 - 24 hr of day 4.

    The simulation is shifted so that the dose of day 4 is at 0 hr; the times
    of the data are relative to it (the times of the paper + 20 min).
    """

    bodyweight = 78.9  # [kg]
    #: healthy, pre-MMTT plasma glucose 4.8 - 5.0 mM; the mean plasma glucose
    #: of the day is the model default (`KI__PG_delta`, from this study)
    fpg = 5  # [mM]
    #: eGFR 96.8 (14.7) ml/min/1.73 m^2
    gfr = 96.8  # [ml/min]

    #: the dose of day 4
    time_dose = 72  # [hr]
    #: the start of the MMTT after the dose (20 min)
    time_mmtt = 1 / 3  # [hr]
    #: the start of the intervals of the RTG after the start of the MMTT [hr]
    times_rtg = (0, 4, 10, 14)

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig2", "Fig3"]:
            df = self.load_dataframe(fig_id)
            for label, df_label in df.groupby("label"):
                dsets[str(label)] = DataSet.from_df(df_label, self.ureg)

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}

        rtg_reset: dict[str, Quantity] = {
            "KI__RTG_int": Q(0, "mM*min"),
            "KI__RTG_time": Q(0, "min"),
        }
        start = self.time_dose + self.time_mmtt
        # once daily on days 1 - 4; the urine of day 4 is collected from the
        # start of the MMTT, the RTG of its intervals
        tcsims["po_can300"] = Simulation(
            time_unit="hr",
            end=self.time_dose + 24.5,
            preinit_changes={
                **self.default_changes(),
                "BW": Q(self.bodyweight, "kg"),
                "[KI__fpg]": Q(self.fpg, "mM"),
                "KI__f_renal_function": Q(self.gfr / 101, "dimensionless"),
                "PODOSE_can": Q(300, "mg"),
            },
            changes=[
                self.add_doses([24, 48, self.time_dose], {"PODOSE_can": Q(300, "mg")}),
                Change(start, {"KI__glc_urine": Q(0, "mmole"), **rtg_reset}),
                Change([start + t for t in self.times_rtg[1:]], rtg_reset),
            ],
            time_shift=-self.time_dose,
        )

        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}

        for key, (dataset, sid, tissue) in {
            "plasma": ("canagliflozin_CAN300", "[Cve_can]", Tissue.PLASMA),
            "uge": ("glucose_cumulative_amount_CAN300", "KI__UGE", Tissue.URINE),
            "rtg": ("renal_threshold_CAN300", "KI__RTG_mean", Tissue.PLASMA),
        }.items():
            mappings[f"fm_can300_{key}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=dataset,
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(self, task="task_po_can300", xid="time", yid=sid),
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
        fig = Figure(
            experiment=self,
            sid="Fig_day4",
            num_rows=1,
            num_cols=3,
            name=f"{self.__class__.__name__} (Healthy, day 4)",
        )
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit=self.unit_time, min=-2, max=26),
            legend=True,
        )
        plots[0].set_yaxis(self.label_can, unit=self.unit_can)
        # the urine before day 4 is not collected
        plots[1].set_yaxis(self.label_uge, unit=self.unit_uge, min=-2, max=70)
        plots[2].set_yaxis(self.label_rtg_mean, unit=self.unit_rtg, min=2, max=5)

        for k, (sid, dataset) in enumerate(
            [
                ("[Cve_can]", "canagliflozin_CAN300"),
                ("KI__UGE", "glucose_cumulative_amount_CAN300"),
                ("KI__RTG_mean", "renal_threshold_CAN300"),
            ]
        ):
            plots[k].add_data(
                task="task_po_can300",
                xid="time",
                yid=sid,
                label="300 mg PO QD",
                color=self.dose_colors[300],
            )
            plots[k].add_data(
                dataset=dataset,
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label="300 mg PO QD",
                color=self.dose_colors[300],
            )

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(Sha2015, output_dir=Sha2015.__name__)

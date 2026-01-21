from typing import Dict

from sbmlsim.data import DataSet, load_pkdb_dataframe
from sbmlsim.fit import FitMapping, FitData
from sbmlutils.console import console

from pkdb_models.models.canagliflozin.experiments.base_experiment import (
    CanagliflozinSimulationExperiment
)
from pkdb_models.models.canagliflozin.experiments.metadata import Tissue, Route, Dosing, ApplicationForm, Health, \
    Fasting, CanagliflozinMappingMetaData, Coadministration

from sbmlsim.plot import Axis, Figure
from sbmlsim.simulation import Timecourse, TimecourseSim

from pkdb_models.models.canagliflozin.helpers import run_experiments


class Devineni2015d(CanagliflozinSimulationExperiment):
    """Simulation experiment of Devineni2015d."""

    groups = {"CAN300": "can300_single", "CAN300_RIF600": "can300_rif600_single",
              "CAN300_2": "can300_2_multi", "CAN300_2_PRO500": "can300_2_pro500_multi",
              "CAN300_3": "can300_3_multi", "CAN300_3_CYC400": "can300_3_cyc400_multi"}

    info = {
        "can": "canagliflozin",
        "m5": "M5",
        "m7": "M7",
    }

    bodyweights = {
        "can300": 75, "can300_rif600": 75,
        "can300_2": 79.6, "can300_2_pro500": 79.6,
        "can300_3": 80.5, "can300_3_cyc400": 80.5
    }

    fpg = 5  # [mM] (Healthy)

    coadministration = [Coadministration.NONE, Coadministration.RIFAMPICIN,
                        Coadministration.NONE, Coadministration.PROBENECID,
                        Coadministration.NONE, Coadministration.CYCLOSPORINE]

    def datasets(self) -> Dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig2", "Fig3", "Fig4", "Tab2A", "Tab3A"]:
            df = load_pkdb_dataframe(f"{self.sid}_{fig_id}", data_path=self.data_path)
            for label, df_label in df.groupby("label"):
                dset = DataSet.from_df(df_label, self.ureg)

                # unit conversion to mole/l
                if label.startswith("canagliflozin_"):
                    dset.unit_conversion("mean", 1 / self.Mr.can)
                elif label.startswith("M5_"):
                    dset.unit_conversion("mean", 1 / self.Mr.m5)
                elif label.startswith("M7_"):
                    dset.unit_conversion("mean", 1 / self.Mr.m7)

                dsets[f"{label}"] = dset

        # console.print(dsets)
        # console.print(dsets.keys())
        return dsets

    def simulations(self) -> Dict[str, TimecourseSim]:
        Q_ = self.Q_
        tcsims = {}

        # single dose
        for sim in ["can300", "can300_rif600"]:
            tcsims[f"po_{sim}_single"] = TimecourseSim(
                Timecourse(
                    start=0,
                    end=73 * 60,  # [min]
                    steps=500,
                    changes={
                        **self.default_changes(),
                        "BW": Q_(self.bodyweights[sim], "kg"),
                        "[KI__fpg]": Q_(self.fpg, "mM"),
                        "PODOSE_can": Q_(300, "mg"),
                    },
                )
            )

        # multiple dose 2
        for sim in ["can300_2", "can300_2_pro500"]:
            tc0 = Timecourse(
                start=0,
                end=24 * 60,  # [min]
                steps=500,
                changes={
                    **self.default_changes(),
                    "BW": Q_(self.bodyweights[sim], "kg"),
                    "[KI__fpg]": Q_(5, "mM"),
                    "PODOSE_can": Q_(300, "mg"),
                },
            )
            changes_multi = {
                "BW": Q_(self.bodyweights[sim], "kg"),
                "[KI__fpg]": Q_(5, "mM"),
                "Aurine_can": Q_(0, "mmole"),  # reset canagliflozin
                "Aurine_m5": Q_(0, "mmole"),  # reset M5
                "Aurine_m7": Q_(0, "mmole"),  # reset M7
                "PODOSE_can": Q_(300, "mg"),
            }
            tc1 = Timecourse(
                start=0,
                end=24 * 60,  # [min]
                steps=500,
                changes=changes_multi
            )
            tc2 = Timecourse(
                start=0,
                end=25 * 60,  # [min]
                steps=500,
                changes=changes_multi
            )

            tcsims[f"po_{sim}_multi"] = TimecourseSim(
                [tc0] + [tc1 for _ in range(15)] + [tc2],
                time_offset=-16 * 24 * 60,
            )

        # multiple dose 3
        for sim in ["can300_3", "can300_3_cyc400"]:
            tc0 = Timecourse(
                start=0,
                end=24 * 60,  # [min]
                steps=500,
                changes={
                    **self.default_changes(),
                    "PODOSE_can": Q_(300, "mg"),
                },
            )
            changes_multi = {
                "BW": Q_(self.bodyweights[sim], "kg"),
                "[KI__fpg]": Q_(5, "mM"),
                "Aurine_can": Q_(0, "mmole"),  # reset canagliflozin
                "Aurine_m5": Q_(0, "mmole"),  # reset M5
                "Aurine_m7": Q_(0, "mmole"),  # reset M7
                "PODOSE_can": Q_(300, "mg"),
            }
            tc1 = Timecourse(
                start=0,
                end=24 * 60,  # [min]
                steps=500,
                changes=changes_multi
            )
            tc2 = Timecourse(
                start=0,
                end=25 * 60,  # [min]
                steps=500,
                changes=changes_multi
            )

            tcsims[f"po_{sim}_multi"] = TimecourseSim(
                [tc0] + [tc1 for _ in range(6)] + [tc2],
                time_offset=-7 * 24 * 60,
            )

        return tcsims

    def fit_mappings(self) -> Dict[str, FitMapping]:

        mappings = {}

        for k, (group, sim) in enumerate(list(self.groups.items())):

            dosing = Dosing.SINGLE if "single" in sim else Dosing.MULTIPLE

            mappings[f"task_po_{sim}_{group}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"canagliflozin_{group}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self, task=f"task_po_{sim}", xid="time", yid="[Cve_can]",
                ),
                metadata=CanagliflozinMappingMetaData(
                    tissue=Tissue.PLASMA,
                    route=Route.PO,
                    application_form=ApplicationForm.TABLET,
                    dosing=dosing,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                    coadministration=self.coadministration[k]
                ),
            )

        for name, sid in [
            ('canagliflozin_urine', 'Aurine_can'),
            ('M5_urine', 'Aurine_m5'),
            ('M7_urine', 'Aurine_m7')
        ]:
            for k, (group, sim) in enumerate(list(self.groups.items())[:2]):

                dosing = Dosing.SINGLE if "single" in sim else Dosing.MULTIPLE

                mappings[f"task_po_{sim}_{name}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=f"{name}_{group}",
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                    ),
                    observable=FitData(
                        self, task=f"task_po_{sim}", xid="time", yid="Aurine_can",
                    ),
                    metadata=CanagliflozinMappingMetaData(
                        tissue=Tissue.URINE,
                        route=Route.PO,
                        application_form=ApplicationForm.TABLET,
                        dosing=dosing,
                        health=Health.HEALTHY,
                        fasting=Fasting.FASTED,
                        coadministration=self.coadministration[k]
                    ),
                )

        # console.print(mappings)
        return mappings

    def figures(self) -> Dict[str, Figure]:
        return {
            **self.figure_multi(),
            **self.figure_urine_rif(),
            **self.figure_urine_pro()
        }

    def figure_multi(self) -> Dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="can multi",
            num_rows=1,
            num_cols=3,
            name=f"{self.__class__.__name__} (Healthy)",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit=self.unit_time), legend=True)
        plots[0].set_yaxis(self.label_can, unit=self.unit_can)
        plots[1].set_yaxis(self.label_can, unit=self.unit_can)
        plots[2].set_yaxis(self.label_can, unit=self.unit_can)

        # Define pairs and labels
        pairs = [
            (["CAN300", "CAN300_RIF600"], ["can300_single", "can300_single"], ["300 mg PO", "300 mg PO + RIF"], 0),
            (["CAN300_2", "CAN300_2_PRO500"], ["can300_2_multi", "can300_2_multi"], ["300 mg PO", "300 mg PO + PRO"],
             1),
            (["CAN300_3", "CAN300_3_CYC400"], ["can300_3_multi", "can300_3_multi"], ["300 mg PO", "300 mg PO + CYC"],
             2),
        ]

        for groups, sims, labels, plot_idx in pairs:
            # simulation
            plots[plot_idx].add_data(
                task=f"task_po_{sims[0]}",
                xid="time",
                yid=f"[Cve_can]",
                label=labels[0],
                color="black",
            )

            # data
            for group, label in zip(groups, labels):
                color = "black" if group == groups[0] else "tab:blue"
                plots[plot_idx].add_data(
                    dataset=f"canagliflozin_{group}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=label,
                    color=color,
                )

        return {
            fig.sid: fig,
        }

    def figure_urine_rif(self) -> Dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig_urine_rif",
            num_rows=1,
            num_cols=3,
            name=f"{self.__class__.__name__} (Healthy)",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="day"), legend=True)
        plots[0].set_yaxis(self.label_can_urine, unit=self.unit_can_urine)
        plots[1].set_yaxis(self.label_m5_urine, unit=self.unit_m5_urine)
        plots[2].set_yaxis(self.label_m7_urine, unit=self.unit_m7_urine)

        for k, sid in enumerate(self.info):
            # simulation (only once)
            plots[k].add_data(
                task=f"task_po_can300_single",
                xid="time",
                yid=f"Aurine_{sid}",
                label="300 mg PO",
                color="black",
            )

            # data (both conditions)
            for group, label, color in [("CAN300", "300 mg PO", "black"),
                                        ("CAN300_RIF600", "300 mg PO + RIF", "tab:blue")]:
                did = self.info[sid]
                plots[k].add_data(
                    dataset=f"{did}_urine_{group}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=label,
                    color=color,
                )

        return {
            fig.sid: fig,
        }

    def figure_urine_pro(self) -> Dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig_urine_pro",
            num_rows=1,
            num_cols=3,
            name=f"{self.__class__.__name__} (Healthy)",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="day"), legend=True)
        plots[0].set_yaxis(self.label_can_urine, unit=self.unit_can_urine)
        plots[1].set_yaxis(self.label_m5_urine, unit=self.unit_m5_urine)
        plots[2].set_yaxis(self.label_m7_urine, unit=self.unit_m7_urine)

        for k, sid in enumerate(self.info):
            # simulation (only once)
            plots[k].add_data(
                task=f"task_po_can300_2_multi",
                xid="time",
                yid=f"Aurine_{sid}",
                label="300 mg PO",
                color="black",
            )

            # data (both conditions)
            for group, label, color in [("CAN300_2", "300 mg PO", "black"),
                                        ("CAN300_2_PRO500", "300 mg PO + PRO", "tab:blue")]:
                did = self.info[sid]
                plots[k].add_data(
                    dataset=f"{did}_urine_{group}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=label,
                    color=color,
                )

        return {
            fig.sid: fig,
        }
    

if __name__ == "__main__":
    run_experiments(Devineni2015d, output_dir=Devineni2015d.__name__)
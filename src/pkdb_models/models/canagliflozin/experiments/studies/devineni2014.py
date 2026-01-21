from typing import Dict
from sbmlsim.data import DataSet, load_pkdb_dataframe
from sbmlsim.fit import FitMapping, FitData
from sbmlsim.plot import Axis, Figure
from sbmlsim.simulation import Timecourse, TimecourseSim
from sbmlutils.console import console
from pkdb_models.models.canagliflozin.experiments.base_experiment import CanagliflozinSimulationExperiment
from pkdb_models.models.canagliflozin.experiments.metadata import Tissue, Route, Dosing, ApplicationForm, Health, \
    Fasting, CanagliflozinMappingMetaData, Coadministration
from pkdb_models.models.canagliflozin.helpers import run_experiments


class Devineni2014(CanagliflozinSimulationExperiment):
    """Simulation experiment of Devineni2014."""

    bodyweight = 75.6  # [kg]
    fpg = 5  # mM (healthy)

    info = {'can300': "CAN300", 'can300_hctz25': "CAN300_HCTZ25"}


    def datasets(self) -> Dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig2", "Tab2A"]:
            df = load_pkdb_dataframe(f"{self.sid}_{fig_id}", data_path=self.data_path)
            for label, df_label in df.groupby("label"):
                dset = DataSet.from_df(df_label, self.ureg)

                # unit conversion to mole/l
                if label.startswith("canagliflozin_"):
                    dset.unit_conversion("mean", 1 / self.Mr.can)

                dsets[f"{label}"] = dset

        # console.print(dsets)
        # console.print(dsets.keys())
        return dsets

    def simulations(self) -> Dict[str, TimecourseSim]:
        Q_ = self.Q_
        tcsims = {}

        # multiple dose
        for sim in self.info.keys():
            tc0 = Timecourse(
                start=0,
                end=24 * 60,  # [min]
                steps=500,
                changes={
                    **self.default_changes(),
                    "PODOSE_can": Q_(300, "mg"),
                    "BW": Q_(self.bodyweight, "kg"),
                    "[KI__fpg]": Q_(self.fpg, "mM"),
                },
            )
            changes_multi = {
                "BW": Q_(self.bodyweight, "kg"),
                "[KI__fpg]": Q_(self.fpg, "mM"),
                "KI__glc_urine": Q_(0, "mmole"),  # reset UGE
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
                [tc0] + [tc1 for _ in range(5)] + [tc2],
                time_offset=-6 * 24 * 60,
            )

        return tcsims

    def fit_mappings(self) -> Dict[str, FitMapping]:

        mappings = {}

        for name, sid in [
            ('canagliflozin', '[Cve_can]'),
            ('glucose_cumulative_amount', 'KI__UGE'),
            ('glucose_renal_threshold', 'KI__RTG'),
        ]:

            for sim, group in self.info.items():

                coadministration = Coadministration.HCTZ if "HCTZ25" in group else Coadministration.NONE

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
                        self, task=f"task_po_{sim}_multi", xid="time", yid=sid,
                    ),
                    metadata=CanagliflozinMappingMetaData(
                        tissue=Tissue.URINE if "cumulative" in name else Tissue.PLASMA,
                        route=Route.PO,
                        application_form=ApplicationForm.TABLET,
                        dosing=Dosing.MULTIPLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.FASTED,
                        coadministration=coadministration
                    ),
                )

        # console.print(mappings)
        return mappings

    def figures(self) -> Dict[str, Figure]:
        return {
            **self.figure_multi(),
            **self.figure_uge(),
            **self.figure_rtg()
        }

    def figure_multi(self) -> Dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="can multi",
            name=f"{self.__class__.__name__} (Healthy)",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit=self.unit_time), legend=True)
        plots[0].set_yaxis(self.label_can, unit=self.unit_can)

        # simulation
        plots[0].add_data(
            task=f"task_po_can300_multi",
            xid="time",
            yid=f"[Cve_can]",
            label=f"300 mg PO",
            color="black",
        )

        # data
        for sim, group in self.info.items():
            color = "black" if group == "CAN300" else "tab:blue"
            label = "300 mg PO" if group == "CAN300" else "300 mg PO + HCTZ"

            plots[0].add_data(
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

    def figure_uge(self) -> Dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig_uge",
            name=f"{self.__class__.__name__} (Healthy)",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="day"), legend=True)
        plots[0].set_yaxis(self.label_uge, unit=self.unit_uge)

        # simulation
        plots[0].add_data(
            task=f"task_po_can300_multi",
            xid="time",
            yid=f"KI__UGE",
            label=f"300 mg PO",
            color="black",
        )

        # data
        for sim, group in self.info.items():
            color = "black" if group == "CAN300" else "tab:blue"
            label = "300 mg PO" if group == "CAN300" else "300 mg PO + HCTZ"

            plots[0].add_data(
                dataset=f"glucose_cumulative_amount_{group}",
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

    def figure_rtg(self) -> Dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig_rtg",
            name=f"{self.__class__.__name__} (Healthy)",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit=self.unit_time), legend=True)
        plots[0].set_yaxis(self.label_rtg, unit=self.unit_rtg)

        # simulation
        plots[0].add_data(
            task=f"task_po_can300_multi",
            xid="time",
            yid=f"KI__RTG",
            label=f"300 mg PO",
            color="black",
        )

        # data
        for sim, group in self.info.items():
            color = "black" if group == "CAN300" else "tab:blue"
            label = "300 mg PO" if group == "CAN300" else "300 mg PO + HCTZ"

            plots[0].add_data(
                dataset=f"glucose_renal_threshold_{group}",
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
    run_experiments(Devineni2014, output_dir=Devineni2014.__name__)

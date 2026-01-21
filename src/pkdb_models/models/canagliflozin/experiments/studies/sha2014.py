from typing import Dict

from sbmlsim.data import DataSet, load_pkdb_dataframe
from sbmlsim.fit import FitMapping, FitData
from sbmlutils.console import console

from pkdb_models.models.canagliflozin.experiments.base_experiment import (
    CanagliflozinSimulationExperiment,
)
from pkdb_models.models.canagliflozin.experiments.metadata import Tissue, Route, Dosing, ApplicationForm, Health, \
    Fasting, CanagliflozinMappingMetaData

from sbmlsim.plot import Axis, Figure
from sbmlsim.simulation import Timecourse, TimecourseSim

from pkdb_models.models.canagliflozin.helpers import run_experiments


class Sha2014(CanagliflozinSimulationExperiment):
    """Simulation experiment of Sha2014."""

    groups = {"PBO": 0, "PBO_K": 0, "CAN30": 30, "CAN30_K": 30, "CAN100": 100, "CAN200": 200, "CAN400": 400}

    bodyweights = {"PBO": 94.2, "PBO_K": 75.5, "CAN30": 88.9, "CAN30_K": 66.2, "CAN100": 66.2,
                   "CAN200": 92.2, "CAN400": 92.7, "CAN300_BID": 94.8}

    fpg = {"PBO": 11.2, "PBO_K": 10.7, "CAN30": 11.1, "CAN30_K": 9.9, "CAN100": 10.3, "CAN200": 11.2,
           "CAN400": 11.6, "CAN300_BID": 10.3}  # mM (T2DM)

    gfr = {"PBO": 98.8, "PBO_K": 77.5, "CAN30": 96.9, "CAN30_K": 77.8, "CAN100": 102.4, "CAN200": 92,
           "CAN400": 104.1, "CAN300_BID": 103.6}  # [ml/min/1.73*m^2]

    def datasets(self) -> Dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig2", "Fig4", "Tab2A"]:
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

        # multiple dose (single daily)
        for group, dose in self.groups.items():
            tc0 = Timecourse(
                start=0,
                end=48 * 60,  # [min]
                steps=500,
                changes={
                    **self.default_changes(),
                    "BW": Q_(self.bodyweights[group], "kg"),
                    "[KI__fpg]": Q_(self.fpg[group], "mM"),
                    "KI__f_renal_function": Q_(self.gfr[group] / 100, "dimensionless"),  # [0, 1]  <=> [0, 100] gfr
                    "PODOSE_can": Q_(dose, "mg"),
                },
            )
            tc1 = Timecourse(
                start=0,
                end=24 * 60,  # [min]
                steps=500,
                changes={
                    "BW": Q_(self.bodyweights[group], "kg"),
                    "[KI__fpg]": Q_(self.fpg[group], "mM"),
                    "KI__f_renal_function": Q_(self.gfr[group] / 100, "dimensionless"),  # [0, 1]  <=> [0, 100] gfr
                    "KI__glc_urine": Q_(0, "mmole"),  # reset UGE
                    "PODOSE_can": Q_(dose, "mg"),
                },
            )
            tc2 = Timecourse(
                start=0,
                end=72 * 60,  # [min]
                steps=500,
                changes={
                    "BW": Q_(self.bodyweights[group], "kg"),
                    "[KI__fpg]": Q_(self.fpg[group], "mM"),
                    "KI__f_renal_function": Q_(self.gfr[group] / 100, "dimensionless"),  # [0, 1]  <=> [0, 100] gfr
                    "KI__glc_urine": Q_(0, "mmole"),  # reset UGE
                    "PODOSE_can": Q_(dose, "mg"),
                },
            )
            tcsims[f"po_can{dose}_multi"] = TimecourseSim(
                [tc0] + [tc1 for _ in range(14)] + [tc2],
                time_offset=-16 * 24 * 60,
            )

            # multiple dose (twice daily)
            dose = 300  # [mg]
            tc0 = Timecourse(
                start=0,
                end=12 * 60,  # [min]
                steps=500,
                changes={
                    **self.default_changes(),
                    "BW": Q_(self.bodyweights[group], "kg"),
                    "[KI__fpg]": Q_(self.fpg[group], "mM"),
                    "KI__f_renal_function": Q_(self.gfr[group] / 100, "dimensionless"),  # [0, 1]  <=> [0, 100] gfr
                    "PODOSE_can": Q_(dose, "mg"),
                },
            )
            tc1 = Timecourse(
                start=0,
                end=36 * 60,  # [min]
                steps=500,
                changes={
                    "BW": Q_(self.bodyweights[group], "kg"),
                    "[KI__fpg]": Q_(self.fpg[group], "mM"),
                    "KI__f_renal_function": Q_(self.gfr[group] / 100, "dimensionless"),  # [0, 1]  <=> [0, 100] gfr
                    "PODOSE_can": Q_(dose, "mg"),
                },
            )
            tc2 = Timecourse(
                start=0,
                end=12 * 60,  # [min]
                steps=500,
                changes={
                    "BW": Q_(self.bodyweights[group], "kg"),
                    "[KI__fpg]": Q_(self.fpg[group], "mM"),
                    "KI__f_renal_function": Q_(self.gfr[group] / 100, "dimensionless"),  # [0, 1]  <=> [0, 100] gfr
                    "KI__glc_urine": Q_(0, "mmole"),  # reset UGE
                    "PODOSE_can": Q_(dose, "mg"),
                },
            )
            tc3 = Timecourse(
                start=0,
                end=72 * 60,  # [min]
                steps=500,
                changes={
                    "BW": Q_(self.bodyweights[group], "kg"),
                    "[KI__fpg]": Q_(self.fpg[group], "mM"),
                    "KI__f_renal_function": Q_(self.gfr[group] / 100, "dimensionless"),  # [0, 1]  <=> [0, 100] gfr
                    "KI__glc_urine": Q_(0, "mmole"),  # reset UGE
                    "PODOSE_can": Q_(dose, "mg"),
                },
            )
            tcsims[f"po_can{dose}_BID_multi"] = TimecourseSim(
                [tc0] + [tc1] + [tc2 for _ in range(28)] + [tc3],
                time_offset=-16 * 24 * 60,
            )

        return tcsims

    def fit_mappings(self) -> Dict[str, FitMapping]:

        mappings = {}

        for name, sid in [
            # ('glucose_cumulative_amount', 'KI__UGE'),
            ('glucose_renal_threshold', 'KI__RTG'),
        ]:

            for group, dose in self.groups.items():
                mappings[f"task_po_can{dose}_{name}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=f"{name}_{group}",
                        xid="time",
                        yid="value" if "cumulative" in name else "mean",
                        yid_sd="mean_sd",
                        count="count",
                    ),
                    observable=FitData(
                        self, task=f"task_po_can{dose}_multi", xid="time", yid=sid,
                    ),
                    metadata=CanagliflozinMappingMetaData(
                        tissue=Tissue.URINE if "cumulative" in name else Tissue.PLASMA,
                        route=Route.PO,
                        application_form=ApplicationForm.TABLET,
                        dosing=Dosing.MULTIPLE,
                        health=Health.T2DM,
                        fasting=Fasting.FASTED,
                    ),
                )

        for name, sid in [
            # ('glucose_cumulative_amount', 'KI__UGE'),
            ('glucose_renal_threshold', 'KI__RTG'),
        ]:

            dose = 300
            mappings[f"task_po_can{dose}_{name}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"{name}_CAN300_BID",
                    xid="time",
                    yid="value" if "cumulative" in name else "mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self, task=f"task_po_can{dose}_BID_multi", xid="time", yid=sid,
                ),
                metadata=CanagliflozinMappingMetaData(
                    tissue=Tissue.URINE if "cumulative" in name else Tissue.PLASMA,
                    route=Route.PO,
                    application_form=ApplicationForm.SOLUTION,
                    dosing=Dosing.MULTIPLE,
                    health=Health.T2DM,
                    fasting=Fasting.FASTED,
                ),
            )

        # console.print(mappings)
        return mappings

    def figures(self) -> Dict[str, Figure]:
        return {
            **self.figure_uge(),
            **self.figure_uge_bid(),
            **self.figure_rtg()
        }

    def figure_uge(self) -> Dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig_uge",
            name=f"{self.__class__.__name__} (T2DM)",
        )
        Figure.legend_fontsize = 9
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="day"), legend=True)
        plots[0].set_yaxis(self.label_uge, unit=self.unit_uge)

        for group, dose in self.groups.items():
            # simulation
            plots[0].add_data(
                task=f"task_po_can{dose}_multi",
                xid="time",
                yid=f"KI__UGE",
                label=f"{dose} mg PO",
                color=self.dose_colors[dose],
            )

        for group, dose in self.groups.items():
            # data
            plots[0].add_data(
                dataset=f"glucose_cumulative_amount_{group}",
                xid="time",
                yid="value",
                yid_sd="mean_sd",
                count="count",
                label=f"{dose} mg PO",
                color=self.dose_colors[dose],
                linestyle=""
            )

        return {
            fig.sid: fig,
        }

    def figure_uge_bid(self) -> Dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig_uge_bid",
            name=f"{self.__class__.__name__} (T2DM)",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="day"), legend=True)
        plots[0].set_yaxis(self.label_uge, unit=self.unit_uge)

        plots[0].add_data(
            task=f"task_po_can300_BID_multi",
            xid="time",
            yid=f"KI__UGE",
            label=f"300 mg PO BID",
            color=self.dose_colors[300],
        )

        plots[0].add_data(
            dataset=f"glucose_cumulative_amount_CAN300_BID",
            xid="time",
            yid="value",
            yid_sd="mean_sd",
            count="count",
            label=f"300 mg PO BID",
            color=self.dose_colors[300],
            linestyle=""
        )

        return {
            fig.sid: fig,
        }

    def figure_rtg(self) -> Dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig_rtg",
            name=f"{self.__class__.__name__} (T2DM)",
        )
        Figure.legend_fontsize=9
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="day"), legend=True)
        plots[0].set_yaxis(self.label_rtg, unit=self.unit_rtg)

        for group, dose in self.groups.items():
            # simulation
            plots[0].add_data(
                task=f"task_po_can{dose}_multi",
                xid="time",
                yid=f"KI__RTG",
                label=f"{dose} mg PO",
                color=self.dose_colors[dose],
            )

        plots[0].add_data(
            task=f"task_po_can300_BID_multi",
            xid="time",
            yid=f"KI__RTG",
            label=f"300 mg PO BID",
            color=self.dose_colors[300],
            linestyle="--",
        )

        for group, dose in self.groups.items():
            # data
            plots[0].add_data(
                dataset=f"glucose_renal_threshold_{group}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"{dose} mg PO",
                color=self.dose_colors[dose],
                linestyle="",
            )

        plots[0].add_data(
            dataset=f"glucose_renal_threshold_CAN300_BID",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label=f"300 mg PO BID",
            color=self.dose_colors[300],
            linestyle="",
        )

        return {
            fig.sid: fig,
        }


if __name__ == "__main__":
    run_experiments(Sha2014, output_dir=Sha2014.__name__)

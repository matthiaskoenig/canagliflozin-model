from typing import Dict
from sbmlsim.data import DataSet, load_pkdb_dataframe
from sbmlsim.fit import FitMapping, FitData
from sbmlsim.plot import Axis, Figure
from sbmlsim.simulation import Timecourse, TimecourseSim
from sbmlutils.console import console
from pkdb_models.models.canagliflozin.experiments.base_experiment import CanagliflozinSimulationExperiment
from pkdb_models.models.canagliflozin.experiments.metadata import Tissue, Route, Dosing, ApplicationForm, Health, \
    Fasting, CanagliflozinMappingMetaData
from pkdb_models.models.canagliflozin.helpers import run_experiments


class Devineni2012(CanagliflozinSimulationExperiment):
    """Simulation experiment of Devineni2012."""

    bodyweights = {0: 95.1, 100: 107.8, 300: 94.1}
    fpg = {0: 8.7, 100: 9, 300: 9.6}

    interventions = {"CAN0": 0, "QD100": 100, "BID300": 300}

    def datasets(self) -> Dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1", "Fig3", "Tab3A"]:
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

        # multiple dose (placebo)
        dose = 0  # [mg]
        tcsims[f"po_can0_multi"] = TimecourseSim(
            Timecourse(
                start=0,
                end=29*24 * 60,  # [min]
                steps=500,
                changes={
                    **self.default_changes(),
                    "BW": Q_(self.bodyweights[dose], "kg"),
                    "[KI__fpg]": Q_(self.fpg[dose], "mM"),
                    "PODOSE_can": Q_(dose, "mg"),
                },
            ),
            time_offset = -26 * 24 * 60,
        )

        # multiple dose (single daily)
        dose = 100  # [mg]
        tc0 = Timecourse(
            start=0,
            end=24 * 60,  # [min]
            steps=500,
            changes={
                **self.default_changes(),
                "BW": Q_(self.bodyweights[dose], "kg"),
                "[KI__fpg]": Q_(self.fpg[dose], "mM"),
                "PODOSE_can": Q_(dose, "mg"),
            },
        )
        tc1 = Timecourse(
            start=0,
            end=24 * 60,  # [min]
            steps=500,
            changes={
                "BW": Q_(self.bodyweights[dose], "kg"),
                "[KI__fpg]": Q_(self.fpg[dose], "mM"),
                "KI__glc_urine": Q_(0, "mmole"),  # reset UGE
                "PODOSE_can": Q_(dose, "mg"),
            },
        )
        tc2 = Timecourse(
            start=0,
            end=48 * 60,  # [min]
            steps=500,
            changes={
                "BW": Q_(self.bodyweights[dose], "kg"),
                "[KI__fpg]": Q_(self.fpg[dose], "mM"),
                "KI__glc_urine": Q_(0, "mmole"),  # reset UGE
                "PODOSE_can": Q_(dose, "mg"),
            },
        )
        tcsims[f"po_can{dose}_multi"] = TimecourseSim(
            [tc0] + [tc1 for _ in range(25)] + [tc2],
            time_offset=-26 * 24 * 60,
        )

        # multiple dose (twice daily)
        dose = 300  # [mg]
        tc0 = Timecourse(
            start=0,
            end=12 * 60,  # [min]
            steps=500,
            changes={
                **self.default_changes(),
                "BW": Q_(self.bodyweights[dose], "kg"),
                "[KI__fpg]": Q_(self.fpg[dose], "mM"),
                "PODOSE_can": Q_(dose, "mg"),
            },
        )
        tc1 = Timecourse(
            start=0,
            end=12 * 60,  # [min]
            steps=500,
            changes={
                "BW": Q_(self.bodyweights[dose], "kg"),
                "[KI__fpg]": Q_(self.fpg[dose], "mM"),
                "KI__glc_urine": Q_(0, "mmole"),  # reset UGE
                "PODOSE_can": Q_(dose, "mg"),
            },
        )
        tc2 = Timecourse(
            start=0,
            end=48 * 60,  # [min]
            steps=500,
            changes={
                # "KI__glc_urine": Q_(0, "mmole"),  # no reset UGE on last 12hr dose
                "BW": Q_(self.bodyweights[dose], "kg"),
                "[KI__fpg]": Q_(self.fpg[dose], "mM"),
                "PODOSE_can": Q_(dose, "mg"),
            },
        )
        tcsims[f"po_can{dose}_multi"] = TimecourseSim(
            [tc0] + [tc1 for _ in range(52)] + [tc2],
            time_offset=-26 * 24 * 60,
        )

        return tcsims

    def fit_mappings(self) -> Dict[str, FitMapping]:

        mappings = {}

        for name, sid in [
            ('canagliflozin', '[Cve_can]'),
        ]:
            for intervention, dose in self.interventions.items():
                if name == 'canagliflozin' and intervention == 'CAN0':
                    continue
                mappings[f"task_po_can{dose}_{name}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=f"{name}_{intervention}_d27",
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                    ),
                    observable=FitData(
                        self, task=f"task_po_can{dose}_multi", xid="time", yid=sid,
                    ),
                    metadata=CanagliflozinMappingMetaData(
                        tissue=Tissue.PLASMA,
                        route=Route.PO,
                        application_form=ApplicationForm.TABLET,
                        dosing=Dosing.MULTIPLE,
                        health=Health.T2DM,
                        fasting=Fasting.FASTED,
                    ),
                )

        for name, sid in [
            ('glucose_cumulative_amount', 'KI__UGE'),
            ('glucose_RT', 'KI__RTG'),
        ]:
            for intervention, dose in self.interventions.items():
                mappings[f"task_po_can{dose}_{name}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=f"{name}_{intervention}_d27",
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                    ),
                    observable=FitData(
                        self, task=f"task_po_can{dose}_multi", xid="time", yid=sid,
                    ),
                    metadata=CanagliflozinMappingMetaData(
                        tissue=Tissue.URINE,
                        route=Route.PO,
                        application_form=ApplicationForm.TABLET,
                        dosing=Dosing.MULTIPLE,
                        health=Health.T2DM,
                        fasting=Fasting.FASTED,
                    ),
                )

        return mappings

    def figures(self) -> Dict[str, Figure]:
        return {
            **self.figure_multi(),
            **self.figure_uge(),
            **self.figure_rtg(),
        }

    def figure_multi(self) -> Dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="multi",
            name=f"{self.__class__.__name__} (T2DM)",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit=self.unit_time, min=-48, max=50), legend=True)
        plots[0].set_yaxis(self.label_can, unit=self.unit_can)
        for intervention, dose in {'QD100': 100, 'BID300': 300}.items():
            # simulation
            plots[0].add_data(
                task=f"task_po_can{dose}_multi",
                xid="time",
                yid=f"[Cve_can]",
                label=f"{dose} mg PO",
                color=self.dose_colors[dose],
            )

            # data
            plots[0].add_data(
                dataset=f"canagliflozin_{intervention}_d27",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"{dose} mg PO",
                color=self.dose_colors[dose],
            )

        return {
            fig.sid: fig,
        }

    def figure_uge(self) -> Dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig_uge",
            name=f"{self.__class__.__name__} (T2DM)",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit=self.unit_time, min=-48, max=50), legend=True)
        plots[0].set_yaxis(self.label_uge, unit=self.unit_uge)

        for intervention, dose in self.interventions.items():
            # simulation
            plots[0].add_data(
                task=f"task_po_can{dose}_multi",
                xid="time",
                yid=f"KI__UGE",
                label=f"{dose} mg PO",
                color=self.dose_colors[dose],
            )

            # data
            plots[0].add_data(
                dataset=f"glucose_cumulative_amount_{intervention}_d27",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"{dose} mg PO",
                color=self.dose_colors[dose],
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
        Figure.legend_fontsize=10
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="day"), legend=True)
        plots[0].set_yaxis(self.label_rtg, unit=self.unit_rtg)

        for intervention, dose in self.interventions.items():
            # simulation
            plots[0].add_data(
                task=f"task_po_can{dose}_multi",
                xid="time",
                yid=f"KI__RTG",
                label=f"{dose} mg PO",
                color=self.dose_colors[dose],
            )

            # data
            plots[0].add_data(
                dataset=f"glucose_RT_{intervention}_d27",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"{dose} mg PO",
                color=self.dose_colors[dose],
                linestyle=""
            )

        return {
            fig.sid: fig,
        }


if __name__ == "__main__":
    run_experiments(Devineni2012, output_dir=Devineni2012.__name__)
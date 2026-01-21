"""Sensitivity analysis."""
from __future__ import annotations

import dill
import numpy as np
import pandas as pd
import roadrunner
from roadrunner._roadrunner import NamedArray

from sbmlsim.sensitivity.analysis import (
    SensitivitySimulation,
    SensitivityOutput,
    LocalSensitivityAnalysis,
    SobolSensitivityAnalysis,
    SamplingSensitivityAnalysis, AnalysisGroup,
)

from sbmlsim.sensitivity.parameters import (
    SensitivityParameter,
    parameters_for_sensitivity_analysis, ParameterType,
)
from sbmlutils.console import console
from pkdb_analysis.pk.pharmacokinetics import TimecoursePK
from pint import UnitRegistry


class CanagliflozinSensitivitySimulation(SensitivitySimulation):
    """Simulation for sensitivity calculation."""


    def simulate(self, r: roadrunner.RoadRunner, changes: dict[str, float]) -> dict[str, float]:
        tend = 20 * 24 * 60  # [min]
        steps = 3000

        # apply changes and simulate
        all_changes = {
            **self.changes_simulation,  # model
            **changes  # sensitivity
        }
        self.apply_changes(r, all_changes, reset_all=True)
        # ensure tolerances
        r.integrator.setValue("absolute_tolerance", self.init_tolerances)
        try:
            s: NamedArray = r.simulate(start=0, end=tend, steps=steps)
        except RuntimeError as err:
            console.rule("CVODE integration error", style="error")
            console.print(all_changes, style="error")
            console.print(str(err), style="error")
            console.rule(style="error")
            raise err

        # pharmacokinetic parameters
        y: dict[str, float] = {}

        # pharmacokinetics
        ureg = UnitRegistry()
        Q_ = ureg.Quantity

        # losartan
        Mr_can = Q_(444.518, "g/mole")
        time = Q_(s["time"], "min")
        tcpk = TimecoursePK(
            time=time,
            concentration=Q_(s["[Cve_can]"], "mM"),
            substance="canagliflozin",
            ureg=ureg,
            dose=Q_(200, "mg")/Mr_can,
        )
        pk_dict = tcpk.pk.to_dict()
        # console.print(pk_dict)
        for pk_key in [
            "aucinf",
            "cmax",
            "thalf",
            "vd",
            "cl",
            "kel",
        ]:
            y[f"[Cve_can]_{pk_key}"] = pk_dict[pk_key]

        # M5, M7
        for sid in [
            "[Cve_m5]",
            "[Cve_m7]"
        ]:
            tcpk = TimecoursePK(
                time=time,
                concentration=Q_(s[sid], "mM"),
                substance="canagliflozin",
                ureg=ureg,
                dose=None,
            )
            pk_dict = tcpk.pk.to_dict()
            # console.print(pk_dict)
            for pk_key in [
                "aucinf",
                "cmax",
                "thalf",
                "kel",
            ]:
                y[f"{sid}_{pk_key}"] = pk_dict[pk_key]

        # pharmacodynamics
        t_idx = np.argmin(np.abs(time - Q_(24 * 60, "min")))
        y["uge24"] = s["KI__UGE"][t_idx]

        return y

    @staticmethod
    def sensitivity_simulation() -> CanagliflozinSensitivitySimulation:
        sensitivity_simulation = CanagliflozinSensitivitySimulation(
            model_path=MODEL_PATH,
            selections=[
                "time",
                "[Cve_can]",
                "[Cve_m5]",
                "[Cve_m7]",
                "KI__UGE",
            ],
            changes_simulation = {
                # ! make sure all the changes from base-experiment are injected here !
                "PODOSE_can": 200,  # [mg]
                "f_cirrhosis": 0,  # [-]
                "KI__f_renal_function": 1.0,  # [-]
            },
            outputs=[
                # FIXME: auto-calculate units
                SensitivityOutput(uid='[Cve_can]_aucinf', name='CAN AUC∞', unit="mM*min"),
                SensitivityOutput(uid='[Cve_can]_cmax', name='CAN Cmax', unit="mM"),
                SensitivityOutput(uid='[Cve_can]_thalf', name='CAN Half-life', unit="min"),
                SensitivityOutput(uid='[Cve_can]_vd', name='CAN Vd', unit="l"),
                SensitivityOutput(uid='[Cve_can]_cl', name='CAN CL', unit="mole/min/mM"),
                SensitivityOutput(uid='[Cve_can]_kel', name='CAN kel', unit="1/min"),

                SensitivityOutput(uid='[Cve_m5]_aucinf', name='M5 AUC∞', unit="mM*min"),
                SensitivityOutput(uid='[Cve_m5]_cmax', name='M5 Cmax', unit="mM"),
                SensitivityOutput(uid='[Cve_m5]_thalf', name='M5 Half-life', unit="min"),
                SensitivityOutput(uid='[Cve_m5]_kel', name='M5 kel', unit="1/min"),

                SensitivityOutput(uid='[Cve_m7]_aucinf', name='M7 AUC∞', unit="mM*min"),
                SensitivityOutput(uid='[Cve_m7]_cmax', name='M7 Cmax', unit="mM"),
                SensitivityOutput(uid='[Cve_m7]_thalf', name='M7 Half-life', unit="min"),
                SensitivityOutput(uid='[Cve_m7]_kel', name='M7 kel', unit="1/min"),

                SensitivityOutput(uid='uge24', name='UGE (24 hr)', unit="g"),
            ]
        )
        console.rule("Outputs", style="white")
        console.print(sensitivity_simulation.outputs)

        return sensitivity_simulation

    def sensitivity_parameters(self) -> list[SensitivityParameter]:
        """Definition of parameters and bounds for sensitivity analysis."""
        console.rule("Parameters", style="white")
        # parameters for sensitivity analysis
        parameters: list[SensitivityParameter] = parameters_for_sensitivity_analysis(
            sbml_path=self.model_path,
            exclude_ids={
                # conversion factors
                "conversion_min_per_day",
                "KI__cf_mg_per_g",
                "KI__cf_ml_per_l",

                # molecular weights
                "Mr_can",
                "Mr_m5",
                "Mr_m7",
                "KI__Mr_glc",

                # unchangable values
                "FQlu",
                "FVhv",
                "FVpo",
                "GFR_healthy",

                # dosing parameters
                "PODOSE_can",
                "ti_can",

                # unused volumes
                "Vurine",
                "Vfeces",
                "Vplasma",
                "Vstomach",
                "LI__Vbi",
                "GU__Vstomach",
            },
            exclude_na=True,
            exclude_zero=True,
        )

        # bounds from fitted parameters
        from pkdb_models.models.canagliflozin.fitting.parameters import parameters_all as fit_parameters
        fit_bounds = [
            (fp.pid, fp.lower_bound, fp.upper_bound, ParameterType.FIT) for fp in fit_parameters
        ]
        SensitivityParameter.parameters_set_bounds(parameters, bounds=fit_bounds)

        # bounds from scaled parameters
        bounds_fraction = 0.15  # fraction of bounds relative to value
        uids_scaling = [
            "GU__f_absorption",
            "KI__f_renal_function",
            "KI__f_ugt1a9",
            "LI__f_ugt1a9",
            "LI__f_ugt2b4",
            "LI__f_cyp3a4",
        ]
        scaling_bounds = [
            (uid, 1 - bounds_fraction, 1 + bounds_fraction, ParameterType.SCALING) for uid in uids_scaling
        ]
        SensitivityParameter.parameters_set_bounds(parameters, bounds=scaling_bounds)

        # references for values
        reference_data={
            "HCT": r"\cite{Mondal2025, Fiseha2023}",
            "BW": r"\cite{Ogden2004, Jones2013, Thompson2009, Brown1997}",
            "FQgu": r"\cite{Jones2013, Thompson2009, Brown1997}",
            "FQh": r"\cite{Jones2013, Wynne1989, Thompson2009, Brown1997}",
            "FQki": r"\cite{Jones2013, Thompson2009, Brown1997}",
            "FVar": r"\cite{Jones2013, Thompson2009, Brown1997}",
            "FVgu": r"\cite{Jones2013, Thompson2009, Brown1997}",
            "FVki": r"\cite{Jones2013, Thompson2009, Brown1997}",
            "FVli": r"\cite{Jones2013, Wynne1989, Thompson2009, Brown1997}",
            "FVlu": r"\cite{Jones2013, Thompson2009, Brown1997}",
            "FVve": r"\cite{Jones2013, Thompson2009, Brown1997}",
            "COBW": r"\cite{Cattermole2017, Patel2021, Collis2001}",
            "KI__f_renal_function": r"\cite{Stevens2024}",
            # "LI__f_cyp2c9": r"\cite{Kusama2009, Wang2014, Maekawa2009}",
        }
        p_dict = {p.uid: p for p in parameters}
        for pid, reference in reference_data.items():
            p = p_dict[pid]
            p.reference = reference
            if p.type == ParameterType.NA:
                p.type = ParameterType.DATA

        # setting missing bounds;
        for p in parameters:
            if np.isnan(p.lower_bound) and np.isnan(p.upper_bound):
                p.lower_bound = p.value * (1 - bounds_fraction)
                p.upper_bound = p.value * (1 + bounds_fraction)

        # print parameters
        pd.options.display.float_format = "{:.5g}".format
        df_parameters = SensitivityParameter.parameters_to_df(parameters)
        console.print(df_parameters)

        return parameters

    def sensitivity_groups(self) -> list[AnalysisGroup]:
        groups = [
            AnalysisGroup(
                uid="control",
                name="Control",
                changes={},
                color="dimgrey",
            ),
            AnalysisGroup(
                uid="mildRI",
                name="Mild renal impairment",
                changes={"KI__f_renal_function": 0.69},
                color="#66c2a4",
            ),
            AnalysisGroup(
                uid="modRI",
                name="Moderate renal impairment",
                changes={"KI__f_renal_function": 0.32},
                color="#2ca25f",
            ),
            AnalysisGroup(
                uid="sevRI",
                name="Severe renal impairment",
                changes={"KI__f_renal_function": 0.19},
                color="#006d2c",
            ),
            AnalysisGroup(
                uid="CPT A",
                name="Mild cirrhosis (CPT A)",
                changes={"f_cirrhosis": 0.399},
                color="#74a9cf",
            ),
            AnalysisGroup(
                uid="CPT B",
                name="Moderate cirrhosis (CPT B)",
                changes={"f_cirrhosis": 0.698},
                color="#2b8cbe",
            ),
            AnalysisGroup(
                uid="CPT C",
                name="Severe cirrhosis (CPT C)",
                changes={"f_cirrhosis": 0.813},
                color="#045a8d",
            )
        ]
        return groups


def local_sensitivity_analysis():
    """Local sensitivity analysis"""
    console.rule("LOCAL SENSITIVITY ANALYSIS", style="blue bold", align="center")

    sensitivity_simulation = CanagliflozinSensitivitySimulation.sensitivity_simulation()
    parameters = sensitivity_simulation.sensitivity_parameters()
    groups = sensitivity_simulation.sensitivity_groups()
    sa = LocalSensitivityAnalysis(
        sensitivity_simulation=sensitivity_simulation,
        parameters=parameters,
        groups=groups,
        results_path=RESULTS_PATH / "sensitivity",
        seed=1234,
        difference=0.01,  # 1% change
    )

    console.rule("Samples", style="white")
    sa.create_samples()

    console.rule("Results", style="white")
    sa.simulate_samples()
    console.print(sa.results)

    console.rule("Sensitivity", style="white")
    sa.calculate_sensitivity()
    console.print(sa.sensitivity)

    console.rule("Plotting", style="white")
    for kg, group in enumerate(sa.groups):
        sa.plot_sensitivity(
            group_id=group.uid,
            sensitivity_key="normalized",
            # title=f"{group.name}",
            cutoff=0.05,
            cluster_rows = False,
            cmap = "seismic",
            vcenter=0.0,
            vmin=-2.0,
            vmax=2.0,
            fig_path=sa.results_path / f"local_sensitivity_{kg:>02}_{group.uid}_{sa.difference}.png",
        )

def sampling_sensitivity_analysis():
    """Sampling sensitivity/uncertainty analysis"""

    console.rule("SAMPLING SENSITIVITY ANALYSIS", style="blue bold", align="center")
    sensitivity_simulation = CanagliflozinSensitivitySimulation.sensitivity_simulation()
    parameters = sensitivity_simulation.sensitivity_parameters()
    groups = sensitivity_simulation.sensitivity_groups()

    sa = SamplingSensitivityAnalysis(
        sensitivity_simulation=sensitivity_simulation,
        parameters=parameters,
        results_path=RESULTS_PATH / "sensitivity",
        N=1000,
        seed=1234,
        groups=groups,
    )

    console.rule("Samples", style="white")
    sa.create_samples()
    console.print(sa.samples)

    console.rule("Results", style="white")
    cache_results: bool = True
    results_path = sa.results_path / f"sampling_sensitivity_N{sa.N}_results.pkl"
    if not cache_results or (cache_results and not results_path.exists()):
        sa.simulate_samples()
        with open(results_path, 'wb') as f:
            dill.dump(sa.results, f)
    else:
        with open(results_path, 'rb') as f:
            sa.results = dill.load(f)

    console.print(sa.results)

    console.rule("Sensitivity", style="white")
    sa.calculate_sensitivity()
    console.print(sa.sensitivity)

    sa.df_sampling_sensitivity(
        df_path=sa.results_path / f"sampling_sensitivity_N{sa.N}_statistics.tsv"
    )

    console.rule("Plotting", style="white")
    sa.plot_sampling_sensitivity(
        fig_path=sa.results_path / f"sampling_sensitivity_N{sa.N}.png",
    )


def global_sensitivity_analysis():
    """Global sensitivity analysis."""

    console.rule("GLOBAL SENSITIVITY ANALYSIS", style="blue bold", align="center")
    sensitivity_simulation = CanagliflozinSensitivitySimulation.sensitivity_simulation()
    parameters = sensitivity_simulation.sensitivity_parameters()
    groups = sensitivity_simulation.sensitivity_groups()
    # only analysis on control group
    groups = [g for g in groups if g.uid == "control"]

    sa = SobolSensitivityAnalysis(
        sensitivity_simulation=sensitivity_simulation,
        parameters=parameters,
        groups=groups,
        results_path=RESULTS_PATH / "sensitivity",
        # N=4096,
        N=16,
        seed=1234,
    )

    console.rule("Samples", style="white")
    sa.create_samples()
    console.print(sa.samples)

    # FIXME: abstract caching
    console.rule("Results", style="white")
    cache_results: bool = True
    results_path = sa.results_path / f"sobol_sensitivity_N{sa.N}_results.pkl"
    if not cache_results or (cache_results and not results_path.exists()):
        sa.simulate_samples()
        with open(results_path, 'wb') as f:
            dill.dump(sa.results, f)
    else:
        with open(results_path, 'rb') as f:
            sa.results = dill.load(f)

    console.print(sa.results)

    console.rule("Sensitivity", style="white")
    cache_sensitivity: bool = True
    sensitivity_path = sa.results_path / f"sobol_sensitivity_N{sa.N}.pkl"
    if not cache_sensitivity or (cache_sensitivity and not sensitivity_path.exists()):
        sa.calculate_sensitivity()
        with open(sensitivity_path, 'wb') as f:
            dill.dump(sa.sensitivity, f)
    else:
        with open(sensitivity_path, 'rb') as f:
            sa.sensitivity = dill.load(f)

    console.print(sa.sensitivity)

    console.rule("Plotting", style="white")
    # Heatmaps
    for kg, group in enumerate(sa.groups):
        for key in ["ST", "S1"]:
            sa.plot_sensitivity(
                group_id=group.uid,
                sensitivity_key=key,
                # title=f"{key} {group.name}",
                cutoff=0.05,
                cluster_rows=False,
                cmap="viridis",
                vcenter=0.5,
                vmin=0.0,
                vmax=1.0,
                fig_path=sa.results_path / f"sobol_sensitivity_N{sa.N}_{kg:>02}_{group.uid}_{key}.png"
            )

        # Barplots
        sa.plot_sobol_indices(
            fig_path=sa.results_path / f"sobol_sensitivity_N{sa.N}_{kg:>02}_{group.uid}.png",
        )



def parameter_table():
    console.rule("PARAMETER TABLE", style="blue bold", align="center")
    sensitivity_simulation = CanagliflozinSensitivitySimulation.sensitivity_simulation()
    parameters = sensitivity_simulation.sensitivity_parameters()
    tex_path = RESULTS_PATH / "sensitivity" / "parameter_table.tex"
    df = SensitivityParameter.parameters_to_df(parameters)
    tex_str = df.to_latex(
        None, index=False, float_format="{:.3g}".format
    )
    tex_str = tex_str.replace("_", r"\_")

    with open(tex_path, 'w') as f:
        f.write(tex_str)


if __name__ == "__main__":

    # requires the `sbmlsim2` branch of https://github.com/matthiaskoenig/sbmlsim.git
    # install with
    # cd sbmlsim
    # git checkout sbmlsim2
    # (pkdb_models) uv pip install -e ../sbmlsim

    # FIXME: add a flag to control resources for parallelization (ncores)

    from pkdb_models.models.canagliflozin import MODEL_PATH, RESULTS_PATH

    results_path = RESULTS_PATH / "sensitivity"
    results_path.mkdir(parents=True, exist_ok=True)

    # parameters
    parameter_table()

    # sensitivity analysis
    # local_sensitivity_analysis()
    # sampling_sensitivity_analysis()
    global_sensitivity_analysis()




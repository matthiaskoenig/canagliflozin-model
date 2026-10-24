"""Sensitivity analysis of the canagliflozin model.

The outputs are the pharmacokinetic parameters of a single oral dose of
canagliflozin and its metabolites M5 and M7 (the non-compartmental analysis of
`pkpdutils`) and the urinary glucose excretion after 24 hr. The parameters are
the parameters of the model with bounds of +-15 % around their value. The
analyses are run as a script, the local analysis by default:

    python -m pkdb_models.models.canagliflozin.sensitivity.sensitivity_analysis
    python -m pkdb_models.models.canagliflozin.sensitivity.sensitivity_analysis local sampling

The analyses run on `pkpdsim.sensitivity.SensitivityRunner`, which writes the
table of the parameters into `results/sensitivity` of the model and the tables
and figures of an analysis into `results/sensitivity/<analysis>`. An analysis
does not vary a parameter which one of its groups sets
(`pkpdsim.sensitivity.free_parameters`): the analyses over the groups leave out
`KI__f_renal_function` (`f_cirrhosis`, 0 in the model, is no parameter of the
analyses). The environment variable `PKPDSIM_SENSITIVITY_N` replaces the
numbers of samples of the global analyses for a quick run, see
`pkpdsim.sensitivity.sample_size`.

The model without canagliflozin is stationary, so the simulation of a group
starts with the dose. The dose is followed for `END_HR` hours, the sampling of
the studies (72-96 hr) and longer.
"""

from collections.abc import Mapping

import numpy as np
from pkpdsim.sensitivity import (
    FastAnalysis,
    LocalAnalysis,
    ParameterType,
    SamplingAnalysis,
    SensitivityGroup,
    SensitivityOutput,
    SensitivityParameter,
    SensitivityRunner,
    SobolAnalysis,
    parameters_from_sbml,
    set_bounds,
    set_relative_bounds,
)
from pkpdutils import NCAOptions
from sbmlsim import Q
from sbmlsim.simulation import PK, Formula, Observable, Simulation

from pkdb_models.models.canagliflozin import MODEL, MODEL_PATH
from pkdb_models.models.canagliflozin.experiments.base_experiment import (
    CanagliflozinSimulationExperiment,
)
from pkdb_models.models.canagliflozin.fitting.parameters import (
    parameters_all as fit_parameters,
)

#: oral dose of the analysis [mg]
DOSE_CAN = 200
#: the hours after the dose
END_HR = 120
#: the limit of quantification of the non-compartmental analysis [mM], about
#: 1e-4 of the maximal plasma concentration of canagliflozin after 200 mg
#: (3.5e-3 mM) and of M5 and M7, so that the noise of the integrator is not
#: the terminal phase
LLOQ = 3e-7
#: fraction of the bounds of a parameter relative to its value
BOUNDS_FRACTION = 0.15

#: outputs of the non-compartmental analysis of canagliflozin -> unit of the output
PK_OUTPUTS_CAN: dict[str, str] = {
    "auc_inf_obs": "mM*min",
    "cmax": "mM",
    "thalf": "min",
    "vz_f": "l",
    "cl_f": "ml/min",
    "lambda_z": "1/min",
}
#: outputs of the non-compartmental analysis of the metabolites -> unit of the output
PK_OUTPUTS_METABOLITES: dict[str, str] = {
    "auc_inf_obs": "mM*min",
    "cmax": "mM",
    "thalf": "min",
    "lambda_z": "1/min",
}
#: the names of the pharmacokinetic parameters in the outputs
PK_NAMES: dict[str, str] = {
    "auc_inf_obs": "AUC∞",
    "cmax": "Cmax",
    "thalf": "Half-life",
    "vz_f": "Vz/F",
    "cl_f": "CL/F",
    "lambda_z": "λz",
}
#: the concentrations in plasma -> name and outputs of their parameters
SUBSTANCES: dict[str, tuple[str, dict[str, str]]] = {
    "[Cve_can]": ("CAN", PK_OUTPUTS_CAN),
    "[Cve_m5]": ("M5", PK_OUTPUTS_METABOLITES),
    "[Cve_m7]": ("M7", PK_OUTPUTS_METABOLITES),
}
#: the concentration of canagliflozin, the only substance with a dose
DOSED = "[Cve_can]"
#: the outputs whose unit has the amount of the dose: the dose is a mass
#: (`PODOSE_can` in mg), so they are divided by the molecular weight (its value
#: at the start, a value per simulation like the parameter of the analysis)
PK_PER_DOSE_MASS: frozenset[str] = frozenset({"vz_f", "cl_f"})
#: the time of the urinary glucose excretion [min], in the time unit of the
#: model as `at` requires
UGE_TIME = 24 * 60


def _pk_id(selection: str) -> str:
    """Get the id of the non-compartmental analysis of a concentration."""
    return f"pk_{selection.strip('[]')}"


def _pk_formula(selection: str, key: str) -> str:
    """Get the formula of a pharmacokinetic output of a concentration."""
    if key in PK_PER_DOSE_MASS:
        return f"{_pk_id(selection)}.{key} / at(Mr_can, 0)"
    return f"{_pk_id(selection)}.{key}"


#: the outputs: the id of a pharmacokinetic output names the concentration with
#: its brackets (`[Cve_can]_cmax`), as the tables of sbmlsim, its
#: observable has the id without them (`Cve_can_cmax`)
OUTPUTS: list[SensitivityOutput] = [
    *(
        SensitivityOutput(
            f"{sid}_{key}", f"{name} {PK_NAMES[key]}", f"{sid.strip('[]')}_{key}"
        )
        for sid, (name, outputs) in SUBSTANCES.items()
        for key in outputs
    ),
    SensitivityOutput("uge24", "UGE (24 hr)"),
]

#: the observables of a simulation, the outputs with their units: the clearance
#: and the volume need the dose of the substance, only canagliflozin has one
OBSERVABLES: list[Observable] = [
    *(
        PK(
            _pk_id(sid),
            sid,
            dose="PODOSE_can" if sid == DOSED else None,
            route="oral" if sid == DOSED else None,
            options=NCAOptions(lloq=LLOQ),
            parameters=list(outputs),
        )
        for sid, (_, outputs) in SUBSTANCES.items()
    ),
    *(
        Formula(f"{sid.strip('[]')}_{key}", _pk_formula(sid, key), unit=unit)
        for sid, (_, outputs) in SUBSTANCES.items()
        for key, unit in outputs.items()
    ),
    # the pharmacodynamics: the urinary glucose excretion after 24 hr
    Formula("uge24", f"at(KI__UGE, {UGE_TIME})", unit="g"),
]


#: the output times [hr]: every 0.02 hr in the first day after the dose
#: (absorption and maximum), every 0.5 hr after it
TIMES_HR: tuple[float, ...] = tuple(
    np.unique(
        np.concatenate(
            [
                np.linspace(0, 24, 1201),
                np.linspace(24, END_HR, 2 * (END_HR - 24) + 1),
            ]
        )
    ).tolist()
)


def sensitivity_simulation(changes: Mapping[str, float]) -> Simulation:
    """Get the simulation of a group: a single oral dose of canagliflozin at time 0."""
    return Simulation(
        start=0,
        end=END_HR,
        times=TIMES_HR,
        time_unit="hr",
        preinit_changes={**changes, "PODOSE_can": Q(DOSE_CAN, "mg")},
    )


_E = CanagliflozinSimulationExperiment

#: the groups the analyses are run for: the control and the classes of renal
#: impairment and of cirrhosis of the simulation experiments
SENSITIVITY_GROUPS: list[SensitivityGroup] = [
    SensitivityGroup("control", "Control", sensitivity_simulation({}), "dimgrey"),
    *(
        SensitivityGroup(
            uid,
            name,
            sensitivity_simulation({"KI__f_renal_function": _E.renal_map[name]}),
            _E.renal_colors[name],
        )
        for uid, name in [
            ("mildRI", "Mild renal impairment"),
            ("moderateRI", "Moderate renal impairment"),
            ("severeRI", "Severe renal impairment"),
        ]
    ),
    *(
        SensitivityGroup(
            uid,
            name,
            sensitivity_simulation({"f_cirrhosis": _E.cirrhosis_map[name]}),
            _E.cirrhosis_colors[name],
        )
        for uid, name in [
            ("mildCirrhosis", "Mild cirrhosis"),
            ("moderateCirrhosis", "Moderate cirrhosis"),
            ("severeCirrhosis", "Severe cirrhosis"),
        ]
    ),
]


def sensitivity_parameters() -> list[SensitivityParameter]:
    """Get the parameters of the analyses with their bounds and references."""
    parameters = parameters_from_sbml(
        MODEL_PATH,
        exclude_ids={
            # conversion factors
            "KI__cf_mg_per_g",
            # molecular weights
            "Mr_can",
            "Mr_m5",
            "Mr_m7",
            "KI__Mr_glc",
            # unchangeable values
            "BW_ref",
            "FQlu",
            "FVhv",
            "FVpo",
            "f_GFR_Qki",
            "KI__fpg_healthy",
            # the integrator of the mean RTG
            "KI__RTG_int",
            "KI__RTG_time",
            # dosing parameters
            "PODOSE_can",
            "ti_can",
            # unused volumes
            "Vurine",
            "Vfeces",
            "Vplasma",
            "Vstomach",
            "LI__Vbi",
        },
        exclude_na=True,
        exclude_zero=True,
    )

    # the fitted parameters, their bounds are set relative to the value below
    set_bounds(
        parameters,
        [(fp.pid, np.nan, np.nan, ParameterType.FIT) for fp in fit_parameters],
    )
    # the scaling factors of the organ functions and enzymes
    set_bounds(
        parameters,
        [
            (uid, 1 - BOUNDS_FRACTION, 1 + BOUNDS_FRACTION, ParameterType.SCALING)
            for uid in [
                "KI__f_renal_function",
                "f_ugt1a9",
                "LI__f_ugt2b4",
                "LI__f_cyp3a4",
                "KI__f_oat",
            ]
        ],
    )

    # the references of the values from the literature
    references = {
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
    }
    by_uid = {p.uid: p for p in parameters}
    for uid, reference in references.items():
        p = by_uid[uid]
        p.reference = reference
        if p.type == ParameterType.NA:
            p.type = ParameterType.DATA

    # every parameter without bounds varies around its value
    set_relative_bounds(parameters, BOUNDS_FRACTION)
    return parameters


#: the analyses of the script, with their groups and numbers of samples
SENSITIVITY = SensitivityRunner(
    model=MODEL,
    parameters=sensitivity_parameters,
    outputs=OUTPUTS,
    observables=OBSERVABLES,
    analyses={
        "local": LocalAnalysis(groups=SENSITIVITY_GROUPS, delta=0.01),
        "sampling": SamplingAnalysis(groups=SENSITIVITY_GROUPS, n=1000),
        "fast": FastAnalysis(groups=SENSITIVITY_GROUPS, n=1000),
        "sobol": SobolAnalysis(groups=SENSITIVITY_GROUPS[:1], n=4096),
    },
    default=("local",),
)


if __name__ == "__main__":
    SENSITIVITY.main()

"""Kidney model of canagliflozin: renal excretion, renal glucuronidation and glucose excretion."""

from sbmlutils.factory import (
    AssignmentRule,
    Compartment,
    Model,
    Parameter,
    RateRule,
    Reaction,
    Species,
    UnitDefinition,
    create_model,
)
from sbmlutils.metadata import (
    BQB,
    SBO,
)

from pkdb_models.models.canagliflozin.models import annotations, templates
from pkdb_models.models.canagliflozin.models.fits import FITS


class U(templates.U):
    """Units of the kidney model."""

    mg_per_g = UnitDefinition("mg_per_g", "mg/g")
    ml_per_min = UnitDefinition("ml_per_min", "ml/min")
    l_per_ml = UnitDefinition("l_per_ml", "l/ml")
    mM_min = UnitDefinition("mM_min", "mmole/l*min")


mid = "canagliflozin_kidney"

_m = Model(
    sid=mid,
    name="Model for the renal excretion of canagliflozin, M5 and M7 and the urinary glucose excretion.",
    notes="""
    Model for the renal excretion of canagliflozin, M5 and M7, the renal
    glucuronidation of canagliflozin to M7 and the urinary glucose excretion.

    - About 33 % of an oral dose is excreted in the urine, mainly as the
      O-glucuronides M5 (13.7 %) and M7 (18.2 %), unchanged canagliflozin
      < 0.5 % [Mamidi2014, Devineni2015b].
    - The renal excretion is relative to the glomerular filtration rate (GFR),
      canagliflozin is 99 % bound to plasma proteins, its renal clearance of
      0.8-1.4 ml/min is the filtration of its unbound fraction
      [Devineni2015c, Inagaki2014].
    - UGT1A9 of the kidney forms M7 [Francke2015]; the renal glucuronidation
      scales with the renal function, which makes the exposure of
      canagliflozin increase in renal impairment [Devineni2015c].
    - Canagliflozin lowers the renal threshold of glucose (RTG) by the
      inhibition of SGLT2; glucose above the RTG is excreted with the GFR.
    """
    + templates.terms_of_use,
    creators=templates.creators,
    units=U,
    model_units=templates.model_units,
    annotations=[
        *annotations.model,
        # tissue
        (BQB.OCCURS_IN, "fma/FMA:7203"),  # kidney
        (BQB.OCCURS_IN, "bto/BTO:0000671"),  # kidney
        (BQB.OCCURS_IN, "NCIT:C12415"),  # kidney
        (BQB.HAS_PROPERTY, "NCIT:C79372"),  # Pharmacokinetics: Excretion
        (BQB.HAS_PROPERTY, "NCIT:C79371"),  # Pharmacokinetics: Metabolism
    ],
)

_m.compartments = [
    Compartment(
        "Vext",
        value=1.5,
        unit=U.liter,
        name="plasma",
        constant=True,
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["plasma"],
        port=True,
    ),
    Compartment(
        "Vki",
        value=0.3,  # 0.4 % of bodyweight
        unit=U.liter,
        name="kidney",
        constant=True,
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["ki"],
        port=True,
    ),
    Compartment(
        "Vurine",
        1.0,
        name="urine",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        port=True,
        annotations=annotations.compartments["urine"],
    ),
]

# ---------------------------------------------------------------------------------------------------------------------
# Pharmacokinetics
# ---------------------------------------------------------------------------------------------------------------------
_m.species = [
    Species(
        "can_ext",
        name="canagliflozin (plasma)",
        initialConcentration=0.0,
        compartment="Vext",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["can"],
        port=True,
    ),
    Species(
        "can_urine",
        name="canagliflozin (urine)",
        initialConcentration=0.0,
        compartment="Vurine",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=True,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["can"],
        port=True,
    ),
    Species(
        "m5_ext",
        name="M5 (plasma)",
        initialConcentration=0.0,
        compartment="Vext",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["m5"],
        port=True,
    ),
    Species(
        "m5_urine",
        name="M5 (urine)",
        initialConcentration=0.0,
        compartment="Vurine",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=True,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["m5"],
        port=True,
    ),
    Species(
        "m7_ext",
        name="M7 (plasma)",
        initialConcentration=0.0,
        compartment="Vext",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["m7"],
        port=True,
    ),
    Species(
        "m7_urine",
        name="M7 (urine)",
        initialConcentration=0.0,
        compartment="Vurine",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=True,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["m7"],
        port=True,
    ),
    Species(
        "cantot_urine",
        name="total canagliflozin (urine)",
        initialConcentration=0.0,
        compartment="Vurine",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=True,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["cantot"],
        notes="""Canagliflozin, M5 and M7 in the urine, compared with the total
        radioactivity in the urine.""",
        port=True,
    ),
]

_m.parameters.extend(
    [
        Parameter(
            "f_renal_function",
            name="renal function",
            value=1.0,
            unit=U.dimensionless,
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            notes="""
            >1.0: increased kidney function
            1.0: normal kidney function (healthy control)
            <1.0: decreased kidney function

            Renal function relative to the healthy glomerular filtration rate
            GFR_base, which is 101 ml/min at 75 kg; a measured creatinine
            clearance or GFR of X ml/min is the renal function X/101. It scales
            the filtration (renal excretion, glucose excretion) and the renal
            glucuronidation (the functional renal mass).
            """,
        ),
        Parameter(
            "GFR_base",
            101,
            U.ml_per_min,
            name="glomerular filtration rate (healthy)",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            port=True,
        ),
        Parameter(
            "f_ugt1a9",
            1,
            U.dimensionless,
            name="scaling factor UGT1A9 activity",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            notes="""Scaling factor of the UGT1A9 activity of the kidney (and the
            liver, the parameter of the whole-body model replaces both).
            1.0: normal activity; <1.0 decreased activity; >1.0 increased activity.
            """,
            port=True,
        ),
        Parameter(
            "f_oat",
            1,
            U.dimensionless,
            name="scaling factor renal anion transport of the glucuronides",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            notes="""Scaling factor of the renal clearance of the glucuronides M5
            and M7, which are secreted by the organic anion transporters
            (OAT1/OAT3) of the proximal tubule. Probenecid, an inhibitor of
            OAT1/OAT3, lowers the renal clearance of M5 by 82 % and of M7 by 58 %
            [Devineni2015d]. 1.0: normal activity; <1.0 inhibited.
            """,
        ),
        Parameter(
            "fu_can",
            0.01,
            U.dimensionless,
            name="fraction unbound in plasma canagliflozin",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            notes="""Canagliflozin is 99 % bound to plasma proteins, mainly
            albumin, independent of the renal and hepatic function
            [Devineni2015c, Devineni2015b].""",
        ),
        Parameter(
            "CANEX_f",
            **FITS.parameter("KI__CANEX_f", unit=U.dimensionless),
            name="renal clearance of unbound canagliflozin relative to the GFR",
            sboTerm=SBO.KINETIC_CONSTANT,
            notes="""
            The renal clearance of canagliflozin is CANEX_f times the filtration
            of its unbound fraction, fu_can * GFR: 1 is filtration alone. The
            renal clearance of 0.8-1.4 ml/min [Chen2015, Inagaki2014,
            Devineni2015d] is about the filtration of the unbound fraction.
            """,
        ),
        Parameter(
            "M5EX_f",
            **FITS.parameter("KI__M5EX_f", unit=U.dimensionless),
            name="renal clearance of M5 relative to the GFR",
            sboTerm=SBO.KINETIC_CONSTANT,
            notes="""
            The renal clearance of M5 is M5EX_f times the GFR, 1.87 l/hr
            (31 ml/min) [Devineni2015d].
            """,
        ),
        Parameter(
            "M7EX_f",
            **FITS.parameter("KI__M7EX_f", unit=U.dimensionless),
            name="renal clearance of M7 relative to the GFR",
            sboTerm=SBO.KINETIC_CONSTANT,
            notes="""
            The renal clearance of M7 is M7EX_f times the GFR, 4.62 l/hr
            (77 ml/min) [Devineni2015d].
            """,
        ),
        Parameter(
            "CAN2M7_k",
            0.133,
            U.per_min,
            name="rate of the renal glucuronidation of canagliflozin to M7 (UGT1A9)",
            sboTerm=SBO.KINETIC_CONSTANT,
            notes="""
            First-order rate of the renal UGT1A9, relative to the volume of the
            kidney: canagliflozin is far below the Km of UGT1A9, its
            pharmacokinetics are dose proportional from 50 to 300 mg
            [Devineni2015e]. The renal share of the clearance is identified by
            the exposure in renal impairment [Devineni2015c].
            """,
        ),
    ]
)

_m.rules.extend(
    [
        AssignmentRule(
            "GFR",
            "f_renal_function * GFR_base",
            unit=U.ml_per_min,
            name="glomerular filtration rate",
        ),
        AssignmentRule(
            "cantot_urine",
            "can_urine + m5_urine + m7_urine",
            U.mmole,
            name="total canagliflozin (urine)",
        ),
    ]
)

_m.reactions = [
    Reaction(
        sid="CAN2M7",
        name="UGT1A9 (can -> m7)",
        equation="can_ext -> m7_ext",
        compartment="Vki",
        sboTerm=SBO.BIOCHEMICAL_REACTION,
        notes="""The glucuronidation of the canagliflozin of the renal plasma;
        the uptake into the tubular cells and the export of M7 are fast.""",
        formula=(
            "f_renal_function * f_ugt1a9 * CAN2M7_k * Vki * can_ext",
            U.mmole_per_min,
        ),
    ),
    Reaction(
        sid="CANEX",
        name="canagliflozin excretion (CANEX)",
        equation="can_ext -> can_urine",
        compartment="Vki",
        sboTerm=SBO.TRANSPORT_REACTION,
        # [ml/min] * [l/ml] * [-] * [-] * [mmole/l]
        formula=(
            "GFR * 0.001 l_per_ml * fu_can * CANEX_f * can_ext",
            U.mmole_per_min,
        ),
    ),
    Reaction(
        sid="M5EX",
        name="M5 excretion (M5EX)",
        equation="m5_ext -> m5_urine",
        compartment="Vki",
        sboTerm=SBO.TRANSPORT_REACTION,
        formula=(
            "GFR * 0.001 l_per_ml * f_oat * M5EX_f * m5_ext",
            U.mmole_per_min,
        ),
    ),
    Reaction(
        sid="M7EX",
        name="M7 excretion (M7EX)",
        equation="m7_ext -> m7_urine",
        compartment="Vki",
        sboTerm=SBO.TRANSPORT_REACTION,
        formula=(
            "GFR * 0.001 l_per_ml * f_oat * M7EX_f * m7_ext",
            U.mmole_per_min,
        ),
    ),
]

# ---------------------------------------------------------------------------------------------------------------------
# Pharmacodynamics
# ---------------------------------------------------------------------------------------------------------------------
_m.species.extend(
    [
        Species(
            "fpg",
            name="fasting plasma glucose (FPG)",
            initialConcentration=5.0,
            compartment="Vext",
            substanceUnit=U.mmole,
            hasOnlySubstanceUnits=False,  # this is a concentration
            boundaryCondition=True,
            sboTerm=SBO.SIMPLE_CHEMICAL,
            annotations=annotations.species["glc"],
            notes="""
            Fasting plasma glucose (FPG), set by the studies. It shifts the RTG
            (SGLT2 is induced in type 2 diabetes) and, with the difference of
            the mean plasma glucose of the day to the FPG (`PG_delta`), gives
            the glucose which is filtered.
            """,
        ),
        Species(
            "glc_urine",
            name="glucose (urine)",
            initialConcentration=0.0,
            compartment="Vurine",
            substanceUnit=U.mmole,
            hasOnlySubstanceUnits=True,
            sboTerm=SBO.SIMPLE_CHEMICAL,
            annotations=annotations.species["glc"],
            port=True,
        ),
    ]
)

_m.parameters.extend(
    [
        Parameter(
            "Mr_glc",
            180.16,
            U.g_per_mole,
            name="molecular weight glucose",
            sboTerm=SBO.MOLECULAR_MASS,
        ),
        Parameter(
            "cf_mg_per_g",
            1000,
            U.mg_per_g,
            name="conversion factor mg per g",
        ),
        Parameter(
            "fpg_healthy",
            5,
            U.mM,
            name="fasting plasma glucose (healthy)",
        ),
        Parameter(
            "PG_delta",
            0.85,
            U.mM,
            name="mean plasma glucose of the day minus the fasting plasma glucose",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            notes="""
            The glucose which is filtered over the day is the mean plasma glucose
            of the day, above the fasting plasma glucose by the meals. In healthy
            subjects about 0.85 mM: the urinary glucose excretion of 285 mmol/day
            over a GFR of 139 l/day with a 24-hr mean RTG of 3.79 mM is a mean
            plasma glucose of 5.85 mM [Sha2015]. Studies which report the 24-hr
            mean plasma glucose set the difference to the FPG.
            """,
        ),
        Parameter(
            "RTG_E50",
            **FITS.parameter("KI__RTG_E50", unit=U.mM),
            name="EC50 reduction in RTG",
            sboTerm=SBO.KINETIC_CONSTANT,
            notes="""
            EC50 of the reduction of the RTG by plasma canagliflozin (total),
            32 ng/ml (95 % CI 19-45 ng/ml) = 7.2e-5 mM [Devineni2013]; the
            fitted value is 34 ng/ml (fit PD_20261019_201254__61546).
            """,
        ),
        Parameter(
            "RTG_gamma",
            1,
            U.dimensionless,
            name="hill coefficient reduction in RTG",
            sboTerm=SBO.KINETIC_CONSTANT,
        ),
        Parameter(
            "RTG_base",
            **FITS.parameter("KI__RTG_base", unit=U.mM),
            name="baseline RTG",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            notes="""RTG without SGLT2 inhibition in healthy subjects (FPG 5 mM),
            which corresponds to the SGLT2 capacity; 12.3-13.5 mM in type 2
            diabetes with an FPG of about 10 mM [Devineni2012, Devineni2013].""",
        ),
        Parameter(
            "RTG_m_fpg",
            **FITS.parameter("KI__RTG_m_fpg", unit=U.dimensionless),
            name="FPG effect on RTG",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            notes="""Increase of the RTG per mM of FPG above the healthy FPG:
            SGLT2 is induced in type 2 diabetes [Rahmoune2005].""",
        ),
        Parameter(
            "RTG_max_inhibition",
            **FITS.parameter("KI__RTG_max_inhibition", unit=U.dimensionless),
            name="maximal relative reduction of the RTG",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            notes="""Maximal reduction of the RTG by SGLT2 inhibition relative to
            the RTG without inhibition, 64 % [Devineni2013]: SGLT1 reabsorbs the
            glucose which SGLT2 does not.""",
        ),
        Parameter(
            "RTG_splay",
            1.0,
            U.mM,
            name="splay of the glucose excretion around the RTG",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            notes="""The thresholds of the nephrons differ, so the glucose
            excretion rises smoothly around the RTG (splay) instead of at a
            sharp threshold; the softplus with a width of 1 mM.""",
        ),
        Parameter(
            "RTG_int",
            0,
            U.mM_min,
            constant=False,
            name="integral of the RTG over the collection interval",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            notes="""Reset to 0 with `RTG_time` at the start of a collection
            interval of the urine, see `RTG_mean`.""",
        ),
        Parameter(
            "RTG_time",
            0,
            U.min,
            constant=False,
            name="duration of the collection interval of the RTG",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            notes="""Reset to 0 with `RTG_int` at the start of a collection
            interval of the urine, see `RTG_mean`.""",
        ),
    ]
)

_m.rules.extend(
    [
        AssignmentRule(
            "pg",
            "fpg + PG_delta",
            U.mM,
            name="mean plasma glucose of the day",
            notes="""The glucose which is filtered.""",
        ),
        AssignmentRule(
            "RTG_fpg",
            "RTG_base + RTG_m_fpg * (fpg - fpg_healthy)",
            U.mM,
            name="RTG without SGLT2 inhibition",
            notes="""
            FPG dependent RTG without SGLT2 inhibition. SGLT2 is induced in T2DM
            [Rahmoune2005].
            """,
        ),
        AssignmentRule(
            "RTG_delta",
            "RTG_fpg * RTG_max_inhibition",
            U.mM,
            name="maximal reduction of the RTG",
        ),
        AssignmentRule(
            variable="RTG",
            value="RTG_fpg - RTG_delta * power(can_ext, RTG_gamma)/ (power(RTG_E50, RTG_gamma) + power(can_ext, RTG_gamma))",
            unit=U.mM,
            name="renal threshold glucose (RTG)",
            notes="""
            Renal threshold glucose.

            The renal threshold for glucose (RTG) is the plasma glucose
            concentration at which the tubular reabsorption of glucose begins to
            saturate; glucose is excreted into the urine in proportion to the
            glucose concentration above this threshold.
            12.3 - 12.7 mM RTG (placebo, T2DM) [Devineni2012]
            """,
        ),
        AssignmentRule(
            variable="RTG_mean",
            value="piecewise(RTG_int/RTG_time, RTG_time > 0 min, RTG)",
            unit=U.mM,
            name="mean RTG of the collection interval",
            notes="""
            The studies report the RTG of a collection interval of the urine (the
            24-hr mean RTG or the RTG of the intervals of the day), the mean of
            the RTG since the last reset of `RTG_int` and `RTG_time`.
            """,
        ),
    ]
)

_m.rate_rules.extend(
    [
        RateRule("RTG_int", "RTG", U.mM),
        RateRule("RTG_time", "1 dimensionless", U.dimensionless),
    ]
)

# Glucose excretion (UGE)
_m.reactions.extend(
    [
        Reaction(
            sid="GLCEX",
            name="glucose excretion (GLCEX)",
            equation="fpg -> glc_urine [can_ext]",
            compartment="Vki",
            sboTerm=SBO.TRANSPORT_REACTION,
            notes="""The filtered glucose above the RTG, the softplus of the
            difference with the width `RTG_splay`: the excretion approaches
            GFR * (pg - RTG) above the RTG and zero below it.""",
            # [ml/min] * [l/ml] * [mmole/l] = [mmole/min]
            formula=(
                "GFR * 0.001 l_per_ml * RTG_splay * ln(1 dimensionless + exp((pg - RTG)/RTG_splay))",
                U.mmole_per_min,
            ),
        ),
    ]
)

_m.rules.extend(
    [
        AssignmentRule(
            "UGE",
            "glc_urine * Mr_glc/cf_mg_per_g",
            unit=U.gram,
            name="urinary glucose excretion (UGE)",
            notes="""
            Urinary glucose excretion, the cumulative amount of glucose in the
            urine.
            """,
        )
    ]
)


model_kidney = _m


if __name__ == "__main__":
    from sbmlode import OdeSystem

    from pkdb_models.models.canagliflozin import MODEL_BASE_PATH

    # create SBML
    results = create_model(
        model=model_kidney,
        filepath=MODEL_BASE_PATH / f"{model_kidney.sid}.xml",
        sbml_level=3,
        sbml_version=2,
    )

    # ODE equations
    ode_system = OdeSystem.from_sbml(results.sbml_path)
    ode_system.write(results.sbml_path.parent / f"{results.sbml_path.stem}.md")

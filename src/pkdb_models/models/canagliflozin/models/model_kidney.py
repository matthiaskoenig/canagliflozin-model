"""Kidney model for the SGLT2 inhibitors."""
import numpy as np
import pandas as pd
from sbmlutils.converters import odefac
from sbmlutils.factory import *
from sbmlutils.metadata import *

from pkdb_models.models.canagliflozin.models import annotations
from pkdb_models.models.canagliflozin.models import templates


class U(templates.U):
    """UnitDefinitions"""

    mg_per_g = UnitDefinition("mg_per_g", "mg/g")
    ml_per_l = UnitDefinition("ml_per_l", "ml/l")
    ml_per_min = UnitDefinition("ml_per_min", "ml/min")



mid = "canagliflozin_kidney"

_m = Model(
    sid=mid,
    name="Model for renal canagliflozin, M5 and M7 excretion.",
    notes=f"""
    Model for renal canagliflozin, M5 and M7 excretion.
    
    - Canagliflozin is eliminated urine (33%, mainly O-glucuronide metabolites) [Deeks2017]
    - ~33 % of the oral dose was excreted in urine (M5: 13.3 %, M7: 17.2 %, canagliflozin <1%) [Devineni2015h]

    => mainly renal excretion of M5 and M7, small excretion of can    
    """ + templates.terms_of_use,
    creators=templates.creators,
    units=U,
    model_units=templates.model_units,
    annotations=annotations.model + [
        # tissue
        (BQB.OCCURS_IN, "fma/FMA:7203"),  # kidney
        (BQB.OCCURS_IN, "bto/BTO:0000671"),  # kidney
        (BQB.OCCURS_IN, "NCIT:C12415"),  # kidney

        (BQB.HAS_PROPERTY, "NCIT:C79372"),  # Pharmacokinetics: Excretion
        (BQB.HAS_PROPERTY, "NCIT:C79371"),  # Pharmacokinetics: Metabolism
    ]
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
        port=True
    ),
    Compartment(
        "Vki",
        value=0.3,  # 0.4 % of bodyweight
        unit=U.liter,
        name="kidney",
        constant=True,
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["ki"],
        port=True
    ),
    Compartment(
        "Vmem",
        value=np.nan,
        unit=U.m2,
        name="plasma membrane",
        constant=True,
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["plasma membrane"],
        spatialDimensions=2,
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
        port=True
    ),
    Species(
        "can",
        name="canagliflozin (kidney)",
        initialConcentration=0.0,
        compartment="Vki",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["can"],
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
        port=True
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
        port=True
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
        port=True
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
        port=True
    ),
    Species(
        "m7",
        name="M7 (kidney)",
        initialConcentration=0.0,
        compartment="Vki",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["m7"],
        port=True
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
        port=True
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
        notes="""Used for comparison with total radioactivity in urine.""",
        port=True
    ),
]

_m.parameters.extend([
    Parameter(
        "f_renal_function",
        name="scaling factor renal function",
        value=1.0,
        unit=U.dimensionless,
        sboTerm=SBO.KINETIC_CONSTANT,
        notes="""scaling factor for renal function. 1.0: normal renal function; 
        <1.0: reduced renal function
        """
    ),
    Parameter(
        "f_ugt1a9",
        1,
        U.dimensionless,
        name="scaling factor UGT1A9 activity",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        notes="""Scaling factor to vary UGT1A9 activity in kidney.
        1.0: normal activity; <1.0 decreased activity; >1.0 increased activity.
        """
    ),
    Parameter(
        "CAN2M7_Vmax",
        0.03875783470445108, # ~10% of hepatic UGT1A9 Vmax for CAN->M7 (Francke2015)
        U.mmole_per_min_l,
        name="Vmax canagliflozin to M7",
        sboTerm=SBO.MAXIMAL_VELOCITY,
        port=True,
    ),
    Parameter(
        "CAN2M7_Km_can",
        0.1, # reused from canaglifllozin liver model
        U.mM,
        name="Km canagliflozin UGT1A9",
        sboTerm=SBO.MICHAELIS_CONSTANT,
        port=True,
    ),
])

_m.reactions = [
    Reaction(
        sid="CANIM",
        name="CANIM",  # canagliflozin import (kidney)
        equation="can_ext <-> can",
        compartment="Vmem",
        sboTerm=SBO.TRANSPORT_REACTION,
        pars=[
            Parameter(
                "CANIM_Vmax",
                10.0,
                U.mmole_per_min_l,
                name="Vmax canagliflozin import",
                sboTerm=SBO.MAXIMAL_VELOCITY,
            ),
            Parameter(
                "CANIM_Km_can",
                0.1,
                U.mM,
                name="Km canagliflozin import",
                sboTerm=SBO.MICHAELIS_CONSTANT,
            ),
        ],
        formula=(
            "f_renal_function * CANIM_Vmax/CANIM_Km_can * Vki * "
            "(can_ext - can)/(1 dimensionless + can_ext/CANIM_Km_can + can/CANIM_Km_can)"
        )
    ),
    Reaction(
        sid="M7IM",
        name="M7IM",  # M7 import/export (kidney)
        equation="m7_ext <-> m7",
        compartment="Vmem",
        sboTerm=SBO.TRANSPORT_REACTION,
        pars=[
            Parameter(
                "M7IM_Vmax",
                10.0,
                U.mmole_per_min_l,
                name="Vmax M7 transport",
                sboTerm=SBO.MAXIMAL_VELOCITY,
            ),
            Parameter(
                "M7IM_Km_m7",
                0.1,
                U.mM,
                name="Km M7 transport",
                sboTerm=SBO.MICHAELIS_CONSTANT,
            ),
        ],
        formula=(
            "f_renal_function * M7IM_Vmax/M7IM_Km_m7 * Vki * (m7_ext - m7)/(1 dimensionless + m7_ext/M7IM_Km_m7 + m7/M7IM_Km_m7)"
        ),
    ),
    Reaction(
        sid="CAN2M7",
        name="UGT1A9 (can -> m7)",
        equation="can -> m7",
        compartment="Vki",
        sboTerm=SBO.BIOCHEMICAL_REACTION,
        pars=[
            Parameter(
                "f_CAN2M7",
                0.13941425128973972,
                U.dimensionless,
                name="scaling factor CAN2M7 kidney vs liver",
                sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                notes="""Scaling factor relative to liver UGT1A9 activity.
                1.0 = equal to liver, < 1.0 = lower, > 1.0 = higher."""
            ),
        ],
        formula=(
            "f_renal_function * f_ugt1a9 * f_CAN2M7 * CAN2M7_Vmax * Vki * can/(can + CAN2M7_Km_can)"
        ),
    ),
    Reaction(
        sid="CANEX",
        name="canagliflozin excretion (CANEX)",
        equation="can_ext -> can_urine",
        compartment="Vki",
        sboTerm=SBO.TRANSPORT_REACTION,
        pars=[
            Parameter(
                "CANEX_k",
                0.003745816607378912,
                U.per_min,
                name="rate urinary excretion of canagliflozin",
                sboTerm=SBO.KINETIC_CONSTANT,
            ),
        ],
        formula=(
            "f_renal_function * CANEX_k * Vki * can_ext"
        )
    ),
    Reaction(
        sid="M5EX",
        name="M5 excretion (M5EX)",
        equation="m5_ext -> m5_urine",
        compartment="Vki",
        sboTerm=SBO.TRANSPORT_REACTION,
        pars=[
            Parameter(
                "M5EX_k",
                0.11095445697907381,
                U.per_min,
                name="rate urinary excretion of m5",
                sboTerm=SBO.KINETIC_CONSTANT,
            ),
        ],
        formula=(
            "f_renal_function * M5EX_k * Vki * m5_ext"
        )
    ),
    Reaction(
        sid="M7EX",
        name="M7 excretion (M7EX)",
        equation="m7_ext -> m7_urine",
        compartment="Vki",
        sboTerm=SBO.TRANSPORT_REACTION,
        pars=[
            Parameter(
                "M7EX_k",
                0.18673479639197138,
                U.per_min,
                name="rate urinary excretion of m7",
                sboTerm=SBO.KINETIC_CONSTANT,
            ),
        ],
        formula=(
            "f_renal_function * M7EX_k * Vki * m7_ext"
        )
    ),

]

_m.rules.extend([
    AssignmentRule("cantot_urine", "can_urine + m5_urine + m7_urine", U.mmole),
])

# ---------------------------------------------------------------------------------------------------------------------
# Pharmacodynamics
# ---------------------------------------------------------------------------------------------------------------------
_m.species.extend([
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
        Fasting plasma glucose (FPG).
        Model depends on the fasting plasma glucose:
        - as a proxy of the daily glucose variation in the glucose excretion
        - to set the glucose dependent RTG values (i.e. T2DM have higher SGLT2 amounts, and consequently higher RTG values)
        """
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
        port=True
    ),
])

_m.parameters.extend([
    Parameter(
        "Mr_glc",
        180,
        U.g_per_mole,
        name=f"molecular weight glc",
        sboTerm=SBO.MOLECULAR_MASS,
    ),
    Parameter(
        "cf_mg_per_g",
        1000,
        U.mg_per_g,
        name=f"Conversion factor mg per g",
    ),
    Parameter(
        "cf_ml_per_l",
        1000,
        U.ml_per_l,
        name=f"Conversion factor ml per l",
    ),
    Parameter(
        "GFR_healthy",
        100,
        U.ml_per_min,
        name=f"Glomerular filtration rate (healthy)",
    ),
    Parameter(
        "RTG_E50",
        1.672069145969639e-05,  # [10 - 200E-6] for optimization; 32E-3/444.518 = 71.9E-6,  # [mM]   [ng/ml]/[g/mole] = [nmole/ml] = µmole/l
        U.mM,
        name="EC50 reduction in RTG",
        sboTerm=SBO.KINETIC_CONSTANT,
        notes="""
        estimated EC50 value was 32 ng/mL (95% CI = 19–45 ng/mL). [Devineni2013]
        """
    ),
    Parameter(
        "RTG_gamma",
        1,  # [1 - 4] for optimization
        U.dimensionless,
        name="hill coefficient reduction in RTG",
        sboTerm=SBO.KINETIC_CONSTANT,
    ),
    Parameter(
        "RTG_base",
        9.003931670662638,  # [10.5 - 14] for optimization
        U.mM,
        name=f"Baseline RTG value",
        notes="""Typical RTG value without SGLT2 inhibitors in healthy subjects.
        
        This corresponds to the SGLT2 concentrations.
        """
    ),
    Parameter(
        "RTG_m_fpg",
        0.7104098476982807,  # [0.2 - 1] for optimization
        U.dimensionless,
        name=f"FPG effect on RTG",
        notes="""Effect of the FPG on the change in RTG_base."""
    ),
    Parameter(
        "RTG_max_inhibition",
        0.6272697309545409,  # [0 - 1] for optimization
        U.dimensionless,
        name=f"RTG maximum inhibition",
        notes="maximum inhibition of RTG via SGLT2"
    ),
    Parameter(
        "fpg_healthy",
        5,
        U.mM,
        name=f"fasting plasma glucose (healthy)",
    ),
])

_m.rules.extend([
    AssignmentRule(
        "RTG_fpg",
        "RTG_base + RTG_m_fpg * (fpg - fpg_healthy)",
        U.mM,
        name=f"RTG value (FPG)",
        notes="""
        FPG dependent base RTG value. SGLT2 is induced in T2DM [Rahmoune2005] 
        """
    ),
    AssignmentRule(
        "RTG_delta",
        "RTG_fpg * RTG_max_inhibition",  # [7 - 10]
        U.mM,
        name=f"RTG value",
        notes="""
        ΔRTG, maximum reduction in RTG due to SGLT2 inhibition.
        Normally around 7 - 10 mM. 
        """
    ),
    AssignmentRule(
        variable="RTG",
        value="RTG_fpg - RTG_delta * power(can_ext, RTG_gamma)/ (power(RTG_E50, RTG_gamma) + power(can_ext, RTG_gamma))",
        unit=U.mM,
        name="renal threshold glucose (RTG)",
        notes="""
        Renal threshold glucose.

        The renal threshold for glucose (RTG) is the plasma glucose concentration at which tubular reabsorption of 
        glucose begins to saturate; glucose is excreted into the urine in direct proportion 
        to the glucose concentration above this threshold.
        12.3 - 12.7 mM RTG (placebo) [Devineni2012]
        """
    ),
    AssignmentRule(
        variable="GFR",
        value="f_renal_function * GFR_healthy",
        unit=U.ml_per_min,
        name="glomerular filtration rate",
    ),
])


# Glucose excretion (UGE)

_m.reactions.extend([
    Reaction(
        sid="GLCEX",
        name="glucose excretion (GLCEX)",
        equation="fpg -> glc_urine [can_ext]",
        compartment="Vki",
        sboTerm=SBO.TRANSPORT_REACTION,
        #  piecewise      | x1, y1, [x2, y2,] [...] [z] | A piecewise function: if (y1), x1.  Otherwise, if (y2), x2, etc.  Otherwise, z.
        formula=(
            # [ml/min]/[ml/l] *[mmole/l] = [mmole/min]
            "piecewise(GFR/cf_ml_per_l * (fpg - RTG), fpg > RTG, 0 mmole_per_min)"   # FIXME: no scaling with liver volume Vki? (GFR should scale with kidney volume)
        )
    ),
])

_m.rules.extend([
    AssignmentRule(
        "UGE", "glc_urine * Mr_glc/cf_mg_per_g", unit=U.gram,
        name="urinary glucose excretion (UGE)",
        notes="""
        Urinary glucose excretion is calculated from cumulative amount of glucose in urine.
        """
    )
])


model_kidney = _m


def canagliflozin_layout(dx=200, dy=200) -> pd.DataFrame:
    """Layout definition."""

    delta_y = 0.5 * dy
    delta_x = 0.7 * dx

    positions = [
        # sid, x, y
        ["fpg", -0.3 * delta_x, 0],
        ["can_ext", 1 * delta_x, 0],
        ["m7_ext", 3 * delta_x, 0],
        ["m5_ext", 4.3*delta_x, 0],

        ["CANIM", 1 * delta_x, 1 * delta_y],
        ["M7IM", 3 * delta_x, 1 * delta_y],

        ["can", 1 * delta_x, 2 * delta_y],
        ["m7", 3 * delta_x, 2 * delta_y],

        ["CAN2M7", 2 * delta_x, 1.5 * delta_y],

        ["GLCEX", -0.3 * delta_x, 3 * delta_y],
        ["CANEX", delta_x, 3 * delta_y],
        ["M7EX", 3*delta_x, 3 * delta_y],
        ["M5EX", 4.3*delta_x, 3 * delta_y],

        ["glc_urine", -0.3 * delta_x, 4 * delta_y],
        ["can_urine", 1* delta_x, 4 * delta_y],
        ["m7_urine", 3 * delta_x, 4 * delta_y],
        ["m5_urine", 4.3*delta_x, 4 * delta_y],
    ]

    df = pd.DataFrame(positions, columns=["id", "x", "y"])
    df.set_index("id", inplace=True)
    return df


def canagliflozin_annotations(dx=200, dy=200) -> list:
    COLOR_BLOOD = "#FF796C"
    COLOR_CELL = "#FFFFFF"
    COLOR_URINE = "#FF7F0E"
    delta_y = 0.5 * dy

    kwargs = {
        "type": cyviz.AnnotationShapeType.ROUND_RECTANGLE,
        "opacity": 20,
        "border_color": "#000000",
        "border_thickness": 2,
    }
    xpos = -0.8 * dx
    width = 4.3 * dx

    annotations = [
        cyviz.AnnotationShape(
            x_pos=xpos, y_pos=-0.5*delta_y, width=width, height=1.5 * delta_y,
            fill_color=COLOR_BLOOD, **kwargs
        ),
        cyviz.AnnotationShape(
            x_pos=xpos, y_pos=delta_y, width=width, height=2* delta_y,
            fill_color=COLOR_CELL, **kwargs
        ),
        cyviz.AnnotationShape(
            x_pos=xpos, y_pos=3 * delta_y, width=width, height=1.5 * delta_y,
            fill_color=COLOR_URINE, **kwargs
        )
    ]
    return annotations

if __name__ == "__main__":
    from pkdb_models.models.canagliflozin import MODEL_BASE_PATH
    from sbmlutils import cytoscape as cyviz

    # create SBML
    results: FactoryResult = create_model(
        model=model_kidney,
        filepath=MODEL_BASE_PATH / f"{model_kidney.sid}.xml",
        sbml_level=3, sbml_version=2,
    )

    ode_factory = odefac.SBML2ODE.from_file(sbml_file=results.sbml_path)
    ode_factory.to_markdown(md_file=results.sbml_path.parent / f"{results.sbml_path.stem}.md")

    # visualization in Cytoscape
    cyviz.visualize_sbml(sbml_path=results.sbml_path, delete_session=False)
    cyviz.apply_layout(layout=canagliflozin_layout())
    cyviz.add_annotations(annotations=canagliflozin_annotations())

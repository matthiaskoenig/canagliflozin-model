"""Canagliflozin intestine model."""
import numpy as np
import pandas as pd
from sbmlutils.converters import odefac

from sbmlutils.cytoscape import visualize_sbml
from sbmlutils.factory import *
from sbmlutils.metadata import *

from pkdb_models.models.templates import terms_of_use

from pkdb_models.models.canagliflozin.models import annotations
from pkdb_models.models.canagliflozin.models import templates


class U(templates.U):
    """UnitDefinitions"""

    per_hr = UnitDefinition("per_hr", "1/hr")
    mg_per_min = UnitDefinition("mg_per_min", "mg/min")


_m = Model(
    "canagliflozin_intestine",
    name="Model for canagliflozin absorption in the small intestine",
    notes="""
    # Model for canagliflozin absorption

    - absorption canagliflozin (can)
    - fraction absorbed: 0.59 (41% in feces)
    - enterohepatische circulation (M5?, M7?, M9?)
    """
    + terms_of_use,
    creators=templates.creators,
    units=U,
    model_units=templates.model_units,
    annotations=annotations.model + [
        # tissue
        (BQB.OCCURS_IN, "fma/FMA:45615"),  # gut
        (BQB.OCCURS_IN, "bto/BTO:0000545"),  # gut
        (BQB.OCCURS_IN, "NCIT:C12736"),  # intestine
        (BQB.OCCURS_IN, "fma/FMA:7199"),  # intestine
        (BQB.OCCURS_IN, "bto/BTO:0000648"),  # intestine

        (BQB.HAS_PROPERTY, "NCIT:C79369"),  # Pharmacokinetics: Absorption
        (BQB.HAS_PROPERTY, "NCIT:C79372"),  # Pharmacokinetics: Excretion
    ]
)

_m.compartments = [
    Compartment(
        "Vext",
        1.0,
        name="plasma",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        port=True,
        annotations=annotations.compartments["plasma"],
    ),
    Compartment(
        "Vgu",
        1.2825,  # 0.0171 [l/kg] * 75 kg
        name="intestine",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        port=True,
        annotations=annotations.compartments["gu"],
    ),
    Compartment(
        "Vlumen",
        1.2825 * 0.9,  # 0.0171 [l/kg] * 75 kg * 0.9,
        name="intestinal lumen (inner part of intestine)",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        constant=False,
        port=True,
        annotations=annotations.compartments["gu_lumen"],
    ),
    Compartment(
        "Vfeces",
        metaId="meta_Vfeces",
        value=1,
        unit=U.liter,
        constant=True,
        name="feces",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        port=True,
        annotations=annotations.compartments["feces"],
    ),
    Compartment(
        "Ventero",
        1.0,
        name="intestinal lining (enterocytes)",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        constant=False,
    ),
    Compartment(
        "Vapical",
        np.nan,
        name="apical membrane (intestinal membrane enterocytes)",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.m2,
        annotations=annotations.compartments["apical"],
        spatialDimensions=2,
    ),
    Compartment(
        "Vbaso",
        np.nan,
        name="basolateral membrane (intestinal membrane enterocytes)",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.m2,
        annotations=annotations.compartments["basolateral"],
        spatialDimensions=2,
    ),
    Compartment(
        "Vstomach",
        metaId="meta_Vstomach",
        value=1,
        unit=U.liter,
        constant=True,
        name="stomach",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        port=True,
        annotations=annotations.compartments["stomach"],
    ),
]


_m.species = [
    Species(
        f"can_stomach",
        metaId=f"meta_can_stomach",
        initialConcentration=0.0,
        compartment="Vstomach",
        substanceUnit=U.mmole,
        name=f"canagliflozin (stomach)",
        hasOnlySubstanceUnits=True,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["can"],
        boundaryCondition=True,
    ),
    Species(
        "can_lumen",
        initialConcentration=0.0,
        name="canagliflozin (intestinal lumen)",
        compartment="Vlumen",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["can"],
        port=True,
    ),
    Species(
        "can_ext",
        initialConcentration=0.0,
        name="canagliflozin (plasma)",
        compartment="Vext",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["can"],
        port=True,
    ),
    Species(
        "can_feces",
        initialConcentration=0.0,
        name="canagliflozin (feces)",
        compartment="Vfeces",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=True,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["can"],
        port=True,
    ),

    Species(
        "m7_lumen",
        initialConcentration=0.0,
        name="M7 (intestinal lumen)",
        compartment="Vlumen",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["m7"],
        port=True,
    ),

    Species(
        "m9_lumen",
        initialConcentration=0.0,
        name="M9 (intestinal lumen)",
        compartment="Vlumen",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["m9"],
        port=True,
    ),
    Species(
        "m7_feces",
        initialConcentration=0.0,
        name="M7 (feces)",
        compartment="Vfeces",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=True,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["m7"],
        port=True,
    ),
    Species(
        "m9_feces",
        initialConcentration=0.0,
        name="M9 (feces)",
        compartment="Vfeces",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=True,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["m9"],
        port=True,
    ),
    Species(
        "cantot_feces",
        initialConcentration=0.0,
        name="total canagliflozin (feces)",
        compartment="Vfeces",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=True,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["cantot"],
        notes="""Used for comparison with total radioactivity in feces.""",
        port=True
    ),

]

_m.parameters = [
    Parameter(
        f"F_can_abs",
        0.59,
        U.dimensionless,
        constant=True,
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        name=f"fraction absorbed canagliflozin",
        notes="""
        Fraction absorbed, i.e., only a fraction of the canagliflozin in the intestinal lumen
        is absorbed. This parameter determines how much of the canagliflozin is excreted.
        
        `F_can_abs` of dose is absorbed. `(1-F_can_abs)` is excreted in feces.
        
        fraction absorbed: 0.59; ~41% in the feces
        """,
    ),
    Parameter(
        "CANABS_k",
        0.015932205013389062,
        unit=U.per_min,
        name="rate of canagliflozin absorption",
        sboTerm=SBO.KINETIC_CONSTANT,
    ),
    Parameter(
        "f_absorption",
        1,
        unit=U.dimensionless,
        name="scaling factor absorption rate",
        sboTerm=SBO.KINETIC_CONSTANT,
        notes="""1.0: normal absorption corresponding to tablet under fasting conditions.
        
        food decreases the absorption rate, i.e. < 1.0.
        """
    ),
]

_m.rules.append(
    AssignmentRule(
        "absorption",
        value="f_absorption * CANABS_k * Vgu * can_lumen",
        unit=U.mmole_per_min,
        name="absorption canagliflozin",
    ),
)

_m.reactions = [
    Reaction(
        "CANABS",
        name="CANABS",
        equation="can_lumen -> can_ext",
        sboTerm=SBO.TRANSPORT_REACTION,
        compartment="Vapical",
        formula=("F_can_abs * absorption", U.mmole_per_min),
    ),

    Reaction(
        sid="CANEXC",
        name=f"CANEXC (feces)",
        compartment="Vlumen",
        equation=f"can_lumen -> can_feces",
        sboTerm=SBO.TRANSPORT_REACTION,
        pars=[],
        formula=(
            f"(1 dimensionless - F_can_abs) * absorption",
            U.mmole_per_min,
        ),
    ),

    Reaction(
        sid="M7EXC",
        name=f"M7EXC (feces)",
        compartment="Vlumen",
        equation=f"m7_lumen -> m7_feces",
        sboTerm=SBO.TRANSPORT_REACTION,
        pars=[],
        formula=(
            f"CANABS_k * Vgu * m7_lumen",
            U.mmole_per_min,
        ),
        notes="""Assumption: same rate as CANABS for simplification."""
    ),

    Reaction(
        sid="M9EXC",
        name=f"M9EXC (feces)",
        compartment="Vlumen",
        equation=f"m9_lumen -> m9_feces",
        sboTerm=SBO.TRANSPORT_REACTION,
        pars=[],
        formula=(
            f"CANABS_k * Vgu * m9_lumen",
            U.mmole_per_min,
        ),
        notes="""Assumption: same rate as CANABS for simplification."""
    ),
]


_m.parameters.extend([
    Parameter(
        f"PODOSE_can",
        0,
        U.mg,
        constant=False,
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        name=f"oral dose canagliflozin [mg]",
        port=True,
    ),
    Parameter(
        f"Ka_dis_can",
        2.0,
        U.per_hr,
        constant=True,
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        name=f"dissolution rate canagliflozin",
        port=True
    ),
    Parameter(
        f"Mr_can",
        444.518,
        U.g_per_mole,
        constant=True,
        name=f"Molecular weight canagliflozin [g/mole]",
        sboTerm=SBO.MOLECULAR_MASS,
        port=True,
    ),
])

# -------------------------------------
# Dissolution of tablet/dose in stomach
# -------------------------------------
_m.reactions.extend(
    [
        # fraction dose available for absorption from stomach
        Reaction(
            sid=f"dissolution_can",
            name=f"dissolution canagliflozin",
            formula=(
                f"Ka_dis_can/60 min_per_hr * PODOSE_can/Mr_can",
                U.mmole_per_min,
            ),
            equation=f"can_stomach -> can_lumen",
            compartment="Vgu",
            notes="""Swallowing, dissolution of tablet, and transport into intestine.
            Overall process describing the rates of this processes.
            """
        ),
    ]
)
_m.rate_rules.append(
    RateRule(f"PODOSE_can", f"-dissolution_can * Mr_can", U.mg_per_min),
)
_m.rules.extend([
    AssignmentRule("cantot_feces", "can_feces + m7_feces + m9_feces", U.mmole),
])
model_intestine = _m


def canagliflozin_layout(dx=200, dy=200) -> pd.DataFrame:
    """Layout definition."""

    delta_y = 0.5 * dy
    delta_x = 1.0 * dx

    positions = [
        # sid, x, y
        ["can_stomach",  0 * delta_x, 0 * delta_y],
        ["can_ext",    1.5 * delta_x, 0 * delta_y],

        ["dissolution_can",   0 * delta_x, 1.0 * delta_y],
        ["CANABS",          1.5 * delta_x, 1.0 * delta_y],

        ["can_lumen", 0 * delta_x, 1.5 * delta_y],
        ["m7_lumen",  1 * delta_x, 1.5 * delta_y],
        ["m9_lumen",  2 * delta_x, 1.5 * delta_y],

        ["CANEXC", 0 * delta_x, 2.5 * delta_y],
        ["M7EXC", 1 * delta_x, 2.5 * delta_y],
        ["M9EXC", 2 * delta_x, 2.5 * delta_y],

        ["can_feces", 0 * delta_x, 3.5 * delta_y],
        ["m7_feces", 1 * delta_x, 3.5 * delta_y],
        ["m9_feces", 2 * delta_x, 3.5 * delta_y],
    ]

    df = pd.DataFrame(positions, columns=["id", "x", "y"])
    df.set_index("id", inplace=True)

    return df


def canagliflozin_annotations(dx=200, dy=200) -> list:
    COLOR_STOMACH = "#1f77b4"
    COLOR_INTESTINE = "#FFFFFF"
    COLOR_BLOOD = "#FF796C"
    COLOR_FECES = "#8c564b"

    kwargs = {
        "type": cyviz.AnnotationShapeType.ROUND_RECTANGLE,
        "opacity": 20,
        "border_color": "#000000",
        "border_thickness": 2,
    }

    dy = 0.5 * dy
    dx = 1.0 * dx

    annotations = [
        cyviz.AnnotationShape(
            x_pos= -0.5 * dx, y_pos=-0.5 * dy, width=dx, height=1.5 * dy,
            fill_color=COLOR_STOMACH, **kwargs
        ),
        cyviz.AnnotationShape(
            x_pos= -0.5 * dx, y_pos=1.0 * dy, width=3 * dx, height=1.5* dy,
            fill_color=COLOR_INTESTINE, **kwargs
        ),
        cyviz.AnnotationShape(
            x_pos= 0.5 * dx, y_pos=-0.5 * dy, width=2 * dx, height=1.5 * dy,
            fill_color=COLOR_BLOOD, **kwargs
        ),
        cyviz.AnnotationShape(
            x_pos=-0.5 * dx, y_pos=2.5 * dy, width=3 * dx, height=1.5 * dy,
            fill_color=COLOR_FECES, **kwargs
        ),
    ]
    return annotations

if __name__ == "__main__":
    from pkdb_models.models.canagliflozin import MODEL_BASE_PATH
    from sbmlutils import cytoscape as cyviz

    results = create_model(
        filepath=MODEL_BASE_PATH / f"{model_intestine.sid}.xml",
        model=model_intestine, sbml_level=3, sbml_version=2
    )

    # ODE equations
    ode_factory = odefac.SBML2ODE.from_file(sbml_file=results.sbml_path)
    ode_factory.to_markdown(md_file=results.sbml_path.parent / f"{results.sbml_path.stem}.md")

    # Visualize
    cyviz.visualize_sbml(sbml_path=results.sbml_path, delete_session=True)
    cyviz.apply_layout(layout=canagliflozin_layout())
    cyviz.add_annotations(annotations=canagliflozin_annotations())
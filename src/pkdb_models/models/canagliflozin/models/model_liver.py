"""Liver model for SGLT2 inhibitors."""
import numpy as np
import pandas as pd

from sbmlutils.factory import *
from sbmlutils.metadata import *

from pkdb_models.models.canagliflozin.models import annotations
from pkdb_models.models.canagliflozin.models import templates


class U(templates.U):
    """UnitDefinitions"""

    pass


mid = "canagliflozin_liver"

_m = Model(
    sid=mid,
    name="Model for hepatic canagliflozin metabolism.",
    notes=f"""
    Model for canagliflozin metabolism.
    """ + templates.terms_of_use,
    creators=templates.creators,
    units=U,
    model_units=templates.model_units,
    annotations=annotations.model + [
        # tissue
        (BQB.OCCURS_IN, "fma/FMA:7197"),
        (BQB.OCCURS_IN, "bto/BTO:0000759"),
        (BQB.OCCURS_IN, "NCIT:C12392"),

        (BQB.HAS_PROPERTY, "NCIT:C79371"),  # Pharmacokinetics: Metabolism
        (BQB.HAS_PROPERTY, "NCIT:C79372"),  # Pharmacokinetics: Excretion
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
        "Vli",
        value=1.5,
        unit=U.liter,
        name="liver",
        constant=True,
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["li"],
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
        "Vapical",
        np.nan,
        name="apical membrane",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.m2,
        annotations=annotations.compartments["apical"],
        spatialDimensions=2,
    ),
    Compartment(
        "Vbi",
        1.0,
        name="bile",
        unit=U.liter,
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["bi"],
        port=True,
    ),
    Compartment(
        "Vlumen",
        1.2825 * 0.9,  # 0.0171 [l/kg] * 75 kg * 0.9, # FIXME: calculate from whole-body
        name="intestinal lumen (inner part of intestine)",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        constant=False,
        port=True,
        annotations=annotations.compartments["gu_lumen"],
    ),

]

_m.species = [
    Species(
        "can_ext",
        name="canagliflozin (plasma)",
        initialConcentration=0.0,
        compartment="Vext",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,  # this is a concentration
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
        hasOnlySubstanceUnits=False,  # this is a concentration
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
        hasOnlySubstanceUnits=False,  # this is a concentration
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["m7"],
        port=True
    ),
    Species(
        "can",
        name="canagliflozin (liver)",
        initialConcentration=0.0,
        compartment="Vli",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,  # this is a concentration
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["can"],
    ),
    Species(
        "m5",
        name="M5 (liver)",
        initialConcentration=0.0,
        compartment="Vli",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,  # this is a concentration
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["m5"],
    ),
    Species(
        "m7",
        name="M7 (liver)",
        initialConcentration=0.0,
        compartment="Vli",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,  # this is a concentration
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["m7"],
    ),
    Species(
        "m9",
        name="M9 (liver)",
        initialConcentration=0.0,
        compartment="Vli",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,  # this is a concentration
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["m9"],
    ),
    Species(
        "m7_bi",
        initialConcentration=0.0,
        name="M7 (bile)",
        compartment="Vbi",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=True,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["m7"],
        notes="""
        Bile M7 in amount.
        """,
    ),
    Species(
        "m9_bi",
        initialConcentration=0.0,
        name="M9 (bile)",
        compartment="Vbi",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=True,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["m9"],
        notes="""
        Bile M9 in amount.
        """,
    ),
    Species(
        "m7_lumen",
        initialConcentration=0.0,
        name="M7 (lumen)",
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
        name="M9 (lumen)",
        compartment="Vlumen",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["m9"],
        port=True,
    ),
]


_m.reactions = [
    Reaction(
        sid="CANIM",
        name="CANIM",
        equation="can_ext <-> can",
        compartment="Vmem",
        sboTerm=SBO.TRANSPORT_REACTION,
        pars=[
            Parameter(
                "CANIM_Vmax",
                4.026019530820937,   # FAST import
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
            )
        ],
        formula=(
            "CANIM_Vmax/CANIM_Km_can * Vli * (can_ext - can)/(1 dimensionless + can_ext/CANIM_Km_can + can/CANIM_Km_can)"
        ),
    ),
    Reaction(
        sid="CAN2M5",
        name="CAN2M5 (UGT2B4)",
        equation="can -> m5",
        compartment="Vli",
        sboTerm=SBO.BIOCHEMICAL_REACTION,
        pars=[
            Parameter(
                "CAN2M5_Vmax",
                0.05457677939498227,
                U.mmole_per_min_l,
                name="Vmax canagliflozin conversion",
                sboTerm=SBO.MAXIMAL_VELOCITY,
            ),
            Parameter(
                "CAN2M5_Km_can",
                3.4933649233538513,
                U.mM,
                name="Km canagliflozin UGT2B4",
                sboTerm=SBO.MICHAELIS_CONSTANT,
            ),
            Parameter(
                "f_ugt2b4",
                1,
                U.dimensionless,
                name="scaling factor UGT2B4 activity",
                sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                notes="""Scaling factor to vary UGT2B4 activity.
                1.0: unchanged activity; < 1.0 decreased activity; >1.0 increased activity.
                """
            )
        ],
        formula=(
            "f_ugt2b4 * CAN2M5_Vmax * Vli * can/(can + CAN2M5_Km_can)"
        ),
    ),
    Reaction(
        sid="CAN2M7",
        name="CAN2M7 (UGT1A9)",
        equation="can -> m7",
        compartment="Vli",
        sboTerm=SBO.BIOCHEMICAL_REACTION,
        pars=[
            Parameter(
                "CAN2M7_Vmax",
                0.0012870703810990754,
                U.mmole_per_min_l,
                name="Vmax canagliflozin conversion",
                sboTerm=SBO.MAXIMAL_VELOCITY,
            ),
            Parameter(
                "CAN2M7_Km_can",
                0.1,
                U.mM,
                name="Km canagliflozin UGT1A9",
                sboTerm=SBO.MICHAELIS_CONSTANT,
            ),
            Parameter(
                "f_ugt1a9",
                1,
                U.dimensionless,
                name="scaling factor UGT1A9 activity",
                sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                notes="""Scaling factor to vary UGT1A9 activity.
                1.0: unchanged activity; < 1.0 decreased activity; >1.0 increased activity.
                """
            )
        ],
        formula=(
            "f_ugt1a9 * CAN2M7_Vmax * Vli * can/(can + CAN2M7_Km_can)"
        ),
    ),
    Reaction(
        sid="CAN2M9",
        name="CAN2M9 (CYP3A4)",
        equation="can -> m9",
        compartment="Vli",
        sboTerm=SBO.BIOCHEMICAL_REACTION,
        pars=[
            Parameter(
                "CAN2M9_Vmax",
                0.005209079912015983,
                U.mmole_per_min_l,
                name="Vmax canagliflozin conversion",
                sboTerm=SBO.MAXIMAL_VELOCITY,
            ),
            Parameter(
                "CAN2M9_Km_can",
                0.1,
                U.mM,
                name="Km canagliflozin CYP3A4",
                sboTerm=SBO.MICHAELIS_CONSTANT,
            ),
            Parameter(
                "f_cyp3a4",
                1,
                U.dimensionless,
                name="scaling factor CYP3A4 activity",
                sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                notes="""Scaling factor to vary CYP3A4 activity.
                1.0: unchanged activity; < 1.0 decreased activity; >1.0 increased activity.
                """
            )
        ],
        formula=(
            "f_cyp3a4 * CAN2M9_Vmax * Vli * can/(can + CAN2M9_Km_can)"
        ),
    ),
    Reaction(
        sid="M5EX",
        name="M5EX",
        equation="m5 <-> m5_ext",
        compartment="Vmem",
        sboTerm=SBO.TRANSPORT_REACTION,
        pars=[
            Parameter(
                "M5EX_Vmax",
                61.874157129269065,  # FAST
                U.mmole_per_min_l,
                name="Vmax M5 export",
                sboTerm=SBO.MAXIMAL_VELOCITY,
            ),
            Parameter(
                "M5EX_Km_m5",
                1.2083379213672167,
                U.mM,
                name="Km M5 export",
                sboTerm=SBO.MICHAELIS_CONSTANT,
            )
        ],
        formula=(
            "M5EX_Vmax/M5EX_Km_m5 * Vli * (m5 - m5_ext)/(1 dimensionless + m5_ext/M5EX_Km_m5 + m5/M5EX_Km_m5)"
        )
    ),
    Reaction(
        sid="M7EX",
        name="M7EX",
        equation="m7 <-> m7_ext",
        compartment="Vmem",
        sboTerm=SBO.TRANSPORT_REACTION,
        pars=[
            Parameter(
                "M7EX_Vmax",
                0.3138528806886005,  # FAST
                U.mmole_per_min_l,
                name="Vmax M7 export",
                sboTerm=SBO.MAXIMAL_VELOCITY,
            ),
            Parameter(
                "M7EX_Km_m7",
                0.1,
                U.mM,
                name="Km M7 export",
                sboTerm=SBO.MICHAELIS_CONSTANT,
            )
        ],
        formula=(
            "M7EX_Vmax/M7EX_Km_m7 * Vli * (m7 - m7_ext)/(1 dimensionless + m7_ext/M7EX_Km_m7 + m7/M7EX_Km_m7)"
        )
    ),

    Reaction(
        sid="M7BIEX",
        name="M7BIEX (bile)",
        equation="m7 -> m7_bi",
        sboTerm=SBO.TRANSPORT_REACTION,
        compartment="Vapical",
        pars=[
            Parameter(
                "MBIEX_k",
                0.0001,
                U.per_min,
                name="rate for M7 and M9 export in bile",
                sboTerm=SBO.KINETIC_CONSTANT,
            )
        ],
        formula=(
            "MBIEX_k * Vli * m7",
            U.mmole_per_min,
        ),
    ),
    Reaction(
        "M7EHC",
        name="M7EHC (enterohepatic circulation)",
        equation="m7_bi -> m7_lumen",
        sboTerm=SBO.TRANSPORT_REACTION,
        compartment="Vlumen",
        formula=("M7BIEX", U.mmole_per_min),
    ),
    Reaction(
        "M9BIEX",
        name="M9BIEX (bile)",
        equation="m9 -> m9_bi",
        sboTerm=SBO.TRANSPORT_REACTION,
        compartment="Vapical",
        formula=(
            "MBIEX_k * Vli * m9",
            U.mmole_per_min,
        ),
    ),
    Reaction(
        "M9EHC",
        name="M9EHC (enterohepatic circulation)",
        equation="m9_bi -> m9_lumen",
        sboTerm=SBO.TRANSPORT_REACTION,
        compartment="Vlumen",
        formula=("M9BIEX", U.mmole_per_min),
    ),
]

model_liver = _m


def canagliflozin_layout(dx=200, dy=200) -> pd.DataFrame:
    """Layout definition."""

    delta_y = 0.5 * dy
    delta_x = 0.7 * dx

    positions = [
        # sid, x, y

        ["m7_ext",  0 * delta_x, 0 * delta_y],
        ["can_ext", 1.5 * delta_x, 0 * delta_y],
        ["m5_ext",  3 * delta_x, 0 * delta_y],

        ["M7EX",  0 * delta_x, 1 * delta_y],
        ["CANIM", 1.5 * delta_x, 1 * delta_y],
        ["M5EX",  3 * delta_x, 1 * delta_y],

        ["m7",  0 * delta_x, 2 * delta_y],
        ["can", 1.5 * delta_x, 2 * delta_y],
        ["m5",  3 * delta_x, 2 * delta_y],

        ["CAN2M7", 0.7 * delta_x, 2.5 * delta_y],
        ["CAN2M5", 2.7 * delta_x, 2.5 * delta_y],
        ["CAN2M9", 1.5 * delta_x, 2.7 * delta_y],

        ["m9", 1.5 * delta_x, 3.3 * delta_y],

        ["M7BIEX", 0 * delta_x, 4.0 * delta_y],
        ["M9BIEX", 1.5 * delta_x, 4.0 * delta_y],

        ["m7_bi", 0 * delta_x, 5 * delta_y],
        ["m9_bi", 1.5 * delta_x, 5 * delta_y],

        ["M7EHC", 0 * delta_x, 6* delta_y],
        ["M9EHC", 1.5 * delta_x, 6 * delta_y],

        ["m7_lumen", 0 * delta_x, 7 * delta_y],
        ["m9_lumen", 1.5 * delta_x, 7 * delta_y],
    ]

    df = pd.DataFrame(positions, columns=["id", "x", "y"])
    df.set_index("id", inplace=True)

    return df


def canagliflozin_annotations(dx=200, dy=200) -> list:
    COLOR_PLASMA = "#FF796C"
    COLOR_LIVER = "#FFFFFF"
    COLOR_BILE = "#F5F5C6"
    COLOE_LUMEN = "#CFEFFF"

    kwargs = {
        "type": cyviz.AnnotationShapeType.ROUND_RECTANGLE,
        "opacity": 20,
        "border_color": "#000000",
        "border_thickness": 2,
    }

    xpos = -0.5 * dx
    width = 3.0 * dx
    delta_y = 0.5 * dy

    annotations = [
        cyviz.AnnotationShape(
            x_pos = xpos, y_pos= -0.5 * delta_y, width = width, height = 1.5 * delta_y,
            fill_color=COLOR_PLASMA, **kwargs
        ),
        cyviz.AnnotationShape(
            x_pos = xpos, y_pos = 1.0 * delta_y, width = width, height = 3.0 * delta_y,
            fill_color=COLOR_LIVER, **kwargs
        ),
        cyviz.AnnotationShape(
            x_pos = xpos, y_pos = 4.0 * delta_y, width = 0.7 * width, height = 2.0 * delta_y,
            fill_color=COLOR_BILE, **kwargs
        ),
        cyviz.AnnotationShape(
            x_pos = xpos, y_pos = 6.0 * delta_y, width = 0.7 * width, height = 1.5 * delta_y,
            fill_color=COLOE_LUMEN, **kwargs
        ),
    ]

    return annotations


if __name__ == "__main__":
    from pkdb_models.models.canagliflozin import MODEL_BASE_PATH
    from sbmlutils import cytoscape as cyviz

    results: FactoryResult = create_model(
        model=model_liver,
        filepath=MODEL_BASE_PATH / f"{model_liver.sid}.xml",
        sbml_level=3, sbml_version=2,
    )

    cyviz.visualize_sbml(sbml_path=results.sbml_path, delete_session=True)
    cyviz.apply_layout(layout=canagliflozin_layout())
    cyviz.add_annotations(annotations=canagliflozin_annotations())

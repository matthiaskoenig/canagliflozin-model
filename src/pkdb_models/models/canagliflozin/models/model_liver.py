"""Liver model of canagliflozin: glucuronidation, oxidation and biliary excretion."""

import numpy as np
from sbmlutils.factory import (
    Compartment,
    Model,
    Parameter,
    Reaction,
    Species,
    create_model,
)
from sbmlutils.metadata import (
    BQB,
    SBO,
)

from pkdb_models.models.canagliflozin.models import annotations, templates
from pkdb_models.models.canagliflozin.models.fits import FITS


class U(templates.U):
    """Units of the liver model."""


mid = "canagliflozin_liver"

_m = Model(
    sid=mid,
    name="Model for hepatic canagliflozin metabolism.",
    notes="""
    Model for the hepatic metabolism of canagliflozin.

    - Canagliflozin is mainly glucuronidated to the inactive O-glucuronides M7
      (UGT1A9) and M5 (UGT2B4); the oxidation to M9 by CYP3A4 is minor (about
      7 % of the dose) [Mamidi2014, Francke2015].
    - The metabolism is first order: canagliflozin is far below the Km of the
      enzymes, its pharmacokinetics are dose proportional from 50 to 300 mg
      [Devineni2015e].
    - The glucuronides are exported into the plasma and the bile; the
      glucuronides of the bile are hydrolysed to canagliflozin in the
      intestine, the source of most of the canagliflozin of the feces
      [Mamidi2014, Devineni2015b]. M9 is excreted into the bile.
    """
    + templates.terms_of_use,
    creators=templates.creators,
    units=U,
    model_units=templates.model_units,
    annotations=[
        *annotations.model,
        # tissue
        (BQB.OCCURS_IN, "fma/FMA:7197"),
        (BQB.OCCURS_IN, "bto/BTO:0000759"),
        (BQB.OCCURS_IN, "NCIT:C12392"),
        (BQB.HAS_PROPERTY, "NCIT:C79371"),  # Pharmacokinetics: Metabolism
        (BQB.HAS_PROPERTY, "NCIT:C79372"),  # Pharmacokinetics: Excretion
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
        "Vli",
        value=1.5,
        unit=U.liter,
        name="liver",
        constant=True,
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["li"],
        port=True,
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
        1.2825 * 0.9,  # 0.0171 [l/kg] * 75 kg * 0.9, replaced by the whole-body model
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
        port=True,
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
        port=True,
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
        port=True,
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
]

# the metabolites in the bile and the intestinal lumen
for sid, name in [("m5", "M5"), ("m7", "M7"), ("m9", "M9")]:
    _m.species.extend(
        [
            Species(
                f"{sid}_bi",
                initialConcentration=0.0,
                name=f"{name} (bile)",
                compartment="Vbi",
                substanceUnit=U.mmole,
                hasOnlySubstanceUnits=True,
                sboTerm=SBO.SIMPLE_CHEMICAL,
                annotations=annotations.species[sid],
                notes=f"""{name} of the bile in amount, which flows into the
                intestinal lumen.""",
            ),
            Species(
                f"{sid}_lumen",
                initialConcentration=0.0,
                name=f"{name} (lumen)",
                compartment="Vlumen",
                substanceUnit=U.mmole,
                hasOnlySubstanceUnits=False,
                sboTerm=SBO.SIMPLE_CHEMICAL,
                annotations=annotations.species[sid],
                port=True,
            ),
        ]
    )

_m.parameters.extend(
    [
        Parameter(
            "f_ugt1a9",
            1,
            U.dimensionless,
            name="scaling factor UGT1A9 activity",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            notes="""Scaling factor of the UGT1A9 activity of the liver (and the
            kidney, the parameter of the whole-body model replaces both).
            1.0: unchanged activity; < 1.0 decreased activity; >1.0 increased activity.
            """,
            port=True,
        ),
        Parameter(
            "f_ugt2b4",
            1,
            U.dimensionless,
            name="scaling factor UGT2B4 activity",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            notes="""Scaling factor of the UGT2B4 activity.
            1.0: unchanged activity; < 1.0 decreased activity; >1.0 increased activity.
            """,
        ),
        Parameter(
            "f_cyp3a4",
            1,
            U.dimensionless,
            name="scaling factor CYP3A4 activity",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            notes="""Scaling factor of the CYP3A4 activity.
            1.0: unchanged activity; < 1.0 decreased activity; >1.0 increased activity.
            """,
        ),
    ]
)

_m.reactions = [
    Reaction(
        sid="CANIM",
        name="canagliflozin import (CANIM)",
        equation="can_ext <-> can",
        compartment="Vmem",
        sboTerm=SBO.TRANSPORT_REACTION,
        pars=[
            Parameter(
                "CANIM_k",
                10.0,
                U.per_min,
                name="rate of the canagliflozin exchange of the liver",
                sboTerm=SBO.KINETIC_CONSTANT,
                notes="""Fast exchange: the uptake does not limit the metabolism,
                which is limited by the hepatic blood flow and the enzymes.""",
            ),
        ],
        formula=("CANIM_k * Vli * (can_ext - can)", U.mmole_per_min),
    ),
    Reaction(
        sid="CAN2M5",
        name="CAN2M5 (UGT2B4)",
        equation="can -> m5",
        compartment="Vli",
        sboTerm=SBO.BIOCHEMICAL_REACTION,
        pars=[
            Parameter(
                "CAN2M5_k",
                **FITS.parameter("LI__CAN2M5_k", unit=U.per_min),
                name="rate of the glucuronidation of canagliflozin to M5 (UGT2B4)",
                sboTerm=SBO.KINETIC_CONSTANT,
            ),
        ],
        formula=("f_ugt2b4 * CAN2M5_k * Vli * can", U.mmole_per_min),
    ),
    Reaction(
        sid="CAN2M7",
        name="CAN2M7 (UGT1A9)",
        equation="can -> m7",
        compartment="Vli",
        sboTerm=SBO.BIOCHEMICAL_REACTION,
        pars=[
            Parameter(
                "CAN2M7_k",
                **FITS.parameter("LI__CAN2M7_k", unit=U.per_min),
                name="rate of the glucuronidation of canagliflozin to M7 (UGT1A9)",
                sboTerm=SBO.KINETIC_CONSTANT,
            ),
        ],
        formula=("f_ugt1a9 * CAN2M7_k * Vli * can", U.mmole_per_min),
    ),
    Reaction(
        sid="CAN2M9",
        name="CAN2M9 (CYP3A4)",
        equation="can -> m9",
        compartment="Vli",
        sboTerm=SBO.BIOCHEMICAL_REACTION,
        pars=[
            Parameter(
                "CAN2M9_k",
                **FITS.parameter("LI__CAN2M9_k", unit=U.per_min),
                name="rate of the oxidation of canagliflozin to M9 (CYP3A4)",
                sboTerm=SBO.KINETIC_CONSTANT,
            ),
        ],
        formula=("f_cyp3a4 * CAN2M9_k * Vli * can", U.mmole_per_min),
    ),
    Reaction(
        sid="M5EX",
        name="M5 export (M5EX)",
        equation="m5 <-> m5_ext",
        compartment="Vmem",
        sboTerm=SBO.TRANSPORT_REACTION,
        pars=[
            Parameter(
                "M5EX_k",
                10.0,
                U.per_min,
                name="rate of the M5 exchange of the liver",
                sboTerm=SBO.KINETIC_CONSTANT,
                notes="""Fast exchange of the glucuronide between the liver and
                the plasma (efflux by MRP3, uptake by OATP1B), so that the
                glucuronide of the plasma is excreted into the bile as well.""",
            ),
        ],
        formula=("M5EX_k * Vli * (m5 - m5_ext)", U.mmole_per_min),
    ),
    Reaction(
        sid="M7EX",
        name="M7 export (M7EX)",
        equation="m7 <-> m7_ext",
        compartment="Vmem",
        sboTerm=SBO.TRANSPORT_REACTION,
        pars=[
            Parameter(
                "M7EX_k",
                10.0,
                U.per_min,
                name="rate of the M7 exchange of the liver",
                sboTerm=SBO.KINETIC_CONSTANT,
                notes="""Fast exchange of the glucuronide between the liver and
                the plasma, see `M5EX_k`.""",
            ),
        ],
        formula=("M7EX_k * Vli * (m7 - m7_ext)", U.mmole_per_min),
    ),
    Reaction(
        sid="M5BIEX",
        name="M5 biliary excretion (M5BIEX)",
        equation="m5 -> m5_bi",
        sboTerm=SBO.TRANSPORT_REACTION,
        compartment="Vapical",
        pars=[
            Parameter(
                "M5BIEX_k",
                **FITS.parameter("LI__M5BIEX_k", unit=U.per_min),
                name="rate of the biliary excretion of M5",
                sboTerm=SBO.KINETIC_CONSTANT,
                notes="""The non-renal elimination of the glucuronide: the
                exposure of M5 increases only 2.4-3.0 fold in severe renal
                impairment and end stage renal disease [Devineni2015c].""",
            ),
        ],
        formula=("M5BIEX_k * Vli * m5", U.mmole_per_min),
    ),
    Reaction(
        sid="M7BIEX",
        name="M7 biliary excretion (M7BIEX)",
        equation="m7 -> m7_bi",
        sboTerm=SBO.TRANSPORT_REACTION,
        compartment="Vapical",
        pars=[
            Parameter(
                "M7BIEX_k",
                **FITS.parameter("LI__M7BIEX_k", unit=U.per_min),
                name="rate of the biliary excretion of M7",
                sboTerm=SBO.KINETIC_CONSTANT,
                notes="""The non-renal elimination of the glucuronide, 2-3 % of
                the dose is M7 in the feces [Mamidi2014].""",
            ),
        ],
        formula=("M7BIEX_k * Vli * m7", U.mmole_per_min),
    ),
    Reaction(
        sid="M9BIEX",
        name="M9 biliary excretion (M9BIEX)",
        equation="m9 -> m9_bi",
        sboTerm=SBO.TRANSPORT_REACTION,
        compartment="Vapical",
        pars=[
            Parameter(
                "M9BIEX_k",
                0.1,
                U.per_min,
                name="rate of the biliary excretion of M9",
                sboTerm=SBO.KINETIC_CONSTANT,
                notes="""M9 is excreted into the bile (7-8 % of the dose in the
                feces, 2.4 % of the radioactivity of the plasma) [Mamidi2014];
                fast, it is not limiting.""",
            ),
        ],
        formula=("M9BIEX_k * Vli * m9", U.mmole_per_min),
    ),
]

# the bile flows into the intestinal lumen
for sid, name in [("m5", "M5"), ("m7", "M7"), ("m9", "M9")]:
    _m.reactions.append(
        Reaction(
            f"{sid.upper()}EHC",
            name=f"{name} bile flow into the intestine",
            equation=f"{sid}_bi -> {sid}_lumen",
            sboTerm=SBO.TRANSPORT_REACTION,
            compartment="Vlumen",
            formula=(f"{sid.upper()}BIEX", U.mmole_per_min),
        )
    )

model_liver = _m


if __name__ == "__main__":
    from pkdb_models.models.canagliflozin import MODEL_BASE_PATH

    create_model(
        model=model_liver,
        filepath=MODEL_BASE_PATH / f"{model_liver.sid}.xml",
        sbml_level=3,
        sbml_version=2,
    )

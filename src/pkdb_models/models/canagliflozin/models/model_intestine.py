"""Intestine model of canagliflozin: dissolution, absorption and fecal excretion."""

import numpy as np
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
    """Units of the intestine model."""

    per_hr = UnitDefinition("per_hr", "1/hr")
    mg_per_min = UnitDefinition("mg_per_min", "mg/min")


_m = Model(
    "canagliflozin_intestine",
    name="Model for canagliflozin absorption in the small intestine",
    notes="""
    # Model for canagliflozin absorption

    - Dissolution of the oral dose and absorption of canagliflozin; the
      fraction absorbed `F_can_abs` of the canagliflozin of the lumen is
      absorbed, the rest is excreted in the feces. The absolute
      bioavailability is 65 % (90 % CI 55-76 %) [Devineni2015b].
    - The glucuronides M5 and M7 of the bile are hydrolysed to canagliflozin in
      the lumen (enterohepatic circulation), the source of most of the
      canagliflozin of the feces (39-41.5 % of the dose). M7 which is not
      hydrolysed is excreted in the feces (2-3 % of the dose), M5 is not
      found in the feces [Mamidi2014, Devineni2015b]. M9 of the bile is
      excreted in the feces (7-8 %).
    - The absorption of canagliflozin is not changed by food: a high fat
      breakfast changes neither the AUC (+8 %) nor Cmax (+0.5 %)
      [Devineni2015e], so the model has no food effect.
    """
    + templates.terms_of_use,
    creators=templates.creators,
    units=U,
    model_units=templates.model_units,
    annotations=[
        *annotations.model,
        # tissue
        (BQB.OCCURS_IN, "bto/BTO:0000545"),  # gut
        (BQB.OCCURS_IN, "NCIT:C12736"),  # intestine
        (BQB.OCCURS_IN, "fma/FMA:7199"),  # intestine
        (BQB.OCCURS_IN, "bto/BTO:0000648"),  # intestine
        (BQB.HAS_PROPERTY, "NCIT:C79369"),  # Pharmacokinetics: Absorption
        (BQB.HAS_PROPERTY, "NCIT:C79372"),  # Pharmacokinetics: Excretion
    ],
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
        "Vapical",
        np.nan,
        name="apical membrane (intestinal membrane enterocytes)",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.m2,
        annotations=annotations.compartments["apical"],
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
        "can_stomach",
        metaId="meta_can_stomach",
        initialConcentration=0.0,
        compartment="Vstomach",
        substanceUnit=U.mmole,
        name="canagliflozin (stomach)",
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
]
for sid, name in [("m5", "M5"), ("m7", "M7"), ("m9", "M9")]:
    _m.species.append(
        Species(
            f"{sid}_lumen",
            initialConcentration=0.0,
            name=f"{name} (intestinal lumen)",
            compartment="Vlumen",
            substanceUnit=U.mmole,
            hasOnlySubstanceUnits=False,
            sboTerm=SBO.SIMPLE_CHEMICAL,
            annotations=annotations.species[sid],
            port=True,
        )
    )
# M5 is not found in the feces, the M5 of the bile is hydrolysed [Mamidi2014]
for sid, name in [("m7", "M7"), ("m9", "M9")]:
    _m.species.extend(
        [
            Species(
                f"{sid}_feces",
                initialConcentration=0.0,
                name=f"{name} (feces)",
                compartment="Vfeces",
                substanceUnit=U.mmole,
                hasOnlySubstanceUnits=True,
                sboTerm=SBO.SIMPLE_CHEMICAL,
                annotations=annotations.species[sid],
                port=True,
            ),
        ]
    )
_m.species.append(
    Species(
        "cantot_feces",
        initialConcentration=0.0,
        name="total canagliflozin (feces)",
        compartment="Vfeces",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=True,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["cantot"],
        notes="""Canagliflozin, M7 and M9 in the feces, compared with the
        total radioactivity in the feces.""",
        port=True,
    )
)

_m.parameters = [
    Parameter(
        "F_can_abs",
        **FITS.parameter("GU__F_can_abs", unit=U.dimensionless),
        constant=True,
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        name="fraction absorbed canagliflozin",
        notes="""
        Fraction absorbed: `F_can_abs` of the canagliflozin of the intestinal
        lumen is absorbed, `(1 - F_can_abs)` is excreted in the feces. The
        absolute bioavailability of 65 % [Devineni2015b] is the fraction
        absorbed times the fraction which escapes the hepatic first pass.
        """,
    ),
    Parameter(
        "CANABS_k",
        **FITS.parameter("GU__CANABS_k", unit=U.per_min),
        name="rate of canagliflozin absorption",
        sboTerm=SBO.KINETIC_CONSTANT,
    ),
    Parameter(
        "GLUHYD_k",
        **FITS.parameter("GU__GLUHYD_k", unit=U.per_min),
        name="rate of the hydrolysis of the glucuronides in the lumen",
        sboTerm=SBO.KINETIC_CONSTANT,
        notes="""
        Hydrolysis of M5 and M7 of the bile to canagliflozin by the
        beta-glucuronidases of the gut bacteria; the glucuronides are unstable
        in the feces [Mamidi2014].
        """,
    ),
    Parameter(
        "METEXC_k",
        0.001,
        unit=U.per_min,
        name="rate of the fecal excretion of the metabolites",
        sboTerm=SBO.KINETIC_CONSTANT,
        notes="""
        Transit of the metabolites of the bile through the intestine into the
        feces (half-life of about 12 hr); M5 is hydrolysed in the feces and
        excreted as canagliflozin.
        """,
    ),
]

_m.rules.append(
    AssignmentRule(
        "absorption",
        value="CANABS_k * Vlumen * can_lumen",
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
        name="CANEXC (feces)",
        compartment="Vlumen",
        equation="can_lumen -> can_feces",
        sboTerm=SBO.TRANSPORT_REACTION,
        formula=(
            "(1 dimensionless - F_can_abs) * absorption",
            U.mmole_per_min,
        ),
    ),
]
for sid, name in [("m5", "M5"), ("m7", "M7")]:
    _m.reactions.append(
        Reaction(
            sid=f"{sid.upper()}HYD",
            name=f"{name} hydrolysis ({sid.upper()}HYD)",
            compartment="Vlumen",
            equation=f"{sid}_lumen -> can_lumen",
            sboTerm=SBO.BIOCHEMICAL_REACTION,
            formula=(f"GLUHYD_k * Vlumen * {sid}_lumen", U.mmole_per_min),
        )
    )
# M5 of the bile which is not hydrolysed in the lumen is hydrolysed in the
# feces (no M5 in the feces, Mamidi2014): it leaves the lumen with the fecal
# transit and is fecal canagliflozin, so the lumen is no slow depot of M5
_m.reactions.append(
    Reaction(
        sid="M5EXC",
        name="M5 excretion (M5EXC, feces, hydrolysed to canagliflozin)",
        compartment="Vlumen",
        equation="m5_lumen -> can_feces",
        sboTerm=SBO.TRANSPORT_REACTION,
        formula=("METEXC_k * Vlumen * m5_lumen", U.mmole_per_min),
    )
)
for sid, name in [("m7", "M7"), ("m9", "M9")]:
    _m.reactions.append(
        Reaction(
            sid=f"{sid.upper()}EXC",
            name=f"{name} excretion ({sid.upper()}EXC, feces)",
            compartment="Vlumen",
            equation=f"{sid}_lumen -> {sid}_feces",
            sboTerm=SBO.TRANSPORT_REACTION,
            formula=(f"METEXC_k * Vlumen * {sid}_lumen", U.mmole_per_min),
        )
    )


_m.parameters.extend(
    [
        Parameter(
            "PODOSE_can",
            0,
            U.mg,
            constant=False,
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            name="oral dose canagliflozin [mg]",
            port=True,
        ),
        Parameter(
            "Ka_dis_can",
            2.0,
            U.per_hr,
            constant=True,
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            name="dissolution rate canagliflozin",
            port=True,
        ),
        Parameter(
            "Mr_can",
            444.518,
            U.g_per_mole,
            constant=True,
            name="Molecular weight canagliflozin [g/mole]",
            sboTerm=SBO.MOLECULAR_MASS,
            port=True,
        ),
    ]
)

# -------------------------------------
# Dissolution of tablet/dose in stomach
# -------------------------------------
_m.reactions.extend(
    [
        # fraction dose available for absorption from stomach
        Reaction(
            sid="dissolution_can",
            name="dissolution canagliflozin",
            formula=(
                "Ka_dis_can/60 min_per_hr * PODOSE_can/Mr_can",
                U.mmole_per_min,
            ),
            equation="can_stomach -> can_lumen",
            compartment="Vgu",
            notes="""Swallowing, dissolution of tablet, and transport into intestine.
            Overall process describing the rates of this processes.
            """,
        ),
    ]
)
_m.rate_rules.append(
    RateRule("PODOSE_can", "-dissolution_can * Mr_can", U.mg_per_min),
)
_m.rules.extend(
    [
        AssignmentRule(
            "cantot_feces",
            "can_feces + m7_feces + m9_feces",
            U.mmole,
            name="total canagliflozin (feces)",
        ),
    ]
)
model_intestine = _m


if __name__ == "__main__":
    from sbmlode import OdeSystem

    from pkdb_models.models.canagliflozin import MODEL_BASE_PATH

    results = create_model(
        filepath=MODEL_BASE_PATH / f"{model_intestine.sid}.xml",
        model=model_intestine,
        sbml_level=3,
        sbml_version=2,
    )

    # ODE equations
    ode_system = OdeSystem.from_sbml(results.sbml_path)
    ode_system.write(results.sbml_path.parent / f"{results.sbml_path.stem}.md")

"""The tolerances of the integrator for the canagliflozin model."""

from sbmlsim.model.tolerances import AbsoluteTolerance


def absolute_tolerance(substance: float, other: float) -> AbsoluteTolerance:
    """Get the absolute tolerance of the integrator for the canagliflozin model.

    The amounts of canagliflozin, its metabolites and glucose are species, the
    doses in mg (`PODOSE_can`, `IVDOSE_can`, `cum_dose_can`) and the integral
    of the renal threshold of glucose with its duration (`KI__RTG_int` [mM*min],
    `KI__RTG_time` [min]) are the targets of rate rules.

    Args:
        substance: tolerance of the species, amounts [mmole] and concentrations
            [mM] (multiplied by the volume of the compartment).
        other: tolerance of the targets of the rate rules [mg, mM*min, min].

    Returns:
        The absolute tolerance per kind of state.
    """
    return AbsoluteTolerance(amount=substance, concentration=substance, other=other)


#: the absolute tolerance of the simulation experiments. The intravenous
#: microdose of Devineni2015b (10 µg, 2.2e-5 mmole) has concentrations of about
#: 1e-7 mM, so the species get a tolerance of 1e-14 instead of 1e-10
ABSOLUTE_TOLERANCE = absolute_tolerance(substance=1e-14, other=1e-10)

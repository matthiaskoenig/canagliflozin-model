"""Simulation experiments which are not a single study."""

from .dose_dependency import DoseDependencyExperiment
from .renal_hepatic_impairment import HepaticRenalImpairment

__all__ = [
    "DoseDependencyExperiment",
    "HepaticRenalImpairment",
]

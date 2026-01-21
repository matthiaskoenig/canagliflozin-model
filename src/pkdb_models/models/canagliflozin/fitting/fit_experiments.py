"""Parameter fit problems for canagliflozin."""
from typing import Dict, List
from sbmlsim.fit.helpers import f_fitexp, filter_empty
from sbmlutils.console import console
from sbmlutils.log import get_logger

from sbmlsim.fit import FitExperiment, FitMapping

from pkdb_models.models.canagliflozin import CANAGLIFLOZIN_PATH, DATA_PATHS
from pkdb_models.models.canagliflozin.experiments.metadata import (
    Tissue, Route, Dosing, ApplicationForm, Health,
    Fasting, CanagliflozinMappingMetaData, Coadministration
)
from pkdb_models.models.canagliflozin.experiments.studies import *


logger = get_logger(__name__)


# --- Experiment classes ---
experiment_classes = [
    Chen2015,
    Devineni2012,
    Devineni2013,
    Devineni2014,
    Devineni2015,
    Devineni2015a,
    Devineni2015b,
    Devineni2015c,
    Devineni2015d,
    Devineni2015e,
    Devineni2016,
    Iijima2015,
    Inagaki2014,
    Kinoshita2015,
    Mamidi2014,
    Mohamed2019,
    Murphy2015,
    Sha2011,
    Sha2014,
    Sha2015,
    Tamborlane2018,
    Wattamwar2020
]

# --- Filters ---
def filter_control(fit_mapping_key: str, fit_mapping: FitMapping) -> bool:
    """Return control experiments/mappings."""

    metadata: CanagliflozinMappingMetaData = fit_mapping.metadata

    # only PO and IV (no SL, MU, RE)
    if metadata.route not in {Route.PO, Route.IV}:
        return False

    # filter coadminstration
    if metadata.coadministration != Coadministration.NONE:
        return False

    # filter health (no renal, cardiac impairment, ...)
    if metadata.health not in {Health.HEALTHY}:
        return False

    # filter multiple dosing (only single dosing)
    if metadata.dosing == Dosing.MULTIPLE:
        return False

    # only fasted subjects
    if metadata.fasting != Fasting.FASTED:
        return False

    # remove outliers
    if metadata.outlier is True:
        return False

    return True

def filter_control_pd(fit_mapping_key: str, fit_mapping: FitMapping) -> bool:
    """Return control experiments/mappings."""

    metadata: CanagliflozinMappingMetaData = fit_mapping.metadata

    # filter coadminstration
    if metadata.coadministration != Coadministration.NONE:
        return False

    # filter health (no renal, cardiac impairment, ...)
    if metadata.health not in {Health.HEALTHY, Health.T2DM, Health.HYPERTENSION}:
        return False

    # only fasted subjects
    if metadata.fasting != Fasting.FASTED:
        return False

    # remove outliers
    if metadata.outlier is True:
        return False

    return True



def filter_iv(fit_mapping_key: str, fit_mapping: FitMapping) -> bool:
    """Only iv data."""
    return fit_mapping.metadata.route == Route.IV

def filter_po(fit_mapping_key: str, fit_mapping: FitMapping) -> bool:
    """Only po data."""
    return fit_mapping.metadata.route == Route.PO

def filter_can(fit_mapping_key: str, fit_mapping: FitMapping) -> bool:
    """Only can data."""
    yid = "__".join(fit_mapping.observable.y.sid.split("__")[1:])
    if yid not in {
        "Afeces_can", "Aurine_can", "Cve_can",
        "Afeces_cantot",
        "Aurine_cantot",
        "Cve_cantot",
    }:
        return False
    return True

def filter_m5(fit_mapping_key: str, fit_mapping: FitMapping) -> bool:
    """Only m5 data."""
    yid = "__".join(fit_mapping.observable.y.sid.split("__")[1:])
    if yid not in {
        "Aurine_m5",
        "Cve_m5"
        }:
        return False
    return True

def filter_m7(fit_mapping_key: str, fit_mapping: FitMapping) -> bool:
    """Only m7 data."""
    yid = "__".join(fit_mapping.observable.y.sid.split("__")[1:])
    if yid not in {
        "Aurine_m7",
        "Afeces_m7",
        "Cve_m7"
        }:
        return False
    return True

def filter_m9(fit_mapping_key: str, fit_mapping: FitMapping) -> bool:
    """Only m9 data."""
    yid = "__".join(fit_mapping.observable.y.sid.split("__")[1:])
    if yid not in {
        "Afeces_m9",
        }:
        return False
    return True

def filter_uge(fit_mapping_key: str, fit_mapping: FitMapping) -> bool:
    """Only UGE data."""
    yid = "__".join(fit_mapping.observable.y.sid.split("__")[1:])
    if yid not in {
        "KI__UGE",
        }:
        return False
    return True

def filter_rtg(fit_mapping_key: str, fit_mapping: FitMapping) -> bool:
    """Only RTG data."""
    yid = "__".join(fit_mapping.observable.y.sid.split("__")[1:])
    if yid not in {
        "KI__RTG",
        }:
        return False
    return True

def filter_pharmacodynamics(fit_mapping_key: str, fit_mapping: FitMapping) -> bool:
    """Only pharmacodynamics data."""
    yid = "__".join(fit_mapping.observable.y.sid.split("__")[1:])
    if yid not in {
        "KI__RTG",
        "KI__UGE"
        }:
        return False
    return True

def filter_pharmacokinetics(fit_mapping_key: str, fit_mapping: FitMapping) -> bool:
    """Only pharmacokinetics data."""
    yid = "__".join(fit_mapping.observable.y.sid.split("__")[1:])
    if yid not in {
        "Afeces_can",
        "Aurine_can",
        "Cve_can",
        "Afeces_cantot",
        "Aurine_cantot",
        "Cve_cantot",
        "Aurine_m5",
        "Cve_m5",
        "Aurine_m7",
        "Afeces_m7",
        "Cve_m7",
        "Afeces_m9"
    }:
        return False
    return True


# --- Fit experiments ---
def f_fitexp_all():
    """All data."""
    return f_fitexp(
        experiment_classes,
        metadata_filters=filter_empty,
        base_path=CANAGLIFLOZIN_PATH,
        data_path=DATA_PATHS,
    )


def f_fitexp_control() -> Dict[str, List[FitExperiment]]:
    """Control data."""
    return f_fitexp(experiment_classes, metadata_filters=filter_control,
                    base_path=CANAGLIFLOZIN_PATH,
                    data_path=DATA_PATHS,
                    )


def f_fitexp_can_iv() -> Dict[str, List[FitExperiment]]:
    """Control data."""
    return f_fitexp(
        experiment_classes, metadata_filters=[filter_control, filter_iv, filter_can],
        base_path=CANAGLIFLOZIN_PATH,
        data_path=DATA_PATHS,
    )

def f_fitexp_can_po() -> Dict[str, List[FitExperiment]]:
    """Control data."""
    return f_fitexp(
        experiment_classes, metadata_filters=[filter_control, filter_po, filter_can],
        base_path=CANAGLIFLOZIN_PATH,
        data_path=DATA_PATHS,
    )

def f_fitexp_can() -> Dict[str, List[FitExperiment]]:
    """Control data."""
    return f_fitexp(
        experiment_classes, metadata_filters=[filter_control, filter_can],
        base_path=CANAGLIFLOZIN_PATH,
        data_path=DATA_PATHS,
    )

def f_fitexp_m5() -> Dict[str, List[FitExperiment]]:
    """Control data."""
    return f_fitexp(
        experiment_classes, metadata_filters=[filter_control, filter_m5],
        base_path=CANAGLIFLOZIN_PATH,
        data_path=DATA_PATHS,
    )

def f_fitexp_m7() -> Dict[str, List[FitExperiment]]:
    """Control data."""
    return f_fitexp(
        experiment_classes, metadata_filters=[filter_control, filter_m7],
        base_path=CANAGLIFLOZIN_PATH,
        data_path=DATA_PATHS,
    )

def f_fitexp_m9() -> Dict[str, List[FitExperiment]]:
    """Control data."""
    return f_fitexp(
        experiment_classes, metadata_filters=[filter_control, filter_m9],
        base_path=CANAGLIFLOZIN_PATH,
        data_path=DATA_PATHS,
    )

def f_fitexp_pharmacokinetics() -> Dict[str, List[FitExperiment]]:
    """Control data."""
    return f_fitexp(
        experiment_classes, metadata_filters=[filter_control, filter_pharmacokinetics],
        base_path=CANAGLIFLOZIN_PATH,
        data_path=DATA_PATHS,
    )


def f_fitexp_uge() -> Dict[str, List[FitExperiment]]:
    """Control data."""
    return f_fitexp(
        experiment_classes, metadata_filters=[filter_control_pd, filter_uge],
        base_path=CANAGLIFLOZIN_PATH,
        data_path=DATA_PATHS,
    )

def f_fitexp_rtg() -> Dict[str, List[FitExperiment]]:
    """Control data."""
    return f_fitexp(
        experiment_classes, metadata_filters=[filter_control_pd, filter_rtg],
        base_path=CANAGLIFLOZIN_PATH,
        data_path=DATA_PATHS,
    )

def f_fitexp_pharmacodynamics() -> Dict[str, List[FitExperiment]]:
    """Control data."""
    return f_fitexp(
        experiment_classes, metadata_filters=[filter_control_pd, filter_pharmacodynamics],
        base_path=CANAGLIFLOZIN_PATH,
        data_path=DATA_PATHS,
    )


if __name__ == "__main__":
    """Test construction of FitExperiments."""

    for f in [
        f_fitexp_all,
        # f_fitexp_control,
        # f_fitexp_can_iv,
        # f_fitexp_can,
        # f_fitexp_m5,
        # f_fitexp_m7,
        # f_fitexp_m9,
        # f_fitexp_rtg,
        # f_fitexp_pharmacokinetics,
        # f_fitexp_pharmacodynamics,
    ]:
        console.rule(style="white")
        console.print(f"{f.__name__}")
        fitexp = f()

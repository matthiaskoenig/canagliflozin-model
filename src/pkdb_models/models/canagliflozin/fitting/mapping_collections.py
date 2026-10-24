"""Parameter fit problems for canagliflozin.

The data of a fit is selected from the fit mappings of the studies in three
steps, see `sbmlsim.fit.helpers`: the filters on the metadata of the mappings
select the training data of the fit and exclude the rest, the outliers are
named once for all mappings and are the training data which is not usable, and
the validation data is the part of the data a fit is evaluated on but not
fitted to. The metadata of a mapping describes its curve, what a fit does with
the curve is decided here.

The training data are the oral and intravenous doses of healthy subjects and
of patients with type 2 diabetes with a normal renal function (the
pharmacokinetics of canagliflozin do not differ between them, Devineni2013,
Sha2011), single doses and exactly encoded multiple doses, fasted or without a
reported meal, without a coadministered drug. The validation data has five
parts, each a different question: the interactions (`INTERACTION_VALIDATION`,
the arms with a coadministered drug, simulated with factors which are not
fitted or without an interaction), the food (`FOOD_VALIDATION`, the model has
no food effect), the doses (`DOSE_VALIDATION`, the twice daily regimens and
the dose above the label), the populations (`POPULATION_VALIDATION`, the renal
impairment, which the model describes with the GFR, the Korean and the
pediatric patients) and the limitations (`LIMITATION_VALIDATION`, data of a
population, an assay or a process the model does not describe). The summaries
of data which is fitted one by one are excluded (`AGGREGATE_MAPPINGS`).
"""

from pkpdsim.fit import mapping_metadata, observable_filter
from pkpdsim.metadata import Coadministration, Fasting, Health
from sbmlsim.console import console
from sbmlsim.experiment import SimulationExperiment
from sbmlsim.fit import FitMapping, FitMappingCollection, MappingKind
from sbmlsim.fit.helpers import FitMappings, MappingFilter

from pkdb_models.models.canagliflozin import CANAGLIFLOZIN_PATH, DATA_PATHS
from pkdb_models.models.canagliflozin.experiments.studies import (
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
    Wattamwar2020,
)

#: the keys of fit mappings by study: the keys of the mappings are SIds of their
#: experiment, which two studies can share, so a named mapping is named with
#: its study
type NamedMappings = dict[str, set[str]]

EXPERIMENT_CLASSES: list[type[SimulationExperiment]] = [
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
    Wattamwar2020,
]

#: observables of the pharmacokinetics: canagliflozin, M5, M7 and M9 in
#: plasma, urine and feces
PK_OBSERVABLES: set[str] = {
    "Cve_can",
    "Cve_m5",
    "Cve_m7",
    "Cve_cantot",
    "Aurine_can",
    "Aurine_m5",
    "Aurine_m7",
    "Aurine_cantot",
    "Afeces_can",
    "Afeces_m7",
    "Afeces_m9",
    "Afeces_cantot",
}

#: observables of the pharmacodynamics: the urinary glucose excretion and the
#: renal threshold of glucose
PD_OBSERVABLES: set[str] = {"KI__UGE", "KI__RTG", "KI__RTG_mean"}

#: the health of the training data: canagliflozin has the same
#: pharmacokinetics in healthy subjects and in type 2 diabetes
TRAINING_HEALTH: frozenset[Health] = frozenset({Health.HEALTHY, Health.T2DM})

#: mappings which are not fitted, the data is not usable
OUTLIER_MAPPINGS: NamedMappings = {}

#: the validation of the interactions: the arms with a coadministered drug.
#: Rifampicin, probenecid and cyclosporine are simulated with factors of the
#: glucuronidation and of the renal transport which are not fitted
#: (`CanagliflozinSimulationExperiment.interactions`); metformin,
#: hydrochlorothiazide and teneligliptin are simulated without an interaction
#: (AUC ratios 0.9-1.12). `filter_training` lets them through for this reason,
#: every other coadministration stays out of the selection altogether
INTERACTION_VALIDATION: NamedMappings = {
    # hydrochlorothiazide at steady state, AUC 1.12 without a known mechanism
    "Devineni2014": {
        "fm_po_can300_hctz25_canagliflozin",
        "fm_po_can300_hctz25_glucose_cumulative_amount",
        "fm_po_can300_hctz25_glucose_renal_threshold",
    },
    # metformin at steady state, AUC 1.10
    "Devineni2015": {"fm_po_can300_met2000_canagliflozin"},
    # rifampicin (induction of UGT1A9, UGT2B4 and CYP3A4), probenecid
    # (inhibition of the UGTs and of the renal OAT) and cyclosporine
    # (inhibition of the UGTs)
    "Devineni2015d": {
        "fm_CAN300_RIF600_canagliflozin",
        "fm_CAN300_RIF600_canagliflozin_urine",
        "fm_CAN300_RIF600_M5_urine",
        "fm_CAN300_RIF600_M7_urine",
        "fm_CAN300_2_PRO500_canagliflozin",
        "fm_CAN300_2_PRO500_canagliflozin_urine",
        "fm_CAN300_2_PRO500_M5_urine",
        "fm_CAN300_2_PRO500_M7_urine",
        "fm_CAN300_3_CYC400_canagliflozin",
    },
    # teneligliptin at steady state
    "Kinoshita2015": {"fm_po_can200_tnl40"},
    # the fixed-dose combinations with metformin
    "Mohamed2019": {"fm_po_can50"},
    "Murphy2015": {"fm_po_can150_fasted", "fm_po_can150_fed"},
    "Wattamwar2020": {"fm_can150_fdc_fasted", "fm_can150_fdc_fed"},
}

#: the validation of the food: the model has no food effect (Devineni2015e,
#: AUC +8 %, Cmax +0.5 % with a high fat breakfast before the dose); the fed
#: arms with metformin are in `INTERACTION_VALIDATION`
FOOD_VALIDATION: NamedMappings = {
    "Devineni2015e": {"fm_po_can300_fed"},
}

#: the validation of the doses: the twice daily regimens and the dose above
#: the label, which the once daily doses of the training predict
DOSE_VALIDATION: NamedMappings = {
    # 400 mg once daily, above the label
    "Iijima2015": {
        "fm_po_can400_d1_canagliflozin",
        "fm_po_can400_d1_canagliflozin_urine",
        "fm_po_can400_d16_canagliflozin",
        "fm_po_can400_d16_canagliflozin_urine",
    },
    # 400 mg twice daily
    "Sha2011": {"fm_can400bid_uge", "fm_can400bid_rtg"},
    # 300 mg twice daily
    "Sha2014": {
        "fm_can300_bid_uge",
        "fm_can300_bid_rtg_baseline",
        "fm_can300_bid_rtg_intervals",
    },
}

#: the validation of the populations: the renal impairment, which the model
#: describes with the GFR (the renal excretion, the renal formation of M7 and
#: the filtered glucose), not fitted; the Korean patients with a lower body
#: weight and GFR; the obese pediatric patients on metformin
POPULATION_VALIDATION: NamedMappings = {
    "Devineni2015c": {
        f"fm_po_can200_{group}_renal_{name}"
        for group in ["mild", "moderate", "severe"]
        for name in [
            "canagliflozin",
            "M5",
            "M7",
            "canagliflozin_cumulative_amount",
            "M5_cumulative_amount",
            "M7_cumulative_amount",
            "glucose_cumulative_amount",
            "glucose_RT",
        ]
    },
    "Inagaki2014": {
        f"fm_po_can_{name}_{dose}_moderate"
        for dose in ["100", "200"]
        for name in [
            "canagliflozin",
            "M5",
            "M7",
            "canagliflozin_urine",
            "glucose_excretion_daily",
        ]
    },
    "Sha2014": {
        f"fm_{group}_{name}"
        for group in ["pbo_k", "can30_k"]
        for name in ["uge", "rtg_baseline", "rtg_d16"]
    },
    "Tamborlane2018": {
        f"fm_can{dose}_{name}"
        for dose in ["100", "300"]
        for name in ["plasma", "uge_baseline", "uge", "rtg"]
    },
}

#: the validation of the limitations of the model: valid data of a population,
#: an assay or a process the model does not describe, which would distort the
#: fitted parameters of the processes it does describe
LIMITATION_VALIDATION: NamedMappings = {
    # hepatic impairment: the cirrhosis model lowers all hepatic metabolism,
    # the glucuronidation of canagliflozin is spared in cirrhosis (AUC ratio
    # 1.10 and 1.09)
    "Devineni2015c": {
        f"fm_po_can300_{group}_hepatic_{name}"
        for group in ["mild", "moderate"]
        for name in [
            "canagliflozin",
            "M5",
            "M7",
            "canagliflozin_cumulative_amount",
            "M5_cumulative_amount",
            "M7_cumulative_amount",
        ]
    },
    # the change of the daily glucose excretion from day 0, compared with the
    # absolute excretion: the model has no glucose excretion of the patients
    # whose plasma glucose is above their own threshold
    "Iijima2015": {f"fm_po_can{dose}_uge_change" for dose in [25, 100, 200, 400]},
    # pooled plasma of radio-HPLC, detection limited late points without SD
    "Mamidi2014": {
        "fm_CAN188_canagliflozin_CAN188",
        "fm_CAN188_M5_CAN188",
        "fm_CAN188_M7_CAN188",
    },
    # the glucose excretion of placebo: the mean plasma glucose of the
    # patients is below their mean threshold, the excretion of the patients
    # above it is lost in a model of the mean (type 2 diabetes: 8-22 g/day
    # against below 1 g/day); in healthy subjects the excretion is close to
    # zero with an SD close to zero (Chen2015 0.009 g/day), which outweighs
    # every other mapping of the PD fit (weighted cost 6500-51000 at a
    # baseline threshold of 9.5-10.5 mM against 259 in total) and pushes the
    # baseline threshold to the upper bound of 13 mM
    "Chen2015": {"fm_po_can_CAN0_glucose_cumulative_amount"},
    "Devineni2012": {"fm_po_CAN0_glucose_cumulative_amount"},
    "Devineni2013": {"fm_po_can0_glucose_cumulative_amount"},
    "Sha2011": {"fm_can0_uge"},
    "Sha2014": {"fm_pbo_uge"},
}

#: the summaries of data which the fits use one by one, excluded from every
#: fit: a mean of subjects would count the subjects twice
AGGREGATE_MAPPINGS: NamedMappings = {
    # the threshold of the same urine and glucose with the GFR of the MDRD
    # equation; the one of the measured creatinine clearance is fitted
    "Chen2015": {
        "fm_po_can_CAN100_glucose_RT_MDRD",
        "fm_po_can_CAN300_glucose_RT_MDRD",
    },
    # the 24-hr mean threshold, the duration weighted mean of the intervals
    "Devineni2015c": {
        f"fm_po_can200_{group}_renal_glucose_RT_mean"
        for group in ["normal", "mild", "moderate", "severe"]
    },
}

#: the validation data by the question it answers
VALIDATION_QUESTIONS: dict[str, NamedMappings] = {
    "interactions": INTERACTION_VALIDATION,
    "food": FOOD_VALIDATION,
    "doses": DOSE_VALIDATION,
    "populations": POPULATION_VALIDATION,
    "limitations": LIMITATION_VALIDATION,
}

#: the validation data
VALIDATION_MAPPINGS: NamedMappings = {
    study: set().union(
        *(mappings.get(study, set()) for mappings in VALIDATION_QUESTIONS.values())
    )
    for mappings in VALIDATION_QUESTIONS.values()
    for study in mappings
}


def study(fit_mapping: FitMapping) -> str:
    """Get the study of a fit mapping, the id of its experiment."""
    return fit_mapping.reference.experiment.sid


def named(
    mappings: NamedMappings, fit_mapping_key: str, fit_mapping: FitMapping
) -> bool:
    """Check whether a fit mapping is one of the named mappings of its study."""
    return fit_mapping_key in mappings.get(study(fit_mapping), set())


def check_named(mappings: NamedMappings, fit_mappings: FitMappings) -> None:
    """Check that the named mappings are fit mappings of their studies.

    Raises:
        ValueError: for a study which is no experiment, or a key which is no fit
            mapping of its study.
    """
    for sid, keys in mappings.items():
        experiment = fit_mappings.experiments.get(sid)
        if experiment is None:
            raise ValueError(f"'{sid}' is no experiment of the fits.")
        if unknown := sorted(keys - set(experiment._fit_mappings)):
            raise ValueError(f"'{unknown}' are no fit mappings of '{sid}'.")


def filter_aggregates(fit_mapping_key: str, fit_mapping: FitMapping) -> bool:
    """No summaries of data which is fitted one by one, see `AGGREGATE_MAPPINGS`."""
    return not named(AGGREGATE_MAPPINGS, fit_mapping_key, fit_mapping)


def filter_training(fit_mapping_key: str, fit_mapping: FitMapping) -> bool:
    """The population of the training data, besides the validation data.

    Healthy subjects and patients with type 2 diabetes without an impairment,
    not fed, without a coadministered drug.
    """
    if named(VALIDATION_MAPPINGS, fit_mapping_key, fit_mapping):
        return True
    metadata = mapping_metadata(fit_mapping)
    return (
        metadata.health in TRAINING_HEALTH
        and metadata.fasting != Fasting.FED
        and metadata.coadministration == Coadministration.NONE
    )


#: Only the pharmacokinetic data.
filter_pk = observable_filter(PK_OBSERVABLES)

#: Only the pharmacodynamic data.
filter_pd = observable_filter(PD_OBSERVABLES)


def mapping_collections(
    filters: MappingFilter | list[MappingFilter],
    validation: NamedMappings = VALIDATION_MAPPINGS,
) -> dict[str, list[FitMappingCollection]]:
    """Select the data of a fit from the fit mappings of the studies.

    The filters select the training data, the mappings which fail them are
    excluded, and so are the summaries of data which is fitted one by one
    (`AGGREGATE_MAPPINGS`) and the data of another population, a meal or a
    coadministered drug (`filter_training`). The outliers are
    `OUTLIER_MAPPINGS`, the validation data is `VALIDATION_MAPPINGS`. Neither
    kind enters the cost; both are simulated and evaluated with the training
    data, so a report says how the fitted parameters describe data they were
    not fitted on.

    Args:
        filters: filters of the training data.
        validation: the keys of the validation data by study.

    Returns:
        The fit mapping collections of all kinds by experiment id.

    Raises:
        ValueError: if an outlier is a mapping of no study or of several.
    """
    fit_mappings = FitMappings(
        experiment_classes=EXPERIMENT_CLASSES,
        base_path=CANAGLIFLOZIN_PATH,
        data_path=DATA_PATHS,
    )
    for mappings in [OUTLIER_MAPPINGS, AGGREGATE_MAPPINGS, validation]:
        check_named(mappings, fit_mappings)
    # sbmlsim selects the outliers by their keys alone, which must name one
    # mapping of all studies
    outliers = {key for keys in OUTLIER_MAPPINGS.values() for key in keys}
    for key in outliers:
        studies = [
            sid
            for sid, experiment in fit_mappings.experiments.items()
            if key in experiment._fit_mappings
        ]
        if len(studies) != 1:
            raise ValueError(f"The outlier '{key}' is a mapping of {studies}.")
    selection = fit_mappings.select(
        filters=[
            *(filters if isinstance(filters, list) else [filters]),
            filter_aggregates,
            filter_training,
        ],
        outliers=outliers,
        validation=lambda key, fit_mapping: named(validation, key, fit_mapping),
        print_info=False,
    )
    # the counts per experiment and kind, not the single mappings
    selection.print(detail=False)
    # the validation mappings by the question they answer
    selected = {
        (sid, key)
        for sid, kinds in selection.kinds.items()
        for key, kind in kinds.items()
        if kind is MappingKind.VALIDATION
    }

    def pairs(mappings: NamedMappings) -> set[tuple[str, str]]:
        return {(sid, key) for sid, keys in mappings.items() for key in keys}

    console.print(
        "validation: "
        + ", ".join(
            f"{len(selected & pairs(mappings))} {question}"
            for question, mappings in VALIDATION_QUESTIONS.items()
        )
    )
    return selection.collections


def f_collections_pk() -> dict[str, list[FitMappingCollection]]:
    """Pharmacokinetic data: canagliflozin, M5, M7 and M9."""
    return mapping_collections([filter_pk])


def f_collections_pd() -> dict[str, list[FitMappingCollection]]:
    """Pharmacodynamic data: the glucose excretion and the renal threshold."""
    return mapping_collections([filter_pd])


if __name__ == "__main__":
    for f_collections in [f_collections_pk, f_collections_pd]:
        console.rule(title=f_collections.__name__, align="left", style="white")
        f_collections()

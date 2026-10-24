"""Base class of the canagliflozin simulation experiments."""

from collections.abc import Iterable, Mapping
from typing import ClassVar, NamedTuple

import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from pkpdsim.experiment import PKPDSimulationExperiment
from pkpdsim.impairment import RENAL_COLORS_END_STAGE, RENAL_FUNCTION_GFR
from sbmlsim import Q
from sbmlsim.units import Quantity

from pkdb_models.models.canagliflozin import MODEL
from pkdb_models.models.canagliflozin.canagliflozin_pk import calculate_canagliflozin_pk


class MolecularWeights(NamedTuple):
    """Molecular weights for the conversion of the data."""

    can: Quantity
    m5: Quantity
    m7: Quantity
    m9: Quantity
    glc: Quantity


class CanagliflozinSimulationExperiment(PKPDSimulationExperiment):
    """Base class of the canagliflozin simulation experiments."""

    pkpd_model = MODEL
    selections = (
        "time",
        # dosing
        "IVDOSE_can",
        "PODOSE_can",
        # venous
        "[Cve_can]",
        "[Cve_cantot]",
        "[Cve_m5]",
        "[Cve_m7]",
        "[KI__fpg]",
        "KI__pg",
        # urine
        "Aurine_can",
        "Aurine_cantot",
        "Aurine_m7",
        "Aurine_m5",
        "KI__glc_urine",
        "KI__GLCEX",
        "KI__UGE",
        "KI__RTG",
        "KI__RTG_mean",
        # feces
        "Afeces_can",
        "Afeces_m7",
        "Afeces_m9",
        "Afeces_cantot",
        # renal excretion rate
        "KI__CANEX",
        # cases
        "KI__f_renal_function",
        "KI__GFR",
        "f_cirrhosis",
    )

    font: ClassVar[dict[str, str | int]] = {"weight": "bold", "size": 22}
    scan_font: ClassVar[dict[str, str | int]] = {"weight": "bold", "size": 15}
    tick_font_size = 15

    # labels
    label_time = "Time"
    label_can = "Canagliflozin"
    label_cantot = "Total Canagliflozin"
    label_m5 = "M5"
    label_m7 = "M7"
    label_m9 = "M9"

    label_glc = "Glucose"
    label_uge = "UGE"
    label_rtg = "RTG"
    label_rtg_mean = "RTG (mean)"
    label_pg = "Mean Glucose"

    label_can_urine = label_can + " Urine"
    label_cantot_urine = label_cantot + "\nUrine"
    label_m5_urine = label_m5 + " Urine"
    label_m7_urine = label_m7 + " Urine"
    label_glc_urine = "Glucose Urine"

    label_can_feces = label_can + " Feces"
    label_m7_feces = label_m7 + " Feces"
    label_m9_feces = label_m9 + " Feces"
    label_cantot_feces = label_cantot + "\nFeces"

    labels: ClassVar[Mapping[str, str]] = {
        "time": "Time",
        "[Cve_can]": label_can,
        "[Cve_cantot]": label_cantot,
        "[Cve_m5]": label_m5,
        "[Cve_m7]": label_m7,
        "[KI__fpg]": label_glc,
        "Aurine_can": label_can_urine,
        "Aurine_m5": label_m5_urine,
        "Aurine_m7": label_m7_urine,
        "Aurine_cantot": label_cantot_urine,
        "KI__glc_urine": label_glc_urine,
        "KI__UGE": label_uge,
        "KI__RTG": label_rtg,
        "KI__RTG_mean": label_rtg_mean,
        "KI__pg": label_pg,
        "Afeces_can": label_can_feces,
        "Afeces_m7": label_m7_feces,
        "Afeces_m9": label_m9_feces,
        "Afeces_cantot": label_cantot_feces,
        "KI__CANEX": f"{label_can}\nExcretion Urine",
    }

    # units
    unit_time = "hr"
    unit_metabolite = "µM"
    unit_metabolite_urine = "µmole"
    unit_metabolite_feces = "µmole"

    unit_can = unit_metabolite
    unit_m5 = unit_metabolite
    unit_m7 = unit_metabolite
    unit_cantot = unit_metabolite
    unit_glc = "mM"
    unit_can_urine = unit_metabolite_urine
    unit_cantot_urine = unit_metabolite_urine
    unit_m5_urine = unit_metabolite_urine
    unit_m7_urine = unit_metabolite_urine
    unit_glc_urine = "mole"
    unit_uge = "g"
    unit_rtg = "mM"
    unit_can_feces = unit_metabolite_feces
    unit_m7_feces = unit_metabolite_feces
    unit_m9_feces = unit_metabolite_feces
    unit_cantot_feces = unit_metabolite_feces

    units: ClassVar[Mapping[str, str]] = {
        "time": unit_time,
        "[Cve_can]": unit_can,
        "[Cve_cantot]": unit_cantot,
        "[Cve_m5]": unit_m5,
        "[Cve_m7]": unit_m7,
        "[KI__fpg]": unit_glc,
        "Aurine_can": unit_can_urine,
        "Aurine_m5": unit_m5_urine,
        "Aurine_m7": unit_m7_urine,
        "Aurine_cantot": unit_cantot_urine,
        "KI__glc_urine": unit_glc_urine,
        "KI__UGE": unit_uge,
        "KI__RTG": unit_rtg,
        "KI__RTG_mean": unit_rtg,
        "KI__pg": unit_glc,
        "Afeces_can": unit_can_feces,
        "Afeces_m7": unit_m7_feces,
        "Afeces_m9": unit_m9_feces,
        "Afeces_cantot": unit_cantot_feces,
        "KI__CANEX": "µmol/min",
        "KI__GLCEX": "mmol/min",
    }

    # ----------- Fasting/food -----
    #: the model has no food effect: a high fat breakfast changes neither the
    #: AUC (+8 %) nor Cmax (+0.5 %) of 300 mg [Devineni2015e]; the fed arms
    #: are validation of it. The colors of the fed and fasted arms
    fasting_colors: ClassVar[dict[str, str]] = {
        "fasted": "black",
        "fed": "tab:red",
    }

    # ----------- Renal function --------------
    #: the classes of the GFR with the end stage renal disease; a measured
    #: creatinine clearance or GFR of X ml/min is the renal function X/101
    renal_map = RENAL_FUNCTION_GFR
    renal_colors = RENAL_COLORS_END_STAGE

    # ----------- Interactions --------------
    #: the activities of the enzymes and transporters of a coadministered drug
    #: (`f_ugt1a9` of liver and kidney, `LI__f_ugt2b4`, `LI__f_cyp3a4`,
    #: `KI__f_oat`), from the mechanism and the observed change of the
    #: exposure, never fitted; the arms are validation data [Devineni2015d]:
    #: - rifampicin 600 mg QD induces the UGTs and CYP3A4 (PXR), the AUC of
    #:   canagliflozin falls to 0.49 (Cmax 0.72)
    #: - probenecid 500 mg BID inhibits the UGTs and the renal secretion of the
    #:   glucuronides by OAT1/OAT3 (renal clearance of M5 -82 %, M7 -58 %), the
    #:   AUC of canagliflozin rises to 1.21
    #: - cyclosporine 400 mg inhibits the glucuronidation (and P-gp, which the
    #:   model has not), the AUC of canagliflozin rises to 1.23
    interactions: ClassVar[dict[str, dict[str, float]]] = {
        "rifampicin": {"f_ugt1a9": 1.8, "LI__f_ugt2b4": 1.8, "LI__f_cyp3a4": 4.0},
        "probenecid": {"f_ugt1a9": 0.9, "LI__f_ugt2b4": 0.9, "KI__f_oat": 0.3},
        "cyclosporine": {"f_ugt1a9": 0.8, "LI__f_ugt2b4": 0.8},
    }

    def interaction_changes(self, drug: str) -> dict[str, Quantity]:
        """Get the changes of the model of a coadministered drug.

        Args:
            drug: the drug, a key of `interactions`.

        Returns:
            The activities of the enzymes and transporters by parameter id.
        """
        return {
            pid: Q(value, "dimensionless")
            for pid, value in self.interactions[drug].items()
        }

    # ----------- Cmaps --------------
    @property
    def renal_cmap(self) -> LinearSegmentedColormap:
        """Colormap of the renal function, from impaired (dark) to normal (light)."""
        return LinearSegmentedColormap.from_list(
            "renal_function",
            ["#013817", "#006d2c", "#2ca25f", "#66c2a4", "#8AEDCC", "#D5F0E7"],
            N=256,
        )

    @property
    def cirrhosis_cmap(self) -> LinearSegmentedColormap:
        """Colormap of the degree of cirrhosis, from none (light) to severe (dark)."""
        return LinearSegmentedColormap.from_list(
            "cirrhosis_severity",
            ["#CEE2F0", "#74a9cf", "#2b8cbe", "#045a8d", "#003352"],
            N=256,
        )

    @property
    def doses_cmap(self) -> LinearSegmentedColormap:
        """Colormap of the doses, from low (light) to high (dark)."""
        return LinearSegmentedColormap.from_list(
            "doses",
            [
                "#FFE5B4",
                "#FFD18A",
                "#FFBD66",
                "#FFA53A",
                "#FF931F",
                "#FF7A16",
                "#FF660D",
                "#F4530A",
                "#E04407",
                "#CC3705",
            ],
            N=256,
        )

    # ----------- Dose map --------------
    # from light to dark with the hue turning from yellow over red to violet:
    # the lightness (OKLab) falls by 0.055 from dose to dose, adjacent doses
    # differ by about 7 (OKLab distance x 100)
    dose_colors: ClassVar[dict[float, str]] = {
        0: "black",
        10: "#F4D665",
        25: "#F9B946",
        30: "#FA9A3A",
        50: "#F47C44",
        100: "#E76157",
        200: "#D24C6A",
        300: "#B73C7A",
        400: "#973384",
        600: "#752D88",
        800: "#542783",
    }

    # ----------- Glucose map --------------
    glucose_colors: ClassVar[dict[float, str]] = {
        5: "black",
        6: "#F5B8D8",
        7: "#EFA3CB",
        8: "#E88EBE",
        9: "#E279B1",
        10: "#DB64A4",
        11: "#D44F97",
    }

    # keys are the parameters of the non-compartmental analysis of pkpdutils,
    # see `canagliflozin_pk`
    pk_labels: ClassVar[Mapping[str, str]] = {
        "auc_last": "AUCend",
        "auc_inf_obs": "AUCinf",
        "tmax": "Tmax",
        "cl_f": "Apparent Clearance",
        "cmax": "Cmax",
        "thalf": "Half-life",
        "lambda_z": "Elimination Rate",
        "vz_f": "Apparent Volume",
    }

    pk_units: ClassVar[Mapping[str, str]] = {
        "auc_last": "µmole/l*hr",
        "auc_inf_obs": "ng/ml*hr",
        "tmax": "hr",
        "cl_f": "ml/min",
        "cmax": "ng/ml",
        "thalf": "hr",
        "lambda_z": "1/hr",
        "vz_f": "l",
    }

    # molecular weights of canagliflozin, its metabolites and glucose
    Mr: ClassVar[MolecularWeights] = MolecularWeights(
        can=Q(444.518, "g/mole"),
        m5=Q(620.6, "g/mole"),
        m7=Q(620.6, "g/mole"),
        m9=Q(460.5, "g/mole"),
        glc=Q(180.16, "g/mole"),
    )

    def calculate_canagliflozin_pk(
        self, scans: Iterable[str] | None = None
    ) -> dict[str, pd.DataFrame]:
        """Calculate the pharmacokinetic parameters of the scans.

        Args:
            scans: keys of the simulations, all simulations by default.

        Returns:
            The parameters of every scan by simulation key, per draw of the
            fitted parameters in a run over them (`uncertainty`).
        """
        keys = self._simulations if scans is None else scans
        across = None if self.uncertainty is None else self.uncertainty.id
        return {
            key: calculate_canagliflozin_pk(
                experiment=self, res=self.results[f"task_{key}"], across=across
            )
            for key in keys
        }

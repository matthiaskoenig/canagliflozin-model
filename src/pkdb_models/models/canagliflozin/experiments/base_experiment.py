"""
Reusable functionality for multiple simulation experiments.
"""
from collections import namedtuple
from typing import Dict

import pandas as pd

from pkdb_models.models.canagliflozin import MODEL_PATH
from sbmlsim.experiment import SimulationExperiment
from sbmlsim.model import AbstractModel
from sbmlsim.task import Task

from matplotlib.colors import LinearSegmentedColormap

# Constants for conversion
from pkdb_models.models.canagliflozin.canagliflozin_pk import calculate_canagliflozin_pk

MolecularWeights = namedtuple("MolecularWeights", "can m5 m7 m9 glc")


class CanagliflozinSimulationExperiment(SimulationExperiment):
    """Base class for all SimulationExperiments."""

    font = {"weight": "bold", "size": 22}
    scan_font = {"weight": "bold", "size": 15}
    tick_font_size = 15
    legend_font_size = 9
    suptitle_font_size = 25

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

    label_can_urine = label_can + " Urine"
    label_cantot_urine = label_cantot + "\nUrine"
    label_m5_urine = label_m5 + " Urine"
    label_m7_urine = label_m7 + " Urine"
    label_glc_urine = "Glucose Urine"

    label_can_feces = label_can + " Feces"
    label_m7_feces = label_m7 + " Feces"
    label_m9_feces = label_m9 + " Feces"
    label_cantot_feces = label_cantot + "\nFeces"

    labels: Dict[str, str] = {
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

    units: Dict[str, str] = {
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
        "Afeces_can": unit_can_feces,
        "Afeces_m7": unit_m7_feces,
        "Afeces_m9": unit_m9_feces,
        "Afeces_cantot": unit_cantot_feces,
        "KI__CANEX": "µmol/min",
        "KI__GLCEX": "mmol/min",
    }

    # ----------- Fasting plasma glucose -----
    fpg_healthy = 5.0  # [mM]
    fpg_t2dm = 8  # [mM]
    fpg_t1dm = 8  # [mM]

    # ----------- Fasting/food -----
    fasting_map = {
        "fasted": 1.0,
        "fed": 0.9,
    }
    fasting_colors = {
        "fasted": "black",
        "fed": "tab:red",
    }

    # ----------- Renal map --------------
    renal_map = {
        "Normal renal function": 101.0 / 101.0,  # 1.0,
        "Mild renal impairment": 69.5 / 101.0,  # 0.69
        "Moderate renal impairment": 32.5 / 101.0,  # 0.32
        "Severe renal impairment": 19.5 / 101.0,  # 0.19
    }

    renal_colors = {
        "Normal renal function": "black",
        "Mild renal impairment": "#66c2a4",
        "Moderate renal impairment": "#2ca25f",
        "Severe renal impairment": "#006d2c",
    }

    # ----------- Cirrhosis map --------------
    cirrhosis_map = {
        "Control": 0,
        "Mild cirrhosis": 0.3994897959183674,  # CPT A
        "Moderate cirrhosis": 0.6979591836734694,  # CPT B
        "Severe cirrhosis": 0.8127551020408164,  # CPT C
    }
    cirrhosis_colors = {
        "Control": "black",
        "Mild cirrhosis": "#74a9cf",  # CPT A
        "Moderate cirrhosis": "#2b8cbe",  # CPT B
        "Severe cirrhosis": "#045a8d",  # CPT C
    }

    # ----------- Cmaps --------------
    @property
    def renal_cmap(self):
        return LinearSegmentedColormap.from_list(
            'renal_function',
            ["#013817", "#006d2c", "#2ca25f", "#66c2a4", "#8AEDCC", "#D5F0E7"],
            N=256
        )

    @property
    def cirrhosis_cmap(self):
        return LinearSegmentedColormap.from_list(
            'cirrhosis_severity',
            ["#CEE2F0", "#74a9cf", "#2b8cbe", "#045a8d", "#003352"],
            N=256
        )

    @property
    def doses_cmap(self):
        return LinearSegmentedColormap.from_list(
            'doses',
            ["#FFE5B4", "#FFD18A", "#FFBD66", "#FFA53A", "#FF931F",
             "#FF7A16","#FF660D", "#F4530A", "#E04407", "#CC3705"],
            N=256
        )
    # ----------- Dose map --------------

    dose_colors = {
        0: "black",
        10: "#FFE5B4",
        25: "#FFD18A",
        30: "#FFBD66",
        50: "#FFA53A",
        100: "#FF931F",
        200: "#FF7A16",
        300: "#FF660D",
        400: "#F4530A",
        600: "#E04407",
        800: "#CC3705",
    }

    # ----------- Glucose map --------------

    glucose_colors = {
        5:  "black",
        6: "#F5B8D8",
        7: "#EFA3CB",
        8: "#E88EBE",
        9: "#E279B1",
        10: "#DB64A4",
        11: "#D44F97",
    }


    pk_labels = {
        "auc": "AUCend",
        "aucinf": "AUCinf",
        "tmax": "Tmax",
        "cl": "Total Clearance",
        # "cl_renal": "Renal clearance",
        "cl_hepatic": "Hepatic Clearance",
        "cmax": "Cmax",
        "thalf": "Half-life",
        "kel": "kel",
        "vd": "vd",
        "Aurine_can": "Canagliflozin Urine",
    }

    pk_units = {
        "auc": "µmole/l*hr",
        "aucinf": "ng/ml*hr",
        "tmax": "hr",
        "cl": "ml/min",
        # "cl_renal": "ml/min",
        "cl_hepatic": "ml/min",
        "cmax": "ng/ml",
        "thalf": "hr",
        "kel": "1/hr",
        "vd": "l",
        "Aurine_can": "µmole",
    }

    def models(self) -> Dict[str, AbstractModel]:
        Q_ = self.Q_
        return {
            "model": AbstractModel(
                source=MODEL_PATH,
                language_type=AbstractModel.LanguageType.SBML,
                changes={},
            )
        }

    @staticmethod
    def _default_changes(Q_):
        """Default changes to simulations."""

        changes = {

            # ============ Pharmacokinetics ============
            # 20251123_221326__d6e52
            #	>>> !Optimal parameter 'Kp_can' within 5% of lower bound! <<<
            # 'ftissue_can': Q_(0.6668666338129446, 'l/min'),  # [0.01 - 10]
            # 'Kp_can': Q_(1.0025087991468038, 'dimensionless'),  # [1 - 50]
            # 'LI__CANIM_Vmax': Q_(4.026019530820937, 'mmol/min/l'),  # [0.001 - 100]
            # 'KI__CANEX_k': Q_(0.003745816607378912, '1/min'),  # [0.0001 - 1]
            # 'GU__CANABS_k': Q_(0.015932205013389062, '1/min'),  # [0.0001 - 1]
            # 'LI__CAN2M5_Vmax': Q_(0.05457677939498227, 'mmol/min/l'),  # [0.001 - 100]
            # 'LI__CAN2M5_Km_can': Q_(3.4933649233538513, 'mM'),  # [0.001 - 100]
            # 'LI__M5EX_Km_m5': Q_(1.2083379213672167, 'mM'),  # [0.01 - 100]
            # 'LI__M5EX_Vmax': Q_(61.874157129269065, 'mmol/min/l'),  # [0.01 - 200]
            # 'KI__M5EX_k': Q_(0.11095445697907381, '1/min'),  # [0.01 - 10]
            # 'ftissue_m5': Q_(0.0071365605418970465, 'l/min'),  # [0.001 - 10]
            # 'Kp_m5': Q_(2.5413820798849263, 'dimensionless'),  # [1 - 50]
            # 'LI__CAN2M7_Vmax': Q_(0.0012870703810990754, 'mmol/min/l'),  # [0.0001 - 100]
            # 'LI__M7EX_Vmax': Q_(0.3138528806886005, 'mmol/min/l'),  # [0.001 - 100]
            # 'KI__M7EX_k': Q_(0.18673479639197138, '1/min'),  # [0.1 - 10]
            # 'ftissue_m7': Q_(0.00015407040706317475, 'l/min'),  # [0.0001 - 10]
            # 'Kp_m7': Q_(39.878498027455976, 'dimensionless'),  # [1 - 250]
            # 'KI__f_CAN2M7': Q_(0.13941425128973972, 'dimensionless'),  # [0.1 - 10]
            # 'LI__CAN2M9_Vmax': Q_(0.005209079912015983, 'mmol/min/l'),  # [0.001 - 100]

            # ============ Pharmacodynamics ============
            # 20251125_214528__b00c9
            # >>> !Optimal parameter 'KI__RTG_base' within 5% of lower bound! <<<
            # 'KI__RTG_E50': Q_(1.672069145969639e-05, 'mM'),  # [1e-08 - 44]
            # 'KI__RTG_base': Q_(9.003931670662638, 'mM'),  # [9 - 14]
            # 'KI__RTG_max_inhibition': Q_(0.6272697309545409, 'dimensionless'),  # [0.2 - 1.0]
            # 'KI__RTG_m_fpg': Q_(0.7104098476982807, 'dimensionless'),  # [0.2 - 3]
        }

        return changes

    def default_changes(self: SimulationExperiment) -> Dict:
        """Default changes to simulations."""
        return CanagliflozinSimulationExperiment._default_changes(Q_=self.Q_)

    def tasks(self) -> Dict[str, Task]:
        if self.simulations():
            return {
                f"task_{key}": Task(model="model", simulation=key)
                for key in self.simulations()
            }
        return {}

    def data(self) -> Dict:
        self.add_selections_data(
            selections=[
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

                # urine
                "Aurine_can",
                "Aurine_cantot",
                "Aurine_m7",
                "Aurine_m5",

                "KI__glc_urine",
                "KI__GLCEX",
                "KI__UGE",
                "KI__RTG",

                # feces
                "Afeces_can",
                "Afeces_m7",
                "Afeces_m9",
                "Afeces_cantot",

                # renal excretion rate
                "KI__CANEX",

                # cases
                'KI__f_renal_function',
                'f_cirrhosis',
                'GU__f_absorption',
            ]
        )
        return {}

    @property
    def Mr(self):
        return MolecularWeights(
            can=self.Q_(444.518, "g/mole"),
            m5=self.Q_(620.6, "g/mole"),
            m7=self.Q_(620.6, "g/mole"),
            m9=self.Q_(460.5, "g/mole"),
            glc=self.Q_(180.16, "g/mole"),
        )

    def calculate_canagliflozin_pk(self, scans: list = []) -> Dict[str, pd.DataFrame]:
       """Calculate canagliflozin parameters for simulations (scans)"""
       pk_dfs = {}
       if scans:
           for sim_key in scans:
               xres = self.results[f"task_{sim_key}"]
               df = calculate_canagliflozin_pk(experiment=self, xres=xres)
               pk_dfs[sim_key] = df
       else:
           for sim_key in self._simulations.keys():
               xres = self.results[f"task_{sim_key}"]
               df = calculate_canagliflozin_pk(experiment=self, xres=xres)
               pk_dfs[sim_key] = df
       return pk_dfs

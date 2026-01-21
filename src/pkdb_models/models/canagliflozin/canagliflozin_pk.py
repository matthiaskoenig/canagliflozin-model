"""Canagliflozin pharmacokinetics."""
import pandas as pd

from pkdb_analysis.pk.pharmacokinetics import TimecoursePK
from sbmlsim.result import XResult
from sbmlutils.log import get_logger


logger = get_logger(__name__)


def calculate_canagliflozin_pk(
    experiment: "CanagliflozinSimulationExperiment",
    xres: XResult,
) -> pd.DataFrame:
    """Calculate canagliflozin parameters.

    Only works for 1D-scans.
    Currently only supporting po scans.
    """
    Q_ = experiment.Q_

    # scanned dimension
    scandim = xres._redop_dims()[0]

    dose_vec = Q_(xres["PODOSE_can"].values[0], xres.uinfo["PODOSE_can"])

    # calculate canagliflozin, M5, M7, M9, total canagliflozin pharmacokinetic parameters
    pk_dicts = list()
    substance_ids = ["can", "m5", "m7", "cantot"]
    substances = ["canagliflozin", "M5", "M7", "total canagliflozin"]

    t_vec: Q_ = xres.dim_mean("time")
    t_vec = Q_(t_vec.magnitude, xres.uinfo["time"])
    for k_dose, dose in enumerate(dose_vec):

        dose_mmole = dose / experiment.Mr.can

        for k_sid, sid in enumerate(substance_ids):
            substance = substances[k_sid]
            c_vec = Q_(
                xres[f"[Cve_{sid}]"].sel({scandim: k_dose}).values,
                xres.uinfo[f"[Cve_{sid}]"]
            )
            tcpk = TimecoursePK(
                time=t_vec,
                concentration=c_vec,
                substance=substance,
                dose=dose_mmole,
                ureg=experiment.ureg,
                min_treshold=1e8
            )

            pk_dict = tcpk.pk.to_dict()
            pk_dict["substance"] = substance
            pk_dicts.append(pk_dict)


        # # print(pk_dict)
        # pk = tcpk.pk
        #
        # # Calculate renal clearance as amount in urine/AUC plasma
        # aurine_vec = Q_(
        #     xres["Aurine_cap"].sel({scandim: k_dose}).values, xres.uinfo["Aurine_cap"]
        # )
        # pk_dict["Aurine_cap"] = aurine_vec.magnitude[-1]
        # pk_dict["Aurine_cap_unit"] = aurine_vec.units
        #
        # cl_renal = aurine_vec[-1] / pk.auc  # [mmole] / [mmole/l*min] = [l/min]
        # pk_dict["cl_renal"] = cl_renal.magnitude
        # pk_dict["cl_renal_unit"] = cl_renal.units
        #
        # pk_dict = tcpk.pk.to_dict()
        # # print(pk_dict)
        #
        # # Calculate renal clearance as amount in urine/AUC plasma
        # aurine_vec = Q_(
        #     xres["Aurine_capss"].sel({scandim: k_dose}).values, xres.uinfo["Aurine_capss"]
        # )
        # pk_dict["Aurine_capss"] = aurine_vec.magnitude[-1]
        # pk_dict["Aurine_capss_unit"] = aurine_vec.units
        # cl_renal = aurine_vec[-1] / pk.auc  # [mmole] / [mmole/l*min] = [l/min]
        # pk_dict["cl_renal"] = cl_renal.magnitude
        # pk_dict["cl_renal_unit"] = cl_renal.units
        #
        # pk_dict["substance"] = "captopril disulfide"
        # pk_dicts.append(pk_dict)

    return pd.DataFrame(pk_dicts)

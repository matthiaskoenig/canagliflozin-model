"""Pharmacokinetic parameters of the canagliflozin scans.

The parameters are the non-compartmental analysis of `pkpdutils`, named like
the variables of its `NCAResult` (e.g. `auc_inf_obs`, `cmax`, `thalf`,
`lambda_z`, `cl_f`, `vz_f`), with the unit of every parameter in
`<name>_unit`. Canagliflozin is analysed in plasma with its oral dose, its
glucuronides M5 and M7 and the total of canagliflozin, M5 and M7 without a
dose, i.e., without clearance and volume. The concentrations below
`LLOQ_FRACTION` of the maximum are below the limit of quantification, so that
the noise of the integrator is not the terminal phase.

A scan has one dimension, the scanned parameter; a run over the draws of the
fitted parameters (`run_simulation pkdb_models.models.canagliflozin
--uncertainty`)
adds the dimension of the draws. The parameters are calculated for every point
of every dimension, a row per point with its position along each dimension
(the columns `point` and, with draws, `draw`), see `summarize`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pandas as pd
from pkpdsim.pk import nca_frame, scan_nca
from pkpdsim.scan import scan_dimensions, start_values
from pkpdutils import NCAResult, Route
from sbmlsim import Q
from sbmlsim.result import ScanResult

if TYPE_CHECKING:
    from pkdb_models.models.canagliflozin.experiments.base_experiment import (
        CanagliflozinSimulationExperiment,
    )

#: oral dose of the scans
DOSE = "PODOSE_can"
#: the analytes (the names of the column `substance`) -> their concentration
#: and whether the dose is theirs
ANALYTES: dict[str, tuple[str, bool]] = {
    "canagliflozin": ("[Cve_can]", True),
    "M5": ("[Cve_m5]", False),
    "M7": ("[Cve_m7]", False),
    "total canagliflozin": ("[Cve_cantot]", False),
}
#: the limit of quantification relative to the maximal concentration
LLOQ_FRACTION = 1e-4


def _scan_dimension(res: ScanResult, across: str | None) -> str:
    """Get the dimension of a scan besides the draws `across`.

    Raises:
        ValueError: if the scan has not one dimension besides the draws.
    """
    dims = scan_dimensions(res, across)
    if len(dims) != 1:
        raise ValueError(
            f"A scan of one dimension is required, not of {dims} (draws: {across})."
        )
    return dims[0]


def _analysis(
    experiment: CanagliflozinSimulationExperiment, res: ScanResult, substance: str
) -> NCAResult:
    """Analyse an analyte at every point of a scan at once.

    Args:
        experiment: experiment of the scan, for the molecular weight.
        res: result of the scan.
        substance: the analyte, a key of `ANALYTES`.

    Returns:
        The analysis over the dimensions of the scan.
    """
    concentration, with_dose = ANALYTES[substance]
    if with_dose:
        # the dose in the substance unit of the concentration, which `cl_f`
        # and `vz_f` require
        dose = Q(start_values(res, DOSE).values, res.units[DOSE]) / experiment.Mr.can
        return scan_nca(
            res,
            concentration,
            dose=dose.to("mmole"),
            route=Route.ORAL,
            substance=substance,
            lloq_fraction=LLOQ_FRACTION,
        )
    # the parameters of the curve alone
    return scan_nca(
        res,
        concentration,
        dose=None,
        route=None,
        substance=substance,
        lloq_fraction=LLOQ_FRACTION,
    )


def calculate_canagliflozin_pk(
    experiment: CanagliflozinSimulationExperiment,
    res: ScanResult,
    across: str | None = None,
) -> pd.DataFrame:
    """Calculate the pharmacokinetic parameters of every simulation of a scan.

    Every analyte is analysed at all points of the scan at once (`scan_nca`).

    Args:
        experiment: experiment of the scan.
        res: result of the scan, a scan of the oral dose.
        across: the dimension of the draws of the fitted parameters, `None`
            for a scan without draws.

    Returns:
        One row per simulation of the scan and analyte, with its position
        (`point`, and `draw` with draws).
    """
    names = {_scan_dimension(res, across): "point"}
    if across is not None:
        names[across] = "draw"
    positions = list(names.values())
    dfs = []
    for substance in ANALYTES:
        df = nca_frame(_analysis(experiment, res, substance))
        df = df.drop(columns="nca_flags").rename(columns=names)
        df.insert(len(positions), "substance", substance)
        dfs.append(
            df[[*positions, *df.columns.drop(positions)]].sort_values(
                positions, kind="stable"
            )
        )
    return pd.concat(dfs, ignore_index=True)


def summarize(
    df: pd.DataFrame, key: str, quantiles: tuple[float, float]
) -> pd.DataFrame:
    """Get the median and the quantiles of a parameter over the draws of every point.

    Args:
        df: the parameters with the columns `point` and `draw`.
        key: the parameter.
        quantiles: the lower and the upper quantile.

    Returns:
        One row per point (the index), the columns `lower`, `median`, `upper`.
    """
    low, high = quantiles
    grouped = df.groupby("point")[key]
    return pd.DataFrame(
        {
            "lower": grouped.quantile(low),
            "median": grouped.median(),
            "upper": grouped.quantile(high),
        }
    ).astype(np.float64)

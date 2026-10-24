"""Canagliflozin: PBPK/PD model of canagliflozin and the urinary glucose excretion.

The paths of the model and its model object `MODEL`, which the commands
`run_simulation`, `run_fit`, `run_report` and `run_identifiability` of pkpdsim
run by its package `pkdb_models.models.canagliflozin`.
"""

from pathlib import Path

from pkpdsim.model import FigureSettings, PKPDModel, SimulatorSettings
from pkpdsim.release.settings import Author, ReleaseSettings

from pkdb_models.models.canagliflozin.tolerances import ABSOLUTE_TOLERANCE

CANAGLIFLOZIN_PATH = Path(__file__).parent

MODEL_BASE_PATH = CANAGLIFLOZIN_PATH / "models" / "output" / "models"
MODEL_PATH = MODEL_BASE_PATH / "canagliflozin_body_flat.xml"

# the subset of the PK-DB studies the model uses, see `data/collect_data.py`
DATA_PATH_BASE = CANAGLIFLOZIN_PATH / "data"
DATA_PATH_CANAGLIFLOZIN = DATA_PATH_BASE / "canagliflozin"
DATA_PATHS = [
    DATA_PATH_CANAGLIFLOZIN,
]

MODEL = PKPDModel(
    name="canagliflozin",
    package=__name__,
    title="Canagliflozin PBPK/PD model",
    path=CANAGLIFLOZIN_PATH,
    model_path=MODEL_PATH,
    data_paths=tuple(DATA_PATHS),
    archive_path=MODEL_BASE_PATH.parent / "canagliflozin_model.omex",
    factory=".models.factory:create_canagliflozin_models",
    experiments=".simulations:EXPERIMENTS",
    fit_definitions=".fitting.fitting:FIT_DEFINITIONS",
    simulator=SimulatorSettings(
        absolute_tolerance=ABSOLUTE_TOLERANCE, relative_tolerance=1e-10
    ),
    figures=FigureSettings(formats=("svg",), fig_dpi=300, legend_fontsize=10),
    fit_identifiability=True,
    # the adopted fits, their records are in models/output/fits
    fits=("PK_20261019_103422__858e3", "PD_20261019_201254__61546"),
    # the release of the model repository
    release=ReleaseSettings(
        title=(
            "Physiologically based pharmacokinetic/pharmacodynamic (PBPK/PD) model"
            " of canagliflozin"
        ),
        repository="matthiaskoenig/canagliflozin-model",
        doi="10.5281/zenodo.13759839",
        authors=(
            Author(
                "Tereshchuk, Vera",
                "0009-0009-3917-4482",
                "Moscow Institute of Physics and Technology; Freie Universität Berlin, Department of Mathematics and Computer Science, Institute of Computer Science, Data Science",
            ),
            Author(
                "Elias, Michelle",
                "0009-0005-7959-3164",
                "Humboldt-University Berlin, Institute for Theoretical Biology, Berlin",
            ),
            Author(
                "König, Matthias",
                "0000-0003-1725-179X",
                (
                    "Humboldt-Universität zu Berlin, Faculty of Life Sciences, Department of Biology, Institute of Theoretical Biology, Systems Medicine of the Liver; University of Stuttgart, Institute of Structural Mechanics and Dynamics in Aerospace Engineering; University of Southern Denmark, Clinical Pharmacology, Pharmacy and Environmental Medicine, Department of Public Health; University Hospital Schleswig-Holstein, Campus Lübeck, First Department of Medicine, Lübeck, Germany"
                ),
            ),
        ),
        keywords=(
            "model",
            "canagliflozin",
            "SGLT2 inhibitor",
            "urinary glucose excretion",
            "type 2 diabetes",
            "pharmacokinetics",
            "pharmacodynamics",
            "PBPK/PD",
            "physiologically based pharmacokinetic/ pharmacodynamic model",
            "SBML",
        ),
        docker_image="matthiaskoenig/canagliflozin",
        funding=(
            "Matthias König was supported by the Federal Ministry of Research, Technology and Space (BMFTR, Germany) within ATLAS by grant number 031L0304B and by the German Research Foundation (DFG) within the Research Unit Program FOR 5151 QuaLiPerF (Quantifying Liver Perfusion-Function Relationship in Complex Resection - A Systems Medicine Approach) by grant number 436883643 and by grant number 465194077 (Priority Programme SPP 2311, Subproject SimLivA). This work was supported by the BMBF-funded de.NBI Cloud within the German Network for Bioinformatics Infrastructure (de.NBI) (031A537B, 031A533A, 031A538A, 031A533B, 031A535A, 031A537C, 031A534A, 031A532B)."
        ),
        description=(
            "This repository provides the canagliflozin physiologically based"
            " pharmacokinetic/pharmacodynamic (PBPK/PD) model: the absorption,"
            " the tissue distribution, the hepatic and renal glucuronidation to"
            " M5 and M7, the oxidation to M9, the biliary excretion of the"
            " metabolites with the enterohepatic circulation and the renal"
            " excretion of canagliflozin, and the inhibition of SGLT2, which"
            " lowers the renal threshold of glucose and increases the urinary"
            " glucose excretion."
        ),
        first_year=2023,
    ),
)
"""The canagliflozin model: its commands, see `pkpdsim.model`."""

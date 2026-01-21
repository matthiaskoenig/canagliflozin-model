from pathlib import Path

CANAGLIFLOZIN_PATH = Path(__file__).parent

MODEL_BASE_PATH = CANAGLIFLOZIN_PATH / "models" / "results" / "models"
MODEL_PATH = MODEL_BASE_PATH / "canagliflozin_body_flat.xml"

RESULTS_PATH = CANAGLIFLOZIN_PATH / "results"
RESULTS_PATH_SIMULATION = RESULTS_PATH / "simulation"
RESULTS_PATH_FIT = RESULTS_PATH / "fit"

# DATA_PATH_BASE = CANAGLIFLOZIN_PATH.parents[3] / "pkdb_data" / "studies"

DATA_PATH_BASE = CANAGLIFLOZIN_PATH / "data"
DATA_PATH_CANAGLIFLOZIN = DATA_PATH_BASE / "canagliflozin"
DATA_PATHS = [
     DATA_PATH_CANAGLIFLOZIN,
]

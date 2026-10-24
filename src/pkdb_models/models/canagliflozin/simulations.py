"""The simulation experiments of the canagliflozin model and their groups.

They are the registry of `MODEL`, the experiments its commands simulate.
"""

from sbmlsim.experiment import SimulationExperiment

from pkdb_models.models.canagliflozin import MODEL
from pkdb_models.models.canagliflozin.experiments.misc import (
    DoseDependencyExperiment,
    HepaticRenalImpairment,
)
from pkdb_models.models.canagliflozin.experiments.scans import (
    CanagliflozinParameterScan,
)
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

EXPERIMENTS: dict[str, list[type[SimulationExperiment]]] = {
    "studies": [
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
    ],
    "dose_dependency": [
        Chen2015,
        Devineni2012,
        Devineni2013,
        Devineni2015a,
        Devineni2016,
        Iijima2015,
        Sha2011,
        Sha2014,
        Tamborlane2018,
    ],
    "hepatic_impairment": [
        Devineni2015c,
    ],
    "renal_impairment": [
        Devineni2015c,
        Inagaki2014,
    ],
    "food": [
        Devineni2015e,
        Murphy2015,
        Wattamwar2020,
    ],
    "misc": [
        DoseDependencyExperiment,
        HepaticRenalImpairment,
    ],
    "scans": [
        CanagliflozinParameterScan,
    ],
}
EXPERIMENTS["all"] = EXPERIMENTS["studies"] + EXPERIMENTS["misc"] + EXPERIMENTS["scans"]


if __name__ == "__main__":
    MODEL.run_simulation_experiments(EXPERIMENTS["all"], MODEL.simulation_dir / "all")

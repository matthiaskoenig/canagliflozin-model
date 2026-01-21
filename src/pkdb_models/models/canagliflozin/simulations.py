"""Run all canagliflozin simulation experiments."""

import shutil
from typing import List
from pathlib import Path
from sbmlutils.console import console
from sbmlutils import log
from pkdb_models.models.canagliflozin.helpers import run_experiments
from pkdb_models.models.canagliflozin.experiments.studies import *
from pkdb_models.models.canagliflozin.experiments.misc import *
from pkdb_models.models.canagliflozin.experiments.scans import *
import pkdb_models.models.canagliflozin as canagliflozin


logger = log.get_logger(__name__)

EXPERIMENTS = {
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
    "scan": [
            CanagliflozinParameterScan,
        ]
}

EXPERIMENTS["all"] = EXPERIMENTS["studies"] + EXPERIMENTS["misc"] + EXPERIMENTS["scan"]


def run_simulation_experiments(
        selected: str = None,
        experiment_classes: List = None,
        output_dir: Path = None
) -> None:
    """Run canagliflozin simulation experiments."""

    # Figure.fig_dpi = 50
    # Figure.legend_fontsize = 10

    # Determine which experiments to run
    if experiment_classes is not None:
        experiments_to_run = experiment_classes
        if output_dir is None:
            output_dir = canagliflozin.RESULTS_PATH_SIMULATION / "custom_selection"
    elif selected:
        # Using the 'selected' parameter
        if selected not in EXPERIMENTS:
            console.rule(style="red bold")
            console.print(
                f"[red]Error: Unknown group '{selected}'. Valid groups: {', '.join(EXPERIMENTS.keys())}[/red]"
            )
            console.rule(style="red bold")
            return
        experiments_to_run = EXPERIMENTS[selected]
        if output_dir is None:
            output_dir = canagliflozin.RESULTS_PATH_SIMULATION / selected
    else:
        console.print("\n[red bold]Error: No experiments specified![/red bold]")
        console.print("[yellow]Use selected='all' or selected='studies' or provide experiment_classes=[...][/yellow]\n")
        return

    # Run the experiments
    run_experiments(experiment_classes=experiments_to_run, output_dir=output_dir)

    # Collect figures into one folder
    figures_dir = output_dir / "_figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    for f in output_dir.glob("**/*.png"):
        if f.parent == figures_dir:
            continue
        try:
            shutil.copy2(f, figures_dir / f.name)
        except Exception as err:
            print(f"file {f.name} in {f.parent} fails, skipping. Error: {err}")
    console.print(f"Figures copied to: file://{figures_dir}", style="info")


if __name__ == "__main__":
    """
    # Run experiments

    # selected = "all"
    # selected = "misc"
    # selected = "studies"
    # selected = "pharmacodynamics"
    # selected = "dose_dependency"
    # selected = "food"
    # selected = "hepatic_impairment"
    # selected = "renal_impairment"
    # selected = "scan"
    """

    run_simulation_experiments(selected="all")
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.13759839.svg)](https://doi.org/10.5281/zenodo.13759839)
[![Release](https://img.shields.io/github/v/release/matthiaskoenig/canagliflozin-model)](https://github.com/matthiaskoenig/canagliflozin-model/releases)
[![Documentation](https://github.com/matthiaskoenig/canagliflozin-model/actions/workflows/docs.yml/badge.svg)](https://matthiaskoenig.github.io/canagliflozin-model/)
[![CI](https://github.com/matthiaskoenig/canagliflozin-model/actions/workflows/ci.yml/badge.svg)](https://github.com/matthiaskoenig/canagliflozin-model/actions/workflows/ci.yml)
[![Docker](https://img.shields.io/docker/v/matthiaskoenig/canagliflozin?sort=semver&label=docker)](https://hub.docker.com/r/matthiaskoenig/canagliflozin)
[![Python](https://img.shields.io/badge/python-3.14-blue)](https://www.python.org)
[![Code license: MIT](https://img.shields.io/badge/code%20license-MIT-blue)](https://opensource.org/license/MIT)
[![Model license: CC BY-SA 4.0](https://img.shields.io/badge/model%20license-CC%20BY--SA%204.0-lightgrey)](https://creativecommons.org/licenses/by-sa/4.0/)

# Physiologically based pharmacokinetic/pharmacodynamic (PBPK/PD) model of canagliflozin

This repository provides the canagliflozin physiologically based pharmacokinetic/pharmacodynamic (PBPK/PD) model: the absorption, the tissue distribution, the hepatic and renal glucuronidation to M5 and M7, the oxidation to M9, the biliary excretion of the metabolites with the enterohepatic circulation and the renal excretion of canagliflozin, and the inhibition of SGLT2, which lowers the renal threshold of glucose and increases the urinary glucose excretion.

Documentation: <https://matthiaskoenig.github.io/canagliflozin-model/>

## Quick start

```bash
git clone https://github.com/matthiaskoenig/canagliflozin-model.git && cd canagliflozin-model
uv sync
uv run run_simulation pkdb_models.models.canagliflozin --action all -r results
```

## How to cite

> Tereshchuk, V., Elias, M. & König, M. (2026). *Physiologically based pharmacokinetic/pharmacodynamic (PBPK/PD) model of canagliflozin*. Zenodo. https://doi.org/10.5281/zenodo.13759839

## License

* Source Code: [MIT](https://opensource.org/license/MIT)
* Documentation: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
* Models: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

&copy; 2023-2026 Vera Tereshchuk, Michelle Elias and Matthias König

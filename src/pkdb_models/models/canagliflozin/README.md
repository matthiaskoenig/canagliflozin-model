# Canagliflozin

Physiologically based pharmacokinetic/pharmacodynamic (PBPK/PD) model of the SGLT2 inhibitor canagliflozin: its oral absorption (dissolution and a fraction absorbed), its distribution into a fast and a deep tissue pool, its glucuronidation to M5 (UGT2B4) and M7 (UGT1A9, in the liver and the kidney) and its oxidation to M9 (CYP3A4), the biliary excretion of the metabolites with the hydrolysis of the glucuronides in the gut lumen (an enterohepatic circulation of canagliflozin), the renal excretion of canagliflozin and of the glucuronides relative to the glomerular filtration rate, and the fecal excretion. The pharmacodynamics are the inhibition of SGLT2 in the kidney, which lowers the renal threshold of glucose (RTG) and increases the urinary glucose excretion (UGE); the RTG rises with the fasting plasma glucose in type 2 diabetes, and the studies are compared with the mean RTG of a collection interval. The model describes renal and hepatic impairment and the interactions with rifampicin, probenecid and cyclosporine (literature based factors of the UGT and transporter activities).

The published version of the model is [canagliflozin-model](https://github.com/matthiaskoenig/canagliflozin-model) ([doi:10.5281/zenodo.13759839](https://doi.org/10.5281/zenodo.13759839)).

## Structure

- `__init__.py`: the paths of the model and its model object `MODEL` with its release metadata and its adopted fits, which the commands below run (pkpdsim).
- `models/`: the tissue models (`model_intestine.py`, `model_liver.py`, `model_kidney.py`) and the whole-body model (`model_body.py`). `models/factory.py` creates the SBML models, the flattened whole-body model which is simulated, the ODEs and the COMBINE archive in `models/output/`; the fitted values come from the adopted fits (`models/fits.py`, `models/output/fits/`).
- `experiments/`: the simulation experiments of the clinical studies (`studies/`), the dose and glucose dependency and the renal and hepatic impairment (`misc/`) and the parameter scans of the dose, the renal function and the cirrhosis, each for fasting plasma glucose levels of 5 to 11 mM (`scans/`, with the pharmacokinetic parameters of the studies in `scans/study_data/`). The fit mappings are described with the vocabulary of `pkpdsim.metadata`.
- `fitting/`: the fit problems of the pharmacokinetics (`PK`) and of the pharmacodynamics on the adopted pharmacokinetics (`PD`), their parameters and the selection of the training, validation and aggregate data.
- `sensitivity/`: the sensitivity analysis of the pharmacokinetics of canagliflozin, M5 and M7 and of the UGE.
- `canagliflozin_pk.py`: the pharmacokinetic parameters of the scans, the non-compartmental analysis of `pkpdutils`.
- `tolerances.py`: the absolute tolerances of the integrator per state.
- `simulations.py`: the simulation experiments and their groups, `MODEL` runs them.
- `tables/`: the tables of the studies and of the computational models.
- `data/`: the data of the studies, a subset of the PK-DB studies (`data/collect_data.py`).
- `TODO.md`: the open issues of the model.

## Commands

```bash
# models, simulations
run_simulation pkdb_models.models.canagliflozin --action factory
run_simulation pkdb_models.models.canagliflozin --action list_experiments
run_simulation pkdb_models.models.canagliflozin --action simulate --experiments all
run_simulation pkdb_models.models.canagliflozin --action simulate --experiments all --uncertainty

# fits, adoption of a fit, reports of stored parameters, identifiability
run_fit pkdb_models.models.canagliflozin --subset=PK --runs=3 --cores=3 --method=DE
run_fit pkdb_models.models.canagliflozin --subset=PD --runs=3 --cores=3 --method=DE
run_fit pkdb_models.models.canagliflozin --adopt PK_<fit id>
run_report pkdb_models.models.canagliflozin --subset=PK results/fit/PK_<fit id>/parameters.json
run_identifiability pkdb_models.models.canagliflozin --subset=PK results/fit/PK_<fit id>/parameters.json

# sensitivity analysis (local by default)
python -m pkdb_models.models.canagliflozin.sensitivity.sensitivity_analysis
```

The results are written into `results/` of the model.

## Adopted fits and uncertainty

The values of the fitted parameters come from the adopted fits of the model,
not from numbers in the code: `PK_20261019_103422__858e3` (15 parameters of
the absorption, the distribution, the metabolism and the excretion) and
`PD_20261019_201254__61546` (4 parameters of the renal threshold, fitted on the
adopted pharmacokinetics). `run_fit pkdb_models.models.canagliflozin --adopt <fit id>`
copies the record of a finished fit (its parameters, problem, profile
likelihood and Fisher information) into `models/output/fits/<fit id>/`, which is
tracked; the ids of the adopted fits are listed in `fits` of the model object
(`__init__.py`). The factory takes the fitted values and their uncertainty from
the records (`models/fits.py`) and writes the uncertainty into the SBML
(`distrib:uncertainty`). `run_simulation ... --uncertainty` runs the
experiments over draws of these distributions and draws the simulations as the
median with a band of quantiles into `results/simulation_uncertainty`. A refit
is: fit, adopt, replace the id in `fits`, rebuild the model. See the
documentation of the repository on fitting (`docs/fitting.md`).

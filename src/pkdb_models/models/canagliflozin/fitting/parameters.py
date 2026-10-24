"""Parameters to optimize in the canagliflozin fits, with their bounds.

The start values are the values of the model, chosen by hand against the
literature (Devineni2015b, Mamidi2014, Devineni2015c, Devineni2013). Not fitted:
the renal formation of M7 (`KI__CAN2M7_k`, see `parameters_pk_metabolism`),
the dissolution (`Ka_dis_can`), the fast exchanges of the liver (`LI__CANIM_k`,
`LI__M5EX_k`, `LI__M7EX_k`) and the biliary excretion of M9 (`LI__M9BIEX_k`,
fast, M9 has no other fate), the fecal transit of the metabolites
(`GU__METEXC_k`, which only the ratio to the hydrolysis identifies), the
fraction unbound (`KI__fu_can`), the hill coefficient (`KI__RTG_gamma`), the
splay of the glucose excretion (`KI__RTG_splay`) and the difference of the mean
to the fasting plasma glucose (`KI__PG_delta`, set by the studies).
"""

from sbmlsim.fit import FitParameter

#: the distribution and the absorption of canagliflozin: Vss 83.5 l, Vz 119 l,
#: tmax 1-2 hr, F 65 % (90 % CI 55-76 %) [Devineni2015b]; the fast tissue pool
#: (`ftissue_can`, `Kp_can`) gives the 6-fold fall within 1 hr after the
#: intravenous dose, the deep pool (`ftissue_deep_can`, `Kp_deep_can`) the
#: terminal half-life of 11-16 hr after the oral doses
parameters_pk_absorption_distribution: list[FitParameter] = [
    FitParameter(
        pid="ftissue_can",
        start_value=0.54,
        lower_bound=0.01,
        upper_bound=5,
        unit="l/min",
    ),
    FitParameter(
        pid="Kp_can",
        start_value=0.32,
        lower_bound=0.05,
        upper_bound=10,
        unit="dimensionless",
    ),
    FitParameter(
        pid="ftissue_deep_can",
        start_value=0.02,
        lower_bound=1e-3,
        upper_bound=0.5,
        unit="l/min",
    ),
    FitParameter(
        pid="Kp_deep_can",
        start_value=2.0,
        lower_bound=0.1,
        upper_bound=10,
        unit="dimensionless",
    ),
    FitParameter(
        pid="GU__CANABS_k",
        start_value=0.0088,
        lower_bound=1e-3,
        upper_bound=0.2,
        unit="1/min",
    ),
    FitParameter(
        pid="GU__F_can_abs",
        start_value=0.69,
        lower_bound=0.4,
        upper_bound=0.99,
        unit="dimensionless",
    ),
]

#: the metabolism of canagliflozin: the hepatic glucuronidation to M5 (UGT2B4)
#: and M7 (UGT1A9) and the oxidation to M9 (CYP3A4). The renal formation of M7
#: (`KI__CAN2M7_k`) is not fitted: the healthy data of the training cannot
#: tell it from the hepatic one, its value was set from the AUC ratios of the
#: renal impairment (Devineni2015c), which are validation data
parameters_pk_metabolism: list[FitParameter] = [
    FitParameter(
        pid="LI__CAN2M5_k",
        start_value=0.099,
        lower_bound=1e-4,
        upper_bound=1,
        unit="1/min",
    ),
    FitParameter(
        pid="LI__CAN2M7_k",
        start_value=0.015,
        lower_bound=1e-4,
        upper_bound=1,
        unit="1/min",
    ),
    FitParameter(
        pid="LI__CAN2M9_k",
        start_value=0.015,
        lower_bound=1e-5,
        upper_bound=0.5,
        unit="1/min",
    ),
]

#: the excretion: the biliary excretion of the glucuronides and their
#: hydrolysis in the intestine (the canagliflozin, M7 and M9 of the feces,
#: Mamidi2014), the renal excretion relative to the GFR (renal clearance of
#: canagliflozin 0.8-1.4 ml/min, of M5 31 ml/min, of M7 77 ml/min,
#: Devineni2015d)
parameters_pk_excretion: list[FitParameter] = [
    FitParameter(
        pid="LI__M5BIEX_k",
        start_value=0.098,
        lower_bound=1e-4,
        upper_bound=1,
        unit="1/min",
    ),
    FitParameter(
        pid="LI__M7BIEX_k",
        start_value=0.02,
        lower_bound=1e-4,
        upper_bound=1,
        unit="1/min",
    ),
    FitParameter(
        pid="GU__GLUHYD_k",
        start_value=0.0019,
        lower_bound=1e-4,
        upper_bound=1,
        unit="1/min",
    ),
    FitParameter(
        pid="KI__CANEX_f",
        start_value=1.0,
        lower_bound=0.2,
        upper_bound=5,
        unit="dimensionless",
    ),
    FitParameter(
        pid="KI__M5EX_f",
        start_value=0.35,
        lower_bound=0.05,
        upper_bound=2,
        unit="dimensionless",
    ),
    FitParameter(
        pid="KI__M7EX_f",
        start_value=0.75,
        lower_bound=0.05,
        upper_bound=2,
        unit="dimensionless",
    ),
]

#: the pharmacodynamics, the renal threshold of glucose (RTG): EC50 32 ng/ml
#: (19-45 ng/ml) and a maximal reduction of 64 % [Devineni2013], the RTG of
#: placebo 12.3-13.5 mM in type 2 diabetes (FPG about 10 mM) [Devineni2012,
#: Devineni2013]; the bounds of the EC50 are 0.44-89 ng/ml
parameters_pd: list[FitParameter] = [
    FitParameter(
        pid="KI__RTG_E50",
        start_value=4.5e-5,
        lower_bound=1e-6,
        upper_bound=2e-4,
        unit="mM",
    ),
    FitParameter(
        pid="KI__RTG_base",
        start_value=9.0,
        lower_bound=6,
        upper_bound=13,
        unit="mM",
    ),
    FitParameter(
        pid="KI__RTG_m_fpg",
        start_value=0.75,
        lower_bound=0.05,
        upper_bound=2,
        unit="dimensionless",
    ),
    FitParameter(
        pid="KI__RTG_max_inhibition",
        start_value=0.6,
        lower_bound=0.3,
        upper_bound=0.9,
        unit="dimensionless",
    ),
]

#: the pharmacokinetics of canagliflozin, M5, M7 and M9
parameters_pk: list[FitParameter] = (
    parameters_pk_absorption_distribution
    + parameters_pk_metabolism
    + parameters_pk_excretion
)

#: all fitted parameters
parameters_all: list[FitParameter] = parameters_pk + parameters_pd

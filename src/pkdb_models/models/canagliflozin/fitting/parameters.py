"""FitParameters for canagliflozin fitting."""
import copy

from sbmlsim.fit import FitParameter


parameters_can_iv = [
    # tissue distribution
    FitParameter(
        pid="ftissue_can",
        lower_bound=0.01,
        start_value=0.1,
        upper_bound=10,
        unit="l/min",
    ),
    FitParameter(
        pid="Kp_can",
        lower_bound=1,
        start_value=10,
        upper_bound=50,
        unit="dimensionless",
    ),

    # hepatic metabolism
    FitParameter(
        pid="LI__CANIM_Vmax",
        lower_bound=1E-3,
        start_value=1.0,
        upper_bound=100,
        unit="mmol/min/l",
    ),
    # kidney removal
    FitParameter(
        pid="KI__CANEX_k",
        lower_bound=1E-4,
        start_value=1E-1,
        upper_bound=1,
        unit="1/min",
    ),
]

parameters_can_po = [
    # absorption rate
    FitParameter(
        pid="GU__CANABS_k",
        lower_bound=1E-4,
        start_value=0.02,
        upper_bound=1,
        unit="1/min",
    ),
]

parameters_m5 = [
    # hepatic metabolism
    FitParameter(
        pid="LI__CAN2M5_Vmax",
        lower_bound=1E-3,
        start_value=0.1,
        upper_bound=100,
        unit="mmol/min/l",
    ),
    FitParameter(
        pid="LI__CAN2M5_Km_can",
        lower_bound=1E-3,
        start_value=0.1,
        upper_bound=100,
        unit="mM",
    ),
    FitParameter(
        pid="LI__M5EX_Km_m5",
        lower_bound=1E-2,
        start_value=0.1,
        upper_bound=100,
        unit="mM",
    ),
    FitParameter(
        pid="LI__M5EX_Vmax",
        lower_bound=1E-2,
        start_value=0.1,
        upper_bound=200,
        unit="mmol/min/l",
    ),
    # kidney removal
    FitParameter(
        pid="KI__M5EX_k",
        lower_bound=1E-2,
        start_value=0.1,
        upper_bound=10,
        unit="1/min",
    ),
    #tissue distribution
    FitParameter(
        pid="ftissue_m5",
        lower_bound=0.001,
        start_value=0.01,
        upper_bound=10,
        unit="l/min",
    ),
    FitParameter(
        pid="Kp_m5",
        start_value=10,
        lower_bound=1,
        upper_bound=50,
        unit="dimensionless",
    ),
]

parameters_m7 = [
    # hepatic metabolism
    FitParameter(
        pid="LI__CAN2M7_Vmax",
        lower_bound=1E-4,
        start_value=0.1,
        upper_bound=100,
        unit="mmol/min/l",
    ),
    FitParameter(
        pid="LI__M7EX_Vmax",
        lower_bound=1E-3,
        start_value=1.0,
        upper_bound=100,
        unit="mmol/min/l",
    ),
    # kidney removal
    FitParameter(
        pid="KI__M7EX_k",
        lower_bound=1E-1,
        start_value=1.0,
        upper_bound=10,
        unit="1/min",
    ),
    #tissue distribution
    FitParameter(
        pid="ftissue_m7",
        lower_bound=0.0001,
        start_value=0.001,
        upper_bound=10,
        unit="l/min",
    ),
    FitParameter(
        pid="Kp_m7",
        lower_bound=1,
        start_value=10,
        upper_bound=250,
        unit="dimensionless",
    ),
    # kidney metabolism
    FitParameter(
        pid="KI__f_CAN2M7",
        lower_bound=0.1,
        start_value=1.0,
        upper_bound=10,
        unit="dimensionless",
    ),
]

parameters_m9 = [
    # hepatic metabolism
    FitParameter(
        pid="LI__CAN2M9_Vmax",
        lower_bound=1E-3,
        start_value=1.0,
        upper_bound=100,
        unit="mmol/min/l",
    ),
]

parameters_rtg = [
    FitParameter(
        pid="KI__RTG_E50",
        lower_bound=0.1E-07,
        start_value=2.5e-06,
        upper_bound=50-6,
        unit="mM",
    ),
    FitParameter(
        pid="KI__RTG_base",
        lower_bound=9,
        start_value=12.5,
        upper_bound=14,
        unit="mM",
    ),
    # FitParameter(
    #     pid="KI__RTG_gamma",
    #     lower_bound=1,
    #     start_value=1.01,
    #     upper_bound=4,
    #     unit="dimensionless",
    # ),
    FitParameter(
        pid="KI__RTG_max_inhibition",
        lower_bound=0.2,
        start_value=0.75,
        upper_bound=1.0,
        unit="dimensionless",
    ),
    FitParameter(
        pid="KI__RTG_m_fpg",
        lower_bound=0.2,
        start_value=1,
        upper_bound=3,
        unit="dimensionless",
    ),

]

parameters_can = parameters_can_iv + parameters_can_po


parameters_pharmacokinetics = parameters_can + parameters_m5 + parameters_m7 + parameters_m9
parameters_pharmacodynamics = parameters_rtg

parameters_control = parameters_can + parameters_m5 + parameters_m7 + parameters_m9 + parameters_rtg
parameters_all = parameters_control

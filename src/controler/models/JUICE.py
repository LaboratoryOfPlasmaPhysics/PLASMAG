from src.model.strategies.strategy_lib.Noise import PSD_R_cr, PSD_R_cr_filtered, PSD_R_Coil, PSD_R_Coil_filtered, \
    PSD_Flicker, PSD_e_en, PSD_e_en_filtered, PSD_e_in, PSD_e_in_filtered, PSD_Total, PSD_Total_filtered, \
    Display_all_PSD, NEMI, Display_all_PSD_filtered, NEMI_FIltered, NEMI_FIlteredv2, NEMI_FIlteredv3, PSD_R_cr_V2, \
    PSD_R_cr_filtered_V2, PSD_R_Coil_V2, PSD_R_Coil_filtered_V2, PSD_Flicker_V2, PSD_e_en_V2, PSD_e_en_filtered_V2, \
    PSD_e_in_V2, PSD_e_in_filtered_V2
from src.model.strategies.strategy_lib.CLTF import CLTF_Strategy_Filtered, \
    CLTF_Strategy_Non_Filtered_legacy, Display_CLTF_OLTF
from src.model.strategies.strategy_lib.OLTF import OLTF_Strategy_Non_Filtered, OLTF_Strategy_Filtered
from src.model.strategies.strategy_lib.TF_ASIC import TF_ASIC_Stage_1_Strategy_linear,  \
    TF_ASIC_Stage_2_Strategy_linear, TF_ASIC_Strategy_linear

from src.model.strategies.strategy_lib.Nz import AnalyticalNzStrategy
from src.model.strategies.strategy_lib.capacitance import AnalyticalCapacitanceStrategy
from src.model.strategies.strategy_lib.frequency import FrequencyVectorStrategy
from src.model.strategies.strategy_lib.impedance import AnalyticalImpedanceStrategy
from src.model.strategies.strategy_lib.inductance import AnalyticalInductanceStrategy
from src.model.strategies.strategy_lib.lambda_strategy import AnalyticalLambdaStrategy
from src.model.strategies.strategy_lib.mu_app import AnalyticalMu_appStrategy
from src.model.strategies.strategy_lib.resistance import AnalyticalResistanceStrategy
from src.model.strategies.strategy_lib.SPICE import SPICE_test, SPICE_op_Amp_gain, SPICE_op_Amp_transcient, \
    SPICE_impedance


STRATEGY_MAP = {
    "resistance": {
        "default": AnalyticalResistanceStrategy,
        "strategies": [AnalyticalResistanceStrategy]
    },
    "frequency_vector": {
        "default": FrequencyVectorStrategy,
        "strategies": [FrequencyVectorStrategy]
    },
    "Nz": {
        "default": AnalyticalNzStrategy,
        "strategies": [AnalyticalNzStrategy]
    },
    "mu_app": {
        "default": AnalyticalMu_appStrategy,
        "strategies": [AnalyticalMu_appStrategy]
    },

     "lambda_param": {
          "default": AnalyticalLambdaStrategy,
          "strategies": [AnalyticalLambdaStrategy]
     },

    "inductance": {
        "default": AnalyticalInductanceStrategy,
        "strategies": [AnalyticalInductanceStrategy]
    },
    "capacitance": {
        "default": AnalyticalCapacitanceStrategy,
        "strategies": [AnalyticalCapacitanceStrategy]
    },
    "impedance": {
        "default": AnalyticalImpedanceStrategy,
        "strategies": [AnalyticalImpedanceStrategy]
    },
    "TF_ASIC_Stage_1": {
        "default": TF_ASIC_Stage_1_Strategy_linear,
        "strategies": [TF_ASIC_Stage_1_Strategy_linear]
    },
    "TF_ASIC_Stage_2": {
        "default": TF_ASIC_Stage_2_Strategy_linear,
        "strategies": [TF_ASIC_Stage_2_Strategy_linear]
    },
    "TF_ASIC_linear": {
        "default": TF_ASIC_Strategy_linear,
        "strategies": [TF_ASIC_Strategy_linear]
    },
    "OLTF_Non_filtered": {
        "default": OLTF_Strategy_Non_Filtered,
        "strategies": [OLTF_Strategy_Non_Filtered]
    },
    "OLTF_Filtered": {
        "default": OLTF_Strategy_Filtered,
        "strategies": [OLTF_Strategy_Filtered]
    },
    "CLTF_Non_filtered": {
        "default": CLTF_Strategy_Non_Filtered_legacy,
        "strategies": [CLTF_Strategy_Non_Filtered_legacy]
    },
    "CLTF_Filtered": {
        "default": CLTF_Strategy_Filtered,
        "strategies": [CLTF_Strategy_Filtered]
    },
    "Display_CLTF_OLTF": {
        "default": Display_CLTF_OLTF,
        "strategies": [Display_CLTF_OLTF]
    },
    "PSD_R_cr": {
        "default": PSD_R_cr,
        "strategies": [PSD_R_cr, PSD_R_cr_V2]
    },
    "PSD_R_cr_filtered": {
        "default": PSD_R_cr_filtered,
        "strategies": [PSD_R_cr_filtered,PSD_R_cr_filtered_V2]
    },
    "PSD_R_Coil": {
        "default": PSD_R_Coil,
        "strategies": [PSD_R_Coil, PSD_R_Coil_V2]
    },
    "PSD_R_Coil_filtered": {
        "default": PSD_R_Coil_filtered,
        "strategies": [PSD_R_Coil_filtered, PSD_R_Coil_filtered_V2]
    },
    "PSD_Flicker": {
        "default": PSD_Flicker,
        "strategies": [PSD_Flicker, PSD_Flicker_V2]
    },
    "PSD_e_en": {
        "default": PSD_e_en,
        "strategies": [PSD_e_en, PSD_e_en_V2]
    },
    "PSD_e_en_filtered": {
        "default": PSD_e_en_filtered,
        "strategies": [PSD_e_en_filtered, PSD_e_en_filtered_V2]
    },
    "PSD_e_in": {
        "default": PSD_e_in,
        "strategies": [PSD_e_in, PSD_e_in_V2]
    },
    "PSD_e_in_filtered": {
        "default": PSD_e_in_filtered,
        "strategies": [PSD_e_in_filtered, PSD_e_in_filtered_V2]
    },
    "PSD_Total": {
        "default": PSD_Total,
        "strategies": [PSD_Total]
    },
    "PSD_Total_filtered": {
        "default": PSD_Total_filtered,
        "strategies": [PSD_Total_filtered]
    },
    "Display_all_PSD": {
        "default": Display_all_PSD,
        "strategies": [Display_all_PSD]
    },
    "Display_all_PSD_filtered": {
        "default": Display_all_PSD_filtered,
        "strategies": [Display_all_PSD_filtered]
    },
    "NEMI": {
        "default": NEMI,
        "strategies": [NEMI]
    },
    "NEMI_FIltered": {
        "default": NEMI_FIltered,
        "strategies": [NEMI_FIltered,NEMI_FIlteredv2, NEMI_FIlteredv3]
    },

}

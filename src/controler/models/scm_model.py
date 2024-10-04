from src.model.strategies.strategy_lib.Noise import NSD_R_cr, NSD_R_Coil, NSD_Flicker, \
    NSD_e_en, NSD_e_in, NSD_Total, Display_all_NSD, Display_all_PSD, Display_all_NSD_filtered, \
    Display_all_PSD_filtered, NEMI, NSD_normalisation
from src.model.strategies.strategy_lib.CLTF import CLTF_Strategy, Display_CLTF_OLTF, \
    Display_CLTF_OLTF_filtered
from src.model.strategies.strategy_lib.OLTF import OLTF_Strategy
from src.model.strategies.strategy_lib.TF_ASIC import TF_ASIC_Stage_1_Strategy_linear,  \
    TF_ASIC_Stage_2_Strategy_linear, TF_ASIC_Strategy_linear

from src.model.strategies.strategy_lib.Nz import AnalyticalNzStrategy, AnalyticalNzDiaboloStrategy
from src.model.strategies.strategy_lib.capacitance import AnalyticalCapacitanceStrategy
from src.model.strategies.strategy_lib.frequency import FrequencyVectorStrategy
from src.model.strategies.strategy_lib.impedance import AnalyticalImpedanceStrategy
from src.model.strategies.strategy_lib.inductance import AnalyticalInductanceStrategy
from src.model.strategies.strategy_lib.lambda_strategy import LukoschusAnalyticalLambdaStrategy, \
    ClercAnalyticalLambdaStrategy
from src.model.strategies.strategy_lib.mu_app import AnalyticalMu_appStrategy, AnalyticalMu_appDiaboloStrategy
from src.model.strategies.strategy_lib.resistance import AnalyticalResistanceStrategy, MultiLayerResistanceStrategy


STRATEGY_MAP = {
    "resistance": {
        "default": AnalyticalResistanceStrategy,
        "strategies": [AnalyticalResistanceStrategy, MultiLayerResistanceStrategy]
    },
    "frequency_vector": {
        "default": FrequencyVectorStrategy,
        "strategies": [FrequencyVectorStrategy]
    },
    "Nz": {
        "default": AnalyticalNzStrategy,
        "strategies": [AnalyticalNzStrategy, AnalyticalNzDiaboloStrategy]
    },
    "mu_app": {
        "default": AnalyticalMu_appStrategy,
        "strategies": [AnalyticalMu_appStrategy, AnalyticalMu_appDiaboloStrategy]
    },
    "lambda_param": {
          "default": LukoschusAnalyticalLambdaStrategy,
          "strategies": [LukoschusAnalyticalLambdaStrategy, ClercAnalyticalLambdaStrategy]
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
    "OLTF": {
        "default": OLTF_Strategy,
        "strategies": [OLTF_Strategy]
    },
    "CLTF": {
        "default": CLTF_Strategy,
        "strategies": [CLTF_Strategy]
    },
    "Display_CLTF_OLTF": {
        "default": Display_CLTF_OLTF,
        "strategies": [Display_CLTF_OLTF, Display_CLTF_OLTF_filtered]
    },
    "NSD_normalisation": {
        "default": NSD_normalisation,
        "strategies": [NSD_normalisation]
    },
    "PSD_R_cr": {
        "default": NSD_R_cr,
        "strategies": [NSD_R_cr]
    },
    "PSD_R_Coil": {
        "default": NSD_R_Coil,
        "strategies": [NSD_R_Coil]
    },
    "PSD_Flicker": {
        "default": NSD_Flicker,
        "strategies": [NSD_Flicker]
    },
    "PSD_e_en": {
        "default": NSD_e_en,
        "strategies": [NSD_e_en]
    },
    "PSD_e_in": {
        "default": NSD_e_in,
        "strategies": [NSD_e_in]
    },
    "PSD_Total": {
        "default": NSD_Total,
        "strategies": [NSD_Total]
    },
    "Display_all_PSD": {
        "default": Display_all_NSD,
        "strategies": [Display_all_NSD, Display_all_PSD]
    },
    "Display_all_PSD_filtered": {
        "default": Display_all_NSD_filtered,
        "strategies": [Display_all_NSD_filtered, Display_all_PSD_filtered]
    },
    "NEMI": {
        "default": NEMI,
        "strategies": [NEMI]
    },
}

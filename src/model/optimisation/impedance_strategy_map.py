from src.model.strategies.strategy_lib.Nz import AnalyticalNzStrategy
from src.model.strategies.strategy_lib.capacitance import AnalyticalCapacitanceStrategy
from src.model.strategies.strategy_lib.frequency import FrequencyVectorStrategy
from src.model.strategies.strategy_lib.impedance import AnalyticalImpedanceStrategy
from src.model.strategies.strategy_lib.inductance import AnalyticalInductanceStrategy
from src.model.strategies.strategy_lib.lambda_strategy import AnalyticalLambdaStrategy
from src.model.strategies.strategy_lib.mu_app import AnalyticalMu_appStrategy
from src.model.strategies.strategy_lib.resistance import AnalyticalResistanceStrategy, AnalyticalResistanceStrategyv2

IMPEDANCE_STRATEGY_MAP = {
    "resistance": {
        "default": AnalyticalResistanceStrategy,
        "strategies": [AnalyticalResistanceStrategy, AnalyticalResistanceStrategyv2]
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
    }
}
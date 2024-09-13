import numpy as np
from src.model.input_parameters import InputParameters
from src.model.strategies import CalculationStrategy


class LukoschusAnalyticalLambdaStrategy(CalculationStrategy):
    """Lukoschus's analytical computation of the coefficient factor

    .. math::

        \lambda = (\\frac{l_{coil}}{l_{core}})^\\frac{-2}{5}

    with:
        - :math:`l_{coil}` : the length of the coil
        - :math:`l_{core}` : the length of the core

    """

    def calculate(self, dependencies: dict, parameters: InputParameters):
        len_coil = parameters.data['len_coil']
        len_core = parameters.data['len_core']
        result = (len_coil / len_core) ** (-2 / 5)

        return {
            "data": result,
            "labels": ["Lambda"],
            "units": [""]
        }

    @staticmethod
    def get_dependencies():
        return ['len_coil', 'len_core']


class ClercAnalyticalLambdaStrategy(CalculationStrategy):
    """Clerc's analytical computation of the coefficient factor

    .. math::

        \lambda = 1.85 - 1.1 * \\frac{l_{coil}}{l_{core}}

    with:
        - :math:`l_{coil}` : the length of the coil
        - :math:`l_{core}` : the length of the core

    """

    def calculate(self, dependencies: dict, parameters: InputParameters):
        len_coil = parameters.data['len_coil']
        len_core = parameters.data['len_core']
        result = 1.85 - 1.1 * (len_coil / len_core)

        return {
            "data": result,
            "labels": ["Lambda"],
            "units": [""]
        }

    @staticmethod
    def get_dependencies():
        return ['len_coil', 'len_core']

import numpy as np
from src.model.input_parameters import InputParameters
from src.model.strategies import CalculationStrategy


class AnalyticalMu_appStrategy(CalculationStrategy):
    """Analytical model of the effective permeability for a cylindrical core

    .. math::
        \\mu_{app} = \\frac{\mu_r}{1 + (N_z . (\\mu_r - 1))}

    with:
        - :math:`\\mu_r` : the relative permeability of the core material
        - :math:`N_z` : the demagnetizing factor, related to the shape of the material

    """

    def calculate(self, dependencies: dict, parameters: InputParameters):
        mu_r = parameters.data["mu_r"]
        Nz = dependencies["Nz"]["data"]
        result = mu_r / (1 + (Nz * (mu_r - 1)))

        return {
            "data": result,
            "labels": ["Mu_app"],
            "units": [""]
        }

    @staticmethod
    def get_dependencies():
        return ["mu_r", "Nz"]


class AnalyticalMu_appDiaboloStrategy(CalculationStrategy):
    """Analytical model of the effective permeability for a diabolo core

    .. math::
        \\mu_{app} = \\frac{\mu_r}{1 + (N_z . \\frac{d_{core}^2}{d_{diabolo}^2} . (\\mu_r - 1))}

    with:
        - :math:`\\mu_r` : the relative permeability of the core material
        - :math:`N_z` : the demagnetizing factor, related to the shape of the material
        - :math:`d_{core}` : the diameter of the center of the core
        - :math:`d_{diabolo}` : the diameter of the end surface of the diabolo

    """

    def calculate(self, dependencies: dict, parameters: InputParameters):
        mu_r = parameters.data['mu_r']
        Nz = dependencies['Nz']['data']
        diam_core = parameters.data['diam_core']
        diabolo_diam_core = parameters.data['diabolo_diam_core']

        result = mu_r / (1 + Nz * (diam_core ** 2) * (mu_r - 1) / (diabolo_diam_core ** 2))

        return {
            "data": result,
            "labels": ["Mu_app"],
            "units": [""]
        }

    @staticmethod
    def get_dependencies():
        return ['mu_r', 'Nz', 'diam_core', 'diabolo_diam_core']

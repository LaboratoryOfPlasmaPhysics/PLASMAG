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

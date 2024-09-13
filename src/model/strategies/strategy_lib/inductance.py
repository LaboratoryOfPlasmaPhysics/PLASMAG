from numpy import pi
from scipy.constants import mu_0
from src.model.input_parameters import InputParameters
from src.model.strategies import CalculationStrategy


class AnalyticalInductanceStrategy(CalculationStrategy):
    """Analytical model of the inductance

    .. math::

        L = \\mu_0 . \\mu_{app} . N_{spire}^2 . S . \lambda_{param} / l_{core}

    with:
        - :math:`\\mu_0` : permeability of vacuum
        - :math:`\\mu_{app}` : apparent permeability of the core material
        - :math:`N_{spire}` : number of spire of the coil
        - :math:`S = \pi . R_s^2` le section of the core
        - :math:`R_s` : radius of the spires
        - :math:`\lambda_{param}` : coefficient factor (see lambda node for more information)
        - :math:`l_{core}` : the length of the core

    """
    def calculate(self, dependencies: dict, parameters: InputParameters):
        nb_spire = parameters.data["nb_spire"]
        ray_spire = parameters.data["ray_spire"]
        len_core = parameters.data["len_core"]

        lambda_param = dependencies["lambda_param"]["data"]
        mu_app = dependencies["mu_app"]["data"]

        section = pi * ray_spire ** 2
        result = mu_0 * mu_app * (nb_spire ** 2) * section * lambda_param / len_core

        return {
            "data": result,
            "labels": ["Inductance"],
            "units": ["H"]
        }

    @staticmethod
    def get_dependencies():
        return ["nb_spire", "ray_spire", "len_core", "lambda_param", "mu_app"]

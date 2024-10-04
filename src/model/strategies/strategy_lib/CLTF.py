from numpy import pi, column_stack

from src.model.input_parameters import InputParameters
from src.model.strategies import CalculationStrategy


class CLTF_Strategy(CalculationStrategy):
    """Analytical model of the Closed Loop Transfer Function (CLTF)

    .. math::

        CLTF(f) = \\frac{\mu_{app} . N_s . S . \omega . H_1(f)}{\sqrt{(1 - L . C . \omega^2)^2 + \omega^2 . (R . C + \\frac{M . H_1(f)}{R_{CR}})^2}}

    With:
        - :math:`\\mu_{app}` : apparent permeability of the core material
        - :math:`N_{spire}` : number of spire of the coil
        - :math:`S = \pi . R_s^2` le section of the core
        - :math:`R_s` : radius of the spires
        - :math:`\omega = 2 \pi f`
        - :math:`f` : frequency
        - :math:`H_1` : transfer function of the ASIC's stage 1
        - :math:`R` : resistance of the coil
        - :math:`L` : inductance of the coil
        - :math:`C` : capacitance of the coil
        - :math:`M` : Mutual inductance (coupling factor between the main coil and the feedback coil)
        - :math:`R_{CR}` : resistance of the counter-reaction coil

    """

    def calculate(self, dependencies: dict, parameters: InputParameters):
        nb_spire = parameters.data["nb_spire"]
        ray_spire = parameters.data["ray_spire"]
        mu_app = dependencies["mu_app"]["data"]
        frequency_vector = dependencies["frequency_vector"]["data"]
        nsd_normalisation = dependencies["NSD_normalisation"]["data"][:, 1]
        h2 = dependencies["TF_ASIC_Stage_2"]["data"][:, 1]

        omega = 2 * pi * frequency_vector
        section = pi * ray_spire ** 2
        numerator = nb_spire * section * mu_app * omega
        cltf = numerator / nsd_normalisation
        cltf_filtered = cltf * h2

        results = column_stack((frequency_vector, cltf, cltf_filtered))

        return {
            "data": results,
            "labels": ["Frequency", "CLTF", "CLTF_filtered"],
            "units": ["Hz", "m^2/s", "m^2/s"]
        }

    @staticmethod
    def get_dependencies():
        return ["nb_spire", "ray_spire", "mu_app", "frequency_vector", "TF_ASIC_Stage_2",
                "NSD_normalisation"]


class Display_CLTF_OLTF(CalculationStrategy):

    def calculate(self, dependencies: dict, parameters: InputParameters):
        frequency_vector = dependencies["CLTF"]["data"][:, 0]
        cltf = dependencies["CLTF"]["data"][:, 1]
        oltf = dependencies["OLTF"]["data"][:, 1]

        result = column_stack((frequency_vector, cltf, oltf))
        return {
            "data": result,
            "labels": ["Frequency", "CLTF", "OLTF"],
            "units": ["Hz", "m^2/s", "m^2/s"]
        }

    @staticmethod
    def get_dependencies():
        return ["CLTF", "OLTF"]


class Display_CLTF_OLTF_filtered(CalculationStrategy):

    def calculate(self, dependencies: dict, parameters: InputParameters):
        frequency_vector = dependencies["CLTF"]["data"][:, 0]
        cltf = dependencies["CLTF"]["data"][:, 2]
        oltf = dependencies["OLTF"]["data"][:, 2]

        result = column_stack((frequency_vector, cltf, oltf))
        return {
            "data": result,
            "labels": ["Frequency", "CLTF_filtered", "OLTF_filtered"],
            "units": ["Hz", "m^2/s", "m^2/s"]
        }

    @staticmethod
    def get_dependencies():
        return ["CLTF", "OLTF"]

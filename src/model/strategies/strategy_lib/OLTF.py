from numpy import pi, column_stack
from src.model.input_parameters import InputParameters
from src.model.strategies import CalculationStrategy


class OLTF_Strategy(CalculationStrategy):
    """Analytical model of the Open Loop Transfer Function (OLTF)

    .. math::

        OLTF(f) = \\frac{\mu_{app} . N_s . S . \omega . H_1(f)}{\sqrt{(1 - L . C . \omega^2)^2 + (\omega . R . C)^2}}

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

    """
    def calculate(self, dependencies: dict, parameters: InputParameters):
        nb_spire = parameters.data["nb_spire"]
        ray_spire = parameters.data["ray_spire"]
        mu_app = dependencies["mu_app"]["data"]
        frequency_vector = dependencies["frequency_vector"]["data"]
        h2 = dependencies["TF_ASIC_Stage_2"]["data"][:, 1]
        L = dependencies["inductance"]["data"]
        C = dependencies["capacitance"]["data"]
        R = dependencies["resistance"]["data"]

        omega = 2 * pi * frequency_vector
        section = pi * ray_spire ** 2
        numerator = nb_spire * section * mu_app * omega
        denominator = ((1 - L * C * omega**2) ** 2 + (R * C * omega) ** 2) ** 0.5
        oltf = numerator / denominator
        oltf_filtered = oltf * h2

        results = column_stack((frequency_vector, oltf, oltf_filtered))

        return {
            "data": results,
            "labels": ["Frequency", "OLTF", "OLTF_filtered"],
            "units": ["Hz", "m^2/s", "m^2/s"]
        }

    @staticmethod
    def get_dependencies():
        return ["nb_spire", "ray_spire", "mu_app", "frequency_vector", "TF_ASIC_Stage_2",
                "inductance", "capacitance", "resistance"]

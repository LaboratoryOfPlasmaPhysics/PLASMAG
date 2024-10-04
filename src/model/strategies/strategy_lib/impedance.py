from numpy import pi, sqrt, column_stack
from src.model.input_parameters import InputParameters
from src.model.strategies import CalculationStrategy


class AnalyticalImpedanceStrategy(CalculationStrategy):
    """Analytical model of the impedance

    .. math::

        Z(f) = \sqrt{\\frac{R^2 + \omega^2}{(1 - L . C . \omega^2)^2 + (\omega . R . C)^2}}

    with:
        - :math:`R` : resistance of the coil
        - :math:`L` : inductance of the coil
        - :math:`C` : capacitance of the coil
        - :math:`\omega = 2 \pi f`
        - :math:`f` : frequency

    """

    def calculate(self, dependencies: dict, parameters: InputParameters):
        R = dependencies["resistance"]["data"]
        L = dependencies["inductance"]["data"]
        C = dependencies["capacitance"]["data"]

        frequency_vector = dependencies["frequency_vector"]["data"]

        impedance_num = (R ** 2) + (L * 2 * pi * frequency_vector) ** 2
        impedance_den = (1 - L * C * (2 * pi * frequency_vector) ** 2) ** 2 \
                        + (R * C * (2 * pi * frequency_vector)) ** 2
        impedance_values = sqrt(impedance_num / impedance_den)
        result = column_stack((frequency_vector, impedance_values))

        return {
            "data": result,
            "labels": ["Frequency", "Impedance"],
            "units": ["Hz", "Ohm"]
        }

    @staticmethod
    def get_dependencies():
        return ["resistance", "inductance", "capacitance", "frequency_vector"]

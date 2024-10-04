from numpy import column_stack
from src.model.input_parameters import InputParameters
from src.model.strategies import CalculationStrategy


class TF_ASIC_Stage_1_Strategy_linear(CalculationStrategy):
    """Analytical model for ASIC stage 1 transfer function

    .. math::

        H_1(f) = \\frac{gain_1}{\sqrt{1 + (\\frac{f}{f_{c1}})^2}}

    with:
        - :math:`gain_1` : gain of the ASIC's stage 1
        - :math:`f` : the frequency
        - :math:`f_{c1}` : the cutting frequency of the 1st stage of the ASIC

    """
    def calculate(self, dependencies: dict, parameters: InputParameters):
        gain_1 = parameters.data["gain_1_linear"]
        stage_1_cutting_freq = parameters.data["stage_1_cutting_freq"]
        frequency_vector = dependencies["frequency_vector"]["data"]

        numerator = gain_1
        denominator = (1 + (frequency_vector / stage_1_cutting_freq) ** 2) ** 0.5
        tf_asic = numerator / denominator

        results = column_stack((frequency_vector, tf_asic))

        return {
            "data": results,
            "labels": ["Frequency", "Transfer Function"],
            "units": ["Hz", ""]
        }

    @staticmethod
    def get_dependencies():
        return ["gain_1_linear", "stage_1_cutting_freq", "frequency_vector"]


class TF_ASIC_Stage_2_Strategy_linear(CalculationStrategy):
    """Analytical model for ASIC stage 2 transfer function

    .. math::

        H_2(f) = \\frac{gain_2}{\sqrt{1 + (\\frac{f}{f_{c2}})^2}}

    with:
        - :math:`gain_2` : gain of the ASIC's stage 2
        - :math:`f` : the frequency
        - :math:`f_{c2}` : the cutting frequency of the 2nd stage of the ASIC

    """

    def calculate(self, dependencies: dict, parameters: InputParameters):
        gain_2 = parameters.data["gain_2_linear"]
        stage_2_cutting_freq = parameters.data["stage_2_cutting_freq"] # Cutting frequency of the second stage in Hz
        frequency_vector = dependencies["frequency_vector"]["data"]

        numerator = gain_2
        denominator = (1 + (frequency_vector / stage_2_cutting_freq) ** 2) ** 0.5
        tf_asic = numerator / denominator

        results = column_stack((frequency_vector, tf_asic))

        return {
            "data": results,
            "labels": ["Frequency", "Transfer Function"],
            "units": ["Hz", ""]
        }

    @staticmethod
    def get_dependencies():
        return ["gain_2_linear", "stage_2_cutting_freq", "frequency_vector"]


class TF_ASIC_Strategy_linear(CalculationStrategy):
    """Analytical model of the total ASIC transfer function

    .. math::

        H(f) = H_1(f) . H_2(f)

    with:
        - :math:`H_1` : transfer function of the ASIC's stage 1
        - :math:`H_2` : transfer function of the ASIC's stage 2
        - :math:`f` : the frequency

    """

    def calculate(self, dependencies: dict, parameters: InputParameters):
        tf_asic_stage1 = dependencies["TF_ASIC_Stage_1"]["data"][:, 1]
        tf_asic_stage2 = dependencies["TF_ASIC_Stage_2"]["data"][:, 1]

        frequency_vector = dependencies["frequency_vector"]["data"]

        results = column_stack((frequency_vector, tf_asic_stage1 * tf_asic_stage2))

        return {
            "data": results,
            "labels": ["Frequency", "Transfer Function"],
            "units": ["Hz", ""]
        }

    @staticmethod
    def get_dependencies():
        return ["TF_ASIC_Stage_1", "TF_ASIC_Stage_2", "frequency_vector"]

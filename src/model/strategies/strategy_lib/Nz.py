from src.model.input_parameters import InputParameters
from src.model.strategies import CalculationStrategy

class AnalyticalNzStrategy(CalculationStrategy):
    """
    TODO: Add description
    """

    def calculate(self, dependencies: dict, parameters: InputParameters):
        diam_core = parameters.data['diam_core']
        len_core = parameters.data['len_core']
        result = diam_core /(2 * (len_core) + diam_core)

        return {
            "data": result,
            "units" : [""],
            "labels" : ["Nz"]
        }

    @staticmethod
    def get_dependencies():
        return ['diam_core', 'len_core']
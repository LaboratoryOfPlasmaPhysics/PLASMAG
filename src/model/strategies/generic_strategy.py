"""
src/model/strategies/generic_strategy.py
PLASMAG 2024 Software, LPP
"""
from abc import ABC, abstractmethod


class CalculationStrategy(ABC):
    """
    Abstract base class for defining calculation strategies within the calculation engine.

    A calculation strategy encapsulates a specific method of computation that
    can be applied to a set of input parameters and dependencies. Implementations
    of this class are expected to provide the logic for performing a calculation
    and specifying its dependencies.

    This class is designed to be subclassed with concrete strategies implementing
    the actual calculation logic tailored to specific computational needs.

    Methods:
        calculate: Performs the calculation based on given dependencies and parameters.
        get_dependencies: Returns a list of names of other calculations this strategy depends on.

    Example:
        Subclass this `CalculationStrategy` to implement a custom calculation method::

            class MyCalculationStrategy(CalculationStrategy):

                def calculate(self, dependencies, parameters):
                    # retrieve user's parameters
                    param1 = parameters.data["param1"]

                    # retrieve values from other nodes
                    frequency_vector = dependencies["frequency_vector"]["data"]
                    dep1 = dependencies["dependency1"]["data"][:, 1]

                    # Custom calculation logic here
                    result = dep1 * param1

                    # results must be returned as a tensor if the quantity depends on another one
                    results = column_stack((frequency_vector, result))

                    # the return format is a dictionary with the numerical results stored in "data", the
                    # labels and units used for plot legend.
                    return {
                        "data": results,
                        "labels": ["Frequency", "myPhysicalQuantity"],
                        "units": ["Hz", "my/Unit"]
                    }

                @staticmethod
                def get_dependencies():
                    # this methode must return the list of user parameters and node values used as input to
                    # the strategy calculation
                    return ['dependency1', 'frequency_vector', 'param1']

    Note:
        - `calculate` method must be overridden in subclasses to provide specific calculation logic.
        - `get_dependencies` method should return a list of the names of all user parameter and other
          node values that the current strategy's calculation depends on.
          This is used by the calculation engine to ensure all dependencies are calculated before
          attempting to calculate this one.
          The list of dependencies should match the keys used to store the results in the `CalculationResults`.
          To know all existing dependencies, they are all listed in the CalculationResults readme file.

    """

    @abstractmethod
    def calculate(self, dependencies: dict, parameters):
        """
        Abstract method to perform the calculation using provided dependencies and parameters.

        Parameters:
            dependencies (dict): A dictionary where keys are the names of the dependencies
                                 (as defined by get_dependencies) and values are the results of those
                                 dependencies' calculations.

            parameters (InputParameters): A reference to the input parameters object/class containing the data

        Returns:
            The result of the calculation. The type and shape of the result depends on the specific
            calculation being performed.

        """
        return NotImplemented

    @staticmethod
    def get_dependencies() -> list[str]:
        """
        Returns a list of names of other calculations that this strategy depends on.

        This method should be overridden in subclasses to specify the exact dependencies
        required for the calculation strategy.

        Returns:
            list[str]: A list of dependency names.

        """
        return []

from numpy import pi
from src.model.input_parameters import InputParameters
from src.model.strategies import CalculationStrategy
from scipy.constants import epsilon_0


class AnalyticalCapacitanceStrategy(CalculationStrategy):
    """Analytical model of the capacitance

    .. math::
        C = \\frac{\pi . \\epsilon_0 . \\epsilon_{insulator} . l_{coil}}{(K_t + 2 * I_t) . N_{layer}^2}
                . (N_{layer} - 1) . (d_{out\_mandrel} + N_{layer} . d_{wire} + (N_{layer} - 1) . K_t)
                + C_{tuning} + C_{triwire}

    with:
        - :math:`\\epsilon_0` : vacuum permittivity
        - :math:`\\epsilon_{insulator}` : the permittivity of the insulator
        - :math:`l_{coil}` : the length of the coil
        - :math:`K_t` : Kapton thick
        - :math:`I_t` : Insulator thick
        - :math:`N_{layer}` : number of coil layers
        - :math:`d_{out\_mandrel}` : the output diameter of the mandrel
        - :math:`d_{wire}` : the diameter of the wire
        - :math:`C_{tuning}` : tuning capacitance
        - :math:`C_{triwire}` : triwire capacitance

    """

    def calculate(self, dependencies: dict, parameters: InputParameters):
        epsilon_insulator = parameters.data["epsilon_insulator"]
        len_coil = parameters.data["len_coil"]
        kapton_thick = parameters.data["kapton_thick"]
        insulator_thick = parameters.data["insulator_thick"]
        diam_out_mandrel = parameters.data["diam_out_mandrel"]
        diam_wire = parameters.data["diam_wire"]
        capa_tuning = parameters.data["capa_tuning"]
        capa_triwire = parameters.data["capa_triwire"]
        nb_spire = parameters.data["nb_spire"]

        nb_spire_per_layer = int(len_coil / diam_wire)
        nb_layer = int(nb_spire / nb_spire_per_layer) + 1

        result = (
                (pi * epsilon_0 * epsilon_insulator * len_coil)
                * (nb_layer - 1) * (diam_out_mandrel + nb_layer * diam_wire + (nb_layer - 1) * kapton_thick)
                / ((kapton_thick + 2 * insulator_thick) * nb_layer ** 2)
                + capa_tuning + capa_triwire
        )

        return {
            "data": result,
            "labels": ["Capacitance"],
            "units": ["F"]
        }

    @staticmethod
    def get_dependencies():
        return ["epsilon_insulator", "len_coil", "kapton_thick", "insulator_thick", "diam_out_mandrel",
                "diam_wire", "capa_tuning", "capa_triwire", "nb_spire"]

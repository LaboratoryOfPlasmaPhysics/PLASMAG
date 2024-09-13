from numpy import pi
from src.model.input_parameters import InputParameters
from src.model.strategies import CalculationStrategy


class AnalyticalResistanceStrategy(CalculationStrategy):
    """Analytical model of the resistance of a monolayer winding

    .. math::

        R = N_{spire} . 2 . \pi . R_s . \\rho_{wire}

    with:
        - :math:`N_{spire}` : number of spire of the coil
        - :math:`R_s` : radius of the spires
        - :math:`\\rho_{wire}` : linear resistance of the wire

    """
    def calculate(self, dependencies: dict, parameters: InputParameters):
        N = parameters.data["nb_spire"]
        Rs = parameters.data["ray_spire"]
        rho = parameters.data["rho_wire"]
        value = N * (2 * pi * Rs) * rho

        return {
            "data": value,
            "labels": ["Resistance"],
            "units": ["Ohm"]
        }

    @staticmethod
    def get_dependencies():
        return ["nb_spire", "ray_spire", "rho_wire"]


class MultiLayerResistanceStrategy(CalculationStrategy):
    """Analytical model of the resistance of a multi-layer winding

    .. math::

        R = \\rho_{wire} . (l_{main\_coil} + l_{feedback})

    with:

        - :math:`\\rho_{wire}` : linear resistance of the wire
        - :math:`l_{main\_coil}` being the length of the main coil, computed with:

            - :math:`l_{main\_coil} = \pi . Ns_{per\_layer\_mc} . N_{layers} . \
                (d_{out\_mandrel} + N_{layers} . d_{wire} + (N_{layers} - 1) . K_t)`
            - :math:`Ns_{per\_layer\_mc}` : the number of spires on each of the main coil layers
            - :math:`N_{layers}` : the number of coil layers
            - :math:`d_{out\_mandrel}` : the output diameter of the mandrel
            - :math:`d_{wire}` : the diameter of the wire
            - :math:`K_t` : the Kapton thick

        - :math:`l_{feedback}` being the length of the feedback coil, computed with:

            - :math:`l_{feedback} = \pi . Ns_{per\_layer\_fb} . N_{layers} \
                . (d_{out\_mandrel} + (N_{layers} + 1) . d_{wire} + (N_{layers} - 1) . K_t)`
            - :math:`Ns_{per\_layer\_fb}` : the number of spires on each of the feedback coil layers

    """
    def calculate(self, dependencies: dict, parameters: InputParameters):
        # get user's values
        len_coil = parameters.data["len_coil"]
        N_spire_main_coil = parameters.data["nb_spire"]
        N_spire_feedback = parameters.data["nb_spire_feedback"]
        diam_out_mandrel = parameters.data["diam_out_mandrel"]
        rho_wire = parameters.data["rho_wire"]
        diam_wire = parameters.data["diam_wire"]
        kapton_thick = parameters.data["kapton_thick"]

        # determine the number of spires that fit in the length of the coil (rounded down)
        Ns_mc_per_layer = int(len_coil / diam_wire)
        # determine the number of layers to have *N_spire_main_coil* in the end (rounded up)
        N_layers = int(N_spire_main_coil / Ns_mc_per_layer) + 1
        # N_layers = int((N_spire_main_coil / Ns_mc_per_layer) + 1)

        # calculate the length of wire needed to wind the main coil
        length_main_coil = pi * Ns_mc_per_layer * N_layers \
            * (diam_out_mandrel + N_layers * diam_wire + (N_layers - 1) * kapton_thick)

        # if no spire are asked for the feedback coil...
        if N_spire_feedback == 0:
            # ... just consider a wire of the same length as the coil
            length_feedback = len_coil
        else:
            # ... else, determine the number of spires in each layer of the feedback coil (rounded up)
            # Ns_fb_per_layer = int((N_spire_feedback / N_layers) + 1)
            Ns_fb_per_layer = int(N_spire_feedback / N_layers) + 1
            # calculate the length of wire needed to wind the feedback coil
            length_feedback = pi * Ns_fb_per_layer * N_layers \
                * (diam_out_mandrel + (N_layers + 1) * diam_wire + (N_layers - 1) * kapton_thick)

        # calculate the resistance of the antenna as that of the total wire length used to wind
        value = rho_wire * (length_main_coil + length_feedback)

        return {
            "data": value,
            "labels": ["Resistance"],
            "units": ["Ohm"]
        }

    @staticmethod
    def get_dependencies():
        return ["len_coil", "nb_spire", "nb_spire_feedback", "diam_out_mandrel", "rho_wire",
                "diam_wire", "kapton_thick"]

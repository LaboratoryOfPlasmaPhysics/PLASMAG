from abc import ABC, abstractmethod

import numpy as np

from src.controler.controller import CalculationController


class BaseEvaluator(ABC):
    def __init__(self, parameters_dict, target, strategy_map):
        self.parameters_dict = parameters_dict
        self.target = target
        self.controller = CalculationController()
        self.controller.swap_strategy_map(strategy_map)

    @abstractmethod
    def evaluate(self, individual):
        pass

    def update_target(self, target):
        self.target = target

    def set_calculation_controller(self, controller):
        self.controller = controller

    def set_strategy_map(self, strategy_map):
        self.controller.swap_strategy_map(strategy_map)


class ResonanceFrequencyEvaluator(BaseEvaluator):

    def determine_resonance_freq(self, freq_vector, impedance_vector):
        index = impedance_vector.argmax()
        return freq_vector[index]


    def evaluate(self, individual):
        len_coil, diam_wire, nb_spire, capa_tuning, capa_triwire = individual

        params = self.parameters_dict.copy()
        params.update({
            'len_coil': len_coil,
            'diam_wire': diam_wire,
            'nb_spire': int(nb_spire),
            'capa_tuning': capa_tuning,
            'capa_triwire': capa_triwire
        })

        try:
            self.controller.update_parameters(params)
            results = self.controller.get_current_results()
            impedance = results['impedance']["data"]
            resonance_freq = self.determine_resonance_freq(impedance[:, 0], impedance[:, 1])
            return abs(resonance_freq - self.target),
        except Exception as e:
            return 1e6,


class NEMIEvaluator(BaseEvaluator):
    def evaluate(self, individual):
        len_coil, diam_wire, nb_spire, capa_tuning, capa_triwire = individual

        params = self.parameters_dict.copy()
        params.update({
            'len_coil': len_coil,
            'diam_wire': diam_wire,
            'nb_spire': int(nb_spire),
            'capa_tuning': capa_tuning,
            'capa_triwire': capa_triwire
        })

        try:
            self.controller.update_parameters(params)
            results = self.controller.get_current_results()
            nemi_values = results['nemi']["data"]
            distances = [(nemi_value - target_value)**2 for nemi_value, target_value in zip(nemi_values, self.target)]
            return sum(distances),
        except Exception as e:
            return 1e6,


class ResonanceFrequencyEvaluator2(BaseEvaluator):

    def determine_resonance_freq(self, freq_vector, impedance_vector):
        index = impedance_vector.argmax()
        return freq_vector[index]

    def evaluate(self, individual):
        len_coil, diam_wire, nb_spire, capa_tuning, capa_triwire = individual

        params = self.parameters_dict.copy()
        params.update({
            'len_coil': len_coil,
            'diam_wire': diam_wire,
            'nb_spire': int(nb_spire),
            'capa_tuning': capa_tuning,
            'capa_triwire': capa_triwire
        })

        try:
            self.controller.update_parameters(params)
            results = self.controller.get_current_results()
            impedance = results['impedance']["data"]
            resonance_freq = self.determine_resonance_freq(impedance[:, 0], impedance[:, 1])
            objective1 = abs(resonance_freq - self.target)
            objective2 = np.sum(np.abs(impedance[:, 1]))  # Example of a second objective
            return objective1, objective2
        except Exception as e:
            return 1e6, 1e6

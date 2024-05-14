import random

import numpy as np

from src.controler.controller import CalculationController
from src.model.optimisation.genetic_optimisation import parameters_dict
from src.model.optimisation.impedance_strategy_map import IMPEDANCE_STRATEGY_MAP
from PyQt6.QtCore import pyqtSignal, QThread

class SimulatedAnnealing(QThread):
    update_signal = pyqtSignal(int, float, float)  # iteration, avg_fitness, best_fitness
    finished_signal = pyqtSignal(dict, float)  # best_parameters, final_resonance_freq

    def __init__(self, parameters_dict, target_resonance_freq=3255, n_iterations=10, bounds=None, initial_temperature=1000, cooling_rate=0.003):
        super().__init__()
        self.parameters_dict = parameters_dict
        self.target_resonance_freq = target_resonance_freq
        self.n_iterations = n_iterations
        self.initial_temperature = initial_temperature
        self.cooling_rate = cooling_rate
        self.bounds = [
            (1e-3, 200e-3),  # len_coil
            (10e-6, 300e-6),  # diam_wire
            (1000, 20000),  # nb_spire
            (1e-3, 10e-3),  # diam_out_mandrel
            (1e-2, 200e-2),  # len_core
            (1e-3, 100e-3),  # diam_core
        ]
        #random init params with bounds
        self.initial_paramater = [random.uniform(b[0], b[1]) for b in self.bounds]

        self.controller = CalculationController()

        self.controller.swap_strategy_map(IMPEDANCE_STRATEGY_MAP)

    def update_target_resonance_freq(self, target_resonance_freq):
        self.target_resonance_freq = target_resonance_freq

    def set_initial_parameters(self, initial_parameters):
        self.initial_paramater = initial_parameters

    def determine_resonance_freq(self, freq_vector, impedance_vector):
        index = impedance_vector.argmax()
        return freq_vector[index]

    def evaluate(self, position):
        # Extract individual parameters from the position
        len_coil, diam_wire, nb_spire, diam_out_mandrel, len_core, diam_core = position

        # Update parameter dictionary with the current position's values
        params = parameters_dict.copy()
        params.update({
            'len_coil': len_coil,
            'diam_wire': diam_wire,
            'nb_spire': int(nb_spire),
            'diam_out_mandrel': diam_out_mandrel,
            'len_core': len_core,
            'diam_core': diam_core
        })

        try:
            self.controller.update_parameters(params)
            results = self.controller.get_current_results()
            impedance = results['impedance']["data"]
            resonance_freq = self.determine_resonance_freq(impedance[:, 0], impedance[:, 1])
            target_resonance_freq = self.target_resonance_freq
            return abs(resonance_freq - target_resonance_freq)
        except Exception as e:
            return 1e6

    def run(self):
        print("Running Simulated Annealing, target resonance freq:", self.target_resonance_freq)
        current_params = np.array(self.initial_paramater)
        current_cost = self.evaluate(current_params)
        best_cost = current_cost  # Initialize the best cost
        temp = self.initial_temperature

        for i in range(self.n_iterations):
            next_params = current_params + np.random.uniform(-0.1, 0.1, size=current_params.shape) * (np.array([b[1] - b[0] for b in self.bounds]) * 0.05)
            next_params = np.clip(next_params, [b[0] for b in self.bounds], [b[1] for b in self.bounds])
            next_cost = self.evaluate(next_params)

            if next_cost < current_cost or np.exp((current_cost - next_cost) / temp) > random.random():
                current_params = next_params
                current_cost = next_cost

                if current_cost < best_cost:
                    best_cost = current_cost  # Update the best cost if current cost is better

            temp *= self.cooling_rate

            if i % 100 == 0:
                print(f"Iteration {i}: Best cost = {best_cost}, Params = {current_params}")
                self.update_signal.emit(i, current_cost, best_cost)

        best_params = {
            'len_coil': current_params[0],
            'diam_wire': current_params[1],
            'nb_spire': int(current_params[2]),
            'diam_out_mandrel': current_params[3],
            'len_core': current_params[4],
            'diam_core': current_params[5]
        }

        self.parameters_dict.update(best_params)

        # Update parameters for the final evaluation
        self.controller.update_parameters(self.parameters_dict)
        final_results = self.controller.get_current_results()
        impedance = final_results['impedance']["data"]
        final_resonance_freq = self.determine_resonance_freq(impedance[:, 0], impedance[:, 1])
        print("Final Resonance Frequency:", final_resonance_freq)

        self.finished_signal.emit(best_params, final_resonance_freq)


if __name__ == "__main__":
    bounds = [
        (1e-3, 200e-3),  # len_coil
        (10e-6, 300e-6),  # diam_wire
        (1000, 20000),  # nb_spire
        (1e-3, 10e-3),  # diam_out_mandrel
        (1e-2, 200e-2),  # len_core
        (1e-3, 100e-3)  # diam_core
    ]
    sa = SimulatedAnnealing(parameters_dict, target_resonance_freq=3255, n_iterations=1000,
                            initial_temperature=1000, cooling_rate=0.99)
    sa.run()
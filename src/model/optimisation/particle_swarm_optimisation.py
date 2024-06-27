import numpy as np
import random
from PyQt6.QtCore import QThread, pyqtSignal

from src.model.optimisation.impedance_strategy_map import IMPEDANCE_STRATEGY_MAP
from src.controler.controller import CalculationController

class ParticleSwarmOptimization(QThread):
    update_signal = pyqtSignal(int, float, float)  # iteration, avg_fitness, best_fitness
    finished_signal = pyqtSignal(dict, float)  # best_parameters, final_resonance_freq

    def __init__(self, parameters_dict, target_resonance_freq=3255, n_particles=10, n_iterations=10, bounds=None):
        super().__init__()
        self.parameters_dict = parameters_dict
        self.target_resonance_freq = target_resonance_freq
        self.n_particles = n_particles
        self.n_iterations = n_iterations
        self.bounds = [
        (1e-3, 200e-3),  # len_coil
        (10e-6, 300e-6), # diam_wire
        (1000, 20000),   # nb_spire
        (1e-3, 10e-3),   # diam_out_mandrel
        (1e-2, 200e-2),  # len_core
        (1e-3, 100e-3),  # diam_core
    ]
        self.controller = CalculationController()

        self.controller.swap_strategy_map(IMPEDANCE_STRATEGY_MAP)


        self.w = 0.5 # Inertia weight
        self.c1 = 0.5 # Cognitive constant
        self.c2 = 0.9 # Social constant

    def clamp_positions(self, positions, bounds):
        for i in range(len(bounds)):
            positions[:, i] = np.clip(positions[:, i], bounds[i][0], bounds[i][1])

    def reflect_positions(self, positions, bounds):
        for i in range(len(bounds)):
            lower_bound, upper_bound = bounds[i]
            over_upper = positions[:, i] > upper_bound
            under_lower = positions[:, i] < lower_bound
            positions[over_upper, i] = 2 * upper_bound - positions[over_upper, i]
            positions[under_lower, i] = 2 * lower_bound - positions[under_lower, i]
            # Ensure they are within bounds after reflection
            positions[:, i] = np.clip(positions[:, i], lower_bound, upper_bound)

    def run(self):
        self.run_optimization()

    def determine_resonance_freq(self, freq_vector, impedance_vector):
        index = impedance_vector.argmax()
        return freq_vector[index]

    def evaluate(self, position):
        params = self.parameters_dict.copy()
        params.update(dict(zip(['len_coil', 'diam_wire', 'nb_spire', 'diam_out_mandrel', 'len_core', 'diam_core'], position)))

        try:
            self.controller.update_parameters(params)
            results = self.controller.get_current_results()
            impedance = results['impedance']["data"]
            resonance_freq = self.determine_resonance_freq(impedance[:, 0], impedance[:, 1])
            return abs(resonance_freq - self.target_resonance_freq),
        except Exception as e:
            return 1e6,

    def update_target_resonance_freq(self, target_resonance_freq):
        self.target_resonance_freq = target_resonance_freq

    def run(self):
        positions = np.array([np.random.uniform(low, high, self.n_particles) for low, high in self.bounds]).T
        velocities = np.zeros_like(positions)
        personal_best_positions = np.copy(positions)
        personal_best_scores = np.array([self.evaluate(pos)[0] for pos in
                                         positions])  # Make sure to take the first element of the tuple returned by evaluate

        global_best_position = personal_best_positions[np.argmin(personal_best_scores)]
        global_best_score = np.min(personal_best_scores)

        for iteration in range(self.n_iterations):
            # Emit the start of a new iteration with the current best global score and average score
            avg_fitness = np.mean(personal_best_scores)
            self.update_signal.emit(iteration, avg_fitness, global_best_score)
            print("Iteration:", iteration, "Average fitness:", avg_fitness, "Best fitness:", global_best_score)
            for i in range(self.n_particles):
                # Update velocity
                r1, r2 = np.random.random(), np.random.random()
                velocities[i] = self.w * velocities[i] + self.c1 * r1 * (
                            personal_best_positions[i] - positions[i]) + self.c2 * r2 * (
                                            global_best_position - positions[i])
                # Update position
                positions[i] += velocities[i]
                self.clamp_positions(positions, self.bounds)
                # Evaluate new position
                current_score = self.evaluate(positions[i])[0]

                # Update personal best
                if current_score < personal_best_scores[i]:
                    personal_best_positions[i] = positions[i]
                    personal_bs = personal_best_scores[i] = current_score

                # Update global best
                if current_score < global_best_score:
                    global_best_position = positions[i]
                    global_best_score = current_score

        # Emit finished signal with best parameters and final results
        best_params = dict(zip(['len_coil', 'diam_wire', 'nb_spire', 'diam_out_mandrel', 'len_core', 'diam_core'],
                               global_best_position))

        self.parameters_dict.update(best_params)

        self.controller.update_parameters(self.parameters_dict)
        final_results = self.controller.get_current_results()
        impedance = final_results['impedance']["data"]
        final_resonance_freq = self.determine_resonance_freq(impedance[:, 0], impedance[:, 1])
        self.finished_signal.emit(best_params, final_resonance_freq)

        print("Best Parameters:", best_params)
        print("Final Resonance Frequency:", final_resonance_freq)


# PSO initialization example:
if __name__ == "__main__":
    parameters_dict = {
        # Initialize all required parameters
        'f_start': 1,
        'f_stop': 1000000,
        'nb_points_per_decade': 1000,
        # Add other necessary parameters
        'mu_insulator': 1,
        'kapton_thick': 30e-6,
        'insulator_thick': 10e-6,
        'diam_out_mandrel': 3.2e-3,
        'len_core': 20e-2,
        'diam_core': 3.2e-3,
        'mu_r': 100000,
        'rho_whire': 1.6,
        'coeff_expansion': 1,
        'stage_1_cutting_freq': 20000,
        'stage_2_cutting_freq': 20000,
        'gain_1_linear': 1,
        'gain_2_linear': 1,
        'mutual_inductance': 0.1,
        'feedback_resistance': 1000,
        'temperature': 300,
        'spice_resistance_test': 1000,
        'Para_A': 1,
        'Para_B': 1,
        'e_en': 1,
        'e_in': 1,
        'Alpha': 1,
        "ray_spire": 5e-3,
        "capa_tuning": 1e-12,
        "capa_triwire": 10e-12
    }
    bounds = [
        (1e-3, 200e-3),  # len_coil
        (10e-6, 300e-6), # diam_wire
        (1000, 20000),   # nb_spire
        (1e-3, 10e-3),   # diam_out_mandrel
        (1e-2, 200e-2),  # len_core
        (1e-3, 100e-3),  # diam_core
    ]
    pso = ParticleSwarmOptimization(parameters_dict, bounds=bounds)
    pso.run()

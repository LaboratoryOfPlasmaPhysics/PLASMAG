import random

import numpy as np
from PyQt6.QtCore import pyqtSignal, QThread
from deap import creator, base, tools, algorithms

from src.model.optimisation.impedance_strategy_map import IMPEDANCE_STRATEGY_MAP
from src.controler.controller import CalculationController

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
class GeneticOptimisation(QThread):
    update_signal = pyqtSignal(int, float, float) # generation, fitness average, best fitness
    finished_signal = pyqtSignal(dict, float)  # best parameters, resonance frequency
    def __init__(self, population_size, generations, mutation_rate, parameters_dict, target_resonance_freq=2430):
        super().__init__()
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.target_resonance_freq = target_resonance_freq
        self.toolbox = None

        self.controller = CalculationController()

        # TODO : change this line
        self.controller.swap_strategy_map(IMPEDANCE_STRATEGY_MAP)

        self.parameters_dict = parameters_dict

        self.init_creator()

    def update_target_resonance_freq(self, target_resonance_freq):
        self.target_resonance_freq = target_resonance_freq
    def determine_resonance_freq(self, freq_vector, impedance_vector):
        index = impedance_vector.argmax()
        return freq_vector[index]

    def evaluate(self, individual):
        len_coil, diam_wire, nb_spire, capa_tuning, capa_triwire = individual

        params = parameters_dict.copy()
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
            target_resonance_freq = self.target_resonance_freq
            return abs(resonance_freq - target_resonance_freq),
        except Exception as e:
            return 1e6,

    def init_creator(self):
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)

        toolbox = base.Toolbox()
        toolbox.register("attr_len_coil", random.uniform, 1e-3, 200e-3)
        toolbox.register("attr_diam_wire", random.uniform, 10e-6, 300e-6)
        toolbox.register("attr_nb_spire", random.uniform, 1000, 20000)
        toolbox.register("attr_capa_tuning", random.uniform, 1e-12, 1000e-12)
        toolbox.register("attr_capa_triwire", random.uniform, 10e-12, 1000e-12)
        toolbox.register("individual", tools.initCycle, creator.Individual,
                         (toolbox.attr_len_coil, toolbox.attr_diam_wire, toolbox.attr_nb_spire,
                          toolbox.attr_capa_tuning, toolbox.attr_capa_triwire),
                         n=1)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        toolbox.register("evaluate", self.evaluate)
        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.3)
        toolbox.register("select", tools.selTournament, tournsize=5)

        self.toolbox = toolbox

    def run_optimisation(self):
        population = self.toolbox.population(n=self.population_size)
        hof = tools.HallOfFame(5)  # Keep the top 5 individuals
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("min", min)
        stats.register("avg", np.mean)

        for gen in range(self.generations):
            population, logbook = algorithms.eaSimple(population, self.toolbox, cxpb=0.7, mutpb=self.mutation_rate,
                                                      ngen=1, stats=stats, halloffame=hof, verbose=False)

            avg_fitness = logbook.select("avg")[0]
            best_fitness = logbook.select("min")[0][0]
            print(best_fitness)
            self.update_signal.emit(gen, avg_fitness, best_fitness)

        best_params = hof[0]
        print("Best Parameters:", best_params)
        print("Best Fitness:", self.evaluate(best_params)[0])

        # Update parameters for the final evaluation
        final_params = {'len_coil': best_params[0], 'diam_wire': best_params[1], 'nb_spire': int(best_params[2]),
                        'capa_tuning': best_params[3], 'capa_triwire': best_params[4]}
        self.controller.update_parameters(final_params)
        final_results = self.controller.get_current_results()
        impedance = final_results['impedance']["data"]
        final_resonance_freq = self.determine_resonance_freq(impedance[:, 0], impedance[:, 1])
        print("Final Resonance Frequency:", final_resonance_freq)
        print("Final parameters:", final_params)
        self.finished_signal.emit(final_params, final_resonance_freq)
        return final_resonance_freq, final_params

    def run(self):
        self.run_optimisation()


if __name__ == "__main__":

    optimisation = GeneticOptimisation(100, 20, 0.3, parameters_dict, target_resonance_freq=24430)
    optimisation.run_optimisation()
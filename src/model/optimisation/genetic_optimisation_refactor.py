import random
import numpy as np
from PyQt6.QtCore import pyqtSignal, QThread
from deap import creator, base, tools, algorithms

from src.model.optimisation.cost_function import ResonanceFrequencyEvaluator, NEMIEvaluator
from src.model.optimisation.impedance_strategy_map import IMPEDANCE_STRATEGY_MAP
from src.controler.controller import CalculationController


class GeneticOptimisation(QThread):
    update_signal = pyqtSignal(int, float, float) # generation, fitness average, best fitness
    finished_signal = pyqtSignal(dict, float)  # best parameters, resonance frequency

    def __init__(self, population_size, generations, mutation_rate, evaluator):
        super().__init__()
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.evaluator = evaluator
        self.toolbox = None

        self.init_creator()

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
        toolbox.register("evaluate", self.evaluator.evaluate)
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
        print("Best Fitness:", self.evaluator.evaluate(best_params)[0])

        # Update parameters for the final evaluation
        final_params = {'len_coil': best_params[0], 'diam_wire': best_params[1], 'nb_spire': int(best_params[2]),
                        'capa_tuning': best_params[3], 'capa_triwire': best_params[4]}
        self.evaluator.controller.update_parameters(final_params)
        final_results = self.evaluator.controller.get_current_results()
        impedance = final_results['impedance']["data"]
        final_resonance_freq = self.evaluator.determine_resonance_freq(impedance[:, 0], impedance[:, 1])
        print("Final Resonance Frequency:", final_resonance_freq)
        print("Final parameters:", final_params)
        self.finished_signal.emit(final_params, final_resonance_freq)
        return final_resonance_freq, final_params

    def run(self):
        self.run_optimisation()



parameters_dict = {
    'f_start': 1,
    'f_stop': 1000000,
    'nb_points_per_decade': 1000,
    'mu_insulator': 1,
    'kapton_thick': 30e-6,
    'insulator_thick': 10e-6,
    'diam_out_mandrel': 3.2e-3,
    'len_core': 20e-2,
    'diam_core': 3.2e-3,
    'mu_r': 100000,
    'rho_wire': 1.6,
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

if __name__ == "__main__":
    # For resonance frequency optimization
    resonance_evaluator = ResonanceFrequencyEvaluator(parameters_dict, target=2350, strategy_map=IMPEDANCE_STRATEGY_MAP)
    optimisation = GeneticOptimisation(100, 20, 0.3, resonance_evaluator)
    optimisation.run_optimisation()

    # resonance_evaluator.update_target(1350)
    # optimisation.run_optimisation()

    # # For NEMI values optimization
    # nemi_target = [1, 2, 3, 4, 5]  # Example target values
    # nemi_evaluator = NEMIEvaluator(parameters_dict, nemi_target, strategy_map=IMPEDANCE_STRATEGY_MAP)
    # optimisation = GeneticOptimisation(100, 20, 0.3, nemi_evaluator)
    # optimisation.run_optimisation()

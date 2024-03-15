import numpy as np
import timeit

from matplotlib import pyplot as plt

from src.model.input_parameters import InputParameters
from model.engine import CalculationEngine
from model.strategies.strategy_lib.Nz import AnalyticalNzStrategy
from model.strategies.strategy_lib.capacitance import AnalyticalCapacitanceStrategy
from model.strategies.strategy_lib.frequency import FrequencyVectorStrategy
from model.strategies.strategy_lib.impedance import AnalyticalImpedanceStrategy
from model.strategies.strategy_lib.inductance import AnalyticalInductanceStrategy
from model.strategies.strategy_lib.lambda_strategy import AnalyticalLambdaStrategy
from model.strategies.strategy_lib.mu_app import AnalyticalMu_appStrategy
from model.strategies.strategy_lib.resistance import AnalyticalResistanceStrategy


# Function to initialize and run the calculation engine
def run_impedance_calculation(f_start, f_stop, nb_points_per_decade):
    """
    Initializes and executes the calculation engine for impedance calculation.

    Args:
        f_start (float): Start frequency for the frequency range.
        f_stop (float): Stop frequency for the frequency range.
        nb_points_per_decade (int): Number of points per decade.

    Returns:
        None. The results are stored within the calculation engine's current output data.
    """
    parameters_dict = {
        'f_start': f_start,
        'f_stop': f_stop,
        'nb_points_per_decade': nb_points_per_decade,
        # Add other parameters required by the strategies
        'mu_insulator': 1,
        'len_coil': 155 * 10 ** -3,
        'kapthon_thick': 30 * 10 ** -6,
        'insulator_thick': 10 * 10 ** -6,
        'diam_out_mandrel': 3.2 * 10 ** -3,
        'diam_wire': 90 * 10 ** -6,
        'capa_tuning': 1 * 10 ** -12,
        'capa_triwire': 150 * 10 ** -12,
        'len_core': 20 * 10 ** -2,
        'diam_core': 3.2 * 10 ** -3,
        'mu_r': 100000,
        'nb_spire': 12100,
        'ray_spire': 5 * 10 ** -3,
        'rho_whire': 1.6,
        'coeff_expansion': 1,
    }
    parameters = InputParameters(parameters_dict)

    calculation_engine = CalculationEngine()
    calculation_engine.update_parameters(parameters)

    # Add all necessary strategies to the engine
    calculation_engine.add_or_update_node('frequency_vector', FrequencyVectorStrategy())
    calculation_engine.add_or_update_node('resistance', AnalyticalResistanceStrategy())
    calculation_engine.add_or_update_node('Nz', AnalyticalNzStrategy())
    calculation_engine.add_or_update_node('mu_app', AnalyticalMu_appStrategy())
    calculation_engine.add_or_update_node('lambda_param', AnalyticalLambdaStrategy())
    calculation_engine.add_or_update_node('inductance', AnalyticalInductanceStrategy())
    calculation_engine.add_or_update_node('capacitance', AnalyticalCapacitanceStrategy())
    calculation_engine.add_or_update_node('impedance', AnalyticalImpedanceStrategy())

    calculation_engine.run_calculations()


# Define benchmark parameters
frequencies_ranges = [(1, 1000), (1, 10000), (10, 100000), (100, 1000000), (1000, 10000000),
                        (10000, 100000000), (100000, 1000000000)


                      ]
points_per_decade = [10, 20, 50, 100, 200, 500, 700, 800, 1000, 1200, 1500, 2000, 2500, 3000,
                     5000, 7000, 10000, 100000]
number_of_runs = 5  # Number of executions to average the calculation time

benchmark_results = []

# Perform the benchmark
for f_range in frequencies_ranges:
    for points in points_per_decade:
        timer = timeit.Timer(lambda: run_impedance_calculation(f_range[0], f_range[1], points))
        time_taken = timer.timeit(number=number_of_runs) / number_of_runs
        benchmark_results.append({'f_range': f_range, 'points': points, 'time_taken': time_taken})

# Plotting the benchmark results
plt.figure(figsize=(10, 6))

for f_range in frequencies_ranges:
    times_for_range = [result['time_taken'] for result in benchmark_results if result['f_range'] == f_range]
    points_for_range = [result['points'] for result in benchmark_results if result['f_range'] == f_range]
    plt.plot(points_for_range, times_for_range, label=f"Frequency range {f_range[0]}-{f_range[1]} Hz", marker='o')

plt.xlabel('Points per decade')
#plt.xscale('log')
plt.ylabel('Average calculation time (seconds)')
plt.title('Calculation Time vs Points per Decade for Different Frequency Ranges')
plt.legend()
plt.grid(True)
plt.show()
from sys import platform
from numpy import abs, array, interp, column_stack
from src.model.input_parameters import InputParameters
from src.model.strategies import CalculationStrategy

import PySpice.Logging.Logging as Logging
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *


class SPICE_test(CalculationStrategy):
    def calculate(self, dependencies: dict, parameters: InputParameters):
        temperature = parameters.data['temperature']
        f_start = parameters.data['f_start']
        f_stop = parameters.data['f_stop']
        spice_resistance_test = parameters.data['spice_resistance_test']

        frequency_vector = dependencies['frequency_vector']['data']
        logger = Logging.setup_logging()

        # convert temperature to degrees Celsius
        temperature = temperature - 273.15

        circuit = Circuit('AC analysis Circuit')

        circuit.model("CustomDiode", 'D', IS=4.352 @ u_nA, RS=0.6459 @ u_Ohm, BV=110 @ u_V, IBV=0.0001 @ u_V, N=1.906)

        # circuit.V('input', 'n1', circuit.gnd, 10@u_V) # DC input voltage
        Vac = circuit.SinusoidalVoltageSource("input", 'n1', circuit.gnd, amplitude=1@ u_V,
                                              frequency=100@u_Hz)  # AC input voltage
        R = circuit.R(1, 'n1', 'n2', spice_resistance_test@u_Ohm)
        C = circuit.C(1, 'n2', circuit.gnd, 1@ u_uF)
        circuit.Diode(1, 'n2', 'n3', model='CustomDiode')
        circuit.R(2, 'n3', circuit.gnd, 1 @u_kOhm)

        simulator = circuit.simulator(temperature=temperature, nominal_temperature=25)

        analysis = simulator.ac(start_frequency=f_start@ u_Hz, stop_frequency=f_stop@u_Hz, number_of_points=10,
                                variation='dec')  # 1 to 1MHz, 10 points per decade

        gain_node_1 = abs(analysis.n1)
        gain_node_2 = abs(analysis.n2)
        gain_node_3 = abs(analysis.n3)

        analysis_freq = array(analysis.frequency)

        interpolated_gain_1 = interp(frequency_vector, analysis_freq, gain_node_1)
        interpolated_gain_2 = interp(frequency_vector, analysis_freq, gain_node_2)
        interpolated_gain_3 = interp(frequency_vector, analysis_freq, gain_node_3)

        result = column_stack((frequency_vector, interpolated_gain_1, interpolated_gain_2, interpolated_gain_3))

        return {
            "data": result,
            "labels": ["Frequency", "Gain Node 1", "Gain Node 2", "Gain Node 3"],
            "units": ["Hz", "V/V", "V/V", "V/V"]
        }

    @staticmethod
    def get_dependencies():
        return ['frequency_vector', "f_start", "f_stop", "spice_resistance_test", "temperature"]


if platform != "win32":
    class SPICE_op_Amp_gain(CalculationStrategy):
        def calculate(self, dependencies: dict, parameters: InputParameters):
            temperature = parameters.data['temperature']
            f_start = parameters.data['f_start']
            f_stop = parameters.data['f_stop']

            R1 = parameters.data['R1']
            R2 = parameters.data['R2']
            R3 = parameters.data['R3']
            R4 = parameters.data['R4']
            R5 = parameters.data['R5']

            frequency_vector = dependencies['frequency_vector']['data']
            logger = Logging.setup_logging()

            # convert temperature to degrees Celsius
            temperature = temperature - 273.15

            opAMP = 'src/model/strategies/strategy_lib/spice_lib/uA741.lib'

            ##*********************************************
            ## Circuit Netlist
            circuit = Circuit('Op-amp circuits - Example 1 Non-inverting op-amp Amplifier')
            circuit.include(opAMP)

            # Define amplitude and frequency of input sinusoid
            amp = 0.1 @ u_V
            freq = 1 @ u_kHz

            # Define transient simulation step time and stop time
            steptime = 1 @ u_us
            finaltime = 5 * (1 / freq)

            source = circuit.SinusoidalVoltageSource(1, 'input', circuit.gnd, amplitude=amp, frequency=freq)
            circuit.V(2, '+Vcc', circuit.gnd, 15 @ u_V)
            circuit.V(3, '-Vcc', circuit.gnd, -15 @ u_V)

            circuit.X(1, 'uA741', 'input', 'v-', '+Vcc', '-Vcc', 'out')

            circuit.R(1, 'v-', circuit.gnd, R1@ u_Ω)
            circuit.R(2, 'v-', 'x', R2@ u_Ω)
            circuit.R(3, 'x', 'out', R3@ u_Ω)
            circuit.R(4, 'x', circuit.gnd, R4@ u_Ω)
            circuit.R('L', 'out', circuit.gnd, R5@ u_Ω)

            ##*********************************************
            ## Simulation: Transient Analysis
            simulator = circuit.simulator(temperature=temperature, nominal_temperature=25)
            analysis = simulator.transient(step_time=steptime, end_time=finaltime)
            analysis = simulator.ac(start_frequency=f_start @ u_Hz, stop_frequency=f_stop @ u_Hz, number_of_points=10,
                                    variation='dec')  # 1 to 1MHz, 10 points per decade

            #print all nodes in the analysis

            input = abs(analysis['input'])
            output = abs(analysis['out'])

            simulation_freq = array(analysis.frequency)

            interpolated_input = interp(frequency_vector, simulation_freq, input)
            interpolated_output = interp(frequency_vector, simulation_freq, output)

            result = column_stack((frequency_vector, interpolated_input, interpolated_output))

            return {
                    "data": result,
                    "labels": ["Frequency", "Gain Input", "Gain output"],
                    "units": ["Hz", "V/V", "V/V"]
                }

        @staticmethod
        def get_dependencies():
            return ['frequency_vector', "f_start", "f_stop", "spice_resistance_test", "temperature", "R1", "R2", "R3", "R4", "R5"]


class SPICE_op_Amp_noise(CalculationStrategy):
    def calculate(self, dependencies: dict, parameters: InputParameters):
        temperature = parameters.data['temperature']
        f_start = parameters.data['f_start']
        f_stop = parameters.data['f_stop']

        R1 = parameters.data['R1']
        R2 = parameters.data['R2']
        R3 = parameters.data['R3']
        R4 = parameters.data['R4']
        R5 = parameters.data['R5']

        frequency_vector = dependencies['frequency_vector']['data']
        logger = Logging.setup_logging()

        # Convert temperature to degrees Celsius
        temperature = temperature - 273.15

        opAMP = 'src/model/strategies/strategy_lib/spice_lib/uA741.lib'

        ##*********************************************
        ## Circuit Netlist
        circuit = Circuit('Op-amp circuits - Noise Analysis for Non-inverting Amplifier')
        circuit.include(opAMP)

        circuit.V(2, '+Vcc', circuit.gnd, 15 @ u_V)
        circuit.V(3, '-Vcc', circuit.gnd, -15 @ u_V)

        circuit.X(1, 'uA741', 'input', 'v-', '+Vcc', '-Vcc', 'out')

        circuit.R(1, 'v-', circuit.gnd, R1@ u_Ω)
        circuit.R(2, 'v-', 'x', R2@ u_Ω)
        circuit.R(3, 'x', 'out', R3@ u_Ω)
        circuit.R(4, 'x', circuit.gnd, R4@ u_Ω)
        circuit.R('L', 'out', circuit.gnd, R5@ u_Ω)

        ##*********************************************
        ## Simulation: Noise Analysis
        simulator = circuit.simulator(temperature=temperature, nominal_temperature=25)
        analysis = simulator.noise(output_node='out', input_node='input', start_frequency=f_start @ u_Hz,
                                   stop_frequency=f_stop @ u_Hz, number_of_points=len(frequency_vector),
                                   variation='lin')

        # Retrieve noise data for each frequency
        frequency = array(analysis.frequency)
        output_noise_voltage = array(analysis.noise_output_voltage_density)

        # Interpolate the results onto the frequency vector if necessary
        interpolated_noise = interp(frequency_vector, frequency, output_noise_voltage)

        result = column_stack((frequency_vector, interpolated_noise))

        return {
            "data": result,
            "labels": ["Frequency", "Output Noise Voltage Density"],
            "units": ["Hz", "V/√Hz"]
        }

    @staticmethod
    def get_dependencies():
        return ['frequency_vector', "f_start", "f_stop", "temperature", "R1", "R2", "R3", "R4", "R5"]


if platform != "win32":
    class SPICE_op_Amp_transcient(CalculationStrategy):
        def calculate(self, dependencies: dict, parameters: InputParameters):
            temperature = parameters.data['temperature']
            f_start = parameters.data['f_start']
            f_stop = parameters.data['f_stop']

            R1 = parameters.data['R1']
            R2 = parameters.data['R2']
            R3 = parameters.data['R3']
            R4 = parameters.data['R4']
            R5 = parameters.data['R5']

            resistance = dependencies['resistance']['data']

            frequency_vector = dependencies['frequency_vector']['data']
            logger = Logging.setup_logging()

            # convert temperature to degrees Celsius
            temperature = temperature - 273.15

            opAMP = 'src/model/strategies/strategy_lib/spice_lib/uA741.lib'

            ##*********************************************
            ## Circuit Netlist
            circuit = Circuit('Op-amp circuits - Example 1 Non-inverting op-amp Amplifier')
            circuit.include(opAMP)

            # Define amplitude and frequency of input sinusoid
            amp = 0.1 @ u_V
            freq = 1 @ u_kHz

            # Define transient simulation step time and stop time
            steptime = 1 @ u_us
            finaltime = 5 * (1 / freq)

            source = circuit.SinusoidalVoltageSource(1, 'input', circuit.gnd, amplitude=amp, frequency=freq)
            circuit.V(2, '+Vcc', circuit.gnd, 15 @ u_V)
            circuit.V(3, '-Vcc', circuit.gnd, -15 @ u_V)

            circuit.X(1, 'uA741', 'input', 'v-', '+Vcc', '-Vcc', 'out')

            circuit.R(1, 'v-', circuit.gnd, resistance @ u_Ω)
            circuit.R(2, 'v-', 'x', R2 @ u_Ω)
            circuit.R(3, 'x', 'out', R3 @ u_Ω)
            circuit.R(4, 'x', circuit.gnd, R4 @ u_Ω)
            circuit.R('L', 'out', circuit.gnd, R5 @ u_Ω)

            ##*********************************************
            ## Simulation: Transient Analysis
            simulator = circuit.simulator(temperature=temperature, nominal_temperature=25)
            analysis = simulator.transient(step_time=steptime, end_time=finaltime)

            # print all nodes in the analysis

            input = analysis['input']
            output = analysis['out']

            time = array(analysis.time)

            result = column_stack((time, input, output))

            return {
                "data": result,
                "labels": ["Time", "Signal Input", "Signal output"],
                "units": ["s", "V", "V"]
            }

        @staticmethod
        def get_dependencies():
            return ['frequency_vector', "f_start", "f_stop", "spice_resistance_test", "temperature", "R1", "R2", "R3", "resistance",
                    "R4", "R5"]


class SPICE_impedance(CalculationStrategy):
    def calculate(self, dependencies: dict, parameters: InputParameters):
        temperature = parameters.data['temperature']
        f_start = parameters.data['f_start']
        f_stop = parameters.data['f_stop']


        resistance = dependencies['resistance']['data']
        capacitance = dependencies['capacitance']['data']
        inductance = dependencies['inductance']['data']

        frequency_vector = dependencies['frequency_vector']['data']

        nb_points_per_decade = parameters.data['nb_points_per_decade']

        logger = Logging.setup_logging()

        # convert temperature to degrees Celsius
        temperature = temperature - 273.15

        circuit = Circuit(' Imp JUICE')

        circuit.SinusoidalVoltageSource('V1', 'N1', circuit.gnd, amplitude=1 @ u_V, frequency=1 @ u_kHz)
        circuit.R('1', 'N001', 'N1', resistance @ u_Ω)
        circuit.C('1', 'N2', 'N1', capacitance @ u_F)
        circuit.L('1', 'N2', 'N001', inductance @ u_H)
        circuit.R('2', 'N2', circuit.gnd, 1 @ u_kΩ)

        circuit.R2.plus.add_current_probe(circuit)

        simulator = circuit.simulator(temperature=temperature, nominal_temperature=25)
        analysis = simulator.ac(start_frequency=f_start @ u_Hz, stop_frequency=f_stop @ u_Hz, number_of_points=nb_points_per_decade,
                                variation='dec')  # 1 to 1MHz, 10 points per decade

        frequency = analysis.frequency
        voltage_N1 = abs(analysis['N001'])
        current_R2 = abs(analysis['vr2_plus'])

        Z = voltage_N1 / current_R2

        simulation_freq = array(analysis.frequency)
        interpolated_Z = interp(frequency_vector, simulation_freq, Z)
        result = column_stack((frequency_vector, interpolated_Z))

        return {
            "data": result,
            "labels": ["Frequency", "Impedance"],
            "units": ["Hz", "Ohm"]
        }

    @staticmethod
    def get_dependencies():
        return ['frequency_vector', "f_start", "f_stop", "temperature", "capacitance",
                "inductance", "resistance"]


if __name__ == "__main__" :
    ##*********************************************
    import math
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.widgets import Cursor
    from matplotlib.pyplot import semilogx
    from matplotlib import pyplot

    logger = Logging.setup_logging()

    from PySpice.Doc.ExampleTools import find_libraries
    from PySpice.Probe.Plot import plot
    from PySpice.Spice.Library import SpiceLibrary

    ##*********************************************
    # Set the path where the op-amp uA741.lib file is located
    # Place the *.lib file in the same folder as the script file

    f_start = 1
    f_stop = 1000000
    circuit = Circuit(' Imp JUICE')

    V1 = circuit.SinusoidalVoltageSource('V1', 'N1', circuit.gnd, amplitude=1 @ u_V, frequency=1 @ u_kHz)
    circuit.R('1', 'N1', 'N001', 550 @ u_Ω)
    circuit.C('1', 'N2', 'N1', 150 @ u_pF)
    circuit.L('1', 'N2', 'N001', 12 @ u_H)
    circuit.R('2', 'N2', circuit.gnd, 1 @ u_kΩ)

    # Set the simulation temperature
    temperature = 25

    # Setup the frequency range
    f_start = 1
    f_stop = 1000000

    # Instantiate the simulator
    simulator = circuit.simulator(temperature=temperature, nominal_temperature=25)

    # Perform the noise analysis
    analysis = simulator.noise(
        output_node='N1',  # Correct node naming
        ref_node='N2',  # Correct node naming
        src='V1',  # Specify the correct noise source
        points=100,
        start_frequency=f_start @ u_Hz,  # Ensure the unit is properly appended
        stop_frequency=f_stop @ u_Hz,  # Ensure the unit is properly appended
        variation='dec'
    )

    # Output the results
    for frequency, noise in zip(analysis.frequency, analysis.noise_voltage_density):
        print(f'Frequency: {frequency} Hz, Noise: {noise} V/√Hz')

    # circuit.R2.plus.add_current_probe(circuit)
    #
    # simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    # analysis = simulator.ac(start_frequency=f_start @ u_Hz, stop_frequency=f_stop @ u_Hz, number_of_points=10,
    #                         variation='dec')  # 1 to 1MHz, 10 points per decade
    #
    # frequency = analysis.frequency.as_ndarray()
    # voltage_N1 = analysis['n1'].as_ndarray()
    # current_R2 = analysis['vr2_plus'].as_ndarray()
    #
    # Z = voltage_N1 / current_R2

    # # plot imepdance and phase
    # fig, ax = plt.subplots(2, 1, figsize=(10, 7))
    # ax[0].semilogx(frequency, np.abs(Z))
    # ax[0].semilogy()
    # ax[0].set_ylabel('Impedance [Ohm]')
    # ax[0].set_title('Impedance of the circuit')
    # ax[0].grid(True)
    #
    # ax[1].semilogx(frequency, np.angle(Z, deg=True))
    # ax[1].set_xlabel('Frequency [Hz]')
    # ax[1].set_ylabel('Phase [°]')
    # ax[1].set_title('Phase of the circuit')
    # ax[1].grid(True)
    #
    # plt.tight_layout()
    # plt.show()

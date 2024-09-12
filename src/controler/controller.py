"""
 src/controller/controller.py
 PLASMAG 2024 Software, LPP
"""
import numpy as np
from src.controler.models.scm_model import STRATEGY_MAP
from src.model.input_parameters import InputParameters
from src.model.engine import CalculationEngine


class CalculationController:
    """
        The CalculationController class is responsible for managing the calculation engine and the input parameters
        of the engine. This controller is the main interface between the user interface and the calculation engine.
        It can be used to run the engine headless or to update the parameters and run the calculations.
    """
    def __init__(self, params_dict=None, backups_count=3):
        """
                Initializes the CalculationController with optional parameters. This controller
                sets up the calculation engine.

                Engine calculation nodes should be added here.

                Parameters:
                - params_dict (dict, optional): A dictionary of parameters to initialize the
                input parameters of the engine.
        """
        self.engine = CalculationEngine(backups_count=backups_count)
        self.backup_count = backups_count
        self.is_data_ready = False
        self.params = None
        self.STRATEGY_MAP = STRATEGY_MAP

        for node_name, info in self.STRATEGY_MAP.items():
            default_strategy = info["default"]()
            self.engine.add_or_update_node(node_name, default_strategy)

        if params_dict:
            self.update_parameters(params_dict)

    def swap_strategy_map(self, strategy_map):
        self.engine = CalculationEngine(backups_count=self.backup_count)
        self.STRATEGY_MAP = strategy_map

        for node_name, info in self.STRATEGY_MAP.items():
            default_strategy = info["default"]()
            self.engine.add_or_update_node(node_name, default_strategy)

        if self.params:
            self.update_parameters(self.params)

    def delete_spice_nodes(self, spice_nodes : list):
        for node_name in spice_nodes:
            self.engine.delete_node(node_name)
            print(f"Deleted node {node_name}")

    def update_parameters(self, params_dict):
        """
               Updates the input parameters of the calculation engine using the provided dictionary. This method
               also triggers the update of the engine's parameters and marks the output data as ready for plot.

               Parameters:
               - params_dict (dict): A dictionary containing the new parameters to be updated in the engine.

               The dict should respect the following format:

                {
                    "param1": value1,
                    "param2": value2,
                    ...
                }

               Returns:
               - dict: The current results after updating the parameters, if any calculation was previously run.
           """
        self.params = params_dict
        new_parameters = InputParameters(self.params)
        self.engine.update_parameters(new_parameters)

        self.is_data_ready = True
        return self.get_current_results()

    def run_calculation(self):
        """
               Executes the calculations based on the current set of parameters and strategies defined in the engine.
               Marks the data as ready and returns the current results.

               Returns:
               - dict: The results of the calculations performed by the engine.
       """
        self.engine.run_calculations()
        self.is_data_ready = True
        return self.get_current_results()

    def get_current_results(self):
        """
                Retrieves the most recent results from the calculation engine output class if the data is marked as
                ready.

                Returns:
                - dict or None: The current results if available; otherwise,
                None if no calculations have been run or data is not ready.
        """
        if not self.is_data_ready:
            return None
        return self.engine.current_output_data.results

    def get_old_results(self):
        """
               Retrieves the previous set of results from the calculation engine.

               Returns:
               - dict: The results of the previous calculations performed by the engine.
           """
        return self.engine.old_output_data.results

    def save_current_results(self, index):
        """
               Saves the current results to the output data of the calculation engine.

               Parameters:
               - index (int): The index of the current results to be saved.
           """
        self.engine.save_calculation_results(index)

    def clear_calculation_results(self):
        """
               Clears the current results from the calculation engine.
           """
        self.engine.clear_calculation_results()

    def set_node_strategy(self, node_name, strategy_class, params_dict):
        strategy_instance = strategy_class()
        # print(strategy_instance)
        self.engine.swap_strategy_for_node(node_name, strategy_instance, params_dict)

    def export_CLTF_NEMI(self, path):
        """
        IF the node is NEMI, and the node CLTF_filtered, plot both in the same graph and save it in the path
        :param path: Full path to save the graph
        :return: SUCCESS or ERROR
        """

        # Retrieve the results of the NEMI node if it exists
        data = self.get_current_results()
        if data is None:
            raise "Error: No data available"

        # Retrieve the results of the CLTF_Filtered node if it exists
        try:
            cltf_data = data.get("CLTF_Filtered", None)
            nemi_data = data.get("NEMI", None)

        except KeyError:
            raise "Error: Missing data for CLTF_Filtered or NEMI"

        try :
            # Plot the data
            import matplotlib.pyplot as plt
            freq_vector = cltf_data["data"][:,0]
            cltf_vector = 20*np.log(cltf_data["data"][:,1])
            nemi_vector = nemi_data["data"][:,1]

            fig, ax1 = plt.subplots()
            color = 'tab:red'
            ax1.set_xlabel('Frequency (Hz)')
            ax1.semilogx()
            ax1.semilogy()

            ax1.set_ylabel('NEMI', color=color)
            ax1.plot(freq_vector, nemi_vector, color=color)
            ax1.tick_params(axis='y', labelcolor=color)

            ax2 = ax1.twinx()
            ax2.semilogx()
            color = 'tab:blue'

            ax2.set_ylabel('CLTF (dB)', color=color)
            ax2.plot(freq_vector, cltf_vector, color=color)
            ax2.tick_params(axis='y', labelcolor=color)

            # add grid
            ax1.grid("both")
            ax2.grid("both")

            path = str(path)

            #if the path does not end with .png
            if not path.endswith(".png"):
                path += ".png"

            print("Saving plot to : " + path)

            plt.savefig(path)


            return "SUCCESS"
        except Exception as e:
            return "ERROR Plotting data : " + str(e)

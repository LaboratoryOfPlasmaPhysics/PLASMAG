import json
import os

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QProgressDialog, QGroupBox, \
    QComboBox, QLineEdit, QTableWidgetItem, QTableWidget, QDialog, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from pint import UnitRegistry

from src.model.optimisation.simulated_annealing import SimulatedAnnealing
from src.model.optimisation.genetic_optimisation import GeneticOptimisation, parameters_dict
from src.model.optimisation.particle_swarm_optimisation import ParticleSwarmOptimization

from PyQt6.QtGui import QDoubleValidator, QColor


ureg: UnitRegistry = UnitRegistry()
def convert_unit(value, from_unit, to_unit):
    """
    Converts the given value from one unit to another using Pint.
    Args:
        value (float): The value to convert.
        from_unit (str): The unit of the input value.
        to_unit (str): The target unit for the conversion.
    Returns:
        float: The converted value.
    """
    if from_unit and to_unit:
        return (value * ureg(from_unit)).to(ureg(to_unit)).magnitude
    return value


class OptimisationTab(QWidget):
    def __init__(self, gui ,parent=None):
        super().__init__(parent)
        self.gui = gui
        self.setup_ui()

        self.optimisation = GeneticOptimisation(100, 20, 0.3, parameters_dict, target_resonance_freq=24430)
        self.pso_optimisation = ParticleSwarmOptimization(parameters_dict)
        self.sa_optimisation = SimulatedAnnealing(parameters_dict, target_resonance_freq=3255, n_iterations=1000, initial_temperature=1000, cooling_rate=0.99)

        self.optimisation.update_signal.connect(self.update_progress)
        self.optimisation.finished_signal.connect(self.display_final_results)

        self.pso_optimisation.update_signal.connect(self.update_progress)
        self.pso_optimisation.finished_signal.connect(self.display_final_results)

        self.sa_optimisation.update_signal.connect(self.update_progress)
        self.sa_optimisation.finished_signal.connect(self.display_final_results)

        self.update_hyperparameters()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)

        # Combobox for method selection
        self.method_combobox = QComboBox()
        self.method_combobox.addItem("Genetic optimisation")
        self.method_combobox.addItem("Particle Swarm optimisation")
        self.method_combobox.addItem("Simulated Annealing")
        self.method_combobox.currentIndexChanged.connect(self.update_hyperparameters)  # Connect the combobox change event
        self.layout.addWidget(self.method_combobox)

        # Scroll area for target selection
        self.target_group_box = QGroupBox("Target")
        self.target_layout = QVBoxLayout()

        self.target_combobox = QComboBox()
        self.target_combobox.addItem("Impedance")
        self.target_combobox.addItem("NEMI(WIP)")
        self.target_combobox.currentIndexChanged.connect(self.update_target)
        self.target_layout.addWidget(self.target_combobox)

        self.target_value_input = QLineEdit()
        self.target_value_input.setPlaceholderText("Enter target impedance value")
        self.target_layout.addWidget(self.target_value_input)

        # NEMI table setup
        self.nemi_table = QTableWidget(3, 1)
        self.nemi_table.setHorizontalHeaderLabels(["Column 1"])
        self.nemi_table.setVerticalHeaderLabels(["Freq", "NEMI Value", "Weight"])
        self.nemi_table.setVisible(False)
        self.nemi_table.itemChanged.connect(self.on_nemi_table_item_changed)
        self.target_layout.addWidget(self.nemi_table)

        self.target_group_box.setLayout(self.target_layout)
        self.layout.addWidget(self.target_group_box)

        # Add hyperparameters section
        self.hyperparameters_group_box = QGroupBox("Hyperparameters")
        self.hyperparameters_layout = QVBoxLayout()
        self.hyperparameters_group_box.setLayout(self.hyperparameters_layout)
        self.layout.addWidget(self.hyperparameters_group_box)

        # Add other controls
        self.label = QLabel("Welcome to the optimisation Tab!")
        self.layout.addWidget(self.label)

        self.optimise_button = QPushButton("Optimise")
        self.optimise_button.clicked.connect(self.on_optimise_clicked)
        self.layout.addWidget(self.optimise_button)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title('Best Fitness over Generations')
        self.ax.grid()
        self.ax.semilogy()
        self.ax.set_xlabel('Generation')
        self.ax.set_ylabel('Best Fitness')

    def update_hyperparameters(self):
        # Clear current hyperparameters layout
        for i in reversed(range(self.hyperparameters_layout.count())):
            self.hyperparameters_layout.itemAt(i).widget().deleteLater()

        method = self.method_combobox.currentText()
        if method == "Genetic optimisation":
            self.add_hyperparameter_field("Number of Generations", "20")
            self.add_hyperparameter_field("Population Size", "100")
            self.add_hyperparameter_field("Mutation Rate", "0.3")
        elif method == "Particle Swarm optimisation":
            self.add_hyperparameter_field("w1", "0.5")
            self.add_hyperparameter_field("c1", "1.0")
            self.add_hyperparameter_field("c2", "1.0")
            self.add_hyperparameter_field("Number of Particles", "50")
            self.add_hyperparameter_field("Number of Iterations", "50")
        elif method == "Simulated Annealing":
            self.add_hyperparameter_field("Cooling Rate", "0.99")
            self.add_hyperparameter_field("Initial Temperature", "5000")
            self.add_hyperparameter_field("Number of Iterations", "2000")

    def add_hyperparameter_field(self, label_text, default_value):
        """
        Add a hyperparameter field to the layout.
        :param label_text:
        :param default_value:
        :return:
        """
        label = QLabel(label_text)
        line_edit = QLineEdit()
        line_edit.setText(default_value)
        self.hyperparameters_layout.addWidget(label)
        self.hyperparameters_layout.addWidget(line_edit)

    def update_target(self):
        """
        Update the target input based on the selected target.
        :return:
        """
        if self.target_combobox.currentText() == "NEMI(WIP)":
            self.target_value_input.setVisible(False)
            self.nemi_table.setVisible(True)
        else:
            self.target_value_input.setVisible(True)
            self.nemi_table.setVisible(False)

    def on_nemi_table_item_changed(self, item):
        """
        Handle the NEMI table item changed event.
        :param item: updated cell item
        :return:
        """
        self.validate_nemi_table()

        if item.column() == self.nemi_table.columnCount() - 1 and item.text():
            self.nemi_table.setColumnCount(self.nemi_table.columnCount() + 1)
            self.nemi_table.setHorizontalHeaderItem(self.nemi_table.columnCount() - 1,
                                                    QTableWidgetItem(f"Column {self.nemi_table.columnCount()}"))

        empty_columns = 0
        for col in range(self.nemi_table.columnCount()):
            is_empty = True
            for row in range(self.nemi_table.rowCount()):
                if self.nemi_table.item(row, col) and self.nemi_table.item(row, col).text():
                    is_empty = False
                    break
            if is_empty:
                empty_columns += 1
            if empty_columns >= 2:
                self.nemi_table.setColumnCount(self.nemi_table.columnCount() - 1)
                self.nemi_table.setHorizontalHeaderItem(self.nemi_table.columnCount() - 1,
                                                        QTableWidgetItem(f"Column {self.nemi_table.columnCount()}"))
                empty_columns -= 1

    def validate_nemi_table(self):
        """
        Table validator for NEMI values.
        If the sum of the weights is not equal to 1, the weight row is highlighted in red.
        If any of the values are invalid, the corresponding cell is highlighted in red.
        :return:
        """
        weight_sum = 0
        is_valid = True
        self.nemi_table.blockSignals(True)  # Block signals temporarily
        try:
            for row in range(self.nemi_table.rowCount()):
                for col in range(self.nemi_table.columnCount()):
                    item = self.nemi_table.item(row, col)
                    if item:
                        try:
                            value = float(item.text())
                            if row == 2:
                                weight_sum += value
                            item.setBackground(QColor(255, 255, 255))  # Set to white for valid input
                        except ValueError:
                            item.setBackground(QColor(255, 0, 0))  # Set to red for invalid input
                            is_valid = False

        finally:
            self.nemi_table.blockSignals(False)  # Unblock signals

        return is_valid

    def on_optimise_clicked(self):
        """Popup message box to confirm the optimisation."""
        try:
            if self.target_combobox.currentText() == "NEMI(WIP)":
                if not self.validate_nemi_table():
                    QMessageBox.warning(self, "Invalid Input", "Please correct the invalid inputs in the NEMI table.")
                    return
                target_value = self.get_nemi_table_values()
            else:
                target_value = float(self.target_value_input.text())
                # Update target resonance frequency based on the selected method
                if self.method_combobox.currentText() == "Genetic optimisation":
                    self.optimisation.update_target_resonance_freq(target_value)
                elif self.method_combobox.currentText() == "Particle Swarm optimisation":
                    self.pso_optimisation.update_target_resonance_freq(target_value)
                elif self.method_combobox.currentText() == "Simulated Annealing":
                    self.sa_optimisation.update_target_resonance_freq(target_value)

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setText("Do you really want to start the optimisation process, it can take few minutes ?")
            msg.setWindowTitle("Confirm")
            msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            msg.setDefaultButton(QMessageBox.StandardButton.No)
            msg.buttonClicked.connect(self.start_optimisation)
            msg.exec()
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid number for the target impedance.")

    def get_nemi_table_values(self):
        """
        Get the values from the table.
        :return:
        """
        nemi_values = {"Freq": [], "NEMI Value": [], "Weight": []}
        for row in range(self.nemi_table.rowCount()):
            for col in range(self.nemi_table.columnCount()):
                item = self.nemi_table.item(row, col)
                if item and item.text():
                    if row == 0:
                        nemi_values["Freq"].append(float(item.text()))
                    elif row == 1:
                        nemi_values["NEMI Value"].append(float(item.text()))
                    elif row == 2:
                        nemi_values["Weight"].append(float(item.text()))
                else:
                    nemi_values["Freq"].append(0)
                    nemi_values["NEMI Value"].append(0)
                    nemi_values["Weight"].append(0)
        return nemi_values

    def start_optimisation(self, button):
        """
        Start the optimisation process, core function to handle the message box button clicked event.
        :param button:
        :return:
        """
        if button.text() == "&Yes":
            # Clear the plot
            self.ax.clear()
            self.ax.set_title('Average Fitness over Generations')
            self.ax.grid()
            self.ax.semilogy()
            self.ax.set_xlabel('Generation')
            self.ax.set_ylabel('Average Fitness')

            hyperparameters = self.get_hyperparameters()

            if self.method_combobox.currentText() == "Genetic optimisation":
                self.optimisation.generations = int(hyperparameters["Number of Generations"])
                self.optimisation.population_size = int(hyperparameters["Population Size"])
                self.optimisation.mutation_rate = float(hyperparameters["Mutation Rate"])
                total_iterations = self.optimisation.generations
            elif self.method_combobox.currentText() == "Particle Swarm optimisation":
                self.pso_optimisation.w1 = float(hyperparameters["w1"])
                self.pso_optimisation.c1 = float(hyperparameters["c1"])
                self.pso_optimisation.c2 = float(hyperparameters["c2"])
                self.pso_optimisation.n_particles = int(hyperparameters["Number of Particles"])
                self.pso_optimisation.n_iterations = int(hyperparameters["Number of Iterations"])
                total_iterations = self.pso_optimisation.n_iterations
            elif self.method_combobox.currentText() == "Simulated Annealing":
                self.sa_optimisation.cooling_rate = float(hyperparameters["Cooling Rate"])
                self.sa_optimisation.initial_temperature = float(hyperparameters["Initial Temperature"])
                self.sa_optimisation.n_iterations = int(hyperparameters["Number of Iterations"])
                total_iterations = self.sa_optimisation.n_iterations

            self.progress_dialog = QProgressDialog("Optimizing...", "Abort", 0, total_iterations, self)
            self.progress_dialog.setModal(True)
            self.progress_dialog.show()

            if self.method_combobox.currentText() == "Genetic optimisation":
                self.optimisation.start()  # Ensure GeneticOptimisation runs in a thread
            elif self.method_combobox.currentText() == "Particle Swarm optimisation":
                self.pso_optimisation.start()  # Ensure PSO runs in a thread
            elif self.method_combobox.currentText() == "Simulated Annealing":
                self.sa_optimisation.start()  # Ensure Simulated Annealing runs in a thread
        else:
            print("optimisation canceled!")

    def get_hyperparameters(self):
        """
        Get the hyperparameters from the input fields.
        :return:
        """
        hyperparameters = {}
        for i in range(self.hyperparameters_layout.count() // 2):
            label = self.hyperparameters_layout.itemAt(2 * i).widget().text()
            value = self.hyperparameters_layout.itemAt(2 * i + 1).widget().text()
            hyperparameters[label] = value
        return hyperparameters

    def update_progress(self, generation, avg_fitness, best_fitness):
        """
        Update the progress dialog and plot the best fitness over generations.
        :param generation: actual generation
        :param avg_fitness: average fitness of the generation
        :param best_fitness: best fitness of the generation
        :return:
        """
        if self.progress_dialog:
            self.progress_dialog.setValue(generation)
            self.ax.plot(generation, best_fitness, 'ro-')  # Plot each point as it comes in
            self.canvas.draw()  # Update the canvas
            if self.method_combobox.currentText() == "Genetic optimisation":
                total_generations = self.optimisation.generations
            elif self.method_combobox.currentText() == "Particle Swarm optimisation":
                total_generations = self.pso_optimisation.n_iterations
            elif self.method_combobox.currentText() == "Simulated Annealing":
                total_generations = self.sa_optimisation.n_iterations

            if generation == total_generations:
                self.progress_dialog.setValue(total_generations)
                self.progress_dialog.close()

    def display_final_results(self, final_params, final_resonance_freq):
        """
        Display the final results of the optimisation.
        :param final_params: best parameters found
        :param final_resonance_freq:
        :return:
        """

        self.progress_dialog.close()

        result_dialog = QDialog(self)
        result_dialog.setWindowTitle("Optimisation Results")
        # big size
        result_dialog.resize(800, 600)


        layout = QVBoxLayout(result_dialog)

        results_text = f"<h2>optimisation Completed!</h2>"
        results_text += f"<p><b>Final Resonance Frequency:</b> {final_resonance_freq:.2f}</p>"
        results_text += "<p><b>Final Parameters:</b></p><ul>"
        for param, value in final_params.items():
            formatted_value = "{:.2e}".format(value)
            results_text += f"<li><b>{param}:</b> {formatted_value}</li>"
        results_text += "</ul>"


        results_label = QLabel(results_text)
        results_label.setWordWrap(True)
        layout.addWidget(results_label)

        save_button = QPushButton("Save Results")
        save_button.clicked.connect(lambda: self.save_results(final_params, export_specific_path=True))
        layout.addWidget(save_button)

        save_button = QPushButton("Load to parameters")
        save_button.clicked.connect(lambda: self.save_results(final_params, export_specific_path=False, reload_to_parameters=True))
        layout.addWidget(save_button)

        result_dialog.setLayout(layout)
        result_dialog.exec()


    def save_results(self, final_params, reload_to_parameters = False,export_specific_path = False):
        """
        Used to save the results of the optimisation to a JSON file or reload the results to the input parameters.
        Also create a temp.json file in the output folder to not lose the results.
        :param final_params: best parameters found
        :param reload_to_parameters: boolean to reload the results to the input parameters
        :param export_specific_path: boolean to export the results to a specific path
        :return:
        """
        try :
            if not export_specific_path:
                # check if /output folder exist

                # if not create it
                try:
                    os.makedirs("output")
                except FileExistsError:
                    pass

                # default path output/temp.json
                path = "output/temp.json"

            else :
                path, _ = QFileDialog.getSaveFileName(self, "Export Optimisation data", "", "json Files (*.png)")

            if not path:
                return

            print("Saving results to:", path)
            print(final_params)

            input_parameters_copy = self.gui.input_parameters.copy()

            print(input_parameters_copy)

            # Update the input parameters with the final results
            for section, params in input_parameters_copy.items():
                if section == "SPICE_circuit" or section == "SPICE":
                    continue
                for param, value in params.items():
                    if str(param) in final_params.keys():
                        input_unit = input_parameters_copy[section][param]["input_unit"]
                        target_unit = input_parameters_copy[section][param]["target_unit"]

                        converted_value = convert_unit(final_params[param], target_unit, input_unit)

                        # only keep 3 decimal places
                        converted_value = round(converted_value, 3)

                        final_params[param] = converted_value

                        input_parameters_copy[section][param]["default"] = final_params[param]
                        print("Updated parameter:", param, "with value:", final_params[param])

            self.saved_path = path

            try :
                # Retrieve the currelnly selected SPICE circuit from the combo box
                selected_circuit = self.gui.spice_circuit_combo.currentText()

                # Add the selected SPICE circuit to the updated parameters
                input_parameters_copy["SPICE_circuit"] = selected_circuit
            except Exception as e:
                print(f"Error adding SPICE circuit to updated parameters: {e}")
                pass

            # Save the results to a file
            with open(path, 'w') as file:
                json.dump(input_parameters_copy, file, indent=4)
                self.reload_on_gui(input_parameters_copy)

        except FileNotFoundError:
            QMessageBox.warning(self, "Invalid File", "Please enter a valid file name.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while saving the results: {e}")


    def reload_on_gui(self, data):
        """
        Reload the results to the input parameters.
        :return:
        """
        # Update the input parameters
        print("Updating input parameters from:", self.saved_path)
        self.gui.import_parameters_from_json(path=self.saved_path, need_filename=False, data=data)
        print("Called function import_parameters_from_json with path:", self.saved_path, "and need_filename:", False)
        self.gui.tabs.setCurrentIndex(0)

    def on_message_box_clicked(self, button):
        """Handle the message box button clicked event."""
        if button.text() == "&Yes":
            print("Optimisation started !")
        else:
            print("Optimisation canceled !")




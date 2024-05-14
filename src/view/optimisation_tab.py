from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QProgressDialog, QGroupBox, \
    QComboBox, QLineEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from src.model.optimisation.simulated_annealing import SimulatedAnnealing
from src.model.optimisation.genetic_optimisation import GeneticOptimisation, parameters_dict
from src.model.optimisation.particle_swarm_optimisation import ParticleSwarmOptimization


class OptimisationTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
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

    def setup_ui(self):
        self.layout = QVBoxLayout(self)

        # Combobox for method selection
        self.method_combobox = QComboBox()
        self.method_combobox.addItem("Genetic Optimization")
        self.method_combobox.addItem("Particle Swarm Optimization")
        self.method_combobox.addItem("Simulated Annealing")
        self.layout.addWidget(self.method_combobox)

        # Scroll area for target selection
        self.target_group_box = QGroupBox("Target")
        self.target_layout = QVBoxLayout()

        self.target_combobox = QComboBox()
        self.target_combobox.addItem("Impedance")
        self.target_layout.addWidget(self.target_combobox)

        self.target_value_input = QLineEdit()
        self.target_value_input.setPlaceholderText("Enter target impedance value")
        self.target_layout.addWidget(self.target_value_input)

        self.target_group_box.setLayout(self.target_layout)
        self.layout.addWidget(self.target_group_box)

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
        self.ax.set_title('Average Fitness over Generations')
        self.ax.grid()
        self.ax.semilogy()
        self.ax.set_xlabel('Generation')
        self.ax.set_ylabel('Average Fitness')



    def on_optimise_clicked(self):
        """Popup message box to confirm the optimisation."""
        try:
            target_value = float(self.target_value_input.text())
            # Update target resonance frequency based on the selected method
            if self.method_combobox.currentText() == "Genetic Optimization":
                self.optimisation.update_target_resonance_freq(target_value)
            elif self.method_combobox.currentText() == "Particle Swarm Optimization":
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


    def start_optimisation(self, button):
        if button.text() == "&Yes":
            # Clear the plot
            self.ax.clear()
            self.ax.set_title('Average Fitness over Generations')
            self.ax.grid()
            self.ax.semilogy()
            self.ax.set_xlabel('Generation')
            self.ax.set_ylabel('Average Fitness')

            if self.method_combobox.currentText() == "Genetic Optimization":
                total_iterations = self.optimisation.generations
            elif self.method_combobox.currentText() == "Particle Swarm Optimization":
                total_iterations = self.pso_optimisation.n_iterations
            elif self.method_combobox.currentText() == "Simulated Annealing":
                total_iterations = self.sa_optimisation.n_iterations

            self.progress_dialog = QProgressDialog("Optimizing...", "Abort", 0, total_iterations, self)  # Update with correct total iterations
            self.progress_dialog.setModal(True)
            self.progress_dialog.show()

            if self.method_combobox.currentText() == "Genetic Optimization":
                self.optimisation.start()
            elif self.method_combobox.currentText() == "Particle Swarm Optimization":
                self.pso_optimisation.start()
            elif self.method_combobox.currentText() == "Simulated Annealing":
                self.sa_optimisation.start()
        else:
            print("Optimization canceled!")

    def update_progress(self, generation, avg_fitness, best_fitness):
        if self.progress_dialog:
            self.progress_dialog.setValue(generation)
            self.ax.plot(generation, best_fitness, 'ro-')  # Plot each point as it comes in
            self.canvas.draw()  # Update the canvas
            if self.method_combobox.currentText() == "Genetic Optimization":
                total_generations = self.optimisation.generations
            elif self.method_combobox.currentText() == "Particle Swarm Optimization":
                total_generations = self.pso_optimisation.n_iterations
            elif self.method_combobox.currentText() == "Simulated Annealing":
                total_generations = self.sa_optimisation.n_iterations

            if generation == total_generations - 1:
                self.progress_dialog.setValue(total_generations)
                self.progress_dialog.close()

    def display_final_results(self, final_params, final_resonance_freq):
        if self.progress_dialog:
            self.progress_dialog.close()
        message = (f"Optimization Completed!\n\n"
                   f"Final Resonance Frequency: {final_resonance_freq:.2f}\n"
                   f"Final Parameters:\n{final_params}")
        QMessageBox.information(self, "Optimisation Results", message)

    def on_message_box_clicked(self, button):
        """Handle the message box button clicked event."""
        if button.text() == "&Yes":
            print("Optimisation started !")
        else:
            print("Optimisation canceled !")








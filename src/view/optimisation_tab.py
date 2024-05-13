from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox


class OptimisationTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)

        self.label = QLabel("Welcome to the optimisation Tab !")
        self.layout.addWidget(self.label)

        self.optimise_button = QPushButton("Optimise")
        self.optimise_button.clicked.connect(self.on_optimise_clicked)
        self.layout.addWidget(self.optimise_button)

    def on_optimise_clicked(self):
        """Popup message box to confirm the optimisation."""

        #show a message box inside a popup
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText("Do you really want to start the optimisation process, it can take few minutes ?")
        msg.setWindowTitle("Confirm")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setDefaultButton(QMessageBox.StandardButton.No)
        msg.buttonClicked.connect(self.on_message_box_clicked)
        msg.exec()

    def on_message_box_clicked(self, button):
        """Handle the message box button clicked event."""
        if button.text() == "&Yes":
            print("Optimisation started !")
        else:
            print("Optimisation canceled !")





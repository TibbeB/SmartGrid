import sys
import os
from main import Smartgrid
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget
os.environ['QT_QPA_PLATFORM'] = 'xcb'

class SimpleGUI(QWidget):
    def __init__(self):
        super().__init__()

        # Create widgets
        self.label = QLabel("Hello, PyQt5!")
        self.button = QPushButton("Click Me")
        self.button.clicked.connect(self.on_button_click)

        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        # Set the main layout for the window
        self.setLayout(layout)

        # Set window properties
        self.setWindowTitle("Simple PyQt5 GUI")
        self.setGeometry(100, 100, 300, 150)

    def on_button_click(self):
        self.label.setText("Button Clicked!")

if __name__ == "__main__":
    # Create the Qt Application
    app = QApplication(sys.argv)

    # Create an instance of your application's GUI
    window = SimpleGUI()

    # Show the GUI
    window.show()

    # Run the application's event loop
    sys.exit(app.exec())
## IMPORTS ##

import sys
from core.sys import display

from PySide6.QtWidgets import (
    QApplication, QPushButton, QMainWindow, QLabel
)
from PySide6.QtCore import Slot

# multiple windows support:
opened_windows = []


# Main Class
class GurkeViewer(QMainWindow):

    def InitializeGurkeViewer(self):
        main_display_resolution = display.get_display_resolution(0) or (1280, 720)
        self.resize(main_display_resolution[0], main_display_resolution[1])
        
        ... # TODO: Create window, set window name, intialize ui

    # GurkeViewer Init:
    def __init__(self, window_instance_name: str):
        super().__init__()

        # Pre-Loading

        

        # Attributes:
        self.window_name: str = window_instance_name
        """Description: Name of the Window."""

        

        self.InitializeGurkeViewer()
        

    

app = QApplication(sys.argv)

# First Window:

main_window = GurkeViewer("Gurke Viewer - Main")
opened_windows.append(main_window)

sys.exit(app.exec())


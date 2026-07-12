## IMPORTS ##

## PACKAGES ##

import sys
from typing import TypedDict

from PySide6.QtWidgets import (
    QApplication, QPushButton, QMainWindow, QLabel
)

## UTILS ##

from core.sys import display
from core.random import randomizer
from states import state_manager

## MAIN PROGRAM ##

## WINDOW SETTINGS ##

class WindowSettingsOverrides(TypedDict, total=False):
    window_initial_resolution: tuple[int, int]
    window_name: str
    window_resizable: bool 

class WindowSettings(TypedDict):
    window_initial_resolution: tuple[int, int]
    window_name: str
    window_resizable: bool


# Main Class
class GurkeViewer(QMainWindow):

    def InitializeGurkeViewer(self):
        ## WINDOW INIT ##

        window_initial_resolution = self.WINDOW_SETTINGS.get("window_initial_resolution")
        window_initial_resolution_X = window_initial_resolution[0]
        window_initial_resolution_Y = window_initial_resolution[1]

        window_title = self.WINDOW_SETTINGS.get("window_name")
        self.setWindowTitle(window_title)

        if self.WINDOW_SETTINGS.get("window_resizable") == False:
            self.setFixedSize(window_initial_resolution_X, window_initial_resolution_Y)
        else:
            self.setBaseSize(window_initial_resolution_X, window_initial_resolution_Y)


        self.show()
        ... # TODO: Create window, set window name, intialize ui
        

    # GurkeViewer Init:
    def __init__(self, WindowSettings: WindowSettingsOverrides | None = None):
        super().__init__()

        # default settings:
        self.WINDOW_SETTINGS: WindowSettings = {
            "window_initial_resolution": display.get_display_resolution(0) or (1280, 720),
            "window_name": "Gurke Viewer - " + randomizer.get_random_string_uuid4(),
            "window_resizable": True
        }
        """
        
            Args:
                window_intial_resolution (tuple[int, int]): The intial Window Resolution the Window will be rendered at startup.
                window_name (str): The Window Name
                window_resizable (bool): Whether the Window can be resized by the User, when false, the Window will stay at the 'window_initial_resolution' forever.
        
        """
        
        if WindowSettings is not None:
            self.WINDOW_SETTINGS.update(WindowSettings)

        self.InitializeGurkeViewer()
        

## WINDOW CREATION ##

# multiple windows support:
opened_windows = []


def CreateWindow(WindowSettings: WindowSettingsOverrides) -> GurkeViewer:
    """

    Creates a new Gurke Viewer window, with the given WindowSettings.

    """

    window = GurkeViewer(WindowSettings=WindowSettings)
    opened_windows.append(window)

    state_manager.edit_ui_state("OpenedWindowsAmount", len(opened_windows))
    return window


app = QApplication(sys.argv)

# First Window:

main_window = CreateWindow({
        "window_name": "Gurke Viewer - Main",
    })

sys.exit(app.exec())


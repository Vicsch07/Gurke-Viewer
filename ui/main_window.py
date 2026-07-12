## IMPORTS & PACKAGES ##

import sys
from typing import TypedDict

from PySide6.QtWidgets import (
    QApplication, QPushButton, QMainWindow, QLabel, QToolBar, QVBoxLayout, QWidget, QHBoxLayout
)

from PySide6.QtCore import (
    QSize, Qt
)



## UTILS ##

from core.sys import display
from core.random import randomizer
from states import state_manager
from ui.utils import (
    ui_position
)
from ui.elements import (
    topbar
)

## MAIN PROGRAM ##

## STYLESHEET ##

STYLE_SHEET = """



"""

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
            self.resize(window_initial_resolution_X, window_initial_resolution_Y)
            
        self.center_on_screen()


        self.show()
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # We align top so the topbar stays at the top
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.topbar = QWidget()
        self.topbar.setStyleSheet("""
            QWidget {
                background-color: #FF00FF; /* Bright Magenta */
                border: 4px solid #00FF00; /* Bright Green Border */
            }
            QPushButton {
                background-color: #FFFF00; /* Bright Yellow Button */
                color: #000000;            /* Black Text */
                font-weight: bold;
                border: 2px solid #FF0000; /* Red Border around Button */
                padding: 5px;
            }
        """)
        self.topbar_horizontal_layout = QHBoxLayout(self.topbar)
        self.topbar_horizontal_layout.setContentsMargins(15, 0, 15, 0)
        self.topbar_horizontal_layout.setSpacing(10)

        self.debug_label = QLabel("DEBUG: TOPBAR IS VISIBLE")
        
        # Make it highly visible with a dark background, white text, and a cyan border
        self.debug_label.setStyleSheet("""
            background-color: #333333;
            color: #FFFFFF;
            font-weight: bold;
            font-size: 14px;
            padding: 8px;
            border: 2px dashed #00FFFF;
        """)
        
        # Center the text inside the label
        self.debug_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Add the label to your topbar's horizontal layout
        self.topbar_horizontal_layout.addWidget(self.debug_label)

        # Add the topbar to the main layout
        self.main_layout.addWidget(self.topbar)
        

    def center_on_screen(self):
        ui_position.center_ui_on_screen(self)

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


def main():
    app = QApplication(sys.argv)

    # First Window:

    main_window = CreateWindow({
            "window_name": "Gurke Viewer - Main",
            "window_initial_resolution": (1280, 720)
        })

    try:
        app.exec()
    except KeyboardInterrupt:
        pass
    except Exception as err:
        print("Generic Error while loading:", err)

    return 

main()
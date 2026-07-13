## IMPORTS & PACKAGES ##

from typing import TypedDict

from PySide6.QtWidgets import (
    QApplication, QPushButton, QMainWindow, QLabel, QVBoxLayout,
      QWidget, QHBoxLayout, QSizePolicy, QSplitter
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
from ui.elements.file_explorer import FileExplorer


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

    def _create_topbar_button(self, text: str) -> QPushButton:
        button = QPushButton(text)
        button.setFixedWidth(40)
        button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)


        return button
    
    def _add_widget_to_topbar(self, widget: QWidget) -> None:
        self.topbar_horizontal_layout.addWidget(widget)

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

        ## Show Screen
        self.show()
        
        ## WIDGETS SETUP ##

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        ## Topbar stays at top
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        ## Topbar Creation
        self.topbar = QWidget()
        self.topbar.setFixedHeight(40)
        self.topbar.setStyleSheet("""

            QPushButton {
                background: transparent;
                border-radius: 0px;
            }
            

        """)

       
        ## Layout
        self.topbar_horizontal_layout = QHBoxLayout(self.topbar) # parent of topbar
        self.topbar_horizontal_layout.setContentsMargins(5, 7, 15, 7) # y, top, x, bottom
        self.topbar_horizontal_layout.setSpacing(0) # idk

        ## Topbar Items
        self.topbar_undo_button = self._create_topbar_button("<")

        self.topbar_redo_button = self._create_topbar_button(">")

        self.topbar_elevate_button = self._create_topbar_button("^")


        ## Add Items to Topbar
        self._add_widget_to_topbar(self.topbar_undo_button)
        self._add_widget_to_topbar(self.topbar_redo_button)
        self._add_widget_to_topbar(self.topbar_elevate_button)

        ## Push everything to the left, -> undo_button, redo_button, elevate_button, refresh_button
        self.topbar_horizontal_layout.addStretch()

       

        

        ## Add the topbar to the main layout
        self.main_layout.addWidget(self.topbar)

         ## Make everything under the topbar correctly sized & positioned:

        self.body_splitter = QSplitter(Qt.Orientation.Horizontal)

        ## FileExplorer View ##

        self.file_explorer = FileExplorer(self)
        self.body_splitter.addWidget(self.file_explorer)

        ## Content View Setup ##

        self.content_view = QWidget()
        self.content_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        ## DEBUG:

        self.content_view.setStyleSheet("background-color: #ffffff")
        
        ## Add the Content View to body layout
        self.body_splitter.addWidget(self.content_view)

        ## Metadata Viewer Setup ##

        self.meta_view = QWidget()
        self.meta_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.meta_view.setMaximumWidth(300)

        ## DEBUG:

        self.meta_view.setStyleSheet("background-color: #ffffff")

        ## Add the Meta View to body layout
        self.body_splitter.addWidget(self.meta_view)
        
        self.main_layout.addWidget(self.body_splitter)
        


        

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
    app = QApplication([])

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
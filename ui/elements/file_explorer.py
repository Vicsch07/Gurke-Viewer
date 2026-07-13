from typing import TYPE_CHECKING

from PySide6.QtWidgets import (
    QWidget, QSizePolicy, QScrollArea, QHBoxLayout, QPushButton, QVBoxLayout
)

from PySide6.QtCore import (
    Qt
)

from states import state_manager
## Fix circular import, and fix QMainWindow type annotation
if TYPE_CHECKING:
    from ui.main_window import GurkeViewer
    
## CONSTANTS:

## TODO: Connect to settings.ini and settings window to change.

## Whether or not to snap the File Explorer at the FILE_EXPLORER_SNAPPING_TARGET_PX point
ENABLE_FILE_EXPLORER_SNAPPING = True

## At which point the snapping starts
FILE_EXPLORER_SNAPPING_LOWER_BOUND_PX = 150

## At which point the snapping at ends
FILE_EXPLORER_SNAPPING_UPPER_BOUND_PX = 170 # TODO: Change to FILE_EXPLORER_SNAPPING_TARGET_THRESHOLD = 25px which does it automatically

## At which point the File Explorer should be snapped at
FILE_EXPLORER_SNAPPING_TARGET_PX = 160 + 2 # 40 * 4 (4 items in topbar) + 2 (vline width)

class FileExplorer(QWidget):
    def _load_file(self):
        ... # TODO: Resolve which plugin to use, then load it with the plugin

    def _add_file_to_file_explorer(self, file_name: str) -> None:
        file_button = QPushButton(file_name)
        file_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        file_button.setFixedHeight(50)

        self.scroll_layout.addWidget(file_button)


    def _on_body_splitter_moved(self, pos: int, idx: int) -> None:
        if not ENABLE_FILE_EXPLORER_SNAPPING:
            return None

        if idx == 1: # idk why actually
            sizes = self.main_window.body_splitter.sizes()
            file_explorer_width = sizes[0]

            if FILE_EXPLORER_SNAPPING_LOWER_BOUND_PX <= file_explorer_width <= FILE_EXPLORER_SNAPPING_UPPER_BOUND_PX:
                adjustment = FILE_EXPLORER_SNAPPING_TARGET_PX - file_explorer_width
                sizes[0] = FILE_EXPLORER_SNAPPING_TARGET_PX
                sizes[1] = sizes[1] - adjustment

                ## temp suspend signals to prevent infinite recursion
                self.main_window.body_splitter.blockSignals(True)

                self.main_window.body_splitter.setSizes(sizes)
                self.main_window.body_splitter.setStretchFactor(0, 0)

                self.main_window.body_splitter.blockSignals(False)
            else:
                self.main_window.body_splitter.setStretchFactor(1, 1)
        
        ...
        
    def __init__(self, main_window: 'GurkeViewer'):
        super().__init__()
        
        self.main_window = main_window
        self.setMaximumWidth(400)
        self.setMinimumWidth(FILE_EXPLORER_SNAPPING_TARGET_PX)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

        ## Snap the file explorer width to 300px when in a 25px range before then releasing the snap again when over or below 25px of 300px width
        main_window.body_splitter.splitterMoved.connect(self._on_body_splitter_moved)
        
        self.file_explorer_layout = QHBoxLayout(self)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.scroll_content = QWidget()
        
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(5, 5, 5, 5)

        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_area.setWidget(self.scroll_content)

        self.file_explorer_layout.addWidget(self.scroll_area)

        self._add_file_to_file_explorer("lol.mp4")


        ...
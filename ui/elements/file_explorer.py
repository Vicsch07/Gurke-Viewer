from typing import TYPE_CHECKING

from PySide6.QtWidgets import (
    QWidget, QSizePolicy
)

## CONSTANTS:

## TODO: Connect to settings.ini and settings window to change.

## Whether or not to snap the File Explorer at the FILE_EXPLORER_SNAPPING_TARGET_PX point
ENABLE_FILE_EXPLORER_SNAPPING = True

## At which point the snapping starts
FILE_EXPLORER_SNAPPING_LOWER_BOUND_PX = 275

## At which point the snapping at ends
FILE_EXPLORER_SNAPPING_UPPER_BOUND_PX = 325 # TODO: Change to FILE_EXPLORER_SNAPPING_TARGET_THRESHOLD = 25px which does it automatically

## At which point the File Explorer should be snapped at
FILE_EXPLORER_SNAPPING_TARGET_PX = 300

## Fix circular import, and fix QMainWindow type annotation
if TYPE_CHECKING:
    from ui.main_window import GurkeViewer

class FileExplorer(QWidget):
    def _on_body_splitter_moved(self, pos: int, idx: int) -> None:
        if not ENABLE_FILE_EXPLORER_SNAPPING:
            return None

        if idx == 1:
            sizes = self.main_window.body_splitter.sizes()
            file_explorer_width = sizes[0]

            if FILE_EXPLORER_SNAPPING_LOWER_BOUND_PX <= file_explorer_width <= FILE_EXPLORER_SNAPPING_UPPER_BOUND_PX:
                adjustment = FILE_EXPLORER_SNAPPING_TARGET_PX - file_explorer_width
                sizes[0] = FILE_EXPLORER_SNAPPING_TARGET_PX
                sizes[1] = sizes[1] - adjustment

                ## temp suspend signals to prevent infinite recursion
                self.main_window.body_splitter.blockSignals(True)

                self.main_window.body_splitter.setSizes(sizes)

                self.main_window.body_splitter.blockSignals(False)
        
        ...
        
    def __init__(self, main_window: 'GurkeViewer'):
        super().__init__()
        
        self.main_window = main_window
        self.setMaximumWidth(400)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        ## Snap the file explorer width to 300px when in a 25px range before then releasing the snap again when over or below 25px of 300px width
        main_window.body_splitter.splitterMoved.connect(self._on_body_splitter_moved)
        
        ...
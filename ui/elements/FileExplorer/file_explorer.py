from typing import TYPE_CHECKING

from PySide6.QtWidgets import (
    QWidget, QSizePolicy, QScrollArea, QHBoxLayout,
    QPushButton, QVBoxLayout, QFrame
)

from PySide6.QtCore import (
    Qt, QVariantAnimation
)

from PySide6.QtGui import (
    QColor
)

from ui.classes.CQPushButton import CQPushButton
from ui.elements.FileExplorer.utils.file_classes import GFile

from states import state_manager
## Fix circular import, and fix QMainWindow type annotation
if TYPE_CHECKING:
    from ui.main_window import GurkeViewer


## CONSTANTS:


## TODO: Connect to settings.ini and settings window to change.

## Whether or not to snap the File Explorer at the FILE_EXPLORER_SNAPPING_TARGET_PX point
ENABLE_FILE_EXPLORER_SNAPPING = True

## At which threshold around the FILE_EXPLORER_SNAPPING_TARGET_PX the snapping should begin and end, for example:
## FILE_EXPLORER_SNAPPING_TARGET_THRESHOLD = 15, FILE_EXPLORER_SNAPPING_TARGET_PX = 162
## that would be equivalent to: FILE_EXPLORER_SNAPPING_LOWER_BOUND_PX = 147 and FILE_EXPLORER_SNAPPING_UPPER_BOUND_PX = 177
##
## Note: the begin threshold is not applicable when settings minimum File Explorer width to FILE_EXPLORER_SNAPPING_TARGET_PX or when: FILE_EXPLORER_MINIMUM_WIDTH - FILE_EXPLORER_SNAPPING_THRESHOLD_PX <= 0
FILE_EXPLORER_SNAPPING_TARGET_THRESHOLD_PX = 15

## At which point the File Explorer should be snapped at
FILE_EXPLORER_SNAPPING_TARGET_PX = 160 + 2 # 40 * 4 (4 items in topbar) + 2 (vline width)

## At which point the body splitter should no longer retract and keep completely retract the file explorer window
FILE_EXPLORER_MINIMUM_WIDTH = FILE_EXPLORER_SNAPPING_TARGET_PX

## At which point the body splitter should no longer extend the file explorer window
FILE_EXPLORER_MAXIMUM_WIDTH = 400

## Extension lookup

from ui.elements.FileExplorer.extension_plugins import file_extension_png
file_extension_lookup = {
    ".png": file_extension_png
}


## MAIN CLASS ##


class FileExplorer(QWidget):
    def _load_file(self, gfile: GFile):
        file_loader_plugin = file_extension_lookup[gfile.FileExtension]
        if not file_loader_plugin:
            return
        
        file_loader_plugin.load()
        ... # TODO: Resolve which plugin to use, then load it with the plugin

    def _add_file_to_file_explorer(self, gfile: GFile) -> None:
        file_button = CQPushButton(gfile.FileName)
        file_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        file_button.setFixedHeight(40) # 32 + ((up / down padding) = 4 * 2 == 8) = 40
        file_button.clicked.connect(self._load_file)

        self.scroll_layout.addWidget(file_button)


    def _on_body_splitter_moved(self, pos: int, idx: int) -> None:
        if not ENABLE_FILE_EXPLORER_SNAPPING:
            return None

        if idx == 1: # idk why actually
            sizes = self.main_window.body_splitter.sizes()
            file_explorer_width = sizes[0]

            if FILE_EXPLORER_SNAPPING_TARGET_PX - FILE_EXPLORER_SNAPPING_TARGET_THRESHOLD_PX <= file_explorer_width <= FILE_EXPLORER_SNAPPING_TARGET_PX + FILE_EXPLORER_SNAPPING_TARGET_THRESHOLD_PX:
                adjustment = FILE_EXPLORER_SNAPPING_TARGET_PX - file_explorer_width
                sizes[0] = FILE_EXPLORER_SNAPPING_TARGET_PX
                sizes[1] = sizes[1] - adjustment

                ## temp suspend signals to prevent infinite recursion
                self.main_window.body_splitter.blockSignals(True)

                self.main_window.body_splitter.setSizes(sizes)
                self.main_window.body_splitter.setStretchFactor(0, 0) # so it doesn't stretch when resizing window when snapped to point

                self.main_window.body_splitter.blockSignals(False)
            else:
                self.main_window.body_splitter.setStretchFactor(1, 1)
        
        ...
        
    def __init__(self, main_window: 'GurkeViewer'):
        super().__init__()
        
        self.main_window = main_window
        self.setMaximumWidth(FILE_EXPLORER_MAXIMUM_WIDTH)
        self.setMinimumWidth(FILE_EXPLORER_MINIMUM_WIDTH)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

        ## Snap the file explorer width to 300px when in a 25px range before then releasing the snap again when over or below 25px of 300px width
        main_window.body_splitter.splitterMoved.connect(self._on_body_splitter_moved)
        
        self.file_explorer_layout = QHBoxLayout(self)
        self.file_explorer_layout.setSpacing(0)
        self.file_explorer_layout.setContentsMargins(0, 0, 0, 0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setContentsMargins(0, 0, 0, 0)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(0)

        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_area.setWidget(self.scroll_content)

        self.file_explorer_layout.addWidget(self.scroll_area)


        ...
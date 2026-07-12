
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt

class Topbar(QWidget):

    def build_topbar(self):
        pass
        ## TOPBAR WIDGET ##

        self.topbar = QWidget()#parent=self.main_window)

        ## HORIZONTAL LAYOUT SETUP ##

        self.topbar_horizontal_layout = QHBoxLayout(self.main_window)
        self.topbar_horizontal_layout.setContentsMargins(15, 0, 15, 0)
        self.topbar_horizontal_layout.setSpacing(10)

        ## TOPBAR ITEMS ##

        ## TEST ITEM ##

        self.test_item = QPushButton()
        self.topbar_horizontal_layout.addWidget(self.test_item)


    def hide_topbar(self):
        ... # TODO: Hide topbar here...


    def __init__(self, main_window: QMainWindow):
        

        self.main_window = main_window

        self.build_topbar()






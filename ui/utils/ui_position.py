from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtGui import QScreen

def center_ui_on_screen(window: QMainWindow) -> None:
    screen = QApplication.primaryScreen().geometry()

    x = (screen.width() - window.width()) // 2
    y = (screen.height() - window.height()) // 2

    window.move(x, y)


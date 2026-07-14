from PySide6.QtWidgets import (
    QPushButton
)

from PySide6.QtGui import (
    QColor
)

from PySide6.QtCore import (
    QVariantAnimation
)

# Custom QPushButton
class CQPushButton(QPushButton):
    def _anim_update_stylesheet(self) -> None:
        self.setStyleSheet(f"""
        
        QPushButton {{
            background-color: {self._anim_background_color.name()};
            border: none;
        }}

        
        
    """)
        
    def _on_color_changed(self, color: QColor):
        self._anim_background_color = color
        self._anim_update_stylesheet()

    def _animate_to(self, target_color: QColor):
        self._anim_background.stop()
        self._anim_background.setStartValue(self._anim_background_color)
        self._anim_background.setEndValue(target_color)
        self._anim_background.start()

    def enterEvent(self, event):
        self._animate_to(self.BUTTON_HOVER_BACKGROUND_COLOR)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._animate_to(self.BUTTON_BACKGROUND_COLOR)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self._animate_to(self.BUTTON_PRESSED_BACKGROUND_COLOR)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.underMouse():
            self._animate_to(self.BUTTON_HOVER_BACKGROUND_COLOR)
        else:
            self._animate_to(self.BUTTON_BACKGROUND_COLOR)
        
        super().mouseReleaseEvent(event)

    def __init__(self, text: str | None):
        super().__init__()

        self.setText(text or "CQPB. text?")
        
        self.BUTTON_BACKGROUND_COLOR = QColor("#1e1e1e")
        self.BUTTON_HOVER_BACKGROUND_COLOR = QColor("#2f2f2f")
        self.BUTTON_PRESSED_BACKGROUND_COLOR = QColor("#000000")

        self._anim_background_color = QColor(self.BUTTON_BACKGROUND_COLOR)
        self._anim_update_stylesheet()

        self._anim_background = QVariantAnimation(self)
        self._anim_background.setDuration(150)
        self._anim_background.valueChanged.connect(self._on_color_changed)

        ...

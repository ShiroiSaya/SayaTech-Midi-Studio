from __future__ import annotations

from PySide6.QtCore import QEasingCurve, QPropertyAnimation, Qt, QTimer
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import QApplication, QWidget


class GlowEffect(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.glow_radius = 0
        self.glow_color = QColor("#4f8cff")
        self._anim = QPropertyAnimation(self, b"glow_radius", self)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def start_glow(self, duration_ms: int = 300) -> None:
        self._anim.stop()
        self._anim.setDuration(duration_ms)
        self._anim.setStartValue(0)
        self._anim.setEndValue(12)
        self._anim.start()

    def stop_glow(self, duration_ms: int = 200) -> None:
        self._anim.stop()
        self._anim.setDuration(duration_ms)
        self._anim.setStartValue(self.glow_radius)
        self._anim.setEndValue(0)
        self._anim.start()

    def paintEvent(self, event):
        if self.glow_radius <= 0:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        color = QColor(self.glow_color)
        for i in range(3):
            alpha = int(255 * (1 - i / 3) * (self.glow_radius / 12))
            color.setAlpha(alpha)
            painter.setPen(QPen(color, 2))
            painter.drawEllipse(
                self.rect().adjusted(i * 2, i * 2, -i * 2, -i * 2)
            )


class PulseEffect(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.pulse_scale = 1.0
        self._anim = QPropertyAnimation(self, b"pulse_scale", self)
        self._anim.setEasingCurve(QEasingCurve.InOutQuad)
        self._anim.setLoopCount(-1)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def start_pulse(self, duration_ms: int = 1000) -> None:
        self._anim.stop()
        self._anim.setDuration(duration_ms)
        self._anim.setStartValue(1.0)
        self._anim.setEndValue(1.1)
        self._anim.start()

    def stop_pulse(self) -> None:
        self._anim.stop()
        self.pulse_scale = 1.0
        self.update()


class ShimmerEffect(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.shimmer_pos = 0.0
        self._anim = QPropertyAnimation(self, b"shimmer_pos", self)
        self._anim.setEasingCurve(QEasingCurve.Linear)
        self._anim.setLoopCount(-1)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def start_shimmer(self, duration_ms: int = 2000) -> None:
        self._anim.stop()
        self._anim.setDuration(duration_ms)
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.start()

    def stop_shimmer(self) -> None:
        self._anim.stop()
        self.shimmer_pos = 0.0
        self.update()

    def paintEvent(self, event):
        if self.shimmer_pos <= 0:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        path = QPainterPath()
        path.addRect(self.rect())

        gradient_width = self.width() * 0.3
        x = self.shimmer_pos * self.width() - gradient_width

        painter.setOpacity(0.3)
        painter.fillRect(
            int(x), 0, int(gradient_width), self.height(),
            QColor("#ffffff")
        )


def apply_ui_enhancements(app: QApplication) -> None:
    app.setProperty("uiEnhancementsEnabled", True)
    app.setProperty("uiGlowEnabled", True)
    app.setProperty("uiPulseEnabled", True)
    app.setProperty("uiShimmerEnabled", True)
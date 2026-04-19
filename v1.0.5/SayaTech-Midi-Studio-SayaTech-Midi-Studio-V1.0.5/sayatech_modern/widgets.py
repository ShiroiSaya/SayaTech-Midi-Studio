from __future__ import annotations

from typing import Optional

from PySide6.QtCore import QEasingCurve, Property, QPropertyAnimation, QRect, Qt, Signal
from PySide6.QtGui import QColor, QCursor, QPainter, QPen
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QDialog,
    QGraphicsOpacityEffect,
    QPushButton,
    QStackedWidget,
    QWidget,
)

from .theme import _palette


def _animations_enabled() -> bool:
    app = QApplication.instance()
    return bool(app.property("uiAnimationsEnabled")) if app else True


def _animation_speed() -> int:
    app = QApplication.instance()
    return int(app.property("uiAnimationSpeed") or 100) if app else 100


def animation_duration(base_ms: int) -> int:
    speed = max(40, _animation_speed())
    return max(40, int(base_ms * 100 / speed))


class AnimatedButton(QPushButton):
    def __init__(self, text: str = "", parent: Optional[QWidget] = None):
        super().__init__(text, parent)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self._opacity_effect = QGraphicsOpacityEffect(self)
        self._opacity_effect.setOpacity(1.0)
        self.setGraphicsEffect(self._opacity_effect)
        self._anim = QPropertyAnimation(self._opacity_effect, b"opacity", self)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)

    def _animate_to(self, value: float) -> None:
        if not _animations_enabled():
            self._opacity_effect.setOpacity(value)
            return
        self._anim.stop()
        self._anim.setDuration(animation_duration(120))
        self._anim.setStartValue(self._opacity_effect.opacity())
        self._anim.setEndValue(value)
        self._anim.start()

    def mousePressEvent(self, event):
        self._animate_to(0.78)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self._animate_to(1.0)
        super().mouseReleaseEvent(event)

    def leaveEvent(self, event):
        self._animate_to(1.0)
        super().leaveEvent(event)


class AnimatedSwitch(QCheckBox):
    toggledAnimated = Signal(bool)

    def __init__(self, text: str = "", parent: Optional[QWidget] = None):
        super().__init__(text, parent)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setMinimumHeight(28)
        self._offset = 1.0 if self.isChecked() else 0.0
        self._anim = QPropertyAnimation(self, b"offset", self)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)
        self.toggled.connect(self._start_transition)

    def sizeHint(self):
        hint = super().sizeHint()
        hint.setHeight(max(30, hint.height()))
        hint.setWidth(max(72, hint.width() + 12))
        return hint

    def _get_offset(self) -> float:
        return self._offset

    def _set_offset(self, value: float) -> None:
        self._offset = float(value)
        self.update()

    offset = Property(float, _get_offset, _set_offset)

    def _target_offset(self) -> float:
        return 1.0 if self.isChecked() else 0.0

    def _sync_offset_immediately(self) -> None:
        self._anim.stop()
        self._set_offset(self._target_offset())

    def setChecked(self, checked: bool) -> None:
        checked = bool(checked)
        before = self.isChecked()
        super().setChecked(checked)
        if self.signalsBlocked() or before == self.isChecked():
            self._sync_offset_immediately()

    def _start_transition(self, checked: bool) -> None:
        end = 1.0 if bool(checked) else 0.0
        if not _animations_enabled():
            self._set_offset(end)
            self.toggledAnimated.emit(bool(checked))
            return
        self._anim.stop()
        self._anim.setDuration(animation_duration(160))
        self._anim.setStartValue(self._offset)
        self._anim.setEndValue(end)
        self._anim.start()
        self.toggledAnimated.emit(bool(checked))

    def hitButton(self, pos):
        return self.contentsRect().contains(pos)

    def _resolve_colors(self) -> tuple[QColor, QColor, QColor, QColor]:
        app = QApplication.instance()
        is_dark = bool(app.property("uiDarkMode")) if app else False
        preset = str(app.property("uiThemePreset") or "ocean") if app else "ocean"
        palette = _palette(is_dark, preset)
        text_color = QColor(palette["text"])
        off_track = QColor(palette["track"])
        on_track = QColor(palette["accent"])
        border = QColor(palette["border"])
        thumb = QColor("#f8fafc") if is_dark else QColor("#ffffff")
        return text_color, off_track, on_track, thumb, border

    def paintEvent(self, event):
        _ = event
        if not self._anim.state() and abs(self._offset - self._target_offset()) > 0.001:
            self._offset = self._target_offset()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        text_color, off_track, on_track, thumb, border = self._resolve_colors()

        rect = self.contentsRect()
        track_w = 42
        track_h = 24
        track_x = rect.x()
        track_y = rect.y() + (rect.height() - track_h) / 2
        track_rect = QRect(int(track_x), int(track_y), track_w, track_h)
        radius = track_h / 2

        painter.setPen(Qt.NoPen)
        painter.setBrush(on_track if self.isChecked() else off_track)
        painter.drawRoundedRect(track_rect, radius, radius)
        painter.setPen(QPen(border, 1))
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(track_rect, radius, radius)

        knob_margin = 3
        knob_d = track_h - knob_margin * 2
        knob_x = track_rect.x() + knob_margin + int((track_w - knob_d - knob_margin * 2) * self._offset)
        knob_rect = QRect(knob_x, track_rect.y() + knob_margin, knob_d, knob_d)
        painter.setPen(Qt.NoPen)
        painter.setBrush(thumb)
        painter.drawEllipse(knob_rect)

        if self.text():
            painter.setPen(text_color)
            text_rect = QRect(track_rect.right() + 10, rect.y(), rect.width() - track_w - 14, rect.height())
            painter.drawText(text_rect, Qt.AlignVCenter | Qt.AlignLeft, self.text())


class FadeStackedWidget(QStackedWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._effect = None
        self._anim = None

    def fade_to_index(self, index: int) -> None:
        if index == self.currentIndex():
            return
        self.setCurrentIndex(index)
        widget = self.currentWidget()
        if widget is None:
            return
        if not _animations_enabled():
            return
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        effect.setOpacity(0.0)
        anim = QPropertyAnimation(effect, b"opacity", widget)
        anim.setDuration(animation_duration(180))
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.OutCubic)

        def cleanup():
            widget.setGraphicsEffect(None)

        anim.finished.connect(cleanup)
        self._effect = effect
        self._anim = anim
        anim.start()


class FadeDialog(QDialog):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setObjectName("Surface")
        self.setAttribute(Qt.WA_StyledBackground, True)

    def showEvent(self, event):
        super().showEvent(event)
        if not _animations_enabled():
            return
        self.setWindowOpacity(0.0)
        anim = QPropertyAnimation(self, b"windowOpacity", self)
        anim.setDuration(animation_duration(140))
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.OutCubic)

        def cleanup():
            try:
                self.setWindowOpacity(1.0)
            except Exception:
                pass

        anim.finished.connect(cleanup)
        self._fade_anim = anim
        anim.start()

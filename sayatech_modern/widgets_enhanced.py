"""
Enhanced Widget Components for SayaTech MIDI Studio
Includes LoadingSpinner, Toast notifications, and improved AnimatedButton
"""

from __future__ import annotations

from typing import Optional, Callable
from PySide6.QtCore import QTimer, Qt, QEasingCurve, QPropertyAnimation, QRect, Property, Signal
from PySide6.QtGui import QColor, QCursor, QPainter, QFont, QConicalGradient
from PySide6.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout


class LoadingSpinner(QWidget):
    """Animated loading spinner with configurable size and speed"""
    
    def __init__(self, size: int = 32, speed: int = 100, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setMinimumSize(size, size)
        self.setMaximumSize(size, size)
        self._size = size
        self._speed = max(40, min(220, speed))  # Constrain speed
        self._rotation = 0
        self._timer = QTimer()
        self._timer.timeout.connect(self._on_rotation_tick)
        self._is_running = False
        
    def _on_rotation_tick(self):
        """Update rotation angle"""
        self._rotation = (self._rotation + 6) % 360
        self.update()
        
    def start(self):
        """Start the spinner animation"""
        if not self._is_running:
            self._is_running = True
            # Calculate interval based on speed setting
            interval = max(10, int(20 * 100 / self._speed))
            self._timer.start(interval)
        
    def stop(self):
        """Stop the spinner animation"""
        self._timer.stop()
        self._is_running = False
        self._rotation = 0
        self.update()
        
    def is_running(self) -> bool:
        """Check if spinner is currently animating"""
        return self._is_running
        
    def set_speed(self, speed: int):
        """Update animation speed (40-220%)"""
        self._speed = max(40, min(220, speed))
        if self._is_running:
            interval = max(10, int(20 * 100 / self._speed))
            self._timer.setInterval(interval)
        
    def paintEvent(self, _event):
        """Paint the loading spinner"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Translate to center
        painter.translate(self._size / 2, self._size / 2)
        painter.rotate(self._rotation)
        
        # Get theme colors
        app = QApplication.instance()
        is_dark = bool(app.property("uiDarkMode")) if app else False
        accent = QColor("#4f8cff" if is_dark else "#2563eb")
        
        # Draw spinner with gradient
        radius = self._size / 4
        rect = QRect(-int(radius), -int(radius), int(radius * 2), int(radius * 2))
        
        # Create conical gradient for smooth appearance
        gradient = QConicalGradient(0, 0, 0)
        gradient.setColorAt(0.0, QColor(accent.red(), accent.green(), accent.blue(), 255))
        gradient.setColorAt(0.4, QColor(accent.red(), accent.green(), accent.blue(), 200))
        gradient.setColorAt(0.7, QColor(accent.red(), accent.green(), accent.blue(), 100))
        gradient.setColorAt(1.0, QColor(accent.red(), accent.green(), accent.blue(), 0))
        
        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(rect)
        
        # Draw center dot
        painter.setBrush(QColor(accent))
        painter.drawEllipse(-2, -2, 4, 4)


class Toast(QWidget):
    """Non-blocking notification toast widget"""
    
    POSITION_TOP_RIGHT = "top_right"
    POSITION_TOP_LEFT = "top_left"
    POSITION_BOTTOM_RIGHT = "bottom_right"
    POSITION_BOTTOM_LEFT = "bottom_left"
    
    STATUS_INFO = "info"
    STATUS_SUCCESS = "success"
    STATUS_ERROR = "error"
    STATUS_WARNING = "warning"
    
    def __init__(self, message: str, duration_ms: int = 3000, status: str = STATUS_INFO, 
                 parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.message = message
        self.status = status
        self.duration_ms = max(1000, min(10000, duration_ms))
        self._opacity = 1.0
        
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMinimumWidth(320)
        self.setMaximumWidth(480)
        self.setMinimumHeight(56)
        
        # Animation
        self._fade_anim = None
        self._auto_close_timer = QTimer()
        self._auto_close_timer.setSingleShot(True)
        self._auto_close_timer.timeout.connect(self.hide_with_animation)
        
    def _get_opacity(self) -> float:
        return self._opacity
        
    def _set_opacity(self, value: float):
        self._opacity = float(value)
        self.setWindowOpacity(value)
        
    opacity = Property(float, _get_opacity, _set_opacity)
    
    def show_notification(self, position: str = POSITION_TOP_RIGHT):
        """Display the notification toast"""
        # Position the widget
        screen = QApplication.primaryScreen()
        if screen:
            screen_geo = screen.geometry()
            margin = 20
            
            if position == self.POSITION_TOP_RIGHT:
                x = screen_geo.right() - self.width() - margin
                y = screen_geo.top() + margin
            elif position == self.POSITION_TOP_LEFT:
                x = screen_geo.left() + margin
                y = screen_geo.top() + margin
            elif position == self.POSITION_BOTTOM_LEFT:
                x = screen_geo.left() + margin
                y = screen_geo.bottom() - self.height() - margin
            else:  # POSITION_BOTTOM_RIGHT
                x = screen_geo.right() - self.width() - margin
                y = screen_geo.bottom() - self.height() - margin
            
            self.move(int(x), int(y))
        
        # Show with fade-in
        self.show()
        self.setWindowOpacity(0.0)
        
        fade_in = QPropertyAnimation(self, b"opacity")
        fade_in.setDuration(200)
        fade_in.setStartValue(0.0)
        fade_in.setEndValue(1.0)
        fade_in.setEasingCurve(QEasingCurve.OutCubic)
        fade_in.start()
        
        # Auto-close timer
        self._auto_close_timer.start(self.duration_ms)
        self._fade_anim = fade_in
        
    def hide_with_animation(self):
        """Hide the notification with fade-out animation"""
        fade_out = QPropertyAnimation(self, b"opacity")
        fade_out.setDuration(200)
        fade_out.setStartValue(1.0)
        fade_out.setEndValue(0.0)
        fade_out.setEasingCurve(QEasingCurve.InCubic)
        fade_out.finished.connect(self.close)
        fade_out.start()
        self._fade_anim = fade_out
        
    def paintEvent(self, _event):
        """Paint the toast notification"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Get theme
        app = QApplication.instance()
        is_dark = bool(app.property("uiDarkMode")) if app else False
        
        # Status colors (accent, background)
        status_colors = {
            self.STATUS_SUCCESS: {
                "accent": "#34d399" if is_dark else "#10b981",
                "bg": "#064e3b" if is_dark else "#d1fae5",
                "text": "#d1fae5" if is_dark else "#065f46",
            },
            self.STATUS_ERROR: {
                "accent": "#f87171" if is_dark else "#ef4444",
                "bg": "#7f1d1d" if is_dark else "#fee2e2",
                "text": "#fecaca" if is_dark else "#991b1b",
            },
            self.STATUS_WARNING: {
                "accent": "#fbbf24" if is_dark else "#f59e0b",
                "bg": "#78350f" if is_dark else "#fef3c7",
                "text": "#fde68a" if is_dark else "#92400e",
            },
            self.STATUS_INFO: {
                "accent": "#60a5fa" if is_dark else "#3b82f6",
                "bg": "#1e3a8a" if is_dark else "#dbeafe",
                "text": "#93c5fd" if is_dark else "#1e40af",
            },
        }
        
        colors = status_colors.get(self.status, status_colors[self.STATUS_INFO])
        
        # Background with rounded corners
        radius = 12
        painter.setBrush(QColor(colors["bg"]))
        painter.setPen(QColor(colors["accent"] + "80"))
        painter.drawRoundedRect(self.rect(), radius, radius)
        
        # Left accent bar
        painter.fillRect(0, 0, 4, self.height(), QColor(colors["accent"]))
        
        # Text
        painter.setPen(QColor(colors["text"]))
        font = QFont("Microsoft YaHei UI", 11)
        font.setWeight(500)
        painter.setFont(font)
        
        text_rect = QRect(20, 8, self.width() - 40, self.height() - 16)
        painter.drawText(text_rect, Qt.AlignVCenter | Qt.TextWordWrap, self.message)


class AnimatedButtonEnhanced(QWidget):
    """Enhanced animated button with scale and shadow effects"""
    
    clicked = Signal()
    
    def __init__(self, text: str = "", parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.text_label = text
        self._is_pressed = False
        self._scale = 1.0
        self._opacity = 1.0
        self._hover = False
        
        # Animations
        self._scale_anim = QPropertyAnimation(self, b"button_scale")
        self._scale_anim.setEasingCurve(QEasingCurve.OutBack)
        
        self._opacity_anim = QPropertyAnimation(self, b"button_opacity")
        self._opacity_anim.setEasingCurve(QEasingCurve.OutCubic)
        
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setMinimumHeight(40)
        self.setMinimumWidth(100)
        
    def _get_scale(self) -> float:
        return self._scale
        
    def _set_scale(self, value: float):
        self._scale = float(value)
        self.update()
        
    def _get_opacity(self) -> float:
        return self._opacity
        
    def _set_opacity(self, value: float):
        self._opacity = float(value)
        self.update()
        
    button_scale = Property(float, _get_scale, _set_scale)
    button_opacity = Property(float, _get_opacity, _set_opacity)
    
    def _get_animation_speed(self) -> int:
        """Get animation speed from app settings"""
        app = QApplication.instance()
        return int(app.property("uiAnimationSpeed") or 100) if app else 100
    
    def mousePressEvent(self, event):
        """Handle mouse press with scale animation"""
        self._is_pressed = True
        
        # Scale down
        self._scale_anim.stop()
        self._scale_anim.setDuration(max(100, int(140 * 100 / self._get_animation_speed())))
        self._scale_anim.setStartValue(self._scale)
        self._scale_anim.setEndValue(0.96)
        self._scale_anim.start()
        
        # Dim opacity
        self._opacity_anim.stop()
        self._opacity_anim.setDuration(100)
        self._opacity_anim.setStartValue(self._opacity)
        self._opacity_anim.setEndValue(0.85)
        self._opacity_anim.start()
        
        super().mousePressEvent(event)
        
    def mouseReleaseEvent(self, event):
        """Handle mouse release with bounce animation"""
        self._is_pressed = False
        
        # Scale back up
        self._scale_anim.stop()
        self._scale_anim.setDuration(max(100, int(200 * 100 / self._get_animation_speed())))
        self._scale_anim.setStartValue(self._scale)
        self._scale_anim.setEndValue(1.0)
        self._scale_anim.start()
        
        # Restore opacity
        self._opacity_anim.stop()
        self._opacity_anim.setDuration(150)
        self._opacity_anim.setStartValue(self._opacity)
        self._opacity_anim.setEndValue(1.0)
        self._opacity_anim.start()
        
        self.clicked.emit()
        super().mouseReleaseEvent(event)
        
    def enterEvent(self, event):
        """Handle hover enter"""
        self._hover = True
        self.update()
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        """Handle hover leave"""
        self._hover = False
        if not self._is_pressed:
            self._scale_anim.stop()
            self._scale_anim.setDuration(150)
            self._scale_anim.setStartValue(self._scale)
            self._scale_anim.setEndValue(1.0)
            self._scale_anim.start()
        self.update()
        super().leaveEvent(event)
        
    def paintEvent(self, _event):
        """Paint the button"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Set opacity
        painter.setOpacity(self._opacity)
        
        # Get theme colors
        app = QApplication.instance()
        is_dark = bool(app.property("uiDarkMode")) if app else False
        theme_preset = str(app.property("uiThemePreset") or "ocean") if app else "ocean"
        
        from .theme import _palette
        palette = _palette(is_dark, theme_preset)
        
        # Calculate dimensions with scale
        width = int(self.width() * self._scale)
        height = int(self.height() * self._scale)
        x = (self.width() - width) // 2
        y = (self.height() - height) // 2
        
        rect = QRect(x, y, width, height)
        radius = 10
        
        # Background color
        if self._hover:
            bg_color = QColor(palette["surface3"])
        else:
            bg_color = QColor(palette["surface2"])
        
        if self._is_pressed:
            bg_color = QColor(palette["surface"])
        
        # Draw background
        painter.setBrush(bg_color)
        painter.setPen(QColor(palette["border"]))
        painter.drawRoundedRect(rect, radius, radius)
        
        # Draw text
        painter.setPen(QColor(palette["text"]))
        painter.setFont(QFont("Microsoft YaHei UI", 11, 600))
        painter.drawText(self.rect(), Qt.AlignCenter, self.text_label)

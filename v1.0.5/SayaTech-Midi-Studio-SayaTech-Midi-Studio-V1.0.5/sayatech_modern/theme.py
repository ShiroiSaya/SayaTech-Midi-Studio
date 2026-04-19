from __future__ import annotations


def _base_palette(dark_mode: bool):
    if dark_mode:
        return {
            "bg": "#03060b",
            "surface": "#09111c",
            "surface2": "#0d1624",
            "surface3": "#132033",
            "text": "#edf2fa",
            "muted": "#91a0b8",
            "border": "#1f2b3b",
            "accent": "#4f8cff",
            "accentText": "#f8fbff",
            "tab": "#101927",
            "tabSelected": "#0a0f18",
            "track": "#28354a",
            "slider": "#6ea8ff",
            "selection": "#3b82f6",
            "selectionText": "#f8fafc",
            "logBg": "#060b12",
        }
    return {
        "bg": "#f6f3f5",
        "surface": "#ffffff",
        "surface2": "#fffdfd",
        "surface3": "#fff8fb",
        "text": "#192433",
        "muted": "#64748b",
        "border": "#e2d7dc",
        "accent": "#2563eb",
        "accentText": "#ffffff",
        "tab": "#fff5f8",
        "tabSelected": "#ffffff",
        "track": "#d5dfec",
        "slider": "#2563eb",
        "selection": "#2563eb",
        "selectionText": "#ffffff",
        "logBg": "#fcfbfc",
    }


def _apply_preset(c: dict, preset: str, dark_mode: bool) -> dict:
    preset = (preset or "ocean").strip().lower()
    if preset == "violet":
        c.update({
            "accent": "#8b5cf6" if not dark_mode else "#a78bfa",
            "slider": "#8b5cf6" if not dark_mode else "#a78bfa",
            "selection": "#8b5cf6" if not dark_mode else "#7c3aed",
            "tab": "#f3efff" if not dark_mode else "#1a132c",
            "surface3": "#f5f1ff" if not dark_mode else "#211938",
        })
    elif preset == "emerald":
        c.update({
            "accent": "#059669" if not dark_mode else "#34d399",
            "slider": "#059669" if not dark_mode else "#34d399",
            "selection": "#059669" if not dark_mode else "#059669",
            "tab": "#ebfbf6" if not dark_mode else "#10241d",
            "surface3": "#eefcf8" if not dark_mode else "#142a22",
        })
    elif preset == "sunset":
        c.update({
            "accent": "#ea580c" if not dark_mode else "#fb923c",
            "slider": "#ea580c" if not dark_mode else "#fb923c",
            "selection": "#ea580c" if not dark_mode else "#ea580c",
            "tab": "#fff1e9" if not dark_mode else "#29180f",
            "surface3": "#fff5ef" if not dark_mode else "#301c13",
        })
    elif preset == "graphite":
        c.update({
            "accent": "#475569" if not dark_mode else "#94a3b8",
            "slider": "#475569" if not dark_mode else "#94a3b8",
            "selection": "#475569" if not dark_mode else "#64748b",
            "tab": "#eef2f6" if not dark_mode else "#111927",
            "surface3": "#f2f5f8" if not dark_mode else "#182131",
        })
    return c


def _palette(dark_mode: bool, preset: str = "ocean"):
    return _apply_preset(_base_palette(dark_mode), preset, dark_mode)


def build_stylesheet(dark_mode: bool = False, scale_percent: int = 100, preset: str = "ocean", backdrop_enabled: bool = False) -> str:
    c = _palette(dark_mode, preset)
    scale = max(0.8, min(1.4, scale_percent / 100.0))
    font = max(11, round(12.2 * scale))
    title = max(18, round(21 * scale))
    section = max(14, round(15 * scale))
    radius_card = max(14, round(18 * scale))
    radius_side = max(16, round(20 * scale))
    radius_control = max(9, round(12 * scale))
    padding_y = max(6, round(8 * scale))
    padding_x = max(10, round(13 * scale))
    field_height = max(18, round(20 * scale))
    slider_handle = max(14, round(16 * scale))
    checkbox_spacing = max(10, round(12 * scale))
    page_bg = "transparent" if backdrop_enabled and not dark_mode else c["bg"]
    scroll_bg = "transparent" if backdrop_enabled and not dark_mode else c["bg"]
    main_bg = c["bg"] if dark_mode else "transparent" if backdrop_enabled else c["bg"]
    return f"""
QApplication, QMainWindow, QWidget#Surface, QDialog#Surface, QWidget#Page, QWidget#CenterSurface, QStackedWidget {{
    background: {main_bg};
    color: {c['text']};
    font-family: 'Microsoft YaHei UI', 'Segoe UI Variable Text', 'PingFang SC', 'Noto Sans SC', sans-serif;
    font-size: {font}px;
}}
QWidget {{
    color: {c['text']};
    font-family: 'Microsoft YaHei UI', 'Segoe UI Variable Text', 'PingFang SC', 'Noto Sans SC', sans-serif;
    font-size: {font}px;
}}
QScrollArea, QAbstractScrollArea, QAbstractScrollArea::viewport, QStackedWidget {{
    background: {scroll_bg};
    border: none;
}}
QAbstractScrollArea > QWidget, QScrollArea > QWidget, QWidget#Page, QWidget#CenterSurface, QWidget#Surface {{
    background: {page_bg};
    border: none;
}}
QSplitter, QSplitterHandle {{
    background: {page_bg};
}}
QDialog#Surface {{
    border-radius: {radius_card}px;
}}
QLabel {{
    background: transparent;
    color: {c['text']};
}}
QMainWindow, QFrame#Surface {{
    background: {main_bg};
}}
QFrame#Card, QFrame#Sidebar {{
    background: transparent;
    border: none;
}}
QPushButton {{
    background: {c['surface2']};
    border: 1px solid {c['border']};
    border-radius: {radius_control}px;
    padding: {padding_y}px {padding_x}px;
    font-weight: 600;
}}
QPushButton:hover, QToolButton:hover {{
    border-color: {c['accent']};
    background: {c['surface3']};
}}
QPushButton[primary="true"] {{
    background: {c['accent']};
    color: {c['accentText']};
    border: none;
    font-weight: 700;
}}
QPushButton[primary="true"]:hover {{
    background: {c['accent']};
}}
QToolButton {{
    background: {c['surface2']};
    border: 1px solid {c['border']};
    border-radius: {radius_control}px;
    padding: {padding_y}px {padding_x}px;
    font-weight: 700;
}}
QLineEdit, QListWidget, QTreeWidget, QTextEdit, QPlainTextEdit, QTabWidget::pane, QComboBox, QSpinBox, QDoubleSpinBox, QKeySequenceEdit, QAbstractSpinBox {{
    background: {c['surface']};
    border: 1px solid {c['border']};
    border-radius: {radius_control}px;
    selection-background-color: {c['selection']};
    selection-color: {c['selectionText']};
}}
QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QSpinBox, QDoubleSpinBox, QKeySequenceEdit, QAbstractSpinBox {{
    padding: {padding_y}px {padding_x}px;
    min-height: {field_height}px;
}}
QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus, QKeySequenceEdit:focus, QAbstractSpinBox:focus, QPlainTextEdit:focus, QListWidget:focus, QTreeWidget:focus {{
    border: 1px solid {c['accent']};
    outline: none;
}}
QAbstractSpinBox QLineEdit, QSpinBox QLineEdit, QDoubleSpinBox QLineEdit {{
    background: transparent;
    border: none;
    color: {c['text']};
    selection-background-color: {c['selection']};
    selection-color: {c['selectionText']};
    padding: 0px;
}}
QPlainTextEdit {{
    background: {c['logBg']};
    font-family: 'Consolas', 'JetBrains Mono', 'Microsoft YaHei UI';
}}
QComboBox::drop-down {{
    border: none;
    width: 22px;
}}
QSpinBox::up-button, QSpinBox::down-button, QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {{
    width: 18px;
    border: none;
}}
QCheckBox {{
    spacing: {checkbox_spacing}px;
    font-weight: 600;
}}
QCheckBox::indicator {{
    width: 0px;
    height: 0px;
}}
QListWidget, QTreeWidget {{
    outline: none;
}}
QListWidget#NavList, QListWidget#NavList:focus {{
    background: transparent;
    border: none;
}}
QListWidget#NavList::item {{
    margin: 3px 0;
    padding: 10px 12px;
    border: none;
    border-radius: 10px;
    color: {c['text']};
}}
QListWidget#NavList::item:hover {{
    background: {c['surface3']};
}}
QListWidget#NavList::item:selected {{
    background: {c['accent']};
    color: {c['accentText']};
    border: none;
    outline: none;
}}
QTreeWidget::item {{
    padding: 6px;
}}
QTreeWidget::item:selected {{
    background: {c['selection']};
    color: {c['selectionText']};
    border-radius: 8px;
}}
QHeaderView::section {{
    background: {c['surface2']};
    border: none;
    border-bottom: 1px solid {c['border']};
    padding: 6px 8px;
    font-weight: 700;
}}
QTabWidget::pane {{
    border: none;
    background: transparent;
}}
QTabBar::tab {{
    background: {c['tab']};
    border: 1px solid {c['border']};
    border-radius: {radius_control}px;
    padding: {padding_y}px {padding_x}px;
    margin-right: 6px;
    color: {c['muted']};
}}
QTabBar::tab:selected {{
    background: {c['tabSelected']};
    color: {c['text']};
}}
QSlider::groove:horizontal {{
    height: 8px;
    border-radius: 4px;
    background: {c['track']};
}}
QSlider::handle:horizontal {{
    background: {c['slider']};
    width: {slider_handle}px;
    margin: -4px 0;
    border-radius: {int(slider_handle/2)}px;
}}
QScrollBar:vertical {{
    width: 10px;
    background: transparent;
}}
QScrollBar::handle:vertical {{
    background: {c['track']};
    border-radius: 5px;
}}
QLabel[muted="true"] {{
    color: {c['muted']};
}}
QLabel[title="true"] {{
    font-size: {title}px;
    font-weight: 700;
}}
QLabel[sectionTitle="true"] {{
    font-size: {section}px;
    font-weight: 700;
    color: {c['text']};
}}
QLabel[sectionDesc="true"] {{
    color: {c['muted']};
    padding-bottom: 2px;
}}
QLabel[fieldLabel="true"] {{
    font-weight: 600;
    color: {c['text']};
}}
QLabel[watermark="true"] {{
    color: {c['muted']};
    font-weight: 700;
    letter-spacing: 0.5px;
}}
QLabel[badge="true"] {{
    background: {c['accent']};
    color: {c['accentText']};
    border-radius: 10px;
    padding: 6px 12px;
    font-weight: 700;
}}
QLabel[kpiTitle="true"] {{
    color: {c['muted']};
    font-size: {max(12, round(12 * scale))}px;
    font-weight: 600;
}}
QLabel[kpiValue="true"] {{
    color: {c['text']};
    font-size: {max(16, round(17 * scale))}px;
    font-weight: 700;
}}
QLabel#StatusValue {{
    font-size: {max(15, round(16 * scale))}px;
    font-weight: 700;
}}
"""

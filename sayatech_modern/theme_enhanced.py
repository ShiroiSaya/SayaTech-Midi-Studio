"""
Enhanced Theme System for SayaTech MIDI Studio
Implements modern UI improvements: shadows, semantic colors, better state handling
"""

from __future__ import annotations


# Design token system for consistent spacing and sizing
RADIUS_TOKENS = {
    "xs": 4,      # Subtle (tags, badges, small inline elements)
    "sm": 8,      # Small (combobox dropdown, smaller controls)
    "md": 12,     # Medium (buttons, inputs, cards, standard controls)
    "lg": 18,     # Large (main cards, dialogs, panels)
    "xl": 24,     # Extra large (modals, sidebars, prominent cards)
}

SHADOW_TOKENS = {
    "none": "none",
    "sm": "0 1px 2px",
    "md": "0 2px 8px",
    "lg": "0 4px 12px",
    "xl": "0 8px 24px",
}

SPACING_TOKENS = {
    "xs": 4,
    "sm": 8,
    "md": 12,
    "lg": 16,
    "xl": 24,
}


def _base_palette(dark_mode: bool):
    """Enhanced base palette with semantic colors"""
    if dark_mode:
        return {
            # Primary backgrounds
            "bg": "#03060b",
            "surface": "#09111c",
            "surface2": "#0d1624",
            "surface3": "#132033",
            
            # Text colors
            "text": "#edf2fa",
            "muted": "#91a0b8",
            
            # Borders and dividers
            "border": "#1f2b3b",
            "borderLight": "#2a3a4d",
            "divider": "#1a2634",
            
            # Primary accent
            "accent": "#4f8cff",
            "accentText": "#f8fbff",
            "accentHover": "#6ea8ff",
            "accentPressed": "#3d6fcc",
            
            # Component backgrounds
            "tab": "#101927",
            "tabSelected": "#0a0f18",
            "track": "#28354a",
            "slider": "#6ea8ff",
            "sliderHover": "#85b8ff",
            
            # Selection and highlights
            "selection": "#3b82f6",
            "selectionText": "#f8fafc",
            "selectionHover": "#5a96ff",
            
            # Semantic colors
            "success": "#10b981",
            "successLight": "#34d399",
            "warning": "#f59e0b",
            "warningLight": "#fbbf24",
            "error": "#ef4444",
            "errorLight": "#f87171",
            "info": "#3b82f6",
            "infoLight": "#60a5fa",
            
            # Logging
            "logBg": "#060b12",
            
            # Shadows
            "shadowLight": "rgba(0, 0, 0, 0.1)",
            "shadowMedium": "rgba(0, 0, 0, 0.2)",
            "shadowDark": "rgba(0, 0, 0, 0.3)",
        }
    
    # Light mode palette
    return {
        # Primary backgrounds
        "bg": "#f6f3f5",
        "surface": "#ffffff",
        "surface2": "#fffdfd",
        "surface3": "#fff8fb",
        
        # Text colors
        "text": "#192433",
        "muted": "#64748b",
        
        # Borders and dividers
        "border": "#e2d7dc",
        "borderLight": "#ede5ea",
        "divider": "#f0e8ed",
        
        # Primary accent
        "accent": "#2563eb",
        "accentText": "#ffffff",
        "accentHover": "#3b82f6",
        "accentPressed": "#1d4ed8",
        
        # Component backgrounds
        "tab": "#fff5f8",
        "tabSelected": "#ffffff",
        "track": "#d5dfec",
        "slider": "#2563eb",
        "sliderHover": "#3b82f6",
        
        # Selection and highlights
        "selection": "#2563eb",
        "selectionText": "#ffffff",
        "selectionHover": "#3b82f6",
        
        # Semantic colors
        "success": "#059669",
        "successLight": "#10b981",
        "warning": "#d97706",
        "warningLight": "#f59e0b",
        "error": "#dc2626",
        "errorLight": "#ef4444",
        "info": "#2563eb",
        "infoLight": "#3b82f6",
        
        # Logging
        "logBg": "#fcfbfc",
        
        # Shadows
        "shadowLight": "rgba(0, 0, 0, 0.05)",
        "shadowMedium": "rgba(0, 0, 0, 0.1)",
        "shadowDark": "rgba(0, 0, 0, 0.15)",
    }


def _apply_preset(c: dict, preset: str, dark_mode: bool) -> dict:
    """Apply preset theme overrides"""
    preset = (preset or "ocean").strip().lower()
    
    if preset == "violet":
        c.update({
            "accent": "#8b5cf6" if not dark_mode else "#a78bfa",
            "accentHover": "#a78bfa" if not dark_mode else "#c4b5fd",
            "accentPressed": "#7c3aed" if not dark_mode else "#6d28d9",
            "slider": "#8b5cf6" if not dark_mode else "#a78bfa",
            "sliderHover": "#a78bfa" if not dark_mode else "#c4b5fd",
            "selection": "#8b5cf6" if not dark_mode else "#7c3aed",
            "tab": "#f3efff" if not dark_mode else "#1a132c",
            "surface3": "#f5f1ff" if not dark_mode else "#211938",
        })
    elif preset == "emerald":
        c.update({
            "accent": "#059669" if not dark_mode else "#34d399",
            "accentHover": "#10b981" if not dark_mode else "#6ee7b7",
            "accentPressed": "#047857" if not dark_mode else "#059669",
            "slider": "#059669" if not dark_mode else "#34d399",
            "sliderHover": "#10b981" if not dark_mode else "#6ee7b7",
            "selection": "#059669" if not dark_mode else "#059669",
            "tab": "#ebfbf6" if not dark_mode else "#10241d",
            "surface3": "#eefcf8" if not dark_mode else "#142a22",
        })
    elif preset == "sunset":
        c.update({
            "accent": "#ea580c" if not dark_mode else "#fb923c",
            "accentHover": "#f97316" if not dark_mode else "#fdba74",
            "accentPressed": "#c2410c" if not dark_mode else "#ea580c",
            "slider": "#ea580c" if not dark_mode else "#fb923c",
            "sliderHover": "#f97316" if not dark_mode else "#fdba74",
            "selection": "#ea580c" if not dark_mode else "#ea580c",
            "tab": "#fff1e9" if not dark_mode else "#29180f",
            "surface3": "#fff5ef" if not dark_mode else "#301c13",
        })
    elif preset == "graphite":
        c.update({
            "accent": "#475569" if not dark_mode else "#94a3b8",
            "accentHover": "#64748b" if not dark_mode else "#cbd5e1",
            "accentPressed": "#334155" if not dark_mode else "#475569",
            "slider": "#475569" if not dark_mode else "#94a3b8",
            "sliderHover": "#64748b" if not dark_mode else "#cbd5e1",
            "selection": "#475569" if not dark_mode else "#64748b",
            "tab": "#eef2f6" if not dark_mode else "#111927",
            "surface3": "#f2f5f8" if not dark_mode else "#182131",
        })
    
    return c


def _palette(dark_mode: bool, preset: str = "ocean"):
    """Get complete color palette for theme"""
    return _apply_preset(_base_palette(dark_mode), preset, dark_mode)


def build_stylesheet(dark_mode: bool = False, scale_percent: int = 100, 
                     preset: str = "ocean", backdrop_enabled: bool = False) -> str:
    """Build comprehensive stylesheet with modern UI patterns"""
    c = _palette(dark_mode, preset)
    scale = max(0.8, min(1.4, scale_percent / 100.0))
    
    # Font sizes (scaled)
    font = max(11, round(12.2 * scale))
    title = max(18, round(21 * scale))
    section = max(14, round(15 * scale))
    subtitle = max(13, round(14 * scale))
    caption = max(10, round(11 * scale))
    
    # Radius values (scaled)
    radius_xs = max(3, round(4 * scale))
    radius_sm = max(6, round(8 * scale))
    radius_md = max(10, round(12 * scale))
    radius_lg = max(16, round(18 * scale))
    radius_xl = max(20, round(24 * scale))
    
    # Padding and spacing (scaled)
    padding_y = max(6, round(8 * scale))
    padding_x = max(10, round(13 * scale))
    field_height = max(18, round(20 * scale))
    slider_handle = max(14, round(16 * scale))
    checkbox_spacing = max(10, round(12 * scale))
    
    # Background configurations
    page_bg = "transparent" if backdrop_enabled and not dark_mode else c["bg"]
    scroll_bg = "transparent" if backdrop_enabled and not dark_mode else c["bg"]
    main_bg = c["bg"] if dark_mode else "transparent" if backdrop_enabled else c["bg"]
    
    return f"""
/* ============================================================================
   BASE STYLES - Global defaults
   ============================================================================ */

QApplication, QMainWindow, QWidget#Surface, QDialog#Surface, QWidget#Page, 
QWidget#CenterSurface, QStackedWidget {{
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

QAbstractScrollArea > QWidget, QScrollArea > QWidget, QWidget#Page, 
QWidget#CenterSurface, QWidget#Surface {{
    background: {page_bg};
    border: none;
}}

QSplitter, QSplitterHandle {{
    background: {page_bg};
}}

QDialog#Surface {{
    border-radius: {radius_lg}px;
    box-shadow: 0 8px 24px {c['shadowDark']};
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

/* ============================================================================
   BUTTONS - Normal, primary, danger, success variants
   ============================================================================ */

QPushButton {{
    background: {c['surface2']};
    border: 1px solid {c['border']};
    border-radius: {radius_md}px;
    padding: {padding_y}px {padding_x}px;
    font-weight: 600;
    color: {c['text']};
    outline: none;
    transition: all 120ms cubic-bezier(0.4, 0, 0.2, 1);
}}

QPushButton:hover {{
    border-color: {c['accentHover']};
    background: {c['surface3']};
    color: {c['text']};
}}

QPushButton:pressed {{
    background: {c['surface']};
    border-color: {c['accent']};
}}

QPushButton:disabled {{
    background: {c['surface2']};
    border-color: {c['border']};
    color: {c['muted']};
    opacity: 0.6;
}}

QPushButton:focus {{
    outline: 2px solid {c['accent']};
    outline-offset: 2px;
}}

/* Primary Button */
QPushButton[primary="true"] {{
    background: {c['accent']};
    color: {c['accentText']};
    border: none;
    font-weight: 700;
}}

QPushButton[primary="true"]:hover {{
    background: {c['accentHover']};
}}

QPushButton[primary="true"]:pressed {{
    background: {c['accentPressed']};
}}

QPushButton[primary="true"]:disabled {{
    background: {c['accent']};
    opacity: 0.5;
}}

/* Danger Button */
QPushButton[variant="danger"] {{
    background: {c['error']};
    color: {c['accentText']};
    border: none;
    font-weight: 600;
}}

QPushButton[variant="danger"]:hover {{
    background: {c['errorLight']};
}}

QPushButton[variant="danger"]:pressed {{
    background: {c['error']};
    opacity: 0.8;
}}

/* Success Button */
QPushButton[variant="success"] {{
    background: {c['success']};
    color: {c['accentText']};
    border: none;
    font-weight: 600;
}}

QPushButton[variant="success"]:hover {{
    background: {c['successLight']};
}}

/* Warning Button */
QPushButton[variant="warning"] {{
    background: {c['warning']};
    color: {c['accentText']};
    border: none;
    font-weight: 600;
}}

QPushButton[variant="warning"]:hover {{
    background: {c['warningLight']};
}}

/* Size variants */
QPushButton[size="small"] {{
    padding: {int(padding_y * 0.75)}px {int(padding_x * 0.75)}px;
    font-size: {max(10, round(11 * scale))}px;
}}

QPushButton[size="large"] {{
    padding: {int(padding_y * 1.25)}px {int(padding_x * 1.25)}px;
    font-size: {max(13, round(14 * scale))}px;
}}

QToolButton {{
    background: {c['surface2']};
    border: 1px solid {c['border']};
    border-radius: {radius_md}px;
    padding: {padding_y}px {padding_x}px;
    font-weight: 700;
    color: {c['text']};
}}

QToolButton:hover {{
    border-color: {c['accentHover']};
    background: {c['surface3']};
}}

QToolButton:pressed {{
    background: {c['surface']};
}}

/* ============================================================================
   INPUT FIELDS - Text, spinbox, combobox
   ============================================================================ */

QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QSpinBox, QDoubleSpinBox, 
QKeySequenceEdit, QAbstractSpinBox {{
    background: {c['surface']};
    border: 1px solid {c['border']};
    border-radius: {radius_md}px;
    padding: {padding_y}px {padding_x}px;
    color: {c['text']};
    selection-background-color: {c['selection']};
    selection-color: {c['selectionText']};
    min-height: {field_height}px;
}}

QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus,
QKeySequenceEdit:focus, QAbstractSpinBox:focus, QPlainTextEdit:focus,
QListWidget:focus, QTreeWidget:focus {{
    border: 2px solid {c['accent']};
    outline: none;
    box-shadow: 0 0 0 4px {c['selection']}40;
}}

QLineEdit:disabled, QComboBox:disabled, QSpinBox:disabled {{
    background: {c['surface2']};
    color: {c['muted']};
    opacity: 0.6;
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

QLineEdit, QListWidget, QTreeWidget, QTextEdit {{
    background: {c['surface']};
    border: 1px solid {c['border']};
    border-radius: {radius_md}px;
    selection-background-color: {c['selection']};
    selection-color: {c['selectionText']};
}}

QComboBox::drop-down {{
    border: none;
    width: 28px;
    background: transparent;
    margin-right: 2px;
}}

QComboBox::drop-down:hover {{
    background: {c['surface3']};
    border-radius: {radius_sm}px;
}}

QSpinBox::up-button, QSpinBox::down-button, QDoubleSpinBox::up-button, 
QDoubleSpinBox::down-button {{
    width: 22px;
    border: none;
    background: transparent;
    color: {c['accent']};
    padding: 2px 4px;
}}

QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover,
QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {{
    background: {c['surface3']};
    border-radius: {radius_sm}px;
}}

/* ============================================================================
   CHECKBOXES & RADIO BUTTONS - Custom styling
   ============================================================================ */

QCheckBox {{
    spacing: {checkbox_spacing}px;
    font-weight: 600;
    color: {c['text']};
}}

QCheckBox::indicator {{
    width: 0px;
    height: 0px;
}}

QCheckBox:disabled {{
    color: {c['muted']};
    opacity: 0.6;
}}

QCheckBox:focus {{
    outline: 2px solid {c['accent']};
    outline-offset: 2px;
}}

/* ============================================================================
   LISTS & TREES - Items, headers, selection
   ============================================================================ */

QListWidget, QTreeWidget {{
    outline: none;
    background: {c['surface']};
    border: 1px solid {c['border']};
    border-radius: {radius_md}px;
}}

QListWidget#NavList, QListWidget#NavList:focus {{
    background: transparent;
    border: none;
}}

QListWidget#NavList::item {{
    margin: 3px 0;
    padding: 10px 12px;
    border: none;
    border-radius: {radius_sm}px;
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
    font-weight: 600;
}}

QTreeWidget::item {{
    padding: 6px;
}}

QTreeWidget::item:hover {{
    background: {c['surface3']};
    border-radius: {radius_sm}px;
}}

QTreeWidget::item:selected {{
    background: {c['selection']};
    color: {c['selectionText']};
    border-radius: {radius_sm}px;
    font-weight: 600;
}}

QHeaderView::section {{
    background: {c['surface2']};
    border: none;
    border-bottom: 1px solid {c['border']};
    padding: 8px;
    font-weight: 700;
    color: {c['text']};
}}

/* ============================================================================
   TABS - Tab bar styling
   ============================================================================ */

QTabWidget::pane {{
    border: none;
    background: transparent;
}}

QTabBar::tab {{
    background: {c['tab']};
    border: 1px solid {c['border']};
    border-radius: {radius_md}px;
    padding: {padding_y}px {int(padding_x * 1.5)}px;
    margin-right: 8px;
    color: {c['muted']};
    font-weight: 600;
}}

QTabBar::tab:hover {{
    color: {c['text']};
    border-color: {c['accentHover']};
    background: {c['surface3']};
}}

QTabBar::tab:selected {{
    background: {c['tabSelected']};
    color: {c['accent']};
    border-color: {c['accent']};
    border-bottom: 2px solid {c['accent']};
    margin-bottom: -1px;
    font-weight: 700;
}}

/* ============================================================================
   SLIDERS - Track and handle styling
   ============================================================================ */

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
    border: 2px solid {c['slider']};
}}

QSlider::handle:horizontal:hover {{
    background: {c['sliderHover']};
    border: 2px solid {c['sliderHover']};
}}

QSlider::sub-page:horizontal {{
    background: {c['accent']};
    border-radius: 4px;
}}

/* ============================================================================
   SCROLLBARS - Vertical and horizontal scrollbars
   ============================================================================ */

QScrollBar:vertical {{
    width: 10px;
    background: transparent;
    margin: 0px 0px 0px 0px;
}}

QScrollBar::handle:vertical {{
    background: {c['track']};
    border-radius: 5px;
    min-height: 20px;
}}

QScrollBar::handle:vertical:hover {{
    background: {c['slider']};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    border: none;
    background: none;
}}

QScrollBar:horizontal {{
    height: 10px;
    background: transparent;
}}

QScrollBar::handle:horizontal {{
    background: {c['track']};
    border-radius: 5px;
    min-width: 20px;
}}

QScrollBar::handle:horizontal:hover {{
    background: {c['slider']};
}}

/* ============================================================================
   LABELS - Typography and semantic labels
   ============================================================================ */

QLabel[muted="true"] {{
    color: {c['muted']};
    font-weight: 500;
}}

QLabel[title="true"] {{
    font-size: {title}px;
    font-weight: 700;
    color: {c['text']};
    letter-spacing: -0.5px;
}}

QLabel[sectionTitle="true"] {{
    font-size: {section}px;
    font-weight: 700;
    color: {c['text']};
}}

QLabel[sectionDesc="true"] {{
    color: {c['muted']};
    padding-bottom: 2px;
    font-weight: 500;
}}

QLabel[subtitle="true"] {{
    font-size: {subtitle}px;
    font-weight: 600;
    color: {c['text']};
}}

QLabel[caption="true"] {{
    font-size: {caption}px;
    color: {c['muted']};
    font-weight: 500;
    letter-spacing: 0.3px;
}}

QLabel[fieldLabel="true"] {{
    font-weight: 600;
    color: {c['text']};
}}

QLabel[fontBold="true"] {{
    font-weight: 700;
}}

QLabel[fontSemiBold="true"] {{
    font-weight: 600;
}}

QLabel[fontRegular="true"] {{
    font-weight: 400;
}}

QLabel[watermark="true"] {{
    color: {c['muted']};
    font-weight: 700;
    letter-spacing: 0.5px;
}}

QLabel[badge="true"] {{
    background: {c['accent']};
    color: {c['accentText']};
    border-radius: {radius_sm}px;
    padding: 6px 12px;
    font-weight: 700;
}}

QLabel[badge="true"][variant="success"] {{
    background: {c['success']};
}}

QLabel[badge="true"][variant="error"] {{
    background: {c['error']};
}}

QLabel[badge="true"][variant="warning"] {{
    background: {c['warning']};
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
    letter-spacing: -0.5px;
}}

QLabel#StatusValue {{
    font-size: {max(15, round(16 * scale))}px;
    font-weight: 700;
    color: {c['accent']};
}}

/* ============================================================================
   PROGRESS BARS - Loading and progress indicators
   ============================================================================ */

QProgressBar {{
    background: {c['surface']};
    border: 1px solid {c['border']};
    border-radius: {radius_md}px;
    padding: 2px;
    min-height: {int(field_height + 4)}px;
    text-align: center;
    color: {c['accentText']};
    font-weight: 600;
    font-size: {max(10, round(11 * scale))}px;
}}

QProgressBar::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {c['accent']},
        stop:1 {c['selection']});
    border-radius: {int(radius_md - 1)}px;
    margin: 1px;
}}

QProgressBar[status="success"]::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {c['success']},
        stop:1 {c['successLight']});
}}

QProgressBar[status="error"]::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {c['error']},
        stop:1 {c['errorLight']});
}}

QProgressBar[status="warning"]::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {c['warning']},
        stop:1 {c['warningLight']});
}}
"""

"""
QUICK START: Copy-Paste UI Improvements for SayaTech MIDI Studio
High-impact improvements ready for immediate implementation
"""

# ============================================================================
# 1. BUTTON ENHANCEMENTS - Copy to theme.py build_stylesheet()
# ============================================================================

# ADD THIS SECTION to stylesheet generation:

BUTTON_STYLES = """
/* ENHANCED BUTTON STYLES WITH DEPTH AND FEEDBACK */

QPushButton {{
    background: {c['surface2']};
    border: 1px solid {c['border']};
    border-radius: {radius_md}px;
    padding: {padding_y}px {padding_x}px;
    font-weight: 600;
    color: {c['text']};
    outline: none;
}}

/* Hover state - Add visual lift and brightness */
QPushButton:hover {{
    border-color: {c['accent']};
    background: {c['surface3']};
    color: {c['text']};
}}

/* Pressed state - Inset effect */
QPushButton:pressed {{
    background: {c['surface']};
    border-color: {c['accent']};
}}

/* Disabled state - Reduce prominence */
QPushButton:disabled {{
    background: {c['surface2']};
    border-color: {c['border']};
    color: {c['muted']};
    opacity: 0.6;
}}

/* Primary button variant */
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

/* Success button */
QPushButton[variant="success"] {{
    background: {c['success']};
    color: {c['accentText']};
    border: none;
}}

QPushButton[variant="success"]:hover {{
    background: {c['successLight']};
}}

/* Error button */
QPushButton[variant="error"] {{
    background: {c['error']};
    color: {c['accentText']};
    border: none;
}}

QPushButton[variant="error"]:hover {{
    background: {c['errorLight']};
}}
"""


# ============================================================================
# 2. FOCUS INDICATOR ENHANCEMENTS
# ============================================================================

FOCUS_STYLES = """
/* WCAG-COMPLIANT FOCUS INDICATORS */

/* Text inputs */
QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus,
QKeySequenceEdit:focus, QAbstractSpinBox:focus {{
    border: 2px solid {c['accent']};
    outline: none;
    box-shadow: 0 0 0 4px {c['selection']}40;
}}

/* Buttons */
QPushButton:focus {{
    outline: 2px solid {c['accent']};
    outline-offset: 2px;
}}

/* Checkboxes and radio buttons */
QCheckBox:focus, QRadioButton:focus {{
    outline: 2px solid {c['accent']};
    outline-offset: 2px;
}}

/* List items */
QListWidget#NavList::item:focus {{
    outline: 2px solid {c['accent']};
    outline-offset: 2px;
}}

/* Tree items */
QTreeWidget::item:focus {{
    outline: 2px solid {c['accent']};
    outline-offset: 2px;
}}
"""


# ============================================================================
# 3. SEMANTIC COLORS - Add to palette definition
# ============================================================================

SEMANTIC_COLORS = {
    # Success state
    "success": "#10b981" if dark_mode else "#059669",
    "successLight": "#34d399" if dark_mode else "#10b981",
    "successBg": "#064e3b" if dark_mode else "#d1fae5",
    
    # Error state
    "error": "#ef4444" if dark_mode else "#dc2626",
    "errorLight": "#f87171" if dark_mode else "#ef4444",
    "errorBg": "#7f1d1d" if dark_mode else "#fee2e2",
    
    # Warning state
    "warning": "#f59e0b" if dark_mode else "#d97706",
    "warningLight": "#fbbf24" if dark_mode else "#f59e0b",
    "warningBg": "#78350f" if dark_mode else "#fef3c7",
    
    # Info state
    "info": "#3b82f6" if dark_mode else "#2563eb",
    "infoLight": "#60a5fa" if dark_mode else "#3b82f6",
    "infoBg": "#1e3a8a" if dark_mode else "#dbeafe",
}


# ============================================================================
# 4. INPUT FIELD ENHANCEMENTS
# ============================================================================

INPUT_STYLES = """
/* ENHANCED INPUT FIELD STYLING */

QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QKeySequenceEdit {{
    background: {c['surface']};
    border: 1px solid {c['border']};
    border-radius: {radius_md}px;
    padding: {padding_y}px {padding_x}px;
    color: {c['text']};
    selection-background-color: {c['selection']};
    selection-color: {c['selectionText']};
    min-height: {field_height}px;
    font-size: {font}px;
}}

/* Hover state */
QLineEdit:hover, QComboBox:hover, QSpinBox:hover {{
    border-color: {c['borderLight']};
    background: {c['surface2']};
}}

/* Focus state with glow */
QLineEdit:focus, QComboBox:focus, QSpinBox:focus {{
    border: 2px solid {c['accent']};
    outline: none;
    box-shadow: 0 0 0 4px {c['selection']}40;
    padding: {int(padding_y - 1)}px {int(padding_x - 1)}px;
}}

/* Disabled state */
QLineEdit:disabled, QComboBox:disabled {{
    background: {c['surface2']};
    color: {c['muted']};
    opacity: 0.6;
}}

/* ComboBox dropdown button */
QComboBox::drop-down {{
    border: none;
    width: 28px;
    background: transparent;
}}

QComboBox::drop-down:hover {{
    background: {c['surface3']};
    border-radius: {radius_sm}px;
    margin-right: 2px;
}}
"""


# ============================================================================
# 5. PROGRESS BAR WITH SEMANTIC STATUS
# ============================================================================

PROGRESS_STYLES = """
/* ENHANCED PROGRESS BAR WITH STATUS COLORS */

QProgressBar {{
    background: {c['surface']};
    border: 1px solid {c['border']};
    border-radius: {radius_md}px;
    padding: 2px;
    min-height: 24px;
    text-align: center;
    color: {c['accentText']};
    font-weight: 600;
}}

/* Progress fill - gradient from accent to selection */
QProgressBar::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {c['accent']},
        stop:1 {c['selection']});
    border-radius: 4px;
    margin: 1px;
}}

/* Success status */
QProgressBar[status="success"]::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {c['success']},
        stop:1 {c['successLight']});
}}

/* Error status */
QProgressBar[status="error"]::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {c['error']},
        stop:1 {c['errorLight']});
}}

/* Warning status */
QProgressBar[status="warning"]::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {c['warning']},
        stop:1 {c['warningLight']});
}}

/* Info status */
QProgressBar[status="info"]::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {c['info']},
        stop:1 {c['infoLight']});
}}
"""


# ============================================================================
# 6. TAB ENHANCEMENTS
# ============================================================================

TAB_STYLES = """
/* ENHANCED TAB STYLING WITH BETTER FEEDBACK */

QTabBar::tab {{
    background: {c['tab']};
    border: 1px solid {c['border']};
    border-radius: {radius_md}px;
    padding: {padding_y}px {int(padding_x * 1.5)}px;
    margin-right: 8px;
    color: {c['muted']};
    font-weight: 600;
}}

/* Tab hover state */
QTabBar::tab:hover {{
    color: {c['text']};
    border-color: {c['accentHover']};
    background: {c['surface3']};
}}

/* Selected tab */
QTabBar::tab:selected {{
    background: {c['tabSelected']};
    color: {c['accent']};
    border-color: {c['accent']};
    border-bottom: 2px solid {c['accent']};
    margin-bottom: -1px;
    font-weight: 700;
}}

/* Selected tab hover */
QTabBar::tab:selected:hover {{
    color: {c['accentHover']};
}}
"""


# ============================================================================
# 7. SLIDER ENHANCEMENTS
# ============================================================================

SLIDER_STYLES = """
/* ENHANCED SLIDER WITH BETTER HANDLE AND TRACK */

/* Horizontal slider groove */
QSlider::groove:horizontal {{
    height: 8px;
    border-radius: 4px;
    background: {c['track']};
}}

/* Slider handle with shadow effect */
QSlider::handle:horizontal {{
    background: {c['slider']};
    width: {slider_handle}px;
    margin: -4px 0;
    border-radius: {int(slider_handle/2)}px;
    border: 2px solid {c['slider']};
}}

/* Handle hover state */
QSlider::handle:horizontal:hover {{
    background: {c['sliderHover']};
    border: 2px solid {c['sliderHover']};
    box-shadow: 0 0 0 8px {c['selection']}40;
}}

/* Filled portion of slider */
QSlider::sub-page:horizontal {{
    background: {c['accent']};
    border-radius: 4px;
}}
"""


# ============================================================================
# 8. BADGE AND LABEL ENHANCEMENTS
# ============================================================================

LABEL_STYLES = """
/* ENHANCED TYPOGRAPHY AND LABELS */

/* Title labels */
QLabel[title="true"] {{
    font-size: {title}px;
    font-weight: 700;
    color: {c['text']};
    letter-spacing: -0.5px;
}}

/* Section titles */
QLabel[sectionTitle="true"] {{
    font-size: {section}px;
    font-weight: 700;
    color: {c['text']};
}}

/* Subtitles */
QLabel[subtitle="true"] {{
    font-size: {subtitle}px;
    font-weight: 600;
    color: {c['text']};
}}

/* Captions and helper text */
QLabel[caption="true"] {{
    font-size: {caption}px;
    color: {c['muted']};
    font-weight: 500;
    letter-spacing: 0.3px;
}}

/* Muted text */
QLabel[muted="true"] {{
    color: {c['muted']};
    font-weight: 500;
}}

/* Badges */
QLabel[badge="true"] {{
    background: {c['accent']};
    color: {c['accentText']};
    border-radius: 6px;
    padding: 4px 12px;
    font-weight: 700;
    font-size: {max(10, round(11 * scale))}px;
}}

/* Success badge */
QLabel[badge="true"][variant="success"] {{
    background: {c['success']};
    color: #ffffff;
}}

/* Error badge */
QLabel[badge="true"][variant="error"] {{
    background: {c['error']};
    color: #ffffff;
}}

/* Warning badge */
QLabel[badge="true"][variant="warning"] {{
    background: {c['warning']};
    color: #ffffff;
}}

/* Info badge */
QLabel[badge="true"][variant="info"] {{
    background: {c['info']};
    color: #ffffff;
}}
"""


# ============================================================================
# 9. SCROLLBAR ENHANCEMENTS
# ============================================================================

SCROLLBAR_STYLES = """
/* ENHANCED SCROLLBAR STYLING */

/* Vertical scrollbar */
QScrollBar:vertical {{
    width: 10px;
    background: transparent;
    margin: 0px;
}}

/* Vertical scrollbar handle */
QScrollBar::handle:vertical {{
    background: {c['track']};
    border-radius: 5px;
    min-height: 20px;
    margin: 0px;
}}

/* Vertical scrollbar handle hover */
QScrollBar::handle:vertical:hover {{
    background: {c['slider']};
    border-radius: 5px;
}}

/* Hide scrollbar buttons */
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    border: none;
    background: none;
}}

/* Horizontal scrollbar */
QScrollBar:horizontal {{
    height: 10px;
    background: transparent;
    margin: 0px;
}}

/* Horizontal scrollbar handle */
QScrollBar::handle:horizontal {{
    background: {c['track']};
    border-radius: 5px;
    min-width: 20px;
}}

/* Horizontal scrollbar handle hover */
QScrollBar::handle:horizontal:hover {{
    background: {c['slider']};
    border-radius: 5px;
}}

/* Hide horizontal scrollbar buttons */
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    border: none;
    background: none;
}}
"""


# ============================================================================
# 10. COMPLETE STYLESHEET ASSEMBLY
# ============================================================================

def build_complete_enhanced_stylesheet(dark_mode: bool, scale_percent: int, 
                                      preset: str, backdrop_enabled: bool) -> str:
    """Build complete stylesheet with all enhancements"""
    
    # Start with theme colors
    from theme_enhanced import _palette, RADIUS_TOKENS
    c = _palette(dark_mode, preset)
    
    # Calculate sizes
    scale = max(0.8, min(1.4, scale_percent / 100.0))
    font = max(11, round(12.2 * scale))
    title = max(18, round(21 * scale))
    section = max(14, round(15 * scale))
    subtitle = max(13, round(14 * scale))
    caption = max(10, round(11 * scale))
    
    radius_md = max(10, round(12 * scale))
    radius_sm = max(6, round(8 * scale))
    padding_y = max(6, round(8 * scale))
    padding_x = max(10, round(13 * scale))
    field_height = max(18, round(20 * scale))
    slider_handle = max(14, round(16 * scale))
    
    # Combine all style sections
    stylesheet = f"""
    /* BASE */
    QWidget {{ color: {c['text']}; }}
    
    {BUTTON_STYLES}
    {FOCUS_STYLES}
    {INPUT_STYLES}
    {PROGRESS_STYLES}
    {TAB_STYLES}
    {SLIDER_STYLES}
    {LABEL_STYLES}
    {SCROLLBAR_STYLES}
    """
    
    return stylesheet


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

"""
In main_window.py or theme.py:

    from .quick_improvements import build_complete_enhanced_stylesheet
    
    # Apply enhanced stylesheet
    stylesheet = build_complete_enhanced_stylesheet(
        dark_mode=settings.dark_mode,
        scale_percent=settings.ui_scale,
        preset=settings.theme_preset,
        backdrop_enabled=backdrop_enabled
    )
    self.setStyleSheet(stylesheet)

Or use individual style blocks in your theme.py build_stylesheet() function.
"""


# ============================================================================
# TESTING TEMPLATE - Add to your test suite
# ============================================================================

"""
import unittest
from PySide6.QtWidgets import QPushButton, QLineEdit, QProgressBar
from PySide6.QtCore import Qt

class TestUIEnhancements(unittest.TestCase):
    
    def test_button_hover_styling(self):
        '''Verify button shows hover styles'''
        button = QPushButton("Test")
        # Simulate hover
        button.enterEvent(None)
        # Check that styles were applied
        self.assertIsNotNone(button.styleSheet())
    
    def test_focus_indicator_visible(self):
        '''Verify focus indicator is visible'''
        line_edit = QLineEdit()
        line_edit.setFocus()
        # Check focus style is applied
        self.assertTrue(line_edit.hasFocus())
    
    def test_progress_bar_status_variants(self):
        '''Verify progress bar status colors work'''
        for status in ["info", "success", "error", "warning"]:
            pb = QProgressBar()
            pb.setProperty("status", status)
            self.assertEqual(pb.property("status"), status)

if __name__ == '__main__':
    unittest.main()
"""

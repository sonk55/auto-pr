from PyQt5.QtWidgets import QPushButton
from styles.dark_theme import COLORS

class PrimaryButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedHeight(32)  # GitHub Desktop 스타일 높이
        self.setStyleSheet(f'''
            QPushButton {{
                background-color: {COLORS['button_primary']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 0 16px;
                font-size: 14px;
                font-weight: 500;
                min-width: 120px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['button_hover']};
            }}
            QPushButton:pressed {{
                background-color: {COLORS['button_primary']};
            }}
        ''')

class SecondaryButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedHeight(32)
        self.setStyleSheet(f'''
            QPushButton {{
                background-color: transparent;
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                padding: 0 16px;
                font-size: 14px;
                font-weight: 500;
                min-width: 120px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['bg_hover']};
                border-color: {COLORS['border_hover']};
            }}
            QPushButton:pressed {{
                background-color: {COLORS['bg_secondary']};
            }}
        ''')
        
class TableInlineButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedHeight(32)
        self.setStyleSheet(f'''
            QPushButton {{
                background-color: transparent;
                color: {COLORS['button_primary']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                padding: 0 0x;
                font-size: 14px;
                min-width: 80px;
                min-height: 24px;
                margin: 0px;
            }}
            QPushButton:hover {{
                color: {COLORS['text_secondary']};
            }}
            QPushButton:pressed {{
                color: {COLORS['text_primary']};
            }}
        ''')
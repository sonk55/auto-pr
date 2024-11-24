from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from styles.dark_theme import COLORS

class TitleLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(f'''
            QLabel {{
                color: {COLORS['text_primary']};
                font-size: 48px;
                font-weight: 300;
                margin: 20px;
            }}
        ''')

class TitleLabelH3(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(f'''
            QLabel {{
                color: {COLORS['text_primary']};
                font-size: 24px;
                font-weight: 400;
                margin: 16px;
            }}
        ''')

class DescriptionLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(f'''
            QLabel {{
                color: {COLORS['text_secondary']};
                font-size: 14px;
                margin: 8px;
            }}
        ''')



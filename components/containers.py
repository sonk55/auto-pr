
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from styles.dark_theme import COLORS

class CardContainer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(40, 40, 40, 40)
        self.layout.setSpacing(20)
        self.setStyleSheet(f'''
            CardContainer {{
                background-color: {COLORS['bg_secondary']};
                border: 1px solid {COLORS['border']};
                border-radius: 12px;
                min-width: 400px;
                max-width: 600px;
            }}
        ''')
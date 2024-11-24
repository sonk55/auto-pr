from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from styles.dark_theme import COLORS

class HeaderWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 10, 20, 10)
        
        # Icon
        icon_label = QLabel()
        icon_pixmap = QPixmap('resources/icons/auto_pr.png')
        scaled_pixmap = icon_pixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon_label.setPixmap(scaled_pixmap)
        icon_label.setStyleSheet('''
            background-color: transparent;
        ''')
        
        # Title
        title_label = QLabel('Auto PR')
        title_label.setStyleSheet(f'''
            background-color: transparent;
            color: {COLORS['text_primary']};
            font-size: 18px;
            font-weight: 600;
            margin-left: 8px;
        ''')
        
        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addStretch()
        
        self.setStyleSheet(f'''
            QWidget {{
                background-color: {COLORS['bg_secondary']};
            }}
        ''')
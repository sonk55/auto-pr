
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QGroupBox
from PyQt5.QtCore import Qt

class BasePlugin(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title = "Base Plugin"
        self._init_base_ui()

    def _init_base_ui(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)
        self.setLayout(self.main_layout)

    def create_group(self, title):
        group = QGroupBox(title)
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #555;
                border-radius: 6px;
                margin-top: 6px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
        """)
        return group

    def create_save_button(self):
        save_btn = QPushButton("Save Configuration")
        save_btn.setFixedWidth(200)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #555;
                padding: 8px 15px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #404040;
            }
            QPushButton:pressed {
                background-color: #505050;
            }
        """)
        return save_btn
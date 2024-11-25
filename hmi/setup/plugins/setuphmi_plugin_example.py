
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class Plugin(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title = "Example"
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("This is an example plugin"))
        self.setLayout(layout)
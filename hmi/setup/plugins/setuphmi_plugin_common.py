from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, 
                           QLineEdit, QPushButton, QGroupBox, QTextEdit)

class Plugin(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title = "Common"
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        
        # Common Settings
        common_group = QGroupBox("Common Settings")
        form = QFormLayout()
        
        self.project_path = QLineEdit()
        self.config_path = QLineEdit()
        self.temp_path = QLineEdit()
        
        form.addRow("Project Path:", self.project_path)
        form.addRow("Config Path:", self.config_path)
        form.addRow("Temp Path:", self.temp_path)
        common_group.setLayout(form)
        
        # Additional Notes
        notes_group = QGroupBox("Additional Notes")
        notes_layout = QVBoxLayout()
        self.notes = QTextEdit()
        notes_layout.addWidget(self.notes)
        notes_group.setLayout(notes_layout)
        
        layout.addWidget(common_group)
        layout.addWidget(notes_group)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def save_settings(self):
        # TODO: Implement settings save
        pass
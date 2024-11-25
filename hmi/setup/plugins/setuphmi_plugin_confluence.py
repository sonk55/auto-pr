from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, 
                            QFormLayout, QPushButton, QGroupBox)

class Plugin(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title = "Confluence"
        
        layout = QVBoxLayout()
        
        # Create settings form
        settings_group = QGroupBox("Confluence Configuration")
        form_layout = QFormLayout()
        
        self.server_url = QLineEdit()
        self.username = QLineEdit()
        self.api_token = QLineEdit()
        self.api_token.setEchoMode(QLineEdit.Password)
        self.space_key = QLineEdit()
        
        form_layout.addRow("Server URL:", self.server_url)
        form_layout.addRow("Username:", self.username)
        form_layout.addRow("API Token:", self.api_token)
        form_layout.addRow("Space Key:", self.space_key)
        
        settings_group.setLayout(form_layout)
        
        # Add save button
        save_button = QPushButton("Save Settings")
        save_button.clicked.connect(self.save_settings)
        
        layout.addWidget(settings_group)
        layout.addWidget(save_button)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def save_settings(self):
        # TODO: Implement settings save logic
        pass

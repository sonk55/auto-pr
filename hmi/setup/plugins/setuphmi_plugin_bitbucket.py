from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, 
                            QFormLayout, QPushButton, QGroupBox)

class Plugin(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title = "Bitbucket"
        
        layout = QVBoxLayout()
        
        # Create settings form
        settings_group = QGroupBox("Bitbucket Configuration")
        form_layout = QFormLayout()
        
        self.server_url = QLineEdit()
        self.api_token = QLineEdit()
        self.api_token.setEchoMode(QLineEdit.Password)
        
        form_layout.addRow("Server URL:", self.server_url)
        form_layout.addRow("API Token:", self.api_token)
        
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

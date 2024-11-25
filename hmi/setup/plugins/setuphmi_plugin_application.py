from PyQt5.QtWidgets import QFormLayout, QLineEdit, QComboBox
from PyQt5.QtCore import Qt
from .setuphmi_plugin_base import BasePlugin

class Plugin(BasePlugin):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title = "Application"
        self._init_ui()

    def _init_ui(self):
        # Application Settings
        app_group = self.create_group("Application Settings")
        form = QFormLayout()
        form.setSpacing(10)
        
        self.app_name = QLineEdit()
        self.app_version = QLineEdit()
        self.app_type = QComboBox()
        self.app_type.addItems(["EXE", "DLL", "Service"])
        
        form.addRow("Application Name:", self.app_name)
        form.addRow("Version:", self.app_version)
        form.addRow("Type:", self.app_type)
        app_group.setLayout(form)
        
        # Debug Settings
        debug_group = self.create_group("Debug Settings")
        debug_form = QFormLayout()
        debug_form.setSpacing(10)
        
        self.debug_port = QLineEdit()
        self.debug_level = QComboBox()
        self.debug_level.addItems(["INFO", "DEBUG", "WARNING", "ERROR"])
        
        debug_form.addRow("Debug Port:", self.debug_port)
        debug_form.addRow("Log Level:", self.debug_level)
        debug_group.setLayout(debug_form)
        
        save_btn = self.create_save_button()
        save_btn.clicked.connect(self.save_settings)
        
        self.main_layout.addWidget(app_group)
        self.main_layout.addWidget(debug_group)
        self.main_layout.addWidget(save_btn, 0, Qt.AlignCenter)
        self.main_layout.addStretch()

    def save_settings(self):
        # TODO: Implement settings save
        pass
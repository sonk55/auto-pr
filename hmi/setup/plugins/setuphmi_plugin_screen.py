
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QSpinBox,
                           QComboBox, QPushButton, QGroupBox, QCheckBox)

class Plugin(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title = "Screen"
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        
        # Display Settings
        display_group = QGroupBox("Display Settings")
        form = QFormLayout()
        
        self.resolution = QComboBox()
        self.resolution.addItems(["1920x1080", "1280x720", "800x600"])
        
        self.color_depth = QComboBox()
        self.color_depth.addItems(["32-bit", "24-bit", "16-bit"])
        
        self.refresh_rate = QSpinBox()
        self.refresh_rate.setRange(30, 144)
        self.refresh_rate.setValue(60)
        
        form.addRow("Resolution:", self.resolution)
        form.addRow("Color Depth:", self.color_depth)
        form.addRow("Refresh Rate:", self.refresh_rate)
        display_group.setLayout(form)
        
        # Additional Settings
        feature_group = QGroupBox("Features")
        feature_layout = QVBoxLayout()
        
        self.vsync = QCheckBox("Enable V-Sync")
        self.fullscreen = QCheckBox("Start in Fullscreen")
        self.hardware_accel = QCheckBox("Hardware Acceleration")
        
        feature_layout.addWidget(self.vsync)
        feature_layout.addWidget(self.fullscreen)
        feature_layout.addWidget(self.hardware_accel)
        feature_group.setLayout(feature_layout)
        
        save_btn = QPushButton("Save Configuration")
        save_btn.clicked.connect(self.save_settings)
        
        layout.addWidget(display_group)
        layout.addWidget(feature_group)
        layout.addWidget(save_btn)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def save_settings(self):
        # TODO: Implement settings save
        pass
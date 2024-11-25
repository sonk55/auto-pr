import os
import importlib
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QStackedWidget, QScrollArea)
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QFont

class SetupHMI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title = 'Setup'
        # Make window frameless
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # Initialize variables for window dragging
        self._drag_pos = None
        # Set default window size
        self.resize(650, 600)  # 윈도우 크기를 1200x800으로 설정
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Add custom title bar
        title_bar = QWidget()
        title_bar.setObjectName("titleBar")
        title_bar.setFixedHeight(40)
        title_bar.setStyleSheet("""
            QWidget#titleBar {
                background-color: #2d2d2d;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-bottom: none;
            }
        """)

        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(10, 0, 10, 0)

        # Title label
        title_label = QLabel(self.title)
        title_label.setStyleSheet("color: white; font-size: 14px;")
        title_label.setFont(QFont("Segoe UI", 10))

        # Close button
        close_btn = QPushButton("×")
        close_btn.setFixedSize(30, 30)
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet("""
            QPushButton {
                color: white;
                border: none;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c42b1c;
                border-radius: 15px;
            }
        """)

        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(close_btn)

        # Main content area with buttons
        outer_content = QVBoxLayout()
        outer_content.setContentsMargins(0, 0, 0, 0)
        outer_content.setSpacing(0)

        # Main content widget (existing content)
        content_widget = QWidget()
        content_widget.setObjectName("contentWidget")
        content_widget.setStyleSheet("""
            QWidget#contentWidget {
                background-color: #1e1e1e;
                border-bottom-left-radius: 10px;
                border-bottom-right-radius: 10px;
                border: 1px solid rgba(255, 255, 255, 0.2);  /* 테두리 투명도 증가 */
                border-top: none;
            }
        """)
        
        # Content layout with button list and stacked widget
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Button list container
        button_container = QWidget()
        button_container.setFixedWidth(150)
        button_container.setStyleSheet("""
            QWidget {
                background-color: #252525;
                border-right: 1px solid rgba(255, 255, 255, 0.2);  /* 테두리 투명도 증가 */
            }
            QPushButton {
                text-align: left;
                padding: 12px 15px;  /* 상하 패딩 증가 */
                margin: 3px 5px;     /* 버튼 주변 여백 추가 */
                border: none;
                border-radius: 4px;   /* 모서리 둥글게 */
                color: white;
                background: transparent;
            }
            /* Remove font-weight from CSS */
            QPushButton:hover {
                background-color: #353535;
            }
            QPushButton:checked {
                background-color: #404040;
                border-left: 3px solid #007acc;
            }
        """)
        
        # Button layout
        self.button_layout = QVBoxLayout(button_container)
        self.button_layout.setContentsMargins(5, 10, 5, 10)  # 여백 추가
        self.button_layout.setSpacing(5)  # 버튼 간격 증가
        
        # Stacked widget for content
        self.stack_widget = QStackedWidget()
        self.stack_widget.setStyleSheet("""
            QStackedWidget {
                background: transparent;
            }
        """)

        content_layout.addWidget(button_container)
        content_layout.addWidget(self.stack_widget)

        # Button container for Save/Cancel
        button_container = QWidget()
        button_container.setFixedHeight(50)
        button_container.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                border-top: 1px solid rgba(255, 255, 255, 0.2);  /* 테두리 투명도 증가 */
            }
            QPushButton {
                min-width: 80px;
                padding: 6px 16px;
                border-radius: 4px;
                color: white;
                background: #2d2d2d;
                font-weight: demiBold;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            QPushButton:hover {
                background: #353535;
            }
            QPushButton:pressed {
                background: #404040;
            }
            #saveButton {
                background: #0E639C;
            }
            #saveButton:hover {
                background: #1177BB;
            }
        """)

        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(10, 0, 10, 0)
        button_layout.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.close)

        save_btn = QPushButton("Save")
        save_btn.setObjectName("saveButton")
        save_btn.clicked.connect(self.save_all_settings)

        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)

        outer_content.addWidget(content_widget)
        outer_content.addWidget(button_container)

        # Add all to main layout
        main_layout.addWidget(title_bar)
        main_layout.addLayout(outer_content)
        
        self.setLayout(main_layout)
        
        # Load plugins
        self.load_plugins()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.pos().y() <= 40:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self._drag_pos is not None:
            self.move(event.globalPos() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._drag_pos = None

    def load_plugins(self):
        plugins_path = os.path.join(os.path.dirname(__file__), 'plugins')
        for filename in os.listdir(plugins_path):
            if (filename.endswith('.py') and 
                filename.startswith('setuphmi_plugin_') and 
                not filename.startswith('setuphmi_plugin_base')):
                try:
                    module_name = f"hmi.setup.plugins.{filename[:-3]}"
                    module = importlib.import_module(module_name)
                    plugin_class = getattr(module, 'Plugin')
                    plugin_instance = plugin_class(self)
                    
                    # Create button for plugin with custom font
                    button = QPushButton(plugin_instance.title)
                    button.setCheckable(True)
                    
                    # Set font with specific weight
                    font = button.font()
                    font.setWeight(QFont.DemiBold)  # or use specific number like 57
                    button.setFont(font)
                    
                    button.clicked.connect(lambda checked, w=plugin_instance, b=button:
                                        self.show_plugin(w, b))
                    
                    # Add button and widget to their containers
                    self.button_layout.addWidget(button)
                    self.stack_widget.addWidget(plugin_instance)
                    
                    # Select first plugin by default
                    if self.stack_widget.count() == 1:
                        button.setChecked(True)
                        self.stack_widget.setCurrentWidget(plugin_instance)
                        
                except Exception as e:
                    print(f"Error loading plugin {filename}: {str(e)}")
        
        # Add stretch at the end of button layout
        self.button_layout.addStretch()

    def show_plugin(self, widget, button):
        # Uncheck all buttons except the clicked one
        for i in range(self.button_layout.count()):
            item = self.button_layout.itemAt(i)
            if item and item.widget() and isinstance(item.widget(), QPushButton):
                if item.widget() != button:
                    item.widget().setChecked(False)
        
        # Show selected plugin
        self.stack_widget.setCurrentWidget(widget)

    def save_all_settings(self):
        # Save settings for all plugins
        for i in range(self.stack_widget.count()):
            plugin = self.stack_widget.widget(i)
            if hasattr(plugin, 'save_settings'):
                try:
                    plugin.save_settings()
                except Exception as e:
                    print(f"Error saving settings for plugin {plugin.title}: {str(e)}")
        self.close()

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = SetupHMI()
    window.show()
    sys.exit(app.exec_())
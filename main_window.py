import os
import ctypes
from PyQt5.QtWidgets import (QMainWindow, QStackedWidget, QMenuBar, QMenu, 
                           QAction, QMessageBox, QDialog, QWidget, QHBoxLayout, QLabel)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize
from pages.start_page import StartPage
from pages.branch_selection_page import BranchSelectionPage
from pages.branch_info_page import BranchInfoPage
from pages.settings_page import SettingsDialog  # 상단에 import 추가
from styles.window_settings import WINDOW_SIZES, get_center_position
from styles.dark_theme import COMMON_STYLE, COLORS

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('AutoPR Desktop')
        width, height = WINDOW_SIZES['MAIN']
        x, y = get_center_position(width, height)
        self.setGeometry(x, y, width, height)

        # Windows AppUserModelID 설정 (반드시 아이콘 설정 전에 해야 함)
        if os.name == 'nt':
            myappid = 'mobis.autopr.desktop.1.0'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        
        # 아이콘 설정
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                               'resources', 'icons', 'auto_pr.svg')
        try:
            if os.path.exists(icon_path):
                icon = QIcon(icon_path)
                # 여러 크기의 아이콘 추가
                sizes = [16, 32, 48, 64, 128, 256]
                taskbar_icon = QIcon()
                for size in sizes:
                    pixmap = icon.pixmap(QSize(size, size))
                    if not pixmap.isNull():
                        taskbar_icon.addPixmap(pixmap)
                self.setWindowIcon(taskbar_icon)
                print(f"Icon loaded successfully from {icon_path}")
            else:
                print(f"Icon file not found at {icon_path}")
        except Exception as e:
            print(f"Error loading icon: {str(e)}")
        self.setStyleSheet(COMMON_STYLE)
        
        # 메뉴바 설정
        self.setup_menubar()
        
        # 스택 위젯 설정
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        
        # 페이지 추가
        self.start_page = StartPage(self)
        self.branch_page = BranchSelectionPage(self)
        self.view_page = BranchInfoPage(self)
        
        self.stack.addWidget(self.start_page)
        self.stack.addWidget(self.branch_page)
        self.stack.addWidget(self.view_page)
        
    def setup_menubar(self):
        # 헤더 컨테이너 생성
        header_container = QWidget()
        header_layout = QHBoxLayout(header_container)
        header_layout.setContentsMargins(10, 0, 0, 0)  # 오른쪽 여백 제거
        header_layout.setSpacing(10)

        # 앱 아이콘
        icon_label = QLabel()
        icon_pixmap = QPixmap('resources/icons/auto_pr.png')
        scaled_pixmap = icon_pixmap.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon_label.setPixmap(scaled_pixmap)
        icon_label.setStyleSheet('background-color: transparent;')

        # 앱 제목
        title_label = QLabel('Auto PR')
        title_label.setStyleSheet(f'''
            background-color: transparent;
            color: {COLORS['text_primary']};
            font-size: 14px;
            font-weight: 600;
        ''')

        # 메뉴바
        menubar = self.menuBar()
        menubar.setStyleSheet(f'''
            QMenuBar {{
                background-color: {COLORS['bg_secondary']};
                color: {COLORS['text_primary']};
                border: none;
                padding: 2px 0px;
            }}
            QMenuBar::item {{
                background-color: transparent;
                padding: 8px 12px;
                margin: 0px 2px;
                border-radius: 4px;
            }}
            QMenuBar::item:selected {{
                background-color: {COLORS['bg_hover']};
            }}
            QMenu {{
                background-color: {COLORS['bg_secondary']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']};
                padding: 4px;
            }}
            QMenu::item {{
                padding: 6px 28px;
                border-radius: 4px;
            }}
            QMenu::item:selected {{
                background-color: {COLORS['bg_hover']};
            }}
        ''')

        # 레이아웃에 위젯 추가 (순서 변경)
        header_layout.addWidget(icon_label)
        header_layout.addWidget(title_label, 0)  # stretch factor 0
        header_layout.addWidget(menubar, 1)  # stretch factor 1로 설정하여 늘어나게 함

        # 컨테이너를 메인윈도우의 메뉴바로 설정
        self.setMenuWidget(header_container)

        # 메뉴 항목 추가
        file_menu = menubar.addMenu('File')
        
        # Settings 액션
        settings_action = QAction('Settings', self)
        settings_action.setShortcut('Ctrl+,')
        settings_action.triggered.connect(self.show_settings)
        file_menu.addAction(settings_action)
        
        file_menu.addSeparator()
        
        # Exit 액션
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Alt+F4')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View 메뉴
        view_menu = menubar.addMenu('View')
        
        # Branch List 액션
        branch_list_action = QAction('Branch List', self)
        branch_list_action.setShortcut('Ctrl+B')
        branch_list_action.triggered.connect(self.show_view_page)
        view_menu.addAction(branch_list_action)
        
        # Help 메뉴
        help_menu = menubar.addMenu('Help')
        
        # About 액션
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def show_settings(self):
        dialog = SettingsDialog(self)
        dialog.exec_()
        # 설정이 변경되었다면 브랜치 리스트를 새로고침
        if dialog.result() == QDialog.Accepted:
            self.view_page.list_page.load_branch_info()
        
    def show_about(self):
        QMessageBox.about(self, 'About Auto-PR',
            'Auto-PR\n\n'
            'Version 1.0.0\n\n'
            'A tool for automating Pull Request creation\n'
            '© 2024 Hyundai Mobis Co., Ltd. All rights reserved.\n\n'
            'Developed by SSong.')
        
    def show_branch_selection(self):
        self.stack.setCurrentWidget(self.branch_page)
        
    def show_start_page(self):
        self.stack.setCurrentWidget(self.start_page)
        
    def show_view_page(self):
        self.stack.setCurrentWidget(self.view_page)
import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from styles.dark_theme import START_WINDOW_STYLE
from styles.window_settings import WINDOW_SIZES, get_center_position
from components.labels import TitleLabel, DescriptionLabel
from components.buttons import PrimaryButton
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                           QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt
from styles.dark_theme import COLORS, START_WINDOW_STYLE
from styles.window_settings import WINDOW_SIZES, get_center_position
from components.labels import TitleLabel, DescriptionLabel
from components.buttons import PrimaryButton
from components.containers import CardContainer
from components.header import HeaderWidget

class StartPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self):
        # 메인 레이아웃
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # # Header 추가
        # header = HeaderWidget(self)
        # main_layout.addWidget(header)
        
        # 카드 컨테이너
        card = CardContainer(self)
        
        # 카드 내부 컨텐츠
        title = TitleLabel('Auto-PR')
        title.setStyleSheet(f'''
            QLabel {{
                color: {COLORS['text_primary']};
                font-size: 72px;
                font-weight: 500;
                letter-spacing: -1px;
                margin-bottom: 20px;
            }}
        ''')
        card.layout.addWidget(title, alignment=Qt.AlignCenter)
        
        # 아이콘 추가
        icon_label = QLabel()
        icon_pixmap = QPixmap('resources/icons/auto_pr.png')  # Make sure to create this icon file
        scaled_pixmap = icon_pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon_label.setPixmap(scaled_pixmap)
        icon_label.setStyleSheet('''
            QLabel {
                margin-bottom: 20px;
            }
        ''')
        card.layout.addWidget(icon_label, alignment=Qt.AlignCenter)
        
        desc = DescriptionLabel('Pull Request 자동 생성 도구')
        desc.setStyleSheet(f'''
            QLabel {{
                color: {COLORS['text_secondary']};
                font-size: 18px;
                margin: 10px 0 30px 0;
            }}
        ''')
        card.layout.addWidget(desc, alignment=Qt.AlignCenter)
        
        # 버튼 컨테이너
        button_container = QHBoxLayout()
        button_container.setSpacing(12)  # 버튼 간격 축소
        
        # 조회하기 버튼
        view_button = PrimaryButton('조회하기')
        view_button.setFixedWidth(140)  # 버튼 폭 조정
        view_button.setFixedHeight(36)  # 버튼 높이 조정
        view_button.setStyleSheet(f'''
            QPushButton {{
                background-color: {COLORS['bg_secondary']};
                border: 1px solid {COLORS['button_primary']};
                color: {COLORS['button_primary']};
                border-radius: 6px;
                padding: 0 16px;
                font-size: 13px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: rgba(46, 164, 79, 0.1);
            }}
        ''')
        view_button.clicked.connect(self.parent().show_view_page)
        
        # 시작하기 버튼
        start_button = PrimaryButton('시작하기')
        start_button.setFixedWidth(140)  # 버튼 폭 조정
        start_button.setFixedHeight(36)  # 버튼 높이 조정
        start_button.setStyleSheet(f'''
            QPushButton {{
                background-color: {COLORS['button_primary']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 0 16px;
                font-size: 13px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {COLORS['button_hover']};
            }}
        ''')
        start_button.clicked.connect(self.parent().show_branch_selection)
        
        button_container.addStretch(1)  # 왼쪽 여백
        button_container.addWidget(view_button)
        button_container.addWidget(start_button)
        button_container.addStretch(1)  # 오른쪽 여백
        card.layout.addLayout(button_container)
        
        # 카드를 중앙에 배치하는 컨테이너
        center_container = QWidget()
        center_layout = QVBoxLayout(center_container)
        center_layout.addStretch(1)
        center_layout.addWidget(card, alignment=Qt.AlignCenter)
        center_layout.addStretch(1)
        
        main_layout.addWidget(center_container)
        
        # 배경색 설정
        self.setStyleSheet(f'''
            QWidget {{
                background-color: {COLORS['bg_primary']};
            }}
        ''')
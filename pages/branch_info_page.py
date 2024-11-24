from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QLineEdit, 
                           QTableWidget, QTableWidgetItem, QHeaderView, QPushButton)  # QPushButton 추가
from PyQt5.QtGui import QIcon  # QIcon 추가
from PyQt5.QtCore import Qt
from pages.branch_info_detail_page import BranchInfoDetailPage
from components.labels import TitleLabel, TitleLabelH3, DescriptionLabel
from components.buttons import PrimaryButton
from components.edit import SearchLineEdit
from config_manager import ConfigManager
from styles.dark_theme import COLORS  # COLORS import 추가
from components.header import HeaderWidget

class BranchInfoPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config_manager = ConfigManager()
        self.setup_ui()
        
    def setup_ui(self):
        # 메인 레이아웃
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # # Header 추가
        # header = HeaderWidget(self)
        # self.main_layout.addWidget(header)
        
        # 스택 위젯 생성
        self.stack = QStackedWidget()
        self.main_layout.addWidget(self.stack)
        
        # 리스트 페이지와 상세 페이지 생성
        self.list_page = BranchListPage(self)
        self.detail_page = BranchInfoDetailPage(self)
        
        # 스택에 페이지 추가
        self.stack.addWidget(self.list_page)
        self.stack.addWidget(self.detail_page)
        
    def show_detail(self, branch_name):
        self.detail_page.show_branch_info(branch_name)
        self.stack.setCurrentWidget(self.detail_page)
        
    def show_list(self):
        self.stack.setCurrentWidget(self.list_page)

class BranchListPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config_manager = ConfigManager()
        self.initUI()
        
    def initUI(self):
        # 전체 레이아웃
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 왼쪽 사이드바 (브랜치 리스트)
        sidebar = QWidget()
        sidebar.setObjectName("SidebarWidget")
        sidebar.setFixedWidth(350)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(16, 16, 16, 16)
        sidebar_layout.setSpacing(8)
        
        # 검색창
        self.search_input = SearchLineEdit('필터...', self)
        self.search_input.setFixedHeight(28)
        self.search_input.textChanged.connect(self.filter_branches)
        sidebar_layout.addWidget(self.search_input)
        
        # 브랜치 테이블
        self.table = QTableWidget()
        self.setup_table()
        sidebar_layout.addWidget(self.table)
        
        # 메인 컨텐츠 영역 (브랜치 상세 정보)
        content = QWidget()
        content.setObjectName("ContentWidget")
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setContentsMargins(24, 24, 24, 24)
        self.content_layout.setSpacing(16)
        
        # 뒤로가기 버튼 (상단으로 이동)
        back_button = PrimaryButton('뒤로가기', self)
        back_button.setFixedWidth(100)  # 버튼 너비 고정
        back_button.clicked.connect(self.parent().parent().show_start_page)
        self.content_layout.addWidget(back_button, 0, Qt.AlignLeft)
        
        # 기본 안내 메시지
        self.default_message = DescriptionLabel('브랜치를 선택하여 상세 정보를 확인하세요')
        self.content_layout.addWidget(self.default_message)
        
        # 브랜치 정보 컨테이너
        self.info_container = QVBoxLayout()
        self.info_container.setSpacing(12)
        self.content_layout.addLayout(self.info_container)
        
        self.content_layout.addStretch(1)
        
        # 레이아웃에 추가
        layout.addWidget(sidebar)
        layout.addWidget(content)
        
        self.load_branch_info()
        
    def setup_table(self):
        self.table.setColumnCount(1)  # 브랜치 이름만 표시
        self.table.setHorizontalHeaderLabels(['Branch Name'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.itemDoubleClicked.connect(self.on_branch_clicked)  # 더블클릭 이벤트 추가
        
        # 코너 버튼 설정
        corner_button = QPushButton()
        corner_button.setIcon(QIcon('resources/icons/auto_pr.png'))  # 아이콘 파일 경로 지정
        corner_button.setFixedSize(32, 32)  # 버튼 크기 설정
        self.table.setCornerWidget(corner_button)
        
        # 테이블 편집 비활성화
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        
        self.table.setStyleSheet(f'''
            QTableWidget {{
                background-color: {COLORS['bg_secondary']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                gridline-color: {COLORS['border']};
            }}
            QHeaderView {{
                background-color: {COLORS['bg_secondary']};
                border-bottom: 1px solid {COLORS['border']};
            }}
            QHeaderView::section {{
                background-color: {COLORS['bg_secondary']};
                color: {COLORS['text_secondary']};
                padding: 8px;
                border: none;
                border-bottom: 1px solid {COLORS['border']};
                font-weight: 600;
            }}
            QTableWidget QTableCornerButton::section {{
                background-color: {COLORS['bg_secondary']};
                border: none;
                border-bottom: 1px solid {COLORS['border']};
                margin: 0px;
                padding: 0px;
            }}
            QTableWidget::item {{
                padding: 8px;
                border: none;
            }}
            QTbleWidget::item:selected {{
                background-color: rgba(88, 166, 255, 0.1);
                color: {COLORS['link']};
            }}
        ''')
        
    def load_branch_info(self):
        branches = self.config_manager.load_branches()  # ConfigManager에서 브랜치 정보 로드
        
        self.table.setRowCount(len(branches))
        for i, branch in enumerate(branches):
            self.table.setItem(i, 0, QTableWidgetItem(branch.get('name', '')))
    
    def filter_branches(self, text):
        for row in range(self.table.rowCount()):
            matched = False
            for col in range(self.table.columnCount()):
                item = self.table.item(row, 0)
                if item and text.lower() in item.text().lower():
                    matched = True
                    break
            self.table.setRowHidden(row, not matched)
    
    def on_branch_clicked(self, item):
        # 브랜치 선택 시 오른쪽에 정보 표시
        branch_name = item.text()
        self.show_branch_details(branch_name)
    
    def show_branch_details(self, branch_name):
        # 기존 정보 제거
        self.default_message.hide()
        while self.info_container.count():
            item = self.info_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # 브랜치 정보 로드
        branches = self.config_manager.load_branches()
        branch_info = next((b for b in branches if b['name'] == branch_name), None)
        
        if branch_info:
            # 브랜치 이름
            title = TitleLabelH3(branch_name)
            self.info_container.addWidget(title)
            
            # 브랜치 정보 표시
            fields = [
                ('Last Commit', 'last_commit'),
                ('Author', 'author'),
                ('Date', 'date'),
            ]
            
            for label, key in fields:
                info = DescriptionLabel(f"{label}: {branch_info.get(key, '')}")
                info.setAlignment(Qt.AlignLeft)
                self.info_container.addWidget(info)

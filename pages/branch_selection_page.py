from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel, 
                           QListWidget, QLineEdit, QPushButton, QHBoxLayout,
                           QListWidgetItem, QLayout, QSizePolicy, QSpacerItem, QMessageBox)
from PyQt5.QtCore import Qt, QSize, QRect, QPoint
from PyQt5.QtGui import QIcon, QFont, QColor
from config_manager import ConfigManager
import sys
from styles.dark_theme import COMMON_STYLE, BRANCH_SELECTION_STYLE
from styles.window_settings import WINDOW_SIZES, get_center_position
from components.header import HeaderWidget
from components.labels import TitleLabel, TitleLabelH3, DescriptionLabel
from components.buttons import PrimaryButton, SecondaryButton  # Import 추가

class FlowLayout(QLayout):
    def __init__(self, parent=None, margin=0, spacing=-1):
        super().__init__(parent)
        self.itemList = []
        self.margin = margin
        self.spacing = spacing
        
    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)
            
    def addItem(self, item):
        self.itemList.append(item)
        
    def count(self):
        return len(self.itemList)
        
    def itemAt(self, index):
        if 0 <= index < len(self.itemList):
            return self.itemList[index]
        return None
        
    def takeAt(self, index):
        if 0 <= index < len(self.itemList):
            return self.itemList.pop(index)
        return None
        
    def expandingDirections(self):
        return Qt.Orientations(Qt.Orientation(0))
        
    def hasHeightForWidth(self):
        return True
        
    def heightForWidth(self, width):
        height = self.doLayout(QRect(0, 0, width, 0), True)
        return height
        
    def setGeometry(self, rect):
        super().setGeometry(rect)
        self.doLayout(rect, False)
        
    def sizeHint(self):
        return self.minimumSize()
        
    def minimumSize(self):
        size = QSize()
        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())
        size += QSize(2 * self.margin, 2 * self.margin)
        return size
        
    def doLayout(self, rect, testOnly):
        x = rect.x()
        y = rect.y()
        lineHeight = 0
        
        for item in self.itemList:
            nextX = x + item.sizeHint().width() + self.spacing
            if nextX - self.spacing > rect.right() and lineHeight > 0:
                x = rect.x()
                y = y + lineHeight + self.spacing
                nextX = x + item.sizeHint().width() + self.spacing
                lineHeight = 0
            
            if not testOnly:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))
            
            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())
        
        return y + lineHeight - rect.y()

class BranchSelectionPage(QWidget):  # QMainWindow 대신 QWidget 상속
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config_manager = ConfigManager()
        self.branch_list = []
        self.filtered_branches = []
        self.selected_branches = []  # 선택된 브랜치 저장 리스트 추가
        self.load_branches()
        self.initUI()
        self.setWindowIcon(QIcon('resources/icons/auto_pr.png'))
        
    def load_branches(self):
        self.branch_list = self.config_manager.get_branch_names()
        self.filtered_branches = self.branch_list.copy()
        
    def initUI(self):
        # 메인 레이아웃
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # # Header 추가
        # header = HeaderWidget(self)
        # main_layout.addWidget(header)
        
        # 컨텐츠 컨테이너
        content_container = QWidget()
        content_layout = QVBoxLayout(content_container)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # 타이틀
        title = TitleLabel('Select Branch')
        title.setStyleSheet('font-weight: bold;')
        title.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(title)
        
        # 검색창과 전체선택 버튼을 담을 컨테이너
        search_container = QWidget()
        search_layout = QHBoxLayout()
        search_layout.setContentsMargins(0, 0, 0, 0)
        
        # 검색창
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search branch...")
        self.search_input.textChanged.connect(self.filter_branches)
        
        # 전체선택 버튼
        self.select_all_button = QPushButton('Select All')
        self.select_all_button.setFixedWidth(100)
        self.select_all_button.setFixedHeight(40)
        self.select_all_button.clicked.connect(self.toggle_select_all)
        
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.select_all_button)
        search_container.setLayout(search_layout)
        content_layout.addWidget(search_container)
        
        # 선택된 브랜치 태그들을 보여줄 컨테이너
        self.tags_container = QWidget()
        self.tags_layout = FlowLayout(margin=10, spacing=5)
        self.tags_container.setLayout(self.tags_layout)
        self.tags_container.setMinimumHeight(50)  # 최소 높이만 설정
        
        palette = self.tags_container.palette()
        palette.setColor(self.tags_container.backgroundRole(), QColor("#1e1e1e"))
        palette.setColor(self.tags_container.foregroundRole(), QColor("#2c2c2c"))
        self.tags_container.setPalette(palette)
        self.tags_container.setAutoFillBackground(True)
        
        self.tags_container.setStyleSheet('''
                QWidget#tags_container {
                background-color: #1e1e1e;
                border-radius: 8px;
                padding: 0px 10px;
                border: 1px solid #2c2c2c;
            }
        ''')
        self.tags_container.setObjectName("tags_container")
        content_layout.addWidget(self.tags_container)

        # 브랜치 리스트
        self.branch_list_widget = QListWidget()
        self.update_branch_list()
        content_layout.addWidget(self.branch_list_widget)

        # 버튼 컨테이너 추가
        button_container = QHBoxLayout()
        button_container.setSpacing(12)
        
        # 뒤로가기 버튼
        back_button = SecondaryButton('뒤로가기')
        back_button.setFixedSize(100, 36)
        back_button.clicked.connect(self.parent().show_start_page)
        
        # 다음 버튼
        next_button = PrimaryButton('다음')
        next_button.setFixedSize(100, 36)
        next_button.clicked.connect(self.on_next_clicked)
        
        button_container.addWidget(back_button)
        button_container.addStretch()
        button_container.addWidget(next_button)
        
        content_layout.addLayout(button_container)
        
        # 컨텐츠 컨테이너를 메인 레이아웃에 추가
        main_layout.addWidget(content_container)
        
        self.setStyleSheet(BRANCH_SELECTION_STYLE)
        
    def toggle_select_all(self):
        # Update the Select All button text
        if self.select_all_button.text() == 'Select All':
            # Change button text to Deselect All
            # self.select_all_button.setText('Deselect All')
            
            # Select all filtered branches
            for branch in self.filtered_branches:
                if branch not in self.selected_branches:
                    self.add_branch_tag(branch)
        else:
            # Change button text back to Select All
            self.select_all_button.setText('Select All')
            
            # Clear all selected branches and remove tags
            for branch in self.selected_branches.copy():
                self.remove_branch_tag(branch)
     
        
    def add_branch_tag(self, branch_name):
        if branch_name not in self.selected_branches:
            self.selected_branches.append(branch_name)
            
            tag_widget = QWidget()
            tag_widget.setProperty('class', 'SelectedBranchTag')
            tag_layout = QHBoxLayout()
            tag_layout.setSpacing(5)
            tag_layout.setContentsMargins(0, 2, 8, 2)  # 여백 약간 증가
            
            # 브랜치 이름 라벨 - sizePolicy 제거하여 자동 크기 조절
            tag_label = QLabel(branch_name)
            tag_label.setStyleSheet('''
                background: transparent;
                color: white; 
                font-size: 12px;
                padding: 2px 4px;  /* 텍스트 주변 여백 추가 */
                margin: 1;  /* 위젯 주변 여백 제거 */
            ''')
            
            # 삭제 버튼
            close_btn = QPushButton('×')
            close_btn.setFixedWidth(20)  # 버튼 크기 고정
            close_btn.setFixedHeight(20)
            close_btn.setFont(QFont('Arial', 30, QFont.Bold))
            close_btn.setProperty('class', 'TagCloseButton')
            close_btn.setCursor(Qt.PointingHandCursor)
            close_btn.setStyleSheet('''
                font-size: 16px;
            ''')
            close_btn.clicked.connect(lambda: self.remove_branch_tag(branch_name))
            
            tag_layout.addWidget(tag_label)
            tag_layout.addWidget(close_btn)
            tag_widget.setLayout(tag_layout)
            
            # 마지막 stretch 제거하고 직접 추가
            self.tags_layout.addWidget(tag_widget)
        self.update_branch_list()

    def remove_branch_tag(self, branch_name):
        if branch_name in self.selected_branches:
            self.selected_branches.remove(branch_name)
            # 태그 위젯 찾아서 제거
            for i in range(self.tags_layout.count()):
                widget = self.tags_layout.itemAt(i).widget()
                if widget and isinstance(widget, QWidget):
                    label = widget.findChild(QLabel)
                    if label and label.text() == branch_name:
                        widget.deleteLater()
                        break
            self.update_branch_list()

    def update_branch_list(self):
        self.branch_list_widget.clear()
        # 선택되지 않은 브랜치만 필터링
        available_branches = [
            branch for branch in self.filtered_branches 
            if branch not in self.selected_branches
        ]
        
        for branch in available_branches:  # filtered_branches 대신 available_branches 사용
            item_widget = QWidget()
            layout = QHBoxLayout()
            layout.setContentsMargins(10, 8, 20, 8)
            
            # 호버 효과를 위한 스타일시트 적용 - 범위 제한
            item_widget.setStyleSheet('''
                QWidget#item_widget {
                    border-radius: 5px;
                    background-color: #1e1e1e;
                }
                QWidget#item_widget:hover {
                    background-color: #2c2c2c;
                }
            ''')
            item_widget.setObjectName("item_widget")  # 객체 이름 설정
            
            # 브랜치 이름 라벨
            branch_label = QLabel(branch)
            branch_label.setStyleSheet('''
                color: white;
                font-size: 16px;
                padding: 5px;
                background: transparent;
            ''')
            
            # Add 버튼 - 클로저 문제 해결을 위해 lambda에 default argument 사용
            add_button = QPushButton('Add')
            add_button.setFixedWidth(60)
            add_button.setFixedHeight(25)
            add_button.clicked.connect(lambda checked, b=branch: self.add_branch_tag(b))
            
            # 레이아웃에 위젯 추가
            layout.addWidget(branch_label)
            layout.addStretch()
            layout.addWidget(add_button)
            
            item_widget.setLayout(layout)
            
            # 리스트 위젯에 아이템 추가
            item = QListWidgetItem()
            item.setSizeHint(item_widget.sizeHint())
            self.branch_list_widget.addItem(item)
            self.branch_list_widget.setItemWidget(item, item_widget)

    def filter_branches(self, text):
        # 검색어로 필터링된 브랜치 중 선택되지 않은 것만 표시
        self.filtered_branches = [
            branch for branch in self.branch_list
            if text.lower() in branch.lower()
        ]
        self.update_branch_list()

    def on_next_clicked(self):
        if not self.selected_branches:
            QMessageBox.warning(self, '경고', '브랜치를 하나 이상 선택해주세요.')
            return
        # TODO: 다음 페이지로 이동하는 로직 구현
        print("Selected branches:", self.selected_branches)

if __name__ == '__main__': 
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = BranchSelectionPage()
    window.show()
    sys.exit(app.exec_())
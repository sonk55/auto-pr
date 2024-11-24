from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy
from components.labels import TitleLabelH3, DescriptionLabel
from components.buttons import PrimaryButton
from config_manager import ConfigManager

class BranchInfoDetailPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config_manager = ConfigManager()
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(30)  # 간격 증가
        layout.setContentsMargins(30, 10, 30, 30)  # 상단 여백 감소
        
        # 상단 여백 추가
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))
        
        self.title = TitleLabelH3('Branch Detail', self)
        layout.addWidget(self.title)
        
        # 타이틀과 정보 컨테이너 사이 여백 추가
        layout.addSpacerItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Fixed))
        
        # 브랜치 정보 컨테이너
        self.info_container = QVBoxLayout()
        self.info_container.setSpacing(15)  # 정보 항목 간 간격 조정
        layout.addLayout(self.info_container)
        
        # 하단 버튼까지 여백을 위한 신축성 있는 공간
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # 버튼 영역
        button_layout = QHBoxLayout()
        back_button = PrimaryButton('뒤로가기', self)
        back_button.clicked.connect(self.parent().show_list)  # 부모(BranchInfoPage)의 show_list 호출
        button_layout.addWidget(back_button)
        layout.addLayout(button_layout)
        
    def show_branch_info(self, branch_name):
        # 기존 위젯 제거
        for i in reversed(range(self.info_container.count())): 
            self.info_container.itemAt(i).widget().setParent(None)
        
        # 브랜치 정보 로드
        branches = self.config_manager.load_branches()
        branch_info = next((b for b in branches if b['name'] == branch_name), None)
        
        if branch_info:
            # 정보 표시
            self.title.setText(f"Branch: {branch_name}")
            fields = [
                ('Last Commit', 'last_commit'),
                ('Author', 'author'),
                ('Date', 'date'),
            ]
            
            for label, key in fields:
                info_label = DescriptionLabel(f"{label}: {branch_info.get(key, '')}")
                self.info_container.addWidget(info_label)

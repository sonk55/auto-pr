from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPlainTextEdit, 
                           QPushButton, QLabel, QMessageBox, QTableWidget, 
                           QTableWidgetItem, QHeaderView, QLineEdit, QListWidget,
                           QListWidgetItem, QWidget)
from PyQt5.QtCore import Qt
import json
from components.buttons import PrimaryButton, SecondaryButton, TableInlineButton
from components.labels import TitleLabelH3
from styles.dark_theme import COLORS
from config_manager import ConfigManager

class BranchEditDialog(QDialog):
    def __init__(self, branch_data, parent=None):
        super().__init__(parent)
        self.branch_data = branch_data.copy()  # 원본 데이터 복사
        self.setup_ui()
        self.load_data()
        self.result_action = 'save'  # 'save' or 'remove'
        self.setFixedSize(500, 600)  # 창 크기 고정

    def setup_ui(self):
        self.setWindowTitle('Edit Branch')
        self.setMinimumSize(400, 500)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Branch Name 입력
        name_layout = QVBoxLayout()
        name_label = QLabel('Branch Name')
        name_label.setStyleSheet(f'color: {COLORS["text_secondary"]}')
        self.name_input = QLineEdit()
        self.name_input.setStyleSheet(f'''
            QLineEdit {{
                background-color: {COLORS['bg_secondary']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                padding: 8px;
            }}
        ''')
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)
        
        # Tags 섹션
        tags_layout = QVBoxLayout()
        tags_label = QLabel('Tags')
        tags_label.setStyleSheet(f'color: {COLORS["text_secondary"]}')
        tags_layout.addWidget(tags_label)
        
        # Tag 입력 및 추가 버튼
        tag_input_layout = QHBoxLayout()
        self.tag_input = QLineEdit()
        self.tag_input.setPlaceholderText('Add new tag...')
        self.tag_input.setStyleSheet(f'''
            QLineEdit {{
                background-color: {COLORS['bg_secondary']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                padding: 8px;
            }}
        ''')
        add_tag_button = PrimaryButton('Add')
        add_tag_button.clicked.connect(self.add_tag)
        tag_input_layout.addWidget(self.tag_input)
        tag_input_layout.addWidget(add_tag_button)
        tags_layout.addLayout(tag_input_layout)
        
        # Tags 리스트
        self.tags_list = QListWidget()
        # 다중 선택 비활성화, 토글 가능하게 설정
        self.tags_list.setSelectionMode(QListWidget.SingleSelection)
        self.tags_list.itemClicked.connect(self.toggle_item_selection)
        self.tags_list.setStyleSheet(f'''
            QListWidget {{
                background-color: {COLORS['bg_secondary']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                padding: 4px;
            }}
            QListWidget::item {{
                padding: 8px;
                border-bottom: 1px solid {COLORS['border']};
                border-radius: 4px;
                margin: 2px;
            }}
            QListWidget::item:last {{
                border-bottom: none;
            }}
            QListWidget::item:selected {{
                background-color: {COLORS['bg_hover']};
                border: 1px solid {COLORS['link']};
                color: {COLORS['link']};
            }}
            QListWidget::item:hover:!selected {{
                background-color: {COLORS['bg_hover']};
            }}
        ''')
        tags_layout.addWidget(self.tags_list)
        
        # Remove Tag 버튼
        remove_tag_button = SecondaryButton('Remove Selected Tag', self)
        remove_tag_button.setStyleSheet(f'''
            QPushButton {{
                color: {COLORS['error']};
                border: 1px solid {COLORS['error']};
                border-radius: 6px;
                min-width: 100px;
            }}
            QPushButton:hover {{
                background-color: rgba(248, 81, 73, 0.1);
                border-color: {COLORS['error']};
            }}
        ''')
        
        remove_tag_button.clicked.connect(self.remove_selected_tag)
        tags_layout.addWidget(remove_tag_button)
        
        layout.addLayout(tags_layout)
        
        # 버튼
        button_layout = QHBoxLayout()
        
        # Remove 버튼 추가 (왼쪽에 배치)
        remove_button = SecondaryButton('Remove Branch', self)
        remove_button.setStyleSheet(f'''
            QPushButton {{
                background-color: rgba(248, 81, 73);
                border: 1px solid {COLORS['error']};
                border-radius: 6px;
                padding: 8px 16px;
                min-width: 100px;
                color: white;
            }}
            QPushButton:hover {{
                background-color: rgba(248, 81, 73, 0.4);
                border-color: {COLORS['error']};
                color: {COLORS['error']};
            }}
        ''')
        remove_button.clicked.connect(self.remove_branch)
        
        save_button = PrimaryButton('Save', self)
        save_button.setStyleSheet(save_button.styleSheet() + '''
            QPushButton {
                min-width: 100px;
                padding: 8px 16px;
            }
        ''')
        save_button.clicked.connect(self.save_changes)
        
        cancel_button = SecondaryButton('Cancel', self)
        cancel_button.setStyleSheet(cancel_button.styleSheet() + '''
            QPushButton {
                min-width: 100px;
                padding: 8px 16px;
            }
        ''')
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(remove_button)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

    def toggle_item_selection(self, item):
        if item.isSelected():
            self.tags_list.clearSelection()
        else:
            item.setSelected(True)

    def load_data(self):
        self.name_input.setText(self.branch_data['name'])
        self.tags_list.clear()
        for tag in self.branch_data['tags']:
            self.tags_list.addItem(tag)

    def add_tag(self):
        tag = self.tag_input.text().strip()
        if tag and tag not in [self.tags_list.item(i).text() 
                              for i in range(self.tags_list.count())]:
            self.tags_list.addItem(tag)
            self.tag_input.clear()

    def remove_selected_tag(self):
        current_item = self.tags_list.currentItem()
        if current_item:
            self.tags_list.takeItem(self.tags_list.row(current_item))

    def save_changes(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.critical(self, 'Error', 'Branch name cannot be empty')
            return
            
        tags = [self.tags_list.item(i).text() 
                for i in range(self.tags_list.count())]
        
        self.branch_data['name'] = name
        self.branch_data['tags'] = tags
        self.accept()

    def remove_branch(self):
        reply = QMessageBox.question(self, 'Confirm Remove', 
                                   f'Are you sure you want to remove branch "{self.branch_data["name"]}"?',
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.result_action = 'remove'
            self.accept()

    def get_result(self):
        return self.result_action, self.branch_data

class NewBranchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.branch_data = {'name': '', 'tags': []}
        self.setFixedSize(500, 600)  # 창 크기 고정

    def setup_ui(self):
        self.setWindowTitle('New Branch')
        self.setMinimumSize(400, 500)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Branch Name 입력
        name_layout = QVBoxLayout()
        name_label = QLabel('Branch Name')
        name_label.setStyleSheet(f'color: {COLORS["text_secondary"]}')
        self.name_input = QLineEdit()
        self.name_input.setStyleSheet(f'''
            QLineEdit {{
                background-color: {COLORS['bg_secondary']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                padding: 8px;
            }}
        ''')
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)
        
        # Tags 섹션 (BranchEditDialog와 동일)
        tags_layout = QVBoxLayout()
        tags_label = QLabel('Tags')
        tags_label.setStyleSheet(f'color: {COLORS["text_secondary"]}')
        tags_layout.addWidget(tags_label)
        
        # Tag 입력 및 추가 버튼
        tag_input_layout = QHBoxLayout()
        self.tag_input = QLineEdit()
        self.tag_input.setPlaceholderText('Add new tag...')
        self.tag_input.setStyleSheet(f'''
            QLineEdit {{
                background-color: {COLORS['bg_secondary']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                padding: 8px;
            }}
        ''')
        add_tag_button = PrimaryButton('Add')
        add_tag_button.clicked.connect(self.add_tag)
        tag_input_layout.addWidget(self.tag_input)
        tag_input_layout.addWidget(add_tag_button)
        tags_layout.addLayout(tag_input_layout)
        
        # Tags 리스트
        self.tags_list = QListWidget()
        # 다중 선택 비활성화, 토글 가능하게 설정
        self.tags_list.setSelectionMode(QListWidget.SingleSelection)
        self.tags_list.itemClicked.connect(self.toggle_item_selection)
        self.tags_list.setStyleSheet(f'''
            QListWidget {{
                background-color: {COLORS['bg_secondary']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                padding: 4px;
            }}
            QListWidget::item {{
                padding: 8px;
                border-bottom: 1px solid {COLORS['border']};
                border-radius: 4px;
                margin: 2px;
            }}
            QListWidget::item:last {{
                border-bottom: none;
            }}
            QListWidget::item:selected {{
                background-color: {COLORS['bg_hover']};
                border: 1px solid {COLORS['link']};
                color: {COLORS['link']};
            }}
            QListWidget::item:hover:!selected {{
                background-color: {COLORS['bg_hover']};
            }}
        ''')
        tags_layout.addWidget(self.tags_list)
        
        # Remove Tag 버튼
        remove_tag_button = SecondaryButton('Remove Selected Tag')
        remove_tag_button.clicked.connect(self.remove_selected_tag)
        tags_layout.addWidget(remove_tag_button)
        
        layout.addLayout(tags_layout)
        
        # 버튼
        button_layout = QHBoxLayout()
        save_button = PrimaryButton('Add', self)
        save_button.clicked.connect(self.save_changes)
        save_button.setStyleSheet(save_button.styleSheet() + '''
            QPushButton {
                min-width: 100px;
                padding: 8px 16px;
            }
        ''')
        
        cancel_button = SecondaryButton('Cancel', self)
        cancel_button.setStyleSheet(cancel_button.styleSheet() + '''
            QPushButton {
                min-width: 100px;
                padding: 8px 16px;
            }
        ''')
        cancel_button.clicked.connect(self.reject)
        
        # 버튼 순서 변경: Save(왼쪽) - 공백 - Cancel(오른쪽)
        button_layout.addWidget(save_button)
        button_layout.addStretch()
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

    def toggle_item_selection(self, item):
        if item.isSelected():
            self.tags_list.clearSelection()
        else:
            item.setSelected(True)

    def add_tag(self):
        tag = self.tag_input.text().strip()
        if tag and tag not in [self.tags_list.item(i).text() 
                              for i in range(self.tags_list.count())]:
            self.tags_list.addItem(tag)
            self.tag_input.clear()

    def remove_selected_tag(self):
        current_item = self.tags_list.currentItem()
        if current_item:
            self.tags_list.takeItem(self.tags_list.row(current_item))

    def save_changes(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.critical(self, 'Error', 'Branch name cannot be empty')
            return
            
        tags = [self.tags_list.item(i).text() 
                for i in range(self.tags_list.count())]
        
        self.branch_data['name'] = name
        self.branch_data['tags'] = tags
        self.accept()

    def get_branch_data(self):
        return self.branch_data

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config_manager = ConfigManager()
        self.all_branches = []  # 전체 브랜치 데이터 저장
        self.setup_ui()
        self.load_branches()
        
    def setup_ui(self):
        self.setWindowTitle('Settings')
        self.setMinimumSize(800, 600)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # 제목
        title = TitleLabelH3('Branch List Configuration')
        layout.addWidget(title)
        
        # 검색 영역과 Add Branch 버튼
        search_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('Search by branch name or tag...')
        self.search_input.textChanged.connect(self.filter_branches)
        self.search_input.setStyleSheet(f'''
            QLineEdit {{
                background-color: {COLORS['bg_secondary']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                padding: 8px;
            }}
            QLineEdit:focus {{
                border-color: {COLORS['border_hover']};
            }}
        ''')
        
        add_branch_button = PrimaryButton('New')
        add_branch_button.clicked.connect(self.add_branch)
        
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(add_branch_button)
        layout.addLayout(search_layout)
        
        # 브랜치 테이블
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Branch Name', 'Tags', 'Actions'])
        
        # 행 높이 설정
        self.table.verticalHeader().setDefaultSectionSize(48)  # 기본 행 높이
        
        # Branch Name 열을 고정 너비로 설정
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.table.setColumnWidth(0, 200)  # Branch Name 열 너비
        
        # Tags 열이 남은 공간을 모두 차지
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        
        # Actions 열 설정
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
        self.table.setColumnWidth(2, 100)
        
        # Add these two lines to make table read-only
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        
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
            }}
            QTableWidget::item {{
                padding: 0px 8px;
                border: none;
            }}
            QTableWidget::item:selected {{
                background-color: rgba(88, 166, 255, 0.1);
                color: {COLORS['link']};
            }}
        ''')
        layout.addWidget(self.table)
        
        # 버튼
        button_layout = QHBoxLayout()
        
        # save_button = PrimaryButton('Save', self)
        # save_button.clicked.connect(self.save_all_changes)
        
        # Close 버튼을 SecondaryButton으로 변경
        close_button = SecondaryButton('Close', self)
        close_button.clicked.connect(self.accept)
        
        # button_layout.addWidget(save_button)
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        layout.addLayout(button_layout)

    # Save 버튼 기능 추가
    def save_all_changes(self):
        if self.config_manager.save_branches(self.all_branches):
            QMessageBox.information(self, 'Success', 'All changes saved successfully')
        else:
            QMessageBox.critical(self, 'Error', 'Failed to save changes')

    def load_branches(self):
        self.all_branches = self.config_manager.load_branches()
        self.update_table(self.all_branches)

    def update_table(self, branches):
        self.table.setRowCount(len(branches))
        
        for i, branch in enumerate(branches):
            # Branch Name
            name_item = QTableWidgetItem(branch['name'])
            name_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.table.setItem(i, 0, name_item)
            
            # Tags
            tags_item = QTableWidgetItem(', '.join(branch['tags']))
            tags_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.table.setItem(i, 1, tags_item)
            
            # Actions 버튼들
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            actions_layout.setSpacing(0)
            
            edit_button = TableInlineButton('Edit', self.table)
            
            edit_button.clicked.connect(lambda checked, row=i: self.edit_branch(row))
            
            actions_layout.addWidget(edit_button)
            actions_layout.addStretch()
            
            self.table.setCellWidget(i, 2, actions_widget)

    def add_branch(self):
        dialog = NewBranchDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            new_branch = dialog.get_branch_data()
            # 동일한 이름의 브랜치가 있는지 확인
            if any(b['name'] == new_branch['name'] for b in self.all_branches):
                QMessageBox.warning(self, 'Warning', 
                                  f'Branch "{new_branch["name"]}" already exists')
                return
                
            self.all_branches.append(new_branch)
            if self.config_manager.save_branches(self.all_branches):
                self.load_branches()
                QMessageBox.information(self, 'Success', 'Branch added successfully')
            else:
                QMessageBox.critical(self, 'Error', 'Failed to add branch')

    def filter_branches(self):
        search_text = self.search_input.text().lower()
        if not search_text:
            self.update_table(self.all_branches)
            return
            
        filtered_branches = []
        for branch in self.all_branches:
            # 브랜치 이름은 부분 일치
            name_match = search_text in branch['name'].lower()
            # 태그는 완전 일치 (대소문자 무시)
            tag_match = search_text in [tag.lower() for tag in branch['tags']]
            
            if name_match or tag_match:
                filtered_branches.append(branch)
                
        self.update_table(filtered_branches)

    def edit_branch(self, row):
        branch_name = self.table.item(row, 0).text()
        branches = self.config_manager.load_branches()
        branch_data = next((b for b in branches if b['name'] == branch_name), None)
        
        if branch_data:
            dialog = BranchEditDialog(branch_data, self)
            if dialog.exec_() == QDialog.Accepted:
                action, updated_data = dialog.get_result()
                if action == 'remove':
                    self.all_branches = [b for b in self.all_branches if b['name'] != branch_name]
                    message = 'Branch removed successfully'
                else:  # action == 'save'
                    self.all_branches = [updated_data if b['name'] == branch_name else b 
                                       for b in self.all_branches]
                    message = 'Branch updated successfully'
                
                if self.config_manager.save_branches(self.all_branches):
                    self.load_branches()
                    QMessageBox.information(self, 'Success', message)
                else:
                    QMessageBox.critical(self, 'Error', 'Failed to save changes')
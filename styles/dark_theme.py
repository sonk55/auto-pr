# GitHub Desktop 색상 정의
COLORS = {
    'bg_primary': '#1f2428',
    'bg_secondary': '#24292e',
    'bg_hover': '#2b3036',  # hover 배경색 추가
    'text_primary': '#ffffff',
    'text_secondary': '#959da5',
    'border': '#444d56',
    'border_hover': '#8b949e',  # hover 테두리 색상 추가
    'button_primary': '#2ea44f',
    'button_hover': '#2c974b',
    'link': '#58a6ff',
    'sidebar_bg': '#24292e',
    'content_bg': '#1f2428',
    'error': '#f85149',  # 에러 색상 추가
    'bg_active': '#323942',  # 버튼 클릭 시 배경색 추가
}

COMMON_STYLE = f'''
    QWidget {{
        background-color: {COLORS['bg_primary']};
        color: {COLORS['text_primary']};
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }}
    QMenuBar {{
        background-color: {COLORS['bg_primary']};
        color: {COLORS['text_primary']};
    }}
    QMenuBar::item {{
        background-color: transparent;
        padding: 8px 12px;
    }}
    QMenuBar::item:selected {{
        background-color: {COLORS['bg_hover']};
    }}
    QMenu {{
        background-color: {COLORS['bg_secondary']};
        border: 1px solid {COLORS['border']};
    }}
    QMenu::item {{
        padding: 6px 28px;
    }}
    QMenu::item:selected {{
        background-color: {COLORS['bg_hover']};
    }}
    QTableWidget {{
        background-color: {COLORS['bg_secondary']};
        border: 1px solid {COLORS['border']};
        border-radius: 6px;
    }}
    QTableWidget::item {{
        padding: 8px;
        border-bottom: 1px solid {COLORS['border']};
    }}
    QLineEdit {{
        background-color: {COLORS['bg_secondary']};
        border: 1px solid {COLORS['border']};
        border-radius: 6px;
        padding: 8px;
        color: {COLORS['text_primary']};
    }}
'''

LAYOUT_STYLE = f'''
    QWidget#SidebarWidget {{
        background-color: {COLORS['sidebar_bg']};
        border-right: 1px solid {COLORS['border']};
    }}
    QWidget#ContentWidget {{
        background-color: {COLORS['content_bg']};
    }}
'''

BRANCH_SELECTION_STYLE = '''
    .SelectedBranchTag {
        background-color: #333333; 
        border-radius: 4px;
        padding: 5px;
        margin: 2px;
    }
    .TagCloseButton {
        background-color: transparent;
        color: #9575CD;
        border: none;
        padding: 2px 5px;
        font-size: 12px;
        font-weight: bold;
    }
    .TagCloseButton:hover {
        color: white;
    }
'''

START_WINDOW_STYLE = '''
    QPushButton {
        border-radius: 25px;
        padding: 15px 30px;
    }
    QPushButton:pressed {
        background-color: #673AB7;
    }
'''
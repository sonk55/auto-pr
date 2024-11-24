from PyQt5.QtWidgets import QApplication

def get_center_position(width, height):
    # 현재 화면의 가운데 위치 계산
    screen = QApplication.desktop().screenGeometry()
    x = (screen.width() - width) // 2
    y = (screen.height() - height) // 2
    return x, y

WINDOW_SIZES = {
    'MAIN': (1200, 1000),
    'START': (1200, 800)
}
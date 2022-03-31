import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QSpacerItem, QPushButton, QHBoxLayout, QApplication, QMainWindow


class TitleBar(QWidget):
    def __init__(self, *args, **kwargs):
        super(TitleBar, self).__init__(*args, **kwargs)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.initUI()

    # 绘制标题栏界面
    def initUI(self):
        window_widget = QWidget(self)
        winTitle_layout = QHBoxLayout()
        winTitle_layout.setSpacing(0)
        winTitle_layout.setContentsMargins(0, 0, 0, 0)
        winIcon = QLabel('icon')
        winTitle = QLabel('window')
        winSpcerItem = QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        winMinBtn = QPushButton('-')
        winRestoreBtn = QPushButton('口')
        winCloseBtn = QPushButton('x')

        winTitle_layout.addWidget(winIcon)
        winTitle_layout.addWidget(winTitle)
        winTitle_layout.addItem(winSpcerItem)
        winTitle_layout.addWidget(winMinBtn)
        winTitle_layout.addWidget(winRestoreBtn)
        winTitle_layout.addWidget(winCloseBtn)

        window_widget.setLayout(winTitle_layout)
        self.setCentralWidget(window_widget)


if __name__ == '__main__':
    # PyQt5高清屏幕自适应设置,以及让添加的高清图标显示清晰，不然designer导入的图标在程序加载时会特别模糊
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    main_win = TitleBar()

    main_win.show()
    sys.exit(app.exec_())


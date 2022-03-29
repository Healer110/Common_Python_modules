import sys
import time
import threading

import numpy as np
import psutil
import pyqtgraph as pg
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QMainWindow, QApplication, QListWidgetItem, QLabel, QWidget, QHBoxLayout, QListWidget
from qt_material import apply_stylesheet
import qdarkstyle
from layout_demo import Ui_MainWindow


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setupUi(self)


        self.left_list.currentRowChanged.connect(self.display_stack_window)
        # self.initUI()

        pass


    # 通过QListWidget导航栏切换item来控制stackWidget页面
    def display_stack_window(self, index):
        self.stackedWidget.setCurrentIndex(index)




    def initUI(self):
        self.setGeometry(300, 300, 600, 620)



if __name__ == '__main__':
    # PyQt5高清屏幕自适应设置
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    main_win = Window()

    # setup stylesheet
    # apply_stylesheet(app, theme='dark_teal.xml')
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    main_win.show()
    sys.exit(app.exec_())
    # aa = np.linspace(-2*np.pi, 2*np.pi, 500)
    # print(aa[0])















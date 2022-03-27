from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(561, 335)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mdiArea = QtWidgets.QMdiArea(self.centralwidget)
        self.mdiArea.setObjectName("mdiArea")
        self.horizontalLayout.addWidget(self.mdiArea)
        self.start_btn = QtWidgets.QPushButton(self.centralwidget)
        self.start_btn.setObjectName("start_btn")
        self.horizontalLayout.addWidget(self.start_btn)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 561, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget_2 = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget_2.setObjectName("dockWidget_2")
        self.dockWidgetContents_2 = QtWidgets.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.dockWidget_2.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget_2)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.start_btn.setText(_translate("MainWindow", "start"))


import sys

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog


# 自定义QDialog组件，增加最大化最小化按钮
class My_Dialog(QDialog):
    def __init__(self, parent=None):
        super(My_Dialog, self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        # self.setWindowFlags(Qt.FramelessWindowHint)  # 去除边框
        self.setWindowFlags(Qt.Dialog | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)  # 最大化最小化关闭按钮
        pass

    def mouseMoveEvent(self, QMouseEvent):  # 5
        x = QMouseEvent.x()
        y = QMouseEvent.y()
        global_x = QMouseEvent.globalX()
        global_y = QMouseEvent.globalY()

        print(x, y)


class Test(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Test, self).__init__()
        # 启动界面，所有需要在init进行初始化的函数跟事件，都要在初始化之后进行
        self.setupUi(self)

        self.start_btn.clicked.connect(self.show_widget)
        self.setMouseTracking(True)
        self.centralwidget.setMouseTracking(True)
        self.start_btn.setMouseTracking(True)
        self.dockWidget_2.setMouseTracking(True)
        self.mdiArea.setMouseTracking(True)

    def show_widget(self):
        self.dialog = My_Dialog(self)
        self.dialog.setMouseTracking(True)
        print(self.dialog.hasMouseTracking())       # 返回设置的状态
        self.dialog.resize(200, 200)
        self.dialog.show()


    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:  # 左键按下
            # self.setText("单击鼠标左键的事件: 自己定义")
            print("单击鼠标左键")  # 响应测试语句
        elif event.buttons() == QtCore.Qt.RightButton:  # 右键按下
            # self.setText("单击鼠标右键的事件: 自己定义")
            print("单击鼠标右键")  # 响应测试语句
        elif event.buttons() == QtCore.Qt.MidButton:  # 中键按下
            # self.setText("单击鼠标中键的事件: 自己定义")
            print("单击鼠标中键")  # 响应测试语句
        elif event.buttons() == QtCore.Qt.LeftButton | QtCore.Qt.RightButton:  # 左右键同时按下
            # self.setText("同时单击鼠标左右键的事件: 自己定义")
            print("单击鼠标左右键")  # 响应测试语句
        elif event.buttons() == QtCore.Qt.LeftButton | QtCore.Qt.MidButton:  # 左中键同时按下
            # self.setText("同时单击鼠标左中键的事件: 自己定义")
            print("单击鼠标左中键")  # 响应测试语句
        elif event.buttons() == QtCore.Qt.MidButton | QtCore.Qt.RightButton:  # 右中键同时按下
            # self.setText("同时单击鼠标右中键的事件: 自己定义")
            print("单击鼠标右中键")  # 响应测试语句
        elif event.buttons() == QtCore.Qt.LeftButton | QtCore.Qt.MidButton \
                | QtCore.Qt.RightButton:  # 左中右键同时按下
            # self.setText("同时单击鼠标左中右键的事件: 自己定义")
            print("单击鼠标左中右键")  # 响应测试语句

    def mouseMoveEvent(self, event):
        globalPos = self.mapToGlobal(event.pos())
        x = globalPos.x()
        y = globalPos.y()
        print(x, y)




if __name__ == '__main__':
    # PyQt5高清屏幕自适应设置
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    main_win = Test()

    main_win.show()
    sys.exit(app.exec_())






import sys
import time
import threading

import numpy as np
import psutil
import pyqtgraph as pg
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QPushButton, QDialog, QHBoxLayout, \
    QGridLayout
from qt_material import apply_stylesheet
from test_result_show_timely import My_Dialog, draw_data_timely

from test import Ui_MainWindow


class Test(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Test, self).__init__()
        # 启动界面，所有需要在init进行初始化的函数跟事件，都要在初始化之后进行
        self.setupUi(self)

        self.start_btn.clicked.connect(self.show_widget)
        # self.start_btn.clicked.connect(self.thread_run)


    def show_widget(self):
        self.dialog = My_Dialog(self)
        self.dialog.setMouseTracking(True)
        self.dialog.setWindowTitle('Show data')
        # self.dialog.resize(200, 200)
        self.plot_layout = QGridLayout()  # 实例化一个网格布局层
        self.plot_layout.setSpacing(0)
        self.plot_layout.setContentsMargins(0, 0, 0, 0)
        self.dialog.setLayout(self.plot_layout)  # 设置K线图部件的布局层
        # self.plot_plt = pg.PlotWidget()  # 实例化一个绘图部件
        self.win = pg.GraphicsLayoutWidget(show=True)  # 实例化一个绘图部件
        self.label = pg.LabelItem(justify='right')  # 添加标签
        self.win.addItem(self.label)  # 将当前的标签添加到窗口
        # self.plot_plt = self.win.addPlot(row=1, col=0, title='H-plane')       # 添加title为设置标签
        self.plot_plt = self.win.addPlot(row=1, col=0)
        self.plot_plt.setLabel('left', 'H-Plane', units='dBm')  # 设置Label
        self.plot_plt.showGrid(x=True, y=True)  # 显示图形网格
        self.plot_layout.addWidget(self.win)

        self.vLine = pg.InfiniteLine(angle=90, movable=False, )  # 创建一个垂直线条
        self.hLine = pg.InfiniteLine(angle=0, movable=False, )  # 创建一个水平线条
        self.plot_plt.addItem(self.vLine, ignoreBounds=True)  # 在图形部件中添加垂直线条
        self.plot_plt.addItem(self.hLine, ignoreBounds=True)  # 在图形部件中添加水平线条

        # 测试两张图的场景：
        self.plot_plt_2 = self.win.addPlot(row=2, col=0)
        self.plot_plt_2.showGrid(x=True, y=True)  # 显示图形网格
        self.plot_plt_2.setLabel('left', 'V-Plane', units='dBm')  # 设置Label
        self.vLine2 = pg.InfiniteLine(angle=90, movable=False, )  # 创建一个垂直线条
        self.hLine2 = pg.InfiniteLine(angle=0, movable=False, )  # 创建一个水平线条
        self.plot_plt_2.addItem(self.vLine2, ignoreBounds=True)  # 在图形部件中添加垂直线条
        self.plot_plt_2.addItem(self.hLine2, ignoreBounds=True)  # 在图形部件中添加水平线条

        # self.tt = np.linspace(-2 * np.pi, 2 * np.pi, 500)
        # self.plot_plt.plot(pen='g').setData(np.sin(self.tt))
        #
        self.move_slot = pg.SignalProxy(self.plot_plt.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)
        self.move_slot_2 = pg.SignalProxy(self.plot_plt_2.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved2)

        self.dialog.show()
        self.data_list = []

        self.Thread1 = NewThread()
        self.Thread1.trigger.connect(self.Plot)

        self.Thread1.start()

    # 绘图
    def Plot(self, list, list1):
        self.tt = np.array(list)
        self.plot_plt.plot().setData(list1[len(list1)-2:],list[len(list)-2:],pen='g',symbol='o')
        self.plot_plt_2.plot().setData(list1[len(list1)-2:],list[len(list)-2:],pen='g',symbol='star')
        # self.plot_plt.plot(clear=True).setData(list1[len(list1) - 2:], list[len(list) - 2:], pen='g', symbol='o')



    def show_widget_bak(self):
        self.dialog = My_Dialog(self)
        self.dialog.setMouseTracking(True)
        # self.dialog.resize(200, 200)
        self.plot_layout = QGridLayout()  # 实例化一个网格布局层
        self.plot_layout.setSpacing(0)
        self.plot_layout.setContentsMargins(0, 0, 0, 0)
        self.dialog.setLayout(self.plot_layout)  # 设置K线图部件的布局层
        # self.plot_plt = pg.PlotWidget()  # 实例化一个绘图部件
        self.win = pg.GraphicsLayoutWidget(show=True)  # 实例化一个绘图部件
        self.win.setWindowTitle('Show data')
        self.label = pg.LabelItem(justify='right')      # 添加标签
        self.win.addItem(self.label)        # 将当前的标签添加到窗口
        self.plot_plt = self.win.addPlot(row=1, col=0)
        self.plot_plt.showGrid(x=True, y=True)  # 显示图形网格
        self.plot_layout.addWidget(self.win)


        self.vLine = pg.InfiniteLine(angle=90, movable=False, )  # 创建一个垂直线条
        self.hLine = pg.InfiniteLine(angle=0, movable=False, )  # 创建一个水平线条
        self.plot_plt.addItem(self.vLine, ignoreBounds=True)  # 在图形部件中添加垂直线条
        self.plot_plt.addItem(self.hLine, ignoreBounds=True)  # 在图形部件中添加水平线条

        # self.plot_plt.setMouseTracking(True)

        self.tt = np.linspace(-2 * np.pi, 2 * np.pi, 500)
        self.plot_plt.plot(pen='g').setData(np.sin(self.tt))

        self.move_slot = pg.SignalProxy(self.plot_plt.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)

        self.dialog.show()


    def mouseMoved(self, evt):
        self.vb = self.plot_plt.vb
        pos = evt[0]  ## using signal proxy turns original arguments into a tuple
        if self.plot_plt.sceneBoundingRect().contains(pos):
            mousePoint = self.vb.mapSceneToView(pos)
            index = int(mousePoint.x())
            if index > 0 and index < self.tt.shape[0]:
                self.label.setText(
                    "<span style='font-size: 12pt'>x=%0.1f,   <span style='color: red'>y1=%0.1f</span>,   <span style='color: green'>y2=%0.1f</span>" % (
                    mousePoint.x(), self.tt[index], self.tt[index]))
            self.vLine.setPos(mousePoint.x())
            self.hLine.setPos(mousePoint.y())

    def mouseMoved2(self, evt):
        self.vb2 = self.plot_plt_2.vb
        pos = evt[0]  ## using signal proxy turns original arguments into a tuple
        if self.plot_plt_2.sceneBoundingRect().contains(pos):
            mousePoint = self.vb2.mapSceneToView(pos)
            index = int(mousePoint.x())
            if index > 0 and index < self.tt.shape[0]:
                self.label.setText(
                    "<span style='font-size: 12pt'>x=%0.1f,   <span style='color: red'>y1=%0.1f</span>,   <span style='color: green'>y2=%0.1f</span>" % (
                    mousePoint.x(), self.tt[index], self.tt[index]))
            self.vLine2.setPos(mousePoint.x())
            self.hLine2.setPos(mousePoint.y())


class NewThread(QThread):
    trigger = pyqtSignal(list,list)
    def __init__(self):
        super(NewThread, self).__init__()
        self.dataList = []
        self.timeList = []
        self.a = 0

    def run(self):
        # print('NewThread start!')

        while True:
            # time.sleep(1)
            # Xtime = time.strftime("%H%M%S")
            Ycpu = "%0.2f" % psutil.cpu_percent(interval=1)
            self.dataList.append(float(Ycpu))
            self.timeList.append(self.a)
            # timelist.append(float(Xtime))
            # print(Xtime, Ycpu)
            self.a += 1
            self.trigger.emit(self.dataList,self.timeList)







if __name__ == '__main__':
    # PyQt5高清屏幕自适应设置
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    main_win = Test()

    # setup stylesheet
    # apply_stylesheet(app, theme='dark_teal.xml')

    main_win.show()
    sys.exit(app.exec_())
    # aa = np.linspace(-2*np.pi, 2*np.pi, 500)
    # print(aa[0])

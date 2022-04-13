import sys
import time

import numpy as np

import pyqtgraph as pg
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QApplication, QHBoxLayout, QGridLayout


# 自定义QDialog组件，增加最大化最小化按钮
class My_Dialog(QDialog):
    def __init__(self, parent=None):
        super(My_Dialog, self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        # self.setWindowFlags(Qt.FramelessWindowHint)  # 去除边框
        self.setWindowFlags(Qt.Dialog | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)  # 最大化最小化关闭按钮
        pass

def draw_data_timely(mainWin: object):

    dialog = My_Dialog(mainWin)
    dialog.setMouseTracking(True)
    # self.dialog.resize(200, 200)
    plot_layout = QGridLayout()  # 实例化一个网格布局层
    plot_layout.setSpacing(0)
    plot_layout.setContentsMargins(0, 0, 0, 0)
    dialog.setLayout(plot_layout)  # 设置K线图部件的布局层
    # self.plot_plt = pg.PlotWidget()  # 实例化一个绘图部件
    win = pg.GraphicsLayoutWidget(show=True)  # 实例化一个绘图部件
    win.setWindowTitle('Show data')
    label = pg.LabelItem(justify='right')  # 添加标签
    win.addItem(label)  # 将当前的标签添加到窗口
    plot_plt = win.addPlot(row=1, col=0)
    plot_plt.showGrid(x=True, y=True)  # 显示图形网格
    plot_layout.addWidget(win)

    vLine = pg.InfiniteLine(angle=90, movable=False, )  # 创建一个垂直线条
    hLine = pg.InfiniteLine(angle=0, movable=False, )  # 创建一个水平线条
    plot_plt.addItem(vLine, ignoreBounds=True)  # 在图形部件中添加垂直线条
    plot_plt.addItem(hLine, ignoreBounds=True)  # 在图形部件中添加水平线条

    # self.plot_plt.setMouseTracking(True)

    tt = np.linspace(-2 * np.pi, 2 * np.pi, 500)
    plot_plt.plot(pen='g').setData(np.sin(tt))



    dialog.show()

    def mouseMoved(evt):
        vb = plot_plt.vb
        pos = evt[0]  ## using signal proxy turns original arguments into a tuple
        if plot_plt.sceneBoundingRect().contains(pos):
            mousePoint = vb.mapSceneToView(pos)
            index = int(mousePoint.x())
            if index > 0 and index < tt.shape[0]:
                label.setText(
                    "<span style='font-size: 12pt'>x=%0.1f,   <span style='color: red'>y1=%0.1f</span>,   <span style='color: green'>y2=%0.1f</span>" % (
                    mousePoint.x(), tt[index], tt[index]))
            vLine.setPos(mousePoint.x())
            hLine.setPos(mousePoint.y())

    move_slot = pg.SignalProxy(plot_plt.scene().sigMouseMoved, rateLimit=60, slot=mouseMoved)

# 实时绘图实现方法
def draw_data_timely_1(mainWin: object):
    '''
    将产生的数据实时的展示到pyqtgraph组件中
    :param mainWin: 传递调用该程序的主程序对象，因为实例化QDialog时，需要主窗口对象
    :return: 返回当前子窗口的对象，以实现实时绘图
    '''

    #generate layout
    app = pg.mkQApp("Data Analysis")
    win = pg.GraphicsLayoutWidget(show=True)
    win.setWindowTitle('Data Analysis')
    label = pg.LabelItem(justify='right')
    win.addItem(label)

    # 实例化QDialog
    qdialog = My_Dialog(mainWin)
    hLayout = QHBoxLayout()
    hLayout.addWidget(win)
    hLayout.setSpacing(0)
    hLayout.setContentsMargins(0, 0, 0, 0)
    qdialog.setLayout(hLayout)
    qdialog.show()

    p1 = win.addPlot(row=1, col=0)
    # p1.showGrid(x=True, y=True)  # 显示图形网格
    # customize the averaged curve that can be activated from the context menu:
    p1.avgPen = pg.mkPen('#FFFFFF')
    p1.avgShadowPen = pg.mkPen('#8080DD', width=10)

    p2 = win.addPlot(row=2, col=0)
    # p2.showGrid(x=True, y=True)  # 显示图形网格

    region = pg.LinearRegionItem()
    region.setZValue(10)
    # Add the LinearRegionItem to the ViewBox, but tell the ViewBox to exclude this
    # item when doing auto-range calculations.
    p2.addItem(region, ignoreBounds=True)

    #pg.dbg()
    p1.setAutoVisible(y=True)


    #create numpy arrays
    #make the numbers large to show that the range shows data from 10000 to all the way 0
    data1 = 10000 + 15000 * pg.gaussianFilter(np.random.random(size=10000), 10) + 3000 * np.random.random(size=10000)
    data2 = 15000 + 15000 * pg.gaussianFilter(np.random.random(size=10000), 10) + 3000 * np.random.random(size=10000)

    p1.plot(data1, pen="r")
    p1.plot(data2, pen="g")

    p2d = p2.plot(data1, pen="w")
    # bound the LinearRegionItem to the plotted data
    region.setClipItem(p2d)

    def update():
        region.setZValue(10)
        minX, maxX = region.getRegion()
        p1.setXRange(minX, maxX, padding=0)

    region.sigRegionChanged.connect(update)

    def updateRegion(window, viewRange):
        rgn = viewRange[0]
        region.setRegion(rgn)

    p1.sigRangeChanged.connect(updateRegion)

    region.setRegion([1000, 2000])

    #cross hair
    vLine = pg.InfiniteLine(angle=90, movable=False)
    hLine = pg.InfiniteLine(angle=0, movable=False)
    p1.addItem(vLine, ignoreBounds=True)
    p1.addItem(hLine, ignoreBounds=True)


    vb = p1.vb

    def mouseMoved(evt):
        pos = evt[0]  ## using signal proxy turns original arguments into a tuple
        if p1.sceneBoundingRect().contains(pos):
            mousePoint = vb.mapSceneToView(pos)
            index = int(mousePoint.x())
            if index > 0 and index < len(data1):
                label.setText("<span style='font-size: 12pt'>x=%0.1f,   <span style='color: red'>y1=%0.1f</span>,   <span style='color: green'>y2=%0.1f</span>" % (mousePoint.x(), data1[index], data2[index]))
            vLine.setPos(mousePoint.x())
            hLine.setPos(mousePoint.y())


    proxy = pg.SignalProxy(p1.scene().sigMouseMoved, rateLimit=60, slot=mouseMoved)
    #p1.scene().sigMouseMoved.connect(mouseMoved)


if __name__ == '__main__':
    # aa = show_data_real_time()
    # pg.exec()

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    main_win = My_Dialog()

    # setup stylesheet
    # apply_stylesheet(app, theme='dark_teal.xml')

    main_win.show()
    sys.exit(app.exec_())

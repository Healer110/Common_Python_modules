import sys


import numpy as np
import psutil
import pyqtgraph as pg
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QDialog, QGridLayout


'''
调用该API时，将主窗口对象传递进来即可，需要其他功能，再自定义修改即可
'''

# 自定义QDialog组件，去掉问号按钮并增加最大化最小化按钮
class My_Dialog(QDialog):
    def __init__(self, parent=None):
        super(My_Dialog, self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        # self.setWindowFlags(Qt.FramelessWindowHint)  # 去除边框
        self.setWindowFlags(Qt.Dialog | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)  # 最大化最小化关闭按钮
        pass


# 实时显示测试数据接口
class realTimeDisplay(My_Dialog):
    # real_time_trig_of_api = pyqtSignal(int, list, list)
    def __init__(self, parent=None):
        '''
        实时显示数据初始化，需要将调用该程序的主窗口对象传递进来
        :param parent: 父窗口对象
        '''
        super(realTimeDisplay, self).__init__(parent)

        # self.show_widget()        # 初始化调用绘图窗口，这里先不自动调用，主程序实例化该对象后，自己调用即可，单独执行该程序时打开

    # 编辑一个QDialog对话框，用来实时显示测试数据
    def show_widget(self):
        '''
        在pyqt5主界面调用pyqtgraph进行绘图，基本的思路是，先创建一个QDialog窗口，该窗口的父窗口就是主窗口。
        然后pyqtgraph绘图部件的主窗口为QDialog，这样就可以在pyqt5主程序中进行调用了。
        关系：
        main_windows ---->realTimeDisplay(main_windows)---->My_Dialog(realTimeDisplay)
        :return:
        '''
        self.setWindowModality(Qt.NonModal)                                     # 设置非模态对话框
        self.setMouseTracking(True)                                             # 设置组件可以对鼠标进行追踪
        self.setWindowTitle('Real-time display')                                # 设置窗口标题
        # self.dialog.resize(200, 200)
        self.plot_layout = QGridLayout()                                        # 实例化一个网格布局层
        self.plot_layout.setSpacing(0)                                          # 设置网格布局space为0
        self.plot_layout.setContentsMargins(0, 0, 0, 0)                         # 设置网格布局margin为0
        self.setLayout(self.plot_layout)                                        # 设置dialog布局为网格布局
        # self.plot_plt = pg.PlotWidget()                                       # 实例化一个绘图部件
        self.win = pg.GraphicsLayoutWidget(show=True)                           # 实例化一个绘图部件，创建后立即显示
        self.label = pg.LabelItem(justify='right')                              # 添加标签
        self.win.addItem(self.label)                                            # 将当前的标签添加到窗口
        # self.plot_plt = self.win.addPlot(row=1, col=0, title='H-plane')       # 添加title为设置标签
        self.plot_plt = self.win.addPlot(row=1, col=0)
        self.plot_plt.setLabel('left', 'H-Plane', units='dBm')                  # 设置Label
        self.plot_plt.showGrid(x=True, y=True)                                  # 显示图形网格
        self.plot_layout.addWidget(self.win)

        self.vLine = pg.InfiniteLine(angle=90, movable=False, )     # 创建一个垂直线条
        self.hLine = pg.InfiniteLine(angle=0, movable=False, )      # 创建一个水平线条
        self.plot_plt.addItem(self.vLine, ignoreBounds=True)        # 在图形部件中添加垂直线条
        self.plot_plt.addItem(self.hLine, ignoreBounds=True)        # 在图形部件中添加水平线条

        # 实例化第二个绘图部件
        self.plot_plt_2 = self.win.addPlot(row=2, col=0)
        self.plot_plt_2.showGrid(x=True, y=True)                    # 显示图形网格
        self.plot_plt_2.setLabel('left', 'V-Plane', units='dBm')    # 设置Label
        self.vLine2 = pg.InfiniteLine(angle=90, movable=False, )    # 创建一个垂直线条
        self.hLine2 = pg.InfiniteLine(angle=0, movable=False, )     # 创建一个水平线条
        self.plot_plt_2.addItem(self.vLine2, ignoreBounds=True)     # 在图形部件中添加垂直线条
        self.plot_plt_2.addItem(self.hLine2, ignoreBounds=True)     # 在图形部件中添加水平线条

        # 设置鼠标移动的触发，限制速率，移动则触发mouseMoved函数
        self.move_slot = pg.SignalProxy(self.plot_plt.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)
        self.move_slot_2 = pg.SignalProxy(self.plot_plt_2.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved2)

        self.show()
        # self.data_list = []

        self.Thread1 = NewThread()
        self.Thread1.trigger.connect(self.Plot)

        self.Thread1.start()

    # 绘图
    def Plot(self, list, list1):
        self.tt = np.array(list)
        self.plot_plt.plot().setData(list1[len(list1)-2:],list[len(list)-2:],pen='g',symbol='o')
        self.plot_plt_2.plot().setData(list1[len(list1)-2:],list[len(list)-2:],pen='r',symbol='star')
        # self.plot_plt.plot(clear=True).setData(list1[len(list1) - 2:], list[len(list) - 2:], pen='g', symbol='o')



    def show_widget_bak(self):
        self.dialog = My_Dialog(self.mainWin)
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

    main_win = realTimeDisplay()
    main_win.show_widget()

    # main_win.show()
    sys.exit(app.exec_())

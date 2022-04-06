import sys
import time

from PyQt5.QtCore import pyqtSignal, QThread, Qt
from PyQt5.QtWidgets import QDialog, QPushButton, QHBoxLayout, QApplication, QVBoxLayout, QMainWindow, QWidget


# 实际执行的逻辑程序，被thread程序调用
class AA():
    # test_signal = pyqtSignal(str, list)
    def __init__(self, signal_trig):
        self.test_signal = signal_trig  # 接收Thread传递进来的信号
        self.hello()

    # 写逻辑函数
    def hello(self):
        for x in range(20):
            self.test_signal.emit(f'我是AA类{x}', list(range(10)))     # 使用Thread信号发送生成的数据
            time.sleep(2)


# 多线程函数--->被主程序调用
class My_thread(QThread):
    thread_trig = pyqtSignal(str, list)
    def __init__(self):
        super(My_thread, self).__init__()

    def run(self):
        a = AA(self.thread_trig)      # 将接收的信号传给调用的程序


# 主程序调用QDialog弹窗，Dialog弹窗会实时处理数据
class My_Dialog_test_signal(QDialog):
    # dialog_trig = pyqtSignal(str, list)
    def __init__(self, parent=None):
        super(My_Dialog_test_signal, self).__init__(parent)
        self.initUi()
        # self.dialog_trig.connect(self.trig_func)

    def initUi(self):
        vLayout = QVBoxLayout()
        btn = QPushButton('QDialog测试按钮')
        vLayout.addWidget(btn)
        self.setLayout(vLayout)
        self.resize(200, 200)
        self.show()

    def trig_func(self, ss, lst):
        print(ss, lst)


# 主界面程序
class CC(QWidget):
    trig = pyqtSignal(str, list)
    def __init__(self):
        super(CC, self).__init__()
        self.initUi()


    def initUi(self):
        btn = QPushButton('单击接收信号')
        self.resize(300, 300)
        hLayout = QHBoxLayout()
        hLayout.addWidget(btn)
        self.setLayout(hLayout)

        btn2 = QPushButton('测试弹窗信号')
        hLayout.addWidget(btn2)

        btn.clicked.connect(self.btn_click)
        btn2.clicked.connect(self.test_threadSignal)

    # 点击按钮调用Thread
    def btn_click(self):
        # self.t = My_thread(self.trig)
        self.t = My_thread()        # 传给My_thread
        self.t.thread_trig.connect(self.cc_print)   # 将Thread中的信号绑定槽函数
        self.t.start()


    def test_threadSignal(self):
        tmp = My_Dialog_test_signal(self)
        self.trig.connect(tmp.trig_func)    # 将主程序的信号绑定弹窗QDialog中的函数

    # 接收Thread信号发出来的值，并由主程序中的信号再次发送出去，由Dialog中的程序处理
    def cc_print(self, ss, lst):
        self.trig.emit(ss, lst)



if __name__ == '__main__':
    # PyQt5高清屏幕自适应设置,以及让添加的高清图标显示清晰，不然designer导入的图标在程序加载时会特别模糊
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    main_win = CC()

    main_win.show()
    sys.exit(app.exec_())


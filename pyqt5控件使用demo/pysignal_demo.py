import sys

from PyQt5.QtCore import pyqtSignal, QThread, Qt
from PyQt5.QtWidgets import QDialog, QPushButton, QHBoxLayout, QApplication


# 实际执行的程序
class AA():
    # test_signal = pyqtSignal(str, list)
    def __init__(self, signal_trig):
        self.test_signal = signal_trig
        self.hello()

    # 写逻辑函数
    def hello(self):
        self.test_signal.emit('我是AA类', list(range(10)))


# 多线程函数
class My_thread(QThread):
    bb_signal = pyqtSignal(str, list)
    def __init__(self):
        super(My_thread, self).__init__()

    def run(self):
        a = AA(self.bb_signal)

    def word(self, ss, lst):
        print(ss, lst)
        # self.bb_signal.emit(ss, lst)


# 主界面程序
class CC(QDialog):
    def __init__(self):
        super(CC, self).__init__()
        self.initUi()


    def initUi(self):
        btn = QPushButton('单击接收信号')
        self.resize(300, 300)
        hLayout = QHBoxLayout()
        hLayout.addWidget(btn)
        self.setLayout(hLayout)

        btn.clicked.connect(self.btn_click)

    def btn_click(self):
        self.t = My_thread()
        self.t.bb_signal.connect(self.cc_print)
        self.t.start()


    def cc_print(self, ss, lst):
        print(ss, lst)



if __name__ == '__main__':
    # PyQt5高清屏幕自适应设置,以及让添加的高清图标显示清晰，不然designer导入的图标在程序加载时会特别模糊
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    main_win = CC()

    main_win.show()
    sys.exit(app.exec_())
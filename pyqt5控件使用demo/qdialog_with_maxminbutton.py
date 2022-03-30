import sys

from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtCore import Qt

'''
该自定义类实现的是在QDialog窗口增加最大化最小化按钮功能，
网上的各种答案基本都不对，花费了好几个小时才搞定了，
self.setWindowFlags(Qt.Dialog | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
网上的各种方式在主窗口调用QDialog窗口时就会出错，使用该方法就会实现该功能
'''


class My_Dialog(QDialog):
    def __init__(self, parent=None):
        super(My_Dialog, self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        # self.setWindowFlags(Qt.FramelessWindowHint)  # 去除边框
        self.setWindowFlags(Qt.Dialog | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        pass


if __name__ == '__main__':
    # QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    main_win = My_Dialog()

    main_win.show()
    sys.exit(app.exec_())

import sys

from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from PyQt5.QtWidgets import QMainWindow, QApplication, QListWidgetItem, QLabel, QWidget, QHBoxLayout, QListWidget, \
    QStyleOptionTitleBar, QStyleFactory
from qt_material import apply_stylesheet
import qdarkstyle
from layout_demo import Ui_MainWindow


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setupUi(self)
        self.reset_dock_title_bar()     # 重置dockWidget标题栏
        # self.set_palette()  # 设置背景
        self.left_list.currentRowChanged.connect(self.display_stack_window)

        # tmp.setFixedHeight(20)
        # self.initUI()
        # self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setWindowFlags(Qt.CustomizeWindowHint)

        self.changeStyle('windowsvista')        # 默认主题
        pass

    # 重置QDockWidget标题栏，放一张图片上去，并将QLabel背景色设置为白色
    def reset_dock_title_bar(self):
        title_label = QLabel()
        title_label.setObjectName('dock_title_label')
        title_label.setAlignment(Qt.AlignCenter)    # 设置QLabel内容居中显示
        title_label.setStyleSheet("QLabel{background-color: rgb(255, 255, 255);space: 0px; margin: 0px;}")
        qpimap = QPixmap('../icons/signal.png')     # 加载图片
        qpimap.scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # 设置图片大小并按比例伸缩
        # qpimap.scaled(title_label.size(), Qt.KeepAspectRatio)     # 另外一种设置图片按照比例缩放的方法
        # title_label.setScaledContents(True)       # 可以使图片根据QLabel的大小进行填充
        title_label.setPixmap(qpimap)
        self.dockWidget_2.setTitleBarWidget(title_label)
        tmp = self.dockWidget_2.titleBarWidget()
        # print(tmp)
        tmp.setMinimumHeight(30)
        # tmp.setFixedHeight(10)

    # 设置背景
    def set_palette(self):
        # 不设置也可以
        self.setAutoFillBackground(True)
        palette = QPalette()
        # 设置背景颜色
        # palette.setColor(self.backgroundRole(), QColor(192, 253, 123))
        # 设置背景图片
        palette.setBrush(self.backgroundRole(), QBrush(QPixmap('../icons/winBack.jpeg')))
        self.setPalette(palette)


    # 通过QListWidget导航栏切换item来控制stackWidget页面
    def display_stack_window(self, index):
        self.stackedWidget.setCurrentIndex(index)

    # 设置自带主题
    def changeStyle(self, styleName):
        '''
        支持如下三种
        ['windowsvista', 'Windows', 'Fusion']
        :param styleName: 主题名称
        :return:
        '''
        # 改变Style
        QApplication.setStyle(QStyleFactory.create(styleName))


if __name__ == '__main__':
    # PyQt5高清屏幕自适应设置,以及让添加的高清图标显示清晰，不然designer导入的图标在程序加载时会特别模糊
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    main_win = Window()

    # setup stylesheet
    # apply_stylesheet(app, theme='dark_teal.xml')
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())


    main_win.show()
    sys.exit(app.exec_())
    # aa = np.linspace(-2*np.pi, 2*np.pi, 500)
    # print(aa[0])

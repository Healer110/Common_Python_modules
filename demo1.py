import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class StackedExample(QWidget):
    def __init__(self):
        super(StackedExample, self).__init__()


        self.setWindowTitle("选堆栈窗口控件:QStackedWidget")
        self.resize(500, 400)

        # 创建一个列表控件
        self.list = QListWidget()
        self.list.insertItem(0, "联系方式")
        self.list.insertItem(1, "个人信息")
        self.list.insertItem(2, "教育程度")

        # 创建三个QWidget类型的子页面
        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = QWidget()

        # 创建一个堆栈窗口控件，并将三个子页面装载进入其中
        self.stack = QStackedWidget()
        self.stack.addWidget(self.stack1)
        self.stack.addWidget(self.stack2)
        self.stack.addWidget(self.stack3)

        # 调用封装好的、用来为子页面添加控件的函数
        self.tab1UI()
        self.tab2UI()
        self.tab3UI()

        layout = QHBoxLayout()
        layout.addWidget(self.list)
        layout.addWidget(self.stack)
        self.setLayout(layout)

        self.list.currentRowChanged.connect(self.display)



    def tab1UI(self):
        layout = QFormLayout()
        layout.addRow("姓名", QLineEdit())
        layout.addRow("地址", QLineEdit())


        self.stack1.setLayout(layout)


    def tab2UI(self):
        layout = QFormLayout()
        sex = QHBoxLayout()
        sex.addWidget(QRadioButton('男'))
        sex.addWidget(QRadioButton('女'))
        layout.addRow("性别", sex)
        layout.addRow("生日", QLineEdit())


        self.stack2.setLayout(layout)


    def tab3UI(self):
        layout = QHBoxLayout()
        layout.addWidget(QLabel("科目"))
        layout.addWidget(QCheckBox("物理"))
        layout.addWidget(QCheckBox("高数"))


        self.stack3.setLayout(layout)


    def display(self, index):
        # 根据index，堆栈窗口控件会切换到相应序号的页面
        self.stack.setCurrentIndex(index)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = StackedExample()
    main.show()
    sys.exit(app.exec_())
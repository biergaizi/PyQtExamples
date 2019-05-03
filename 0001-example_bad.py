#!/usr/bin/env python3

import sys

from time import sleep
from PyQt4 import QtCore, QtGui

# 创建一个实例窗口
class ExampleWindow(QtGui.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        # 创建一个下载按钮
        self.button1 = QtGui.QPushButton('Click to Download', self)

        # 没用的按钮，用于点击观察界面是否假死
        self.button2 = QtGui.QPushButton('Test UI Response', self)

        # 「点击按钮」信号触发 self.download()
        self.button1.clicked.connect(self.download)

        # 创建一个文本标签
        self.label1 = QtGui.QLabel(self)
        self.label1.setText("Waiting to Download")

        # 随意设置位置和大小，无视即可
        self.button1.move(20, 20)
        self.button2.move(20, 130)
        self.label1.move(20, 100)
        self.setGeometry(300, 300, 250, 180) 

        self.show()

    def download(self):
        # 错误的操作：将耗时代码直接写入图形界面代码。
        # 这会导致整个图形界面暂时停止工作，造成假死。
        sleep(5)
        self.label1.setText("File Downloaded!")

def main():
    app = QtGui.QApplication(sys.argv)
    example = ExampleWindow()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()


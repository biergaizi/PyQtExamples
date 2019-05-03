#!/usr/bin/env python3

import sys
import threading

from time import sleep
from PyQt4 import QtCore, QtGui

# 创建一个实例窗口
class ExampleWindow(QtGui.QWidget):

    # 创建自定义「下载完成」信号
    download_finished_signal = QtCore.pyqtSignal()

    # 创建自定义「下载进度」信号。
    # 和其他信号不同，这个信号带一个参数，其类型为 int。
    download_progress_signal = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        # 定义空对象，用于占位。
        self.download_thread = None

        # 创建一个下载按钮
        self.button1 = QtGui.QPushButton('Click to Download', self)

        # 没用的按钮，用于点击观察界面是否假死
        self.button2 = QtGui.QPushButton('Test UI Response', self)

        # 「点击按钮」信号触发 self.download_start
        self.button1.clicked.connect(self.download_start)

        # 「下载完成」信号触发 self.download_finished
        self.download_finished_signal.connect(self.download_finished)

        # 「下载进度」信号触发 self.download_progress
        self.download_progress_signal.connect(self.download_progress)

        # 创建一个文本标签
        self.label1 = QtGui.QLabel(self)
        self.label1.setText("Waiting to Download")

        # 随意设置位置和大小，无视即可
        self.button1.move(20, 20)
        self.button2.move(20, 130)
        self.label1.move(20, 100)
        self.setGeometry(300, 300, 250, 180) 

        self.show()

    def download_start(self):
        # 正确的操作：当图形界面需要进行耗时代码时，应该启动一个独立的
        # Python 线程。这个线程独立于图形界面代码工作，因此不会造成假死。
        # 当下载完成时，该线程触发 self.download_finished_signal() 通知
        # 主程序更新界面。

        if self.download_thread and self.download_thread.is_alive():
            # 线程已创建过而且正在运行了，无视用户的点击，函数立刻结束。
            return

        # group 参数必须制定，但不使用，填写 None。
        # target 参数是欲在线程中执行的函数对象。
        # args 是一个 Python 列表，指定参数。这里没有参数，故不使用。
        self.download_thread = threading.Thread(group=None, target=self.download)

        # 启动线程！
        self.download_thread.start()

        self.label1.setText("Now Downloading...")

        # 至此，该函数退出，将图形界面的控制权暂时还归 Qt 主循环.

    def download(self):
        # 线程本体。这里可以执行耗时操作。

        # 警告：该线程独立于图形界面代码工作，因此不会造成假死。
        # 但是同理，也严禁在本函数中操作图形界面！否则将会产生随机
        # 崩溃的未定义行为。

        # 线程要对界面进行的任何修改，都必须通过「Qt 信号」这一事件传递
        # 机制，告诉主界面你要做什么，具体怎么做，要在信号所连接的界面代码
        # 中进行。

        # 循环 5 次，从 0 到 4，不是 5。
        # Python 中的 range(a, b) 是 [a, b)，半开半闭区间。
        for i in range(0, 5):
            # 计算进度
            progress = (i / 4) * 100

            # 触发主界面的 self.download_progress_signal，更新进度。
            # 注意，这里我们传递了一个参数。
            self.download_progress_signal.emit(int(progress))

            # 继续进行阻塞操作
            sleep(1)

        # 我们在这里触发主界面的 self.download_finished_signal()
        self.download_finished_signal.emit()

    # 这是一个带参数的 pyqtSlot. 类型必须与信号的声明一致。
    @QtCore.pyqtSlot(int)
    def download_progress(self, progress):
        # 使用字符串格式化，类似 C 的 printf
        self.label1.setText("Progress: %d%%" % (progress))

        # 相当于
        #self.label1.setText("Progress: " + str(progress) + "%")
        

    # Qt 中，一个信号的接受者被称为「槽」（slot）。
    # 在 Python 中，务必使用修饰器 @QtCore.pyqtSlot() 进行标注。
    @QtCore.pyqtSlot()
    def download_finished(self):
        # 下载完成后，线程触发 download_finished_signal，而该信号连接
        # download_finished（见 __init()__）。通知主界面更新文本。

        self.label1.setText("File Downloaded!")
        
        # 可以在这里禁用按钮，防止用户重复点击
        self.button1.setEnabled(False)

def main():
    app = QtGui.QApplication(sys.argv)
    example = ExampleWindow()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()


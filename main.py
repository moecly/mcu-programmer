import sys
from dfu import dfu
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
from time import sleep
import threading
from monitor_usb import monitor_usb
from PyQt5.QtGui import QFont

class monitor_usb_device(QThread):
    def __init__(self):
        self.mon_usb = monitor_usb()
        return super(monitor_usb_device, self).__init__()
    
    push = pyqtSignal(list)
    pop = pyqtSignal(list)

    def run(self):
        while True:
            push_drv, pop_drv = self.mon_usb.detect_usb_event() 
            if len(push_drv) != 0:
                print("插入: " + str(push_drv))
                self.push.emit(push_drv)

            if len(pop_drv) != 0:
                print("弹出: " + str(pop_drv))
                self.pop.emit(pop_drv)
            sleep(1)

class main_window(QWidget):
    def __init__(self):
        super(main_window, self).__init__()
        # self.setGeometry(100, 100, 400, 200)
        self.setFixedSize(700, 500);
        # 主layout
        self.h_box_layout = QHBoxLayout()
        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.h_box_layout)
        self.setLayout(self.main_layout)

        # 设置窗口标题
        self.setWindowTitle("DSDFU")

        # 存储driver
        self.drivers = []

        # 创建 QFont 对象并设置字体大小
        push_button_font = QFont()
        push_button_font.setPointSize(26)  # 设置字体大小为16点
        # 烧录按钮
        self.programmer_push_button = QPushButton()
        self.programmer_push_button.setText("programmer")
        self.programmer_push_button.setFont(push_button_font)
        self.programmer_push_button.clicked.connect(self.on_programmer_push_button_clicked)
        self.main_layout.addWidget(self.programmer_push_button)

        # 清空按钮
        self.clear_push_button = QPushButton()
        self.clear_push_button.setText("clear")
        self.clear_push_button.setFont(push_button_font)
        self.clear_push_button.clicked.connect(self.on_clear_push_button_clicked)
        self.main_layout.addWidget(self.clear_push_button)

        # 创建 QFont 对象并设置字体大小
        listwidget_font = QFont()
        listwidget_font.setPointSize(16)  # 设置字体大小为16点

        # listwidget显示识别到的设备
        self.rec_dev_listwidget = QListWidget()
        self.rec_dev_listwidget.setFont(listwidget_font)
        self.h_box_layout.addWidget(self.rec_dev_listwidget)

        # label显示状态
        self.curr_dev_num = 0

        # 创建 QFont 对象并设置字体大小
        status_label_font = QFont()
        status_label_font.setPointSize(46)  # 设置字体大小为16点
        # 将 QFont 应用到 QLabel
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignCenter)  # 居中对齐
        self.h_box_layout.addWidget(self.status_label)
        self.status_label.setText(str(self.curr_dev_num))
        self.status_label.setFont(status_label_font)

        # listwidget显示烧录成功的设备
        self.writer_success_dev_listwidget = QListWidget()
        self.writer_success_dev_listwidget.setFont(listwidget_font)
        self.h_box_layout.addWidget(self.writer_success_dev_listwidget)
        
        self.monitor_usb_thread = monitor_usb_device()
        self.monitor_usb_thread.push.connect(self.on_monitor_usb_push_signal)
        self.monitor_usb_thread.pop.connect(self.on_monitor_usb_pop_signal)
        self.monitor_usb_thread.start()
        
        # 线程管理
        self.thread_manager = []

    def on_programmer_push_button_clicked(self):
        print(f"开始烧写: {self.drivers}")
        for item in self.drivers:
            thread = threading.Thread(target=self.write_to_device_in_thread, args=(item,))
            thread.start()
            self.thread_manager.append(thread)
            self.rec_dev_listwidget.addItem(item)
            self.curr_dev_num = self.curr_dev_num + 1
            self.status_label.setText(str(self.curr_dev_num))
    
    def on_clear_push_button_clicked(self):
        self.rec_dev_listwidget.clear()
        self.writer_success_dev_listwidget.clear()

    def write_to_device_in_thread(self, drive_letter):
        dfu.write_to_device(drive_letter)

    def on_monitor_usb_push_signal(self, driver):
        for item in driver:
            self.drivers.append(f"检测到: {item[0]}")

    def on_monitor_usb_pop_signal(self, driver):
        for item in driver:
            self.drivers.remove(item[0])
            self.writer_success_dev_listwidget.addItem(f"{item[0]}: 烧写完成")
            self.curr_dev_num = self.curr_dev_num - 1
            self.status_label.setText(str(self.curr_dev_num))
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = main_window()
    window.show()
    sys.exit(app.exec_())
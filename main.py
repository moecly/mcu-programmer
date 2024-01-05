import os
import sys
from dfu import dfu
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
from time import sleep

class write_device(QThread):
    def __init__(self, drive_letter='C'):
        self.drive_letter = drive_letter
        super(write_device, self).__init__()

    progress_signal = pyqtSignal(str)
    info = pyqtSignal(str)
    finished = pyqtSignal()

    def run(self):
        # 用于烧录设备
        drive_letter = self.drive_letter
        drive = drive_letter + ':'
        write_tool = dfu()

        # 发送进度信号
        self.progress_signal.emit("等待设备连接...")

        # 执行后台任务
        while not os.path.exists(drive):
            sleep(1)
        
        # 发送进度信号
        self.progress_signal.emit("开始写入...")
        
        if not write_tool.write_to_device(drive_letter):
            self.progress_signal.emit("源文件不存在")
            self.info.emit(str(drive_letter) + " 烧写失败")
        else:
            self.progress_signal.emit("烧写完成!")
            self.info.emit(str(drive_letter) + " 烧写成功")
        self.finished.emit()

class main_window(QWidget):
    def __init__(self):
        super(main_window, self).__init__()
        self.setGeometry(100, 100, 400, 200)
        # 主layout
        self.h_box_layout = QHBoxLayout()
        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.h_box_layout)
        self.setLayout(self.main_layout)

        # listwidget显示识别到的设备
        self.rec_dev_listwidget = QListWidget()
        self.h_box_layout.addWidget(self.rec_dev_listwidget)

        # label显示状态
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignCenter)  # 居中对齐
        self.h_box_layout.addWidget(self.status_label)
        self.status_label.setText("DFU")

        # listwidget显示烧录成功的设备
        self.writer_success_dev_listwidget = QListWidget()
        self.h_box_layout.addWidget(self.writer_success_dev_listwidget)
        
        # 线程管理
        self.thread_manager = []

        worker0 = write_device('D')
        self.thread_manager.append(worker0)
        worker0.info.connect(self.on_info_signal)
        worker0.progress_signal.connect(self.on_progress_signal)
        worker0.finished.connect(lambda: self.on_finish_signal(worker0))
        worker0.start()
        self.rec_dev_listwidget.addItem('D')

        worker1 = write_device('E')
        self.thread_manager.append(worker1)
        worker1.info.connect(self.on_info_signal)
        worker1.progress_signal.connect(self.on_progress_signal)
        worker1.finished.connect(lambda: self.on_finish_signal(worker1))
        worker1.start()
        self.rec_dev_listwidget.addItem('E')
    
    def on_finish_signal(self, worker):
        if worker in self.thread_manager:
            self.thread_manager.remove(worker)
    
    def on_progress_signal(self, message):
        # 在这里处理进度信号，例如更新标签文本或执行其他图形化修改
        self.status_label.setText(message)
    
    def on_info_signal(self, message):
        self.writer_success_dev_listwidget.addItem(message)

    # def nativeEvent(self, eventType, message):
    #     print(message)
    #     msg_type = message.message
    #     if msg_type == 0x0219:  # WM_DEVICECHANGE
    #         dev_broadcast_hdr = message.lParam
    #         if message.wParam == 0x8000:  # DBT_DEVICEARRIVAL
    #             if dev_broadcast_hdr.dbch_devicetype == 0x00000002:  # DBT_DEVTYP_VOLUME
    #                 dev_broadcast_volume = dev_broadcast_hdr.cast_to('DEV_BROADCAST_VOLUME*')
    #                 if dev_broadcast_volume.dbcv_flags == 0:
    #                     dec_driver = self.first_drive_from_mask(dev_broadcast_volume.dbcv_unitmask)
    #                     # 在这里启动你的线程或进行其他操作
    #                     worker = write_device(dec_driver)
    #                     worker_thread = QThread()
    #                     worker.moveToThread(self.worker_thread)
    #                     worker.finished.connect(self.worker_thread.quit)
    #                     worker.progress_signal.connect(self.on_progress_signal)
    #                     worker.info.connect(self.on_info_signal)
    #                     worker_thread.finished.connect(self.worker.deleteLater)
    #                     worker_thread.started.connect(self.worker.do_work)
    #                     worker_thread.start()
    #                     self.rec_dev_listwidget.addItem(dec_driver)
    #         elif message.wParam == 0x8004:  # DBT_DEVICEREMOVECOMPLETE
    #             if dev_broadcast_hdr.dbch_devicetype == 0x00000002:  # DBT_DEVTYP_VOLUME
    #                 dev_broadcast_volume = dev_broadcast_hdr.cast_to('DEV_BROADCAST_VOLUME*')
    #                 if dev_broadcast_volume.dbcv_flags == 0:
    #                     dec_driver = self.first_drive_from_mask(dev_broadcast_volume.dbcv_unitmask)
    #                     self.writer_success_dev_listwidget.addItem(dec_driver + " 烧写成功")
    #     return super(main_window, self).nativeEvent(eventType, message)

    # def first_drive_from_mask(self, mask):
    #     drive = 0
    #     while not (mask & 1):
    #         mask >>= 1
    #         drive += 1
    #     return chr(ord('A') + drive)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = main_window()
    window.show()
    sys.exit(app.exec_())
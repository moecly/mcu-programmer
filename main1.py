import threading
from dfu import dfu

def write_to_device_in_thread(drive_letter):
    writer = dfu()
    writer.write_to_device(drive_letter)

def main():
    # 设置线程参数
    drive_letter0 = 'D'
    drive_letter1 = 'E'

    # 创建线程
    thread0 = threading.Thread(target=write_to_device_in_thread, args=(drive_letter0,))
    thread1 = threading.Thread(target=write_to_device_in_thread, args=(drive_letter1,))

    # 启动线程
    thread0.start()
    thread1.start()

    # 主线程继续执行其他任务...

    # 等待线程结束
    thread0.join()
    thread1.join()

if __name__ == "__main__":
    main()
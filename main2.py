import psutil
import time

def get_removable_disks():
    # 获取可移动磁盘列表
    partitions = psutil.disk_partitions()
    removable_disks = [partition.device for partition in partitions if 'removable' in partition.opts]
    return removable_disks

def detect_usb_events():
    known_usb_devices = set()

    while True:
        current_usb_devices = get_removable_disks()

        # 检测新插入的U盘
        new_usb_devices = set(current_usb_devices) - known_usb_devices
        for usb_device in new_usb_devices:
            print(f"新U盘插入，盘符为：{usb_device}")

        # 检测拔出的U盘
        removed_usb_devices = known_usb_devices - set(current_usb_devices)
        for usb_device in removed_usb_devices:
            print(f"U盘拔出，盘符为：{usb_device}")

        # 更新已知的U盘设备列表
        known_usb_devices = set(current_usb_devices)

        time.sleep(1)

if __name__ == "__main__":
    detect_usb_events()
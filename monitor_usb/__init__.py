import psutil

class monitor_usb():
    def __init__(self):
        self.known_usb_devices = set()

    def get_removable_disks(self):
        # 获取可移动磁盘列表
        partitions = psutil.disk_partitions()
        removable_disks = [partition.device for partition in partitions if 'removable' in partition.opts]
        return removable_disks

    def detect_usb_event(self):
        current_usb_devices = self.get_removable_disks()

        # 检测新插入的U盘
        new_usb_devices = set(current_usb_devices) - self.known_usb_devices

        # 检测拔出的U盘
        removed_usb_devices = self.known_usb_devices - set(current_usb_devices)

        # 更新已知的U盘设备列表
        self.known_usb_devices = set(current_usb_devices)
        return list(new_usb_devices), list(removed_usb_devices)

if __name__ == "__main__":
    pass
    # monitor_usb.detect_usb_events()
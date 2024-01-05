from monitor_usb import monitor_usb
from dfu import dfu
import threading
from time import sleep

arr = []

def write_to_device_in_thread(drive_letter):
    dfu.write_to_device(drive_letter)

def monitor_usb_event():
    mon_usb = monitor_usb()
    while True:
        push, pop = mon_usb.detect_usb_event()
        for item in push:
            print(f"已插入: {item[0]}")
            arr.append(item[0])
            # thread = threading.Thread(target=write_to_device_in_thread, args=(item[0],))
            # thread.daemon = True
            # thread.start()
        for item in pop:
            print(f"{item[0]}: 已烧写完成")
            arr.remove(item[0])

def main():
    thread = threading.Thread(target=monitor_usb_event)
    thread.daemon = True
    thread.start()
    while True:
        user_input = input("Press 's' and Enter to execute the function: ")
        if user_input.lower() == 's':
            print(f"开始烧写: {arr}")
            for item in arr:
                thread = threading.Thread(target=write_to_device_in_thread, args=(item,))
                thread.daemon = True
                thread.start()
        else:
            print("Invalid input. Please press 's' to execute the function.")

if __name__ == "__main__":
    main()
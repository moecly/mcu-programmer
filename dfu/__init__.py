import os
import subprocess

class dfu():
    def __init__(self):
        pass

    @staticmethod
    def copy_file(src, dst):
        # 构建复制文件的命令
        command = f'copy "{src}" "{dst}"'

        try:
            # 调用命令并等待完成
            subprocess.run(command, shell=True, check=True)
            print(f'文件从 {src} 复制到 {dst} 成功！')
        except subprocess.CalledProcessError as e:
            print(f'复制文件时发生错误：{e}')

    # def copy_file(self, src, dst, fail_if_exists=False):
        # kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

        # # 定义参数类型
        # LPCTSTR = ctypes.c_wchar_p
        # BOOL = ctypes.wintypes.BOOL

        # # 调用CopyFileW函数
        # success = kernel32.CopyFileW(LPCTSTR(src), LPCTSTR(dst), BOOL(fail_if_exists))
        
        # # 检查复制是否成功
        # if not success:
        #     error_code = ctypes.get_last_error()
        #     raise WindowsError(error_code, ctypes.FormatError(error_code))
        
    @classmethod
    def write_to_device(cls, drive_letter='C'):
        if not cls.write_app_to_device(drive_letter):
            return False
        if not cls.write_end_to_device(drive_letter):
            return False
        return True

    @classmethod
    def write_app_to_device(cls, drive_letter='C'):
        drive = drive_letter + ':'
        src_app_file = os.path.join(os.getcwd(), 'app.bin')
        dst_app_file = os.path.join(drive, 'app.bin')
        
        if not os.path.exists(src_app_file):
            return False
        
        try:
            # shutil.copyfile(src_app_file, dst_app_file)
            cls.copy_file(src_app_file, dst_app_file)
        except Exception as e:
            print(e)
            return False
        return True

    @classmethod
    def write_end_to_device(cls, drive_letter='C'):
        drive = drive_letter + ':'
        src_end_file = os.path.join(os.getcwd(), 'end.txt')
        dst_end_file = os.path.join(drive, 'end.txt')
        
        if not os.path.exists(src_end_file):
            return False
        
        try:
            # shutil.copyfile(src_end_file, dst_end_file)
            cls.copy_file(src_end_file, dst_end_file)
        except Exception as e:
            print(e)
            return False
        return True


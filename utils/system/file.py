# utils/system/file.py

import os

def check_file_exist(file_path):
    """
    检查文件是否存在

    :param file_path: 文件路径
    :return: bool is_exist
    """

    if os.path.exists(file_path):
        return True
    else:
        return False
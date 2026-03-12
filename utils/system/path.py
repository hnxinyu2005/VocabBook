# utils/system/path.py

import os
import re
from utils.constants import DEFAULT_WORDBOOK, WORDBOOKS_FOLDER_NAME

def get_wordbook_csv_path(filename):
    '''
    生成单词本csv文件路径

    :param filename: 文件名 无需后缀
    :return: 安全的csv绝对路径
    '''

    # 去除空格和多余后缀
    filename_stripped = filename.strip() if filename else ""
    # 空文件名默认使用DEFAULT_WORDBOOK
    if not filename_stripped:
        filename_stripped = DEFAULT_WORDBOOK
    # 去除已有的.csv后缀
    if filename_stripped.lower().endswith(".csv"):
        filename_stripped = filename_stripped[:-4]

    # 过滤路径遍历字符 + 非法字符
    # 禁止包含路径分隔符（/、\）和路径遍历符（../、./）
    forbidden_chars = r"[\\/:\*\?\"<>|]" # 系统非法文件名字符 + 路径符
    # 替换所有非法字符为下划线
    safe_filename = re.sub(forbidden_chars, "_", filename_stripped)
    # 进一步过滤路径遍历关键词（防止../变形绕过，如..\、. ./等）
    safe_filename = re.sub(r"\.\.+", "_", safe_filename) # 过滤多个点
    safe_filename = re.sub(r"\.\s*/", "_", safe_filename) # 过滤. / 形式
    safe_filename = re.sub(r"\.\s*\\", "_", safe_filename) # 过滤. \ 形式

    # 强制限制路径在单词本目录内
    # 拼接基础文件名
    csv_filename = f"{safe_filename}.csv"
    # 获取单词本目录的绝对路径
    base_dir = os.path.abspath(
        os.path.join(os.path.dirname(os.path.dirname(__file__)), WORDBOOKS_FOLDER_NAME)
    )
    # 拼接目标文件路径
    file_path = os.path.join(base_dir, csv_filename)
    # 强制转换为绝对路径 防止相对路径绕过
    file_path = os.path.abspath(file_path)

    # 确保文件路径在单词本目录内
    # 检查目标路径是否是单词本目录的子路径
    if not file_path.startswith(base_dir + os.sep):
        # 若跳出 则强制使用默认文件名
        csv_filename = f"{DEFAULT_WORDBOOK}.csv"
        file_path = os.path.join(base_dir, csv_filename)

    return file_path
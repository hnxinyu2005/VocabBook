# utils/system/file.py

import os
import csv
from utils.constants import DEFAULT_ENCODING
from utils.system.path import get_wordbook_csv_path

def check_file_exist(file_path):
    """
    检查文件是否存在

    :param file_path: 文件路径
    :return: bool is_exist
    """

    return os.path.exists(file_path)

def get_all_wordbooks():
    """
    获取所有单词本

    :return: [{"name": "单词本名称", "path": "文件路径", "word_count": 单词数量}, ...]
    """

    from core.csv_manager import get_wordbook_word_count

    # 目录存在
    default_book_path = get_wordbook_csv_path("default")
    wordbook_dir = os.path.dirname(default_book_path)
    if not os.path.exists(wordbook_dir):
        os.makedirs(wordbook_dir)
        return []  # 空目录返回空列表

    # 遍历目录下的CSV文件
    wordbooks = []
    for filename in os.listdir(wordbook_dir):
        # 只处理CSV文件
        if not filename.endswith(".csv"):
            continue
        file_path = os.path.join(wordbook_dir, filename) # 拼接完整路径
        book_name = os.path.splitext(filename)[0] # 提取单词本名称（去掉.csv后缀）

        # 校验文件合法性
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                # 检查必要字段
                required_fields = {"word", "meaning"}
                if not required_fields.issubset(reader.fieldnames):
                    continue  # 字段不全，跳过该文件

        except Exception as e:
            print(f"读取单词本 {filename} 失败，{e}")
            continue

        # 传入：单词本名称 + 编码格式（从constants导入）
        word_count = get_wordbook_word_count(
            filename=book_name,  # 传入单词本名称（无.csv后缀）
            encoding=DEFAULT_ENCODING  # 使用统一编码常量
        )

        wordbooks.append({
            "name": book_name,
            "path": file_path,
            "word_count": word_count
        })

    return wordbooks
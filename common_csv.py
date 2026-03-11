# utils/common_csv.py

import pandas as pd
import os

import word_constants
from word_constants import WORDBOOKS_FOLDER_NAME, DEFAULT_WORDBOOK, STANDARD_CSV_HEADERS, DEFAULT_ENCODING

# 两个拆分函数
from split_meaning import split_word_meaning
from split_example import split_word_example

def get_wordbook_csv_path(filename):
    csv_filename = f"{filename.strip()}.csv"
    file_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        WORDBOOKS_FOLDER_NAME,
        csv_filename
    )
    return file_path

def validate_wordbook_csv(file_path):
    '''
    检查csv是否存在及验证表头

    :param file_path: 文件路径
    :return:tuple (is_valid: bool, error_msg: str)
             - is_valid: True=校验通过，False=校验失败
             - error_msg: 空字符串=无错误，否则为具体错误信息
    '''

    # 文件是否存在
    if not os.path.exists(file_path):
        return False, f"{file_path} 文件不存在"

    # 表头合规性
    try:
        # 仅读取表头
        df = pd.read_csv(file_path, encoding=DEFAULT_ENCODING, nrows=0)
        csv_headers = list(df.columns)

        # 检查是否缺少标准字段
        missing_headers = [h for h in STANDARD_CSV_HEADERS if h not in csv_headers]
        if missing_headers:
            return False, f"缺少标准表头字段，{file_path} 的表头：{missing_headers}，标准表头：{STANDARD_CSV_HEADERS}"

        # 所有校验通过
        return True, ""

    except Exception as e:
        return False, f"读取CSV表头失败，{str(e)}"

def validate_wordbook_csv_content(file_path):
    '''
    检查csv的文件内容是否符合规范，主要检查word和meaning字段是否为空
    
    :param file_path: 文件路径
    :return:tuple (is_valid: bool, error_msg: str)
             - is_valid: True=校验通过，False=校验失败
             - error_msg: 空字符串=无错误，否则为具体错误信息
    '''


def read_processed_csv(filename=DEFAULT_WORDBOOK, encoding=DEFAULT_ENCODING, validate=True, split_fields=True):
    '''
    读取csv并完成预处理。

    :param filename: 文件名
    :param encoding: 编码格式
    :param validate: 是否校验csv格式
    :param split_fields: 是否自动拆分
    :return: pandas.DataFrame 处理后的单词数据
    '''

    # 缺少filename则为默认单词库 写在了函数定义

    # 获取单词库路径
    file_path = get_wordbook_csv_path(filename)

    # 检查文件存在性及表头规范
    if validate:
        is_valid, error_msg = validate_wordbook_csv(file_path)
        if not is_valid:
            print(error_msg)


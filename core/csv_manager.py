# core/csv_manager.py

import pandas as pd
import os
import re

from utils.constants import DEFAULT_WORDBOOK, STANDARD_CSV_HEADERS, DEFAULT_ENCODING, DEFAULT_VALUES
from utils.text.split_meaning import split_word_meaning
from utils.text.split_example import split_word_example
from utils.math.calculate_word_accuracy import calculate_accuracy_numeric
from utils.system.path import get_wordbook_csv_path
from utils.system.file import check_file_exist

def validate_csv_headers(file_path):
    """
    检查csv是否存在及验证表头

    :param file_path: 文件路径
    :return:tuple (is_valid: bool, error_msg: str)
             - is_valid: True=校验通过，False=校验失败
             - error_msg: 空字符串=无错误，否则为具体错误信息
    """
    # 文件是否存在
    if not check_file_exist(file_path):
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
    """
    检查csv的文件内容是否符合规范，主要检查word和meaning字段是否为空

    :param file_path: 文件路径
    :return:tuple (is_valid: bool, error_msg: str)
             - is_valid: True=校验通过，False=校验失败
             - error_msg: 空字符串=无错误，否则为具体错误信息
    """
    # 无需重复检查文件存在性（validate_wordbook_csv已校验）
    # 无需重复捕获读取异常（validate_wordbook_csv已处理表头读取）

    df = pd.read_csv(file_path, encoding=DEFAULT_ENCODING)

    # 将空值、纯空格统一视为空
    df['word'] = df['word'].astype(str).str.strip()
    df['meaning'] = df['meaning'].astype(str).str.strip()

    # 检查word字段为空的行
    empty_word_rows = df[df['word'] == ''].index.tolist()
    # +2：1行是表头，行索引从0开始
    empty_word_rows_human = [i + 2 for i in empty_word_rows]

    # 检查meaning字段为空的行
    empty_meaning_rows = df[df['meaning'] == ''].index.tolist()
    empty_meaning_rows_human = [i + 2 for i in empty_meaning_rows]

    # 汇总错误信息
    error_msgs = []
    if empty_word_rows_human:
        error_msgs.append(f"word字段为空的行：{empty_word_rows_human}")
    if empty_meaning_rows_human:
        error_msgs.append(f"meaning字段为空的行：{empty_meaning_rows_human}")

    # 6. 返回校验结果
    if error_msgs:
        return False, f"{file_path} 内容校验失败，{'; '.join(error_msgs)}"
    else:
        return True, ""


def create_wordbook_csv(filename, encoding=DEFAULT_ENCODING):
    """
    新建csv并写入标准表头

    :param filename: 文件名 无需带后缀
    :param encoding: 编码格式
    :return: tuple (is_done: bool, error_msg: str)
             - is_valid: True=写入完成，False=写入失败
             - error_msg: 空字符串=无错误，否则为具体错误信息
    """

    # 去除首尾空格后检查是否为空
    filename_stripped = filename.strip()
    if not filename_stripped:
        return False, "文件名不能为空"

    # 增强文件名校验（禁止路径符+系统保留字符）
    # 定义禁止的字符 路径分隔符（/、\） + Windows系统保留字符（: * ? " < > |）
    forbidden_chars = r"[\\/:\*\?\"<>|]"
    # 检查是否包含禁止字符
    if re.search(forbidden_chars, filename_stripped):
        # 提取用户输入中的非法字符
        illegal_chars = re.findall(forbidden_chars, filename_stripped)
        # 去重并格式化提示
        unique_illegal = list(set(illegal_chars))
        return False, f"文件名 {filename_stripped} 包含非法字符：{unique_illegal}，禁止使用 / \ : * ? \" < > | 等字符"

    # 名称不能包含空格
    if " " in filename_stripped:
        return False, f"文件名 {filename_stripped} 包含空格，不允许创建,可用英文下划线代替"

    # 获取文件路径
    file_path = get_wordbook_csv_path(filename_stripped)

    # 检查文件是否已存在
    if check_file_exist(file_path):
        return False, f"文件名 {file_path} 已存在，无法重复创建"

    try:
        # 确保单词库文件夹存在 不存在则创建
        wordbooks_folder = os.path.dirname(file_path)
        if not os.path.exists(wordbooks_folder):
            os.makedirs(wordbooks_folder, exist_ok=True)

        # 创建空DataFrame并写入标准表头
        empty_df = pd.DataFrame(columns=STANDARD_CSV_HEADERS)
        empty_df.to_csv(
            file_path,
            encoding=encoding,
            index=False, # 不写入行索引
            header=True # 写入表头
        )

        return True, f"文件 {file_path} 创建成功"

    except Exception as e:
        return False, f"文件 {file_path} 创建失败，{str(e)}"

def delete_wordbook_csv(filename):
    """
    删除单词本

    :param filename: 文件名
    :return: tuple (is_done: bool, error_msg: str)
             - is_valid: True=删除完成，False=删除失败
             - error_msg: 空字符串=无错误，否则为具体错误信息
    """

    # 去除空格并检查空值
    filename_stripped = filename.strip()
    if not filename_stripped:
        return False, "单词本名称不能为空"

    # 禁止删除默认单词本
    if filename_stripped == DEFAULT_WORDBOOK:
        return False, f"禁止删除默认单词本（{DEFAULT_WORDBOOK}）"

    # 获取单词本文件路径
    file_path = get_wordbook_csv_path(filename_stripped)

    # 检查文件是否存在
    if not check_file_exist(file_path):
        return False, f"单词本文件不存在：{file_path}"

    # 执行删除操作
    try:
        os.remove(file_path)
        return True, f"单词本「{filename_stripped}」已成功删除（路径：{file_path}）"
    except PermissionError:
        return False, f"删除失败，无文件操作权限，或文件正在被其他程序占用（{file_path}）"
    except Exception as e:
        return False, f"删除单词本出错：{str(e)}"

def write_processed_csv(text, filename=DEFAULT_WORDBOOK, encoding=DEFAULT_ENCODING):
    """
    将**已经处理好的文本**写入csv
    存在性校验和格式校验是必须的，文件名输错会报错，留空则默认default

    :param text: 单词数据，支持两种格式：
                 1. 单条数据：字典（如{"word":"author", "phonetic":"/ˈɔːθə(r)/",...}）
                 2. 多条数据：列表包含多个字典
    :param filename: 文件名 无需带后缀
    :param encoding: 编码格式
    :return: tuple (is_done: bool, error_msg: str)
             - is_done: True=写入完成，False=写入失败
             - error_msg: 空字符串=无错误，否则为具体错误信息
    """

    # 缺少filename则为默认单词库 写在了函数定义
    # 去空格后检查
    filename_stripped = filename.strip()
    if not filename_stripped:
        filename_stripped = DEFAULT_WORDBOOK
    # 获取单词库路径
    file_path = get_wordbook_csv_path(filename_stripped)

    # 检查文件是否存在
    file_exists = os.path.exists(file_path)
    if file_exists:
        is_valid, error_msg = validate_csv_headers(file_path)
        if not is_valid:
            return False, f"文件格式校验失败，{error_msg}"
    else:
        return False, f"文件 {file_path} 不存在，无法写入数据"

    # text格式处理
    data_list = None
    if isinstance(text, dict):
        data_list = [text]  # 单条字典转列表
    elif isinstance(text, list):
        data_list = text
        # 校验列表元素都是字典
        if not all(isinstance(item, dict) for item in data_list):
            return False, "多条数据格式错误，列表中必须全是字典"
    else:
        return False, f"输入数据格式错误，仅支持字典/字典列表，当前类型为{type(text)}"

    # 数据处理 + 写入（重构为容错逻辑）
    try:
        # 读取已存在的合规文件
        final_df = pd.read_csv(file_path, encoding=encoding, dtype=str)

        # 成功数据列表 + 失败信息列表
        new_data = []  # 存储合规的单词数据
        fail_messages = []  # 存储失败单词的信息 用于提示
        existing_words = set(final_df['word'].astype(str).str.strip())  # 已存在的单词

        # 遍历所有待写入单词 容错逻辑：跳过错误数据，继续处理后续
        for idx, item in enumerate(data_list):
            row_num = idx + 1
            word_row = {col: "" for col in STANDARD_CSV_HEADERS}

            # 填充用户输入字段
            for key, value in item.items():
                if key in STANDARD_CSV_HEADERS:
                    word_row[key] = str(value).strip() if value is not None else ""

            # 容错 不直接return 收集错误后跳过
            # 校验必填字段
            if not word_row['word']:
                fail_messages.append(f"第{row_num}条：核心单词（word）不能为空")
                continue  # 跳过当前错误数据 处理下一条
            if not word_row['meaning']:
                fail_messages.append(f"第{row_num}条：单词释义（meaning）不能为空")
                continue

            # 校验单词唯一性
            current_word = word_row['word']
            if current_word in existing_words:
                fail_messages.append(f"第{row_num}条：单词「{current_word}」已存在，不允许重复")
                continue

            # 系统字段不再强制覆盖 优先使用用户输入
            # 1. review_count 用户传入则校验是否为数字 非法则用默认0
            try:
                # 先取用户传入的值（如果有且非空）
                user_review = item.get('review_count', '').strip()
                if user_review and user_review.isdigit():
                    word_row['review_count'] = user_review
                else:
                    word_row['review_count'] = "0" # 无合法值则用默认
            except:
                word_row['review_count'] = "0"

            # correct_count 同上
            try:
                user_correct = item.get('correct_count', '').strip()
                if user_correct and user_correct.isdigit():
                    word_row['correct_count'] = user_correct
                else:
                    word_row['correct_count'] = "0"
            except:
                word_row['correct_count'] = "0"

            # last_review 用户传入则用 无则为空字符串
            try:
                user_last_review = item.get('last_review', '').strip()
                word_row['last_review'] = user_last_review if user_last_review else ""
            except:
                word_row['last_review'] = ""

            # 合规数据加入列表 更新已存在单词集合
            new_data.append(word_row)
            existing_words.add(current_word)

        # 写入逻辑：有合规数据则写入
        success_count = len(new_data)
        fail_count = len(fail_messages)

        if success_count > 0:
            # 拼接合规数据并写入
            new_df = pd.DataFrame(new_data)
            final_df = pd.concat([final_df, new_df], ignore_index=True)
            final_df.to_csv(file_path, encoding=encoding, index=False, header=True)

        # 汇总成功/失败信息
        # 构建提示信息
        result_msg = f"共处理{success_count + fail_count}条数据，成功写入{success_count}条，失败{fail_count}条。"
        if fail_count > 0:
            result_msg += "\n失败详情：" + "；".join(fail_messages)

        # 有至少1条成功则为True 全失败则为False
        is_done = success_count > 0
        return is_done, result_msg

    except Exception as e:
        # 系统级错误（如文件权限、编码错误），整体写入失败
        return False, f"写入过程出现系统错误：{str(e)}"

def read_processed_csv(filename=DEFAULT_WORDBOOK, encoding=DEFAULT_ENCODING, validate=True, split_fields=True):
    """
    读取csv并完成预处理。

    :param filename: 文件名
    :param encoding: 编码格式
    :param validate: 是否校验csv存在性及格式
    :param split_fields: 是否自动拆分
    :return: pandas.DataFrame 处理后的单词数据
    """

    # 缺少filename则为默认单词库 写在了函数定义
    # 获取单词库路径
    file_path = get_wordbook_csv_path(filename)

    if validate:
        # 检查文件存在性及表头规范
        is_valid, error_msg = validate_csv_headers(file_path)
        if not is_valid:
            print(error_msg)
            return pd.DataFrame()

        # 检查数据合法性
        is_valid, error_msg = validate_wordbook_csv_content(file_path)
        if not is_valid:
            print(error_msg)
            return pd.DataFrame()

    try:
        # 读取CSV
        final_df = pd.read_csv(
            file_path,
            encoding=encoding,
            dtype={col: str for col in STANDARD_CSV_HEADERS} # 所有标准字段都存为字符串
        )

        # 空值预处理 核心融入DEFAULT_VALUES
        # 去除所有字段首尾空格
        for col in final_df.columns:
            final_df[col] = final_df[col].astype(str).str.strip()

        # 填充逻辑
        for col, default_val in DEFAULT_VALUES.items():
            if col in final_df.columns:
                # 把nan替换为默认值
                final_df[col] = final_df[col].fillna(default_val)
                # 把空字符串替换为默认
                final_df[col] = final_df[col].replace("", default_val)
                # 把可能的"nan"字符串也替换掉
                final_df[col] = final_df[col].replace("nan", default_val)

        # 复习/正确率数值化处理
        final_df["review_count_num"] = pd.to_numeric(final_df["review_count"], errors="coerce").fillna(0).astype(int)
        final_df["correct_count_num"] = pd.to_numeric(final_df["correct_count"], errors="coerce").fillna(0).astype(int)

        final_df["accuracy"] = final_df.apply(
            lambda row: calculate_accuracy_numeric(row["review_count_num"], row["correct_count_num"]),
            axis=1
        )

        # 拆分函数
        if split_fields:
            # 拆分释义
            final_df["meaning_split"] = final_df["meaning"].apply(split_word_meaning)

            # 拆分例句
            def get_example_split(row):
                # 调用现成的例句拆分函数
                example_result = split_word_example(row["example"], row["example_trans"])
                # 返回整合后的字典
                return {
                    "example": example_result["example_list"],
                    "example_trans": example_result["example_trans_list"]
                }

            final_df["example_split"] = final_df.apply(get_example_split, axis=1)

        # 重置索引
        final_df = final_df.reset_index(drop=True)

        return final_df

    except Exception as e:
        print(f"读取并预处理CSV失败，{str(e)}")
        return pd.DataFrame()


def get_wordbook_word_count(filename=DEFAULT_WORDBOOK, encoding=DEFAULT_ENCODING):
    """
    统计指定单词本的有效单词数量

    :param filename: 单词本名称
    :param encoding: 编码格式
    :return: int - 有效单词数量（异常时返回0）
    """
    # 获取文件路径
    file_path = get_wordbook_csv_path(filename.strip())

    # 文件不存在直接返回0
    if not check_file_exist(file_path):
        return 0

    # 读取并统计有效单词数量
    try:
        # 读取CSV（仅读取word列，提升性能）
        df = pd.read_csv(
            file_path,
            encoding=encoding,
            usecols=['word'],  # 只加载需要的列，减少内存占用
            dtype={'word': str}
        )

        # 过滤无效数据（空值、纯空格）
        df['word'] = df['word'].astype(str).str.strip()
        valid_words = df[df['word'] != '']  # 排除空单词

        # 返回有效单词数量
        return len(valid_words)

    except Exception as e:
        # 异常时返回0（避免UI层崩溃）
        print(f"统计单词本「{filename}」数量失败，{str(e)}")
        return 0

# 我背你走到最后 能不能不要回头 你紧紧地抱住我 说你不需要承诺
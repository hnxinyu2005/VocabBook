# utils/common_csv.py

import pandas as pd
import os

from word_constants import WORDBOOKS_FOLDER_NAME, DEFAULT_WORDBOOK, STANDARD_CSV_HEADERS, DEFAULT_ENCODING, DEFAULT_VALUES

# 两个拆分函数
from split_meaning import split_word_meaning
from split_example import split_word_example
# 计算正确率
from calculate_word_accuracy import calculate_accuracy_numeric

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

    is_valid = True
    error_msgs = ""

    if validate:
        # 检查文件存在性及表头规范
        is_valid, error_msg = validate_wordbook_csv(file_path)
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
        df = pd.read_csv(
            file_path,
            encoding=encoding,
            dtype={col: str for col in STANDARD_CSV_HEADERS} # 所有标准字段都存为字符串
        )

        # 空值预处理 核心融入DEFAULT_VALUES
        # 去除所有字段首尾空格
        for col in df.columns:
            df[col] = df[col].astype(str).str.strip()

        # 填充空值除word/meaning不能为空 其他字段用DEFAULT_VALUES填充
        for col, default_val in DEFAULT_VALUES.items():
            if col in df.columns:
                df[col] = df[col].replace("", default_val)  # 空字符串替换为友好提示

        # 复习/正确率数值化处理
        df["review_count_num"] = pd.to_numeric(df["review_count"], errors="coerce").fillna(0).astype(int)
        df["correct_count_num"] = pd.to_numeric(df["correct_count"], errors="coerce").fillna(0).astype(int)

        df["accuracy"] = df.apply(
            lambda row: calculate_accuracy_numeric(row["review_count_num"], row["correct_count_num"]),
            axis=1
        )

        # 拆分函数
        if split_fields:
            # 拆分释义
            df["meaning_split"] = df["meaning"].apply(split_word_meaning)

            # 拆分例句
            def get_example_split(row):
                # 调用现成的例句拆分函数
                example_result = split_word_example(row["example"], row["example_trans"])
                # 返回整合后的字典
                return {
                    "example": example_result["example_list"],
                    "example_trans": example_result["example_trans_list"]
                }

            df["example_split"] = df.apply(get_example_split, axis=1)

        # 重置索引
        df = df.reset_index(drop=True)

        return df

    except Exception as e:
        print(f"读取并预处理CSV失败，{str(e)}")
        return pd.DataFrame()

# 读内容测试
# 读内容测试
if __name__ == "__main__":
    print("=" * 80)
    print("📝 测试：读取并展示 wordbooks/default.csv 内容")
    print("=" * 80)

    # 1. 读取default.csv（先关闭校验，避免空值导致读取失败，方便看完整数据）
    print("\n1️⃣ 读取default.csv（关闭校验+开启字段拆分）：")
    df = read_processed_csv("default", validate=False, split_fields=True)

    if df.empty:
        print("❌ 读取失败：文件为空或不存在")
    else:
        print(f"✅ 读取成功，共 {len(df)} 条单词数据")

        # 2. 输出核心字段预览（替换nan为更友好的显示）
        print("\n2️⃣ 核心字段预览：")
        core_fields = ["word", "phonetic", "textbook", "unit", "accuracy"]
        # 替换DataFrame中的nan为空字符串，显示更友好
        df_display = df[core_fields].fillna("暂无数据")
        print(df_display.to_string(index=False))

        # 3. 输出单个单词的拆分示例（健壮版：优先找author，没有则用第一个单词）
        print("\n3️⃣ 字段拆分示例：")
        # 优先找author，不存在则取第一个单词
        target_word = "author"
        if (df["word"] == target_word).any():
            sample_row = df[df["word"] == target_word].iloc[0]
            print(f"👉 选中单词：{target_word}")
        else:
            sample_row = df.iloc[0]
            target_word = sample_row["word"]
            print(f"👉 未找到{target_word}，使用第一个单词：{target_word}")

        print(f"   释义拆分（meaning_split）：{sample_row['meaning_split']}")
        print(f"   例句拆分（example_split）：{sample_row['example_split']}")

        # 4. 输出正确率计算示例
        print("\n4️⃣ 正确率计算详情：")
        accuracy_fields = ["word", "review_count_num", "correct_count_num", "accuracy"]
        print(df[accuracy_fields].to_string(index=False))

        # 5. 验证空值填充（找第一个phonetic为空的单词）
        print("\n5️⃣ 空值填充验证：")
        # 找phonetic为空/na的单词
        empty_phonetic_row = df[df["phonetic"].isna() | (df["phonetic"] == "")].iloc[0] if len(
            df[df["phonetic"].isna() | (df["phonetic"] == "")]) > 0 else df.iloc[0]
        word_name = empty_phonetic_row["word"]
        phonetic_value = empty_phonetic_row["phonetic"]
        # 显示填充结果（替换nan为"未填充"）
        phonetic_display = phonetic_value if not pd.isna(phonetic_value) else "未填充"
        print(f"👉 单词「{word_name}」的phonetic：{phonetic_display}")

        print("\n" + "=" * 80)
        print("✅ 测试完成！")
        print("=" * 80)
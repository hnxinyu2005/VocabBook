import os
import pandas as pd
from datetime import datetime

def txt_to_csv(txt_file_path, csv_filename):
    """
    读取指定TXT文件，解析单词数据并写入CSV
    :param txt_file_path: TXT文件的绝对/相对路径（如 "words.txt"）
    :param csv_filename: 要写入的CSV文件名（如 "default.csv"）
    """
    # 定义路径
    # 获取utils文件夹的上级目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    wordbooks_dir = os.path.join(parent_dir, "wordbooks")
    target_csv = os.path.join(wordbooks_dir, csv_filename)

    # 定义字段顺序
    all_headers = [
        "word", "phonetic", "meaning", "example",
        "example_trans", "textbook", "unit",
        "review_count", "correct_count", "last_review"
    ]

    # 读取并解析TXT文件
    parsed_data = []
    try:
        with open(txt_file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line_num, line in enumerate(lines, 1):
                line = line.strip()  # 去除换行/空格
                if not line:
                    continue  # 跳过空行

                # 解析规则：按 "\" " 拆分（双引号+空格），去除首尾的双引号
                fields = [field.strip('"') for field in line.split('" "')]

                # 校验字段数量 必须是7个
                if len(fields) != 7:
                    print(f"第{line_num}行格式错误：字段数={len(fields)}，需为7个，已跳过")
                    continue

                # 处理留空字段 <null> → 空字符串
                fields = ["" if field == "<null>" else field for field in fields]

                # 补充系统字段：review_count=0, correct_count=0, last_review=当前时间
                fields.extend([
                    0,  # review_count
                    0,  # correct_count
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # last_review
                ])

                parsed_data.append(fields)
        print(f"成功解析TXT文件：共{len(parsed_data)}条有效单词数据")

    except FileNotFoundError:
        print(f"错误：未找到TXT文件 {txt_file_path}")
        return False
    except Exception as e:
        print(f"解析TXT文件失败：{str(e)}")
        return False

    # 写入CSV文件
    try:
        # 创建DataFrame并写入
        df = pd.DataFrame(parsed_data, columns=all_headers)
        # 追加数据
        df.to_csv(target_csv, mode="a", header=False, index=False, encoding="utf-8")
        print(f"✅ 已追加{len(parsed_data)}条数据到 {target_csv}")

        return True

    except Exception as e:
        print(f"写入CSV失败：{str(e)}")
        return False

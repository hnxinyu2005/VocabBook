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
    # 去除首尾空格
    filename_stripped = filename.strip()
    # 去除已有的.csv后缀
    if filename_stripped.lower().endswith(".csv"):
        filename_stripped = filename_stripped[:-4]
    # 拼接.csv后缀
    csv_filename = f"{filename_stripped}.csv"
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


def create_wordbook_csv(filename, encoding=DEFAULT_ENCODING):
    '''
    新建csv并写入标准表头

    :param filename: 文件名 无需带后缀
    :param encoding: 编码格式
    :return: tuple (is_done: bool, error_msg: str)
             - is_valid: True=写入完成，False=写入失败
             - error_msg: 空字符串=无错误，否则为具体错误信息
    '''

    # 去除首尾空格后检查是否为空
    filename_stripped = filename.strip()
    if not filename_stripped:
        return False, "文件名不能为空"

    # 名称不能包含空格
    if " " in filename_stripped:
        return False, f"文件名 {filename_stripped} 包含空格，不允许创建"

    # 获取文件路径
    file_path = get_wordbook_csv_path(filename_stripped)

    # 检查文件是否已存在
    if os.path.exists(file_path):
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
        return False, f"文件 {file_path} 床架你失败，{str(e)}"

def write_processed_csv(text, filename=DEFAULT_WORDBOOK, encoding=DEFAULT_ENCODING):
    '''
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
    '''

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
        is_valid, error_msg = validate_wordbook_csv(file_path)
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

            # 合规数据补充系统字段
            word_row['review_count'] = "0"
            word_row['correct_count'] = "0"
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
    '''
    读取csv并完成预处理。

    :param filename: 文件名
    :param encoding: 编码格式
    :param validate: 是否校验csv存在性及格式
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

'''
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

        # 2. 输出核心字段预览（替换nan为更友好的显示，总考察次数放正确率前）
        print("\n2️⃣ 核心字段预览：")
        # 调整字段顺序：总考察次数(review_count_num) → 正确率(accuracy)
        core_fields = ["word", "phonetic", "textbook", "unit", "review_count_num", "accuracy"]
        # 替换DataFrame中的nan为空字符串，显示更友好 + 重命名列名更易读
        df_display = df[core_fields].fillna("暂无数据").rename(
            columns={
                "review_count_num": "总考察次数",
                "accuracy": "正确率(%)",
                "phonetic": "音标",
                "textbook": "教材",
                "unit": "单元"
            }
        )
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

        # 4. 输出正确率计算示例（总考察次数放正确率前，重命名列名）
        print("\n4️⃣ 正确率计算详情：")
        accuracy_fields = ["word", "review_count_num", "correct_count_num", "accuracy"]
        df_accuracy = df[accuracy_fields].rename(
            columns={
                "review_count_num": "总考察次数",
                "correct_count_num": "正确次数",
                "accuracy": "正确率(%)"
            }
        )
        print(df_accuracy.to_string(index=False))

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
'''

'''
# 测试创建单词本
if __name__ == "__main__":
    print("=" * 80)
    print("📝 测试：创建单词本CSV文件")
    print("=" * 80)

    # 测试场景1：创建空名称的单词本（预期失败）
    print("\n1️⃣ 测试场景：创建空名称的单词本")
    is_done, error_msg = create_wordbook_csv("")
    print(f"   结果：{'✅ 成功' if is_done else '❌ 失败'}")
    print(f"   提示：{error_msg}")

    # 测试场景2：创建名称含空格的单词本（预期失败）
    print("\n2️⃣ 测试场景：创建名称含空格的单词本（test book）")
    is_done, error_msg = create_wordbook_csv("test book")
    print(f"   结果：{'✅ 成功' if is_done else '❌ 失败'}")
    print(f"   提示：{error_msg}")

    # 测试场景3：创建新的合法单词本（预期成功）
    test_book_name = "test_new_wordbook"
    print(f"\n3️⃣ 测试场景：创建新的合法单词本（{test_book_name}）")
    is_done, error_msg = create_wordbook_csv(test_book_name)
    print(f"   结果：{'✅ 成功' if is_done else '❌ 失败'}")
    print(f"   提示：{error_msg}")

    # 测试场景4：重复创建同一个单词本（预期失败）
    print(f"\n4️⃣ 测试场景：重复创建单词本（{test_book_name}）")
    is_done, error_msg = create_wordbook_csv(test_book_name)
    print(f"   结果：{'✅ 成功' if is_done else '❌ 失败'}")
    print(f"   提示：{error_msg}")

    # 可选：清理测试文件（创建成功后删除，避免残留）
    if os.path.exists(get_wordbook_csv_path(test_book_name)):
        os.remove(get_wordbook_csv_path(test_book_name))
        print(f"\n5️⃣ 清理测试文件：已删除 {test_book_name}.csv")

    print("\n" + "=" * 80)
    print("✅ 创建单词本测试完成！")
    print("=" * 80)
'''

# 测试写入单词数据（覆盖核心场景+全字段数据）
if __name__ == "__main__":
    print("=" * 80)
    print("📝 测试：写入单词数据到CSV（容错逻辑+全字段数据）")
    print("=" * 80)

    # 前置准备：创建测试用单词本（确保文件存在且格式合规）
    test_book_name = "test_write_wordbook"
    # 先删除残留的测试文件（避免影响）
    test_book_path = get_wordbook_csv_path(test_book_name)
    if os.path.exists(test_book_path):
        os.remove(test_book_path)
    # 创建新的测试单词本
    create_done, create_msg = create_wordbook_csv(test_book_name)
    print(f"🔧 前置准备：{create_msg}")

    # ---------------- 测试场景1：写入单条合法数据 ----------------
    print("\n1️⃣ 测试场景：写入单条合法单词数据")
    single_valid_data = {
        "word": "teacher",
        "phonetic": "/ˈtiːtʃə(r)/",
        "meaning": "n. 教师,老师;导师  v. 教书,授课",
        "example": "Our **teacher** always encourages us to think independently.",
        "example_trans": "我们的老师总是鼓励我们独立思考。",
        "textbook": "牛津《初阶英汉双解词典》",
        "unit": "Unit 6; p28"
    }
    is_done, error_msg = write_processed_csv(single_valid_data, test_book_name)
    print(f"   结果：{'✅ 成功' if is_done else '❌ 失败'}")
    print(f"   提示：{error_msg}")

    # ---------------- 测试场景2：写入多条混合错误数据（容错逻辑） ----------------
    print("\n2️⃣ 测试场景：写入多条混合错误数据（验证容错）")
    multi_mixed_data = [
        {"word": "", "meaning": "n. 学生", "phonetic": "/ˈstjuːdnt/"},  # 空word（失败）
        {"word": "student", "meaning": "", "phonetic": "/ˈstjuːdnt/"},  # 空meaning（失败）
        {"word": "teacher", "meaning": "n. 教师", "phonetic": "/ˈtiːtʃə(r)/"},  # 重复word（失败）
        {"word": "doctor", "meaning": "n. 医生,大夫;博士", "phonetic": "/ˈdɒktə(r)/",  # 合法数据（成功）
         "textbook": "新东方《四级词汇》", "unit": "Word List 2; p5"},
    ]
    is_done, error_msg = write_processed_csv(multi_mixed_data, test_book_name)
    print(f"   结果：{'✅ 部分成功' if is_done else '❌ 全部失败'}")
    print(f"   提示：{error_msg}")

    # ---------------- 测试场景3：写入错误格式数据（非字典/列表） ----------------
    print("\n3️⃣ 测试场景：写入错误格式数据（字符串）")
    wrong_format_data = "teacher,/ˈtiːtʃə(r)/,n. 教师"  # 非字典/列表
    is_done, error_msg = write_processed_csv(wrong_format_data, test_book_name)
    print(f"   结果：{'✅ 成功' if is_done else '❌ 失败'}")
    print(f"   提示：{error_msg}")

    # ---------------- 测试场景4：文件名留空（默认default.csv） ----------------
    print("\n4️⃣ 测试场景：文件名留空（默认写入default.csv）")
    # 先确保default.csv存在
    default_path = get_wordbook_csv_path(DEFAULT_WORDBOOK)
    if not os.path.exists(default_path):
        create_wordbook_csv(DEFAULT_WORDBOOK)
    # 写入单条合法数据到默认文件
    default_data = {"word": "engineer", "meaning": "n. 工程师,技师", "phonetic": "/ˌendʒɪˈnɪə(r)/"}
    is_done, error_msg = write_processed_csv(default_data, filename="")  # 文件名留空
    print(f"   结果：{'✅ 成功' if is_done else '❌ 失败'}")
    print(f"   提示：{error_msg}")

    # ---------------- 测试场景5：写入全字段完整数据（包含例句/翻译等所有字段） ----------------
    print("\n5️⃣ 测试场景：写入全字段完整数据（含例句、翻译、教材、单元）")
    full_field_data = {
        "word": "programmer",
        "phonetic": "/ˈprəʊɡræmə(r)/",
        "meaning": "n. 程序员,编程人员;程序设计器  v. 为...编写程序",
        "example": "The **programmer** spent 3 hours debugging the code; A good **programmer** must master multiple languages.",
        "example_trans": "这位程序员花了3小时调试代码；一名优秀的程序员必须掌握多种语言。",
        "textbook": "Python编程：从入门到实践",
        "unit": "Chapter 1; p15"
    }
    is_done, error_msg = write_processed_csv(full_field_data, test_book_name)
    print(f"   结果：{'✅ 成功' if is_done else '❌ 失败'}")
    print(f"   提示：{error_msg}")

    # ---------------- 测试场景6：验证全字段写入结果（读取完整数据） ----------------
    print("\n6️⃣ 验证全字段写入结果（展示所有字段）")
    df = read_processed_csv(test_book_name, validate=False)
    # 筛选出全字段测试数据
    full_data_row = df[df["word"] == "programmer"].iloc[0] if (df["word"] == "programmer").any() else None
    if full_data_row is not None:
        print("   全字段数据写入结果：")
        print(f"      单词：{full_data_row['word']}")
        print(f"      音标：{full_data_row['phonetic']}")
        print(f"      释义：{full_data_row['meaning']}")
        print(f"      例句：{full_data_row['example']}")
        print(f"      例句翻译：{full_data_row['example_trans']}")
        print(f"      教材：{full_data_row['textbook']}")
        print(f"      单元：{full_data_row['unit']}")
        print(f"      系统字段-考察次数：{full_data_row['review_count']}")
        print(f"      系统字段-正确次数：{full_data_row['correct_count']}")
    else:
        print("   ❌ 未找到全字段测试数据")

    # ---------------- 测试场景7：验证所有写入结果（读取文件） ----------------
    print("\n7️⃣ 验证所有写入结果（读取测试文件）")
    print(f"   测试文件中现有单词：{list(df['word'].dropna())}")

    # ---------------- 清理测试文件 ----------------
    print("\n🔧 清理测试文件")
    # 删除测试单词本
    if os.path.exists(test_book_path):
        os.remove(test_book_path)
        print(f"   已删除：{test_book_name}.csv")
    # 可选：删除default.csv中测试数据（如需保留默认文件可注释）
    if os.path.exists(default_path):
        df_default = pd.read_csv(default_path, encoding=DEFAULT_ENCODING)
        df_default = df_default[df_default['word'] != 'engineer']  # 移除测试数据
        df_default.to_csv(default_path, index=False, encoding=DEFAULT_ENCODING)
        print(f"   已清理default.csv中的测试数据")

    print("\n" + "=" * 80)
    print("✅ 写入单词数据测试完成！")
    print("=" * 80)
# tests/test_common_csv.py

import sys
import os
# 把项目根目录加入 sys.path，让测试能导入 utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 然后导入你的模块
from utils.common_csv import (
    get_wordbook_csv_path,
    create_wordbook_csv,
    validate_wordbook_csv,
    validate_wordbook_csv_content,
    write_processed_csv,
    read_processed_csv
)
from word_constants import WORDBOOKS_FOLDER_NAME, DEFAULT_WORDBOOK, DEFAULT_ENCODING, STANDARD_CSV_HEADERS
import pandas as pd

# 覆盖所有功能的完整测试代码
if __name__ == "__main__":
    print("=" * 80)
    print("📝 完整功能测试：utils/common_csv.py")
    print("=" * 80)

    # 前置准备：清理可能残留的测试文件
    test_book_name = "test_full_function"
    test_book_path = get_wordbook_csv_path(test_book_name)
    default_path = get_wordbook_csv_path(DEFAULT_WORDBOOK)
    for path in [test_book_path, default_path]:
        if os.path.exists(path):
            os.remove(path)

    # ---------------- 测试1：get_wordbook_csv_path 安全测试 ----------------
    print("\n1️⃣ 测试：get_wordbook_csv_path 路径安全防护")
    test_cases_path = [
        ("../etc/passwd", "路径遍历测试"),
        ("test/../hack", "相对路径测试"),
        ("test*book", "非法字符测试"),
        ("test book.csv", "带.csv后缀测试"),
        ("", "空文件名测试"),
        ("valid_book", "合法文件名测试")
    ]
    for input_name, desc in test_cases_path:
        result_path = get_wordbook_csv_path(input_name)
        base_dir = os.path.abspath(
            os.path.join(os.path.dirname(os.path.dirname(__file__)), WORDBOOKS_FOLDER_NAME)
        )
        is_safe = result_path.startswith(base_dir + os.sep)
        print(f"   {desc}：输入「{input_name}」→ 输出「{os.path.basename(result_path)}」→ {'✅ 安全' if is_safe else '❌ 危险'}")

    # ---------------- 测试2：create_wordbook_csv 文件创建测试 ----------------
    print("\n2️⃣ 测试：create_wordbook_csv 单词本创建")
    test_cases_create = [
        ("", "空文件名", False),
        ("test/../hack", "路径遍历", False),
        ("test*book", "非法字符", False),
        ("test book", "包含空格", False),
        (test_book_name, "合法文件名", True),
        (test_book_name, "重复创建", False)
    ]
    for input_name, desc, expect_success in test_cases_create:
        is_done, error_msg = create_wordbook_csv(input_name)
        status = "✅ 成功" if is_done else "❌ 失败"
        match_expect = "（符合预期）" if (is_done == expect_success) else "（不符合预期！）"
        print(f"   {desc}：{status}{match_expect}")
        if not is_done:
            print(f"      提示：{error_msg}")

    # ---------------- 测试3：validate_wordbook_csv 表头校验测试 ----------------
    print("\n3️⃣ 测试：validate_wordbook_csv 表头校验")
    # 3.1 测试文件不存在
    is_valid, error_msg = validate_wordbook_csv(get_wordbook_csv_path("not_exist"))
    print(f"   文件不存在：{'❌ 失败' if not is_valid else '✅ 成功'} → 提示：{error_msg}")
    # 3.2 测试正常文件
    is_valid, error_msg = validate_wordbook_csv(test_book_path)
    print(f"   正常文件：{'✅ 成功' if is_valid else '❌ 失败'} → 提示：{error_msg}")
    # 3.3 测试表头缺失（手动创建坏文件）
    bad_header_path = get_wordbook_csv_path("bad_header_test")
    pd.DataFrame(columns=["word", "bad_column"]).to_csv(bad_header_path, index=False, encoding=DEFAULT_ENCODING)
    is_valid, error_msg = validate_wordbook_csv(bad_header_path)
    print(f"   表头缺失：{'❌ 失败' if not is_valid else '✅ 成功'} → 提示：{error_msg}")
    os.remove(bad_header_path)

    # ---------------- 测试4：validate_wordbook_csv_content 内容校验测试 ----------------
    print("\n4️⃣ 测试：validate_wordbook_csv_content 内容校验")
    # 4.1 先写入坏数据
    bad_content_df = pd.DataFrame(columns=STANDARD_CSV_HEADERS)
    bad_content_df.loc[0] = ["", "test", "n. 测试", "", "", "", "", "0", "0", ""]  # word为空
    bad_content_df.loc[1] = ["test2", "test", "", "", "", "", "", "0", "0", ""]  # meaning为空
    bad_content_df.loc[2] = ["test3", "test", "n. 测试3", "", "", "", "", "0", "0", ""]  # 正常
    bad_content_df.to_csv(test_book_path, index=False, encoding=DEFAULT_ENCODING)
    # 4.2 校验
    is_valid, error_msg = validate_wordbook_csv_content(test_book_path)
    print(f"   内容校验：{'❌ 失败' if not is_valid else '✅ 成功'} → 提示：{error_msg}")
    # 4.3 恢复空文件
    pd.DataFrame(columns=STANDARD_CSV_HEADERS).to_csv(test_book_path, index=False, encoding=DEFAULT_ENCODING)

    # ---------------- 测试5：write_processed_csv 写入测试 ----------------
    print("\n5️⃣ 测试：write_processed_csv 单词写入（容错逻辑）")
    # 5.1 单条合法数据
    single_data = {"word": "teacher", "meaning": "n. 教师", "phonetic": "/ˈtiːtʃə(r)/"}
    is_done, error_msg = write_processed_csv(single_data, test_book_name)
    print(f"   单条合法数据：{'✅ 成功' if is_done else '❌ 失败'} → 提示：{error_msg}")
    # 5.2 多条混合错误数据
    multi_data = [
        {"word": "", "meaning": "n. 学生"},  # 空word
        {"word": "student", "meaning": ""},  # 空meaning
        {"word": "teacher", "meaning": "n. 教师"},  # 重复
        {"word": "doctor", "meaning": "n. 医生", "review_count": "10", "correct_count": "8", "last_review": "2026-03-12"}  # 合法+自定义系统字段
    ]
    is_done, error_msg = write_processed_csv(multi_data, test_book_name)
    print(f"   多条混合错误数据：{'✅ 部分成功' if is_done else '❌ 全部失败'} → 提示：{error_msg}")
    # 5.3 非法系统字段
    bad_sys_data = {"word": "engineer", "meaning": "n. 工程师", "review_count": "abc", "correct_count": "-5"}
    is_done, error_msg = write_processed_csv(bad_sys_data, test_book_name)
    print(f"   非法系统字段：{'✅ 成功（用默认值）' if is_done else '❌ 失败'} → 提示：{error_msg}")
    # 5.4 默认文件名
    create_wordbook_csv(DEFAULT_WORDBOOK)  # 先创建默认文件
    default_data = {"word": "default_word", "meaning": "n. 默认单词"}
    is_done, error_msg = write_processed_csv(default_data, filename="")
    print(f"   默认文件名：{'✅ 成功' if is_done else '❌ 失败'} → 提示：{error_msg}")

    # ---------------- 测试6：read_processed_csv 读取测试 ----------------
    print("\n6️⃣ 测试：read_processed_csv 单词读取")
    # 6.1 正常读取（开启校验+字段拆分）
    df = read_processed_csv(test_book_name, validate=True, split_fields=True)
    print(f"   正常读取：{'✅ 成功' if not df.empty else '❌ 失败'} → 共 {len(df)} 条数据")
    if not df.empty:
        print(f"      单词列表：{list(df['word'])}")
        # 验证系统字段
        doctor_row = df[df['word'] == 'doctor'].iloc[0]
        print(f"      自定义系统字段验证：doctor的review_count={doctor_row['review_count']}, correct_count={doctor_row['correct_count']}, last_review={doctor_row['last_review']}")
        # 验证字段拆分
        if 'meaning_split' in df.columns:
            print(f"      字段拆分验证：meaning_split存在")
    # 6.2 关闭校验读取
    df_no_validate = read_processed_csv(test_book_name, validate=False)
    print(f"   关闭校验读取：{'✅ 成功' if not df_no_validate.empty else '❌ 失败'}")

    # ---------------- 清理测试文件 ----------------
    print("\n🔧 清理测试文件")
    for path in [test_book_path, default_path]:
        if os.path.exists(path):
            os.remove(path)
            print(f"   已删除：{os.path.basename(path)}")

    print("\n" + "=" * 80)
    print("✅ 完整功能测试完成！")
    print("=" * 80)
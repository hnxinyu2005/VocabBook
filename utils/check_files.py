import os
import pandas as pd

def check_and_fix_wordbooks(csv_filename):
    """
    分步检查并修复wordbooks相关内容
    :param csv_filename: 要检查的CSV文件名（如 "default.csv"、"custom.csv"）
    """
    current_dir = os.path.dirname(os.path.abspath(__file__)) # 获取当前脚本所在目录
    parent_dir = os.path.dirname(current_dir) # 回退到上级目录

    # 定义核心参数
    wordbooks_dir = os.path.join(parent_dir, "wordbooks")  # 上级目录下的wordbooks
    target_csv = os.path.join(wordbooks_dir, csv_filename)  # 目标CSV路径
    standard_headers = [
        "word", "phonetic", "meaning", "example",
        "example_trans", "textbook", "unit",
        "review_count", "correct_count", "last_review"
    ]
    fix_log = []  # 记录修复操作

    # 文件夹
    print(f"检查wordbooks文件夹")
    if not os.path.exists(wordbooks_dir):
        os.makedirs(wordbooks_dir)
        fix_log.append(f"修复：创建了文件夹 {wordbooks_dir}")
        print(f"文件夹 {wordbooks_dir} 已创建")
    else:
        print(f"文件夹 {wordbooks_dir} 存在")

    # 目标CSV文件
    print(f"检查 {csv_filename} 文件")
    if not os.path.exists(target_csv):
        # 创建空文件并写入标准表头
        df_new = pd.DataFrame(columns=standard_headers)
        df_new.to_csv(target_csv, index=False, encoding="utf-8")
        fix_log.append(f"修复：创建了文件 {target_csv} 并写入标准表头")
        print(f"文件 {target_csv} 已创建，包含标准表头")
    else:
        print(f"文件 {target_csv} 存在")

    # 表头
    print(f"\n检查 {csv_filename} 表头")
    try:
        df = pd.read_csv(target_csv, encoding="utf-8")
        current_headers = df.columns.tolist()

        if current_headers != standard_headers:
            # 表头不匹配 → 重建文件（清空内容+写入标准表头）
            df_new = pd.DataFrame(columns=standard_headers)
            df_new.to_csv(target_csv, index=False, encoding="utf-8")
            fix_log.append(f"修复：表头不匹配，已重建 {target_csv} 并写入标准表头")
            print(f"表头不匹配（标准：{standard_headers} | 当前：{current_headers}）")
            print(f"重建文件并写入标准表头")
        else:
            print(f"表头完全匹配标准要求")
    except Exception as e:
        # 读取失败（文件损坏/编码错误）→ 重建文件
        df_new = pd.DataFrame(columns=standard_headers)
        df_new.to_csv(target_csv, index=False, encoding="utf-8")
        fix_log.append(f"修复：读取文件失败（{str(e)}），已重建 {target_csv} 并写入标准表头")
        print(f"读取文件失败：{str(e)}")
        print(f"重建文件并写入标准表头")

    # 最终结果汇总
    print("\n检查修复完成")
    if fix_log:
        print("修复操作记录：")
        for idx, log in enumerate(fix_log, 1):
            print(f"   {idx}. {log}")
    else:
        print("所有检查项均通过，无需任何修复")
    return True
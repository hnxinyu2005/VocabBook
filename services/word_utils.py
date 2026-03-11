# services/word_utils.py
def calculate_accuracy(review_count: int, correct_count: int) -> str:
    """计算正确率"""
    if review_count == 0:
        return "0%"
    accuracy = (correct_count / review_count) * 100
    return f"{accuracy:.1f}%"

def split_meaning(meaning: str) -> list[dict]:
    """拆分释义为词性列表"""

    pos_list = []

    # 空
    if not meaning:
        return pos_list

    # 拆分输入的释义文本
    meaning_parts = meaning.split()
    # 存储当前正在处理的词性和释义
    current_pos = ""
    current_trans = ""

    # 识别词性标记
    for part in meaning_parts:
        # 片段以“.”结尾且长度小于等于4判定为词性标记
        if part.endswith(".") and len(part) <= 4:
            # 如果已有未保存的词性 先把之前的存入列表
            if current_pos:
                pos_list.append({"pos": current_pos, "trans": current_trans.strip("; ")})
            # 更新当前词性为新识别的词性标记 重置释义文本
            current_pos = part
            current_trans = ""
        else:
            # 不是词性标记 拼接到当前释义文本中
            current_trans += " " + part

    # 添加最后一组
    if current_pos:
        pos_list.append({"pos": current_pos, "trans": current_trans.strip("; ")})

    return pos_list

def split_examples(example: str, example_trans: str) -> list[dict]:
    """拆分多例句"""
    examples = []

    # 都为空
    if not example and not example_trans:
        return [{"en": "暂无例句", "zh": "暂无翻译"}]

    # 拆分英文例句 按分号分割 去除每个例句两端的空格 若输入为空则返回空列表
    en_list = [e.strip() for e in example.split(";")] if example else []
    # 拆分中文翻译
    zh_list = [t.strip() for t in example_trans.split(";")] if example_trans else []

    # 确定最大长度
    max_len = max(len(en_list), len(zh_list), 1)

    # 补全缺失的例句/翻译
    en_list += ["暂无例句"] * (max_len - len(en_list))
    zh_list += ["暂无翻译"] * (max_len - len(zh_list))

    # 拼接
    for e, t in zip(en_list, zh_list):
        examples.append({"en": e, "zh": t})

    return examples
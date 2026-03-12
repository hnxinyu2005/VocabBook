# utils/split_meaning.py
from utils.constants import POS_MAX_LENGTH

def split_word_meaning(meaning):
    '''
    拆分单词释义字符串，提取词性和对应翻译。
    当前路径下的 README.md 写有详细规则。

    :param meaning: 释义字符串
    :return: list[dict]
    '''

    result = []
    # 输入为空返回空
    if not isinstance(meaning, str) or meaning.strip() == "":
        return result
    # 首尾去空格
    clean_meaning = meaning.strip()

    # 按两个空格拆分 识别不同词性
    single_pos_list = clean_meaning.split("  ")

    for single_pos_str in single_pos_list:
        # 按第一个空格拆分
        pos_trans_parts = single_pos_str.split(" ", 1)

        # 只有词性无翻译
        if len(pos_trans_parts) < 2:
            pos = single_pos_str.strip()
            trans_part = ""
        else:
            pos = pos_trans_parts[0].strip()
            trans_part = pos_trans_parts[1].strip()

        # 标准词性核验
        is_standard_pos = len(pos) <= POS_MAX_LENGTH and pos.endswith(".") and pos != ""
        if not is_standard_pos:
            continue

        # 拆分翻译部分
        trans_list = [t.strip() for t in trans_part.split(";") if t.strip()] if trans_part else [""]

        result.append({"pos": pos, "trans_list": trans_list})

    return result



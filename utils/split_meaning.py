# utils/split_meaning.py
from word_constants import POS_MAX_LENGTH

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

if __name__ == "__main__":
    # 测试用例1：核心场景（多词性+多意思+同意思多描述）
    test1 = "n. 著作家,作者;创始人  v. 写作"
    print("🔹 测试1（核心场景）：")
    print("输入：", test1)
    print("输出：", split_word_meaning(test1))
    print("预期：", [{"pos":"n.","trans_list":["著作家,作者","创始人"]}, {"pos":"v.","trans_list":["写作"]}])
    print("-" * 60)

    # 测试用例2：包含最长标准词性（modal.）
    test2 = "modal. 能够,可以;必须  adj. 开心的,快乐的"
    print("🔹 测试2（最长词性）：")
    print("输入：", test2)
    print("输出：", split_word_meaning(test2))
    print("预期：", [{"pos":"modal.","trans_list":["能够,可以","必须"]}, {"pos":"adj.","trans_list":["开心的,快乐的"]}])
    print("-" * 60)

    # 测试用例3：边界场景（只有词性无翻译）
    test3 = "prep.  "
    print("🔹 测试3（只有词性无翻译）：")
    print("输入：", test3)
    print("输出：", split_word_meaning(test3))
    print("预期：", [{"pos":"prep.","trans_list":[""]}])
    print("-" * 60)

    # 测试用例4：边界场景（输入为空/非字符串）
    test4_1 = ""
    test4_2 = None
    test4_3 = 123
    print("🔹 测试4（输入为空/非字符串）：")
    print("输入空字符串：", split_word_meaning(test4_1))  # 预期 []
    print("输入None：", split_word_meaning(test4_2))      # 预期 []
    print("输入数字：", split_word_meaning(test4_3))      # 预期 []
    print("-" * 60)

    # 测试用例5：非标准词性（会被过滤）
    test5 = "abc 作者  n. 创始人"
    print("🔹 测试5（非标准词性过滤）：")
    print("输入：", test5)
    print("输出：", split_word_meaning(test5))
    print("预期：", [{"pos":"n.","trans_list":["创始人"]}])

# utils/split_example.py

def split_word_example(example, example_trans):
    '''
    拆分单词例句和对应翻译字符串，保证例句与翻译列表长度一一对应。

    :param example: 单词例句原文字符串
    :param example_trans: 单词例句翻译字符串
    :return: 字符串列表
    '''

    result = {
        "example_list": [],
        "example_trans_list": []
    }
    # 处理例句输入 非字符串/空值转为空字符串 去首尾空格
    if not isinstance(example, str):
        clean_example = ""
    else:
        clean_example = example.strip()

    # 处理翻译输入 逻辑同上
    if not isinstance(example_trans, str):
        clean_trans = ""
    else:
        clean_trans = example_trans.strip()

    # 拆分例句 按英文分号分割 过滤空元素（如连续分号导致的空字符串）
    if clean_example == "":
        example_list = []
    else:
        # 拆分后对每个元素去首尾空格 过滤纯空格/空字符串的无效元素
        example_list = [item.strip() for item in clean_example.split(";") if item.strip() != ""]

    # 拆分翻译 逻辑同上
    if clean_trans == "":
        trans_list = []
    else:
        trans_list = [item.strip() for item in clean_trans.split(";") if item.strip() != ""]

    # 保证两个列表长度一致
    # 例句和翻译必须一一对应 短的列表补空字符串
    max_length = max(len(example_list), len(trans_list))

    # 对例句列表补空 长度不足max_length末尾补空
    example_list += [""] * (max_length - len(example_list))
    # 对翻译列表补空
    trans_list += [""] * (max_length - len(trans_list))

    # 组装
    result["example_list"] = example_list
    result["example_trans_list"] = trans_list

    return result
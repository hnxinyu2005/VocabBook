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

if __name__ == "__main__":
    # 测试用例1：核心场景（多例句+多翻译，含**标记）
    test1_example = "Our guest on today's \"Book Talk\" is John Black, the **author** of the new bestseller, Retire Early.;Another sentence with **author**."
    test1_trans = "我们今天的《图书访谈》栏目嘉宾是约翰·布莱克，他是畅销新书《提前退休》的作者。;另一个包含作者的句子。"
    print("🔹 测试1（核心场景）：")
    print("输入例句：", test1_example)
    print("输入翻译：", test1_trans)
    print("输出结果：", split_word_example(test1_example, test1_trans))
    print("预期结果：", {
        "example_list": [
            "Our guest on today's \"Book Talk\" is John Black, the **author** of the new bestseller, Retire Early.",
            "Another sentence with **author**."
        ],
        "example_trans_list": [
            "我们今天的《图书访谈》栏目嘉宾是约翰·布莱克，他是畅销新书《提前退休》的作者。",
            "另一个包含作者的句子。"
        ]
    })
    print("-" * 80)

    # 测试用例2：边界场景（例句多/翻译少）
    test2_example = "句1;句2;句3"
    test2_trans = "译1;译2"
    print("🔹 测试2（例句多/翻译少）：")
    print("输入例句：", test2_example)
    print("输入翻译：", test2_trans)
    print("输出结果：", split_word_example(test2_example, test2_trans))
    print("预期结果：", {
        "example_list": ["句1", "句2", "句3"],
        "example_trans_list": ["译1", "译2", ""]
    })
    print("-" * 80)

    # 测试用例3：边界场景（输入为空/非字符串）
    test3_example = None
    test3_trans = ""
    print("🔹 测试3（输入为空/非字符串）：")
    print("输入例句：", test3_example)
    print("输入翻译：", test3_trans)
    print("输出结果：", split_word_example(test3_example, test3_trans))
    print("预期结果：", {"example_list": [], "example_trans_list": []})
    print("-" * 80)

    # 测试用例4：边界场景（含空元素的拆分）
    test4_example = "  句1;;句2  ;  "  # 含连续分号和首尾空格
    test4_trans = "  译1;;译2  ;  "
    print("🔹 测试4（含空元素拆分）：")
    print("输入例句：", test4_example)
    print("输入翻译：", test4_trans)
    print("输出结果：", split_word_example(test4_example, test4_trans))
    print("预期结果：", {
        "example_list": ["句1", "句2"],
        "example_trans_list": ["译1", "译2"]
    })

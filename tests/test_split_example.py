# tests/test_split_example.py

from utils.text.split_example import split_word_example

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

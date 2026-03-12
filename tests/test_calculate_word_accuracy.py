# tests/test_calculate_word_accuracy.py

from utils.math.calculate_word_accuracy import calculate_word_accuracy

if __name__ == "__main__":
    # 测试用例1：核心场景（正常计算-整除）
    test1_review = 10
    test1_correct = 5
    print("🔹 测试1（核心场景-整除）：")
    print("输入：review_count={}, correct_count={}".format(test1_review, test1_correct))
    print("输出结果：", calculate_word_accuracy(test1_review, test1_correct))
    print("预期结果：", "50.0%")
    print("-" * 80)

    # 测试用例2：核心场景（正常计算-非整除）
    test2_review = 3
    test2_correct = 1
    print("🔹 测试2（核心场景-非整除）：")
    print("输入：review_count={}, correct_count={}".format(test2_review, test2_correct))
    print("输出结果：", calculate_word_accuracy(test2_review, test2_correct))
    print("预期结果：", "33.3%")
    print("-" * 80)

    # 测试用例3：边界场景（总次数为0）
    test3_review = 0
    test3_correct = 5
    print("🔹 测试3（边界场景-总次数为0）：")
    print("输入：review_count={}, correct_count={}".format(test3_review, test3_correct))
    print("输出结果：", calculate_word_accuracy(test3_review, test3_correct))
    print("预期结果：", "0.0%")
    print("-" * 80)

    # 测试用例4：边界场景（正确次数为0）
    test4_review = 5
    test4_correct = 0
    print("🔹 测试4（边界场景-正确次数为0）：")
    print("输入：review_count={}, correct_count={}".format(test4_review, test4_correct))
    print("输出结果：", calculate_word_accuracy(test4_review, test4_correct))
    print("预期结果：", "0.0%")
    print("-" * 80)

    # 测试用例5：异常场景（传入非数字字符串）
    test5_review = "abc"
    test5_correct = 10
    print("🔹 测试5（异常场景-非数字字符串）：")
    print("输入：review_count={}, correct_count={}".format(test5_review, test5_correct))
    print("输出结果：", calculate_word_accuracy(test5_review, test5_correct))
    print("预期结果：", "0.0%")
    print("-" * 80)

    # 测试用例6：异常场景（传入空值None）
    test6_review = None
    test6_correct = 5
    print("🔹 测试6（异常场景-空值None）：")
    print("输入：review_count={}, correct_count={}".format(test6_review, test6_correct))
    print("输出结果：", calculate_word_accuracy(test6_review, test6_correct))
    print("预期结果：", "0.0%")
    print("-" * 80)
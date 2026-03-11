# utils/calculate_word_accuracy.py
# 计算单词正确率

def calculate_word_accuracy(review_count, correct_count):
    """
    计算单词正确率 返回带一位小数的百分比字符串

    :param review_count: 总考察次数
    :param correct_count: 正确次数
    :return: 正确率字符串
    """
    try:
        review_count = int(review_count) if review_count else 0
        correct_count = int(correct_count) if correct_count else 0
    except (ValueError, TypeError):
        # 传入错误返回 0
        return "0.0%"

    # 考察次数为 0 返回 0
    if review_count == 0:
        return "0.0%"

    accuracy = (correct_count / review_count) * 100
    return f"{accuracy:.1f}%"
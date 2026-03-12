# utils/calculate_word_accuracy.py

# 计算单词正确率
def calculate_accuracy_numeric(review_count, correct_count):
    '''
    内部辅助函数：计算单词正确率,返回纯数值，保留1位小数
    供DataFrame批量计算使用

    :param review_count: int 总考察次数
    :param correct_count: int 正确次数
    :return: float 正确率数值
    '''
    try:
        review_count = int(review_count) if review_count else 0
        correct_count = int(correct_count) if correct_count else 0
    except (ValueError, TypeError):
        return 0.0

    if review_count == 0:
        return 0.0

    accuracy = (correct_count / review_count) * 100
    return round(accuracy, 1)

def calculate_word_accuracy(review_count, correct_count):
    """
    计算单词正确率 返回带一位小数的百分比字符串

    :param review_count: 总考察次数
    :param correct_count: 正确次数
    :return: 正确率字符串
    """
    accuracy_num = calculate_accuracy_numeric(review_count, correct_count)
    return f"{accuracy_num:.1f}%"
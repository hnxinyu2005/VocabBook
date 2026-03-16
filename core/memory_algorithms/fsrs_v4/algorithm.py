# core/memory_algorithms/fsrs_v4/algorithm.py

from core.memory_algorithms.fsrs_v4.constants import FSRSReviewRating, FSRS_DEFAULT_RATING, FSRS_V4_DEFAULT_PARAMS

def calculate_initial_stability(rating: FSRSReviewRating = FSRS_DEFAULT_RATING) -> float:
    """计算首次评分后的初始稳定性"""
    w = FSRS_V4_DEFAULT_PARAMS
    initial_stability = w[rating.value - 1]
    return initial_stability

def calculate_initial_difficulty(rating: FSRSReviewRating = FSRS_DEFAULT_RATING) -> float:
    """首次评分后的初始难度"""
    w = FSRS_V4_DEFAULT_PARAMS
    w4 = w[4]
    w5 = w[5]
    G = rating.value
    initial_difficulty = w4 - (G - 3) * w5
    initial_difficulty = max(1.0, min(10.0, initial_difficulty)) # 难度要求在1~10之间
    return round(initial_difficulty, 2)

def calculate_updated_difficulty(current_difficulty: float, rating: FSRSReviewRating, w=FSRS_V4_DEFAULT_PARAMS) -> float:
    """
    计算复习后的新难度

    :param current_difficulty: 当前难度
    :param rating: 本次复习的评分等级
    :param w: 参数
    :return: 新难度 2位小数 取值范围1到10
    """
    w6 = w[6]
    w7 = w[7]
    d0_3 = w[4]

    # 计算临时难度
    G = rating.value
    temp_d = current_difficulty - w6 * (G - 3)

    # 均值回归修正和取值范围
    d_prime = w7 * d0_3 + (1 - w7) * temp_d
    d_prime = max(1.0, min(10.0, d_prime))

    return round(d_prime, 2)

def calculate_retrievability(days_since_review: float, stability: float) -> float:
    """
    计算上次复习t天后的可见索性

    :param days_since_review: 自上次复习的天数
    :param stability: 单词当前稳定性
    :return: 可检索性
    """
    stability = max(0.01, stability) # 避免除以0（稳定性最小为0.01）

    denominator = 1 + (days_since_review / (9 * stability))
    retrievability = 1 / denominator

    return round(retrievability, 3)

def calculate_review_interval(stability: float, target_recall: float = 0.9) -> float:
    """
    计算下次复习间隔

    :param stability: 当前单词稳定性
    :param target_recall: 目标回忆率
    :return: 下次复习间隔（天 2位小数）
    """
    target_recall = max(0.1, min(0.99, target_recall)) # 避免目标回忆率非法

    interval = 9 * stability * (1 / target_recall - 1)
    interval = max(0.1, interval) # 间隔最小为0.1天

    return round(interval, 2)
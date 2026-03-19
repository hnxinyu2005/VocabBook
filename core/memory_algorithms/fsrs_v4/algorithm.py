# core/memory_algorithms/fsrs_v4/algorithm.py

import math
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

def calculate_updated_stability_success(
    current_difficulty: float,
    current_stability: float,
    retrievability: float,
    rating: FSRSReviewRating,
    w=FSRS_V4_DEFAULT_PARAMS
) -> float:
    """
    计算复习成功后的新稳定性

    :param current_difficulty: 单词当前难度
    :param current_stability: 单词当前稳定性
    :param retrievability: 复习时的可见索性
    :param rating: 复习评分
    :param w: 官方参数
    :return: 复习后的新稳定性（大于等于原稳定性，2位小数）
    """
    # 防错处理
    current_stability = max(0.01, current_stability)  # 稳定性不能为0
    current_difficulty = max(1.0, min(10.0, current_difficulty))  # 难度约束1~10
    retrievability = max(0.0, min(1.0, retrievability))  # 可检索性约束0~1

    w8 = w[8]
    w9 = w[9]
    w10 = w[10]
    w15 = w[15]
    w16 = w[16]

    exp_w8 = math.exp(w8) # 计算基础指数项 e^w8
    difficulty_term = 11 - current_difficulty # 乘以难度修正项 (11 - D)
    stability_decay_term = current_stability ** (-w9) # 乘以稳定性衰减项 S^(-w9)
    retrievability_term = math.exp(w10 * (1 - retrievability)) - 1 # 计算可检索性影响项 e^(w10*(1-R)) - 1
    core_factor = exp_w8 * difficulty_term * stability_decay_term * retrievability_term # 合并核心增幅因子（前4步相乘）
    # 按评分添加系数
    if rating == FSRSReviewRating.HARD:  # G=2
        core_factor *= w15
    elif rating == FSRSReviewRating.EASY:  # G=4
        core_factor *= w16
    # G=3（GOOD）不处理
    new_stability = current_stability * (core_factor + 1) # 加1后乘以原稳定性，得到新稳定性
    new_stability = max(current_stability, new_stability) # 复习成功后稳定性≥原稳定性（SInc≥1）

    return round(new_stability, 2)
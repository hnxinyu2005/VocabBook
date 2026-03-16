# core/memory_algorithms/fsrs_v4/constants.py
from enum import IntEnum

class FSRSReviewRating(IntEnum):
    AGAIN = 1
    HARD = 2
    GOOD = 3
    EASY = 4

# 前端展示值 低版本不兼容StrEnum
FSRS_REVIEW_RATING_TEXT = {
    FSRSReviewRating.AGAIN: "完全不认识",
    FSRSReviewRating.HARD: "回忆困难",
    FSRSReviewRating.GOOD: "认识",
    FSRSReviewRating.EASY: "完全掌握"
}

# 用户不给定初始值则赋默认值
FSRS_DEFAULT_RATING = FSRSReviewRating.HARD

# 官方默认17个参数
FSRS_V4_DEFAULT_PARAMS = [
    0.4, #w_1
    0.6, #w_2
    2.4, #w_3
    5.8, #w_4
    4.93, #w_5
    0.94, #w_6
    0.86, #w_7
    0.01, #w_8
    1.49, #w_9
    0.14, #w_10
    0.94, #w_11
    2.18, #w_12
    0.05, #w_13
    0.34, #w_14
    1.26, #w_15
    0.29, #w_16
    2.61 #w_17
]
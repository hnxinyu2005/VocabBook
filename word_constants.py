# services/word_constants.py

# 单词文件夹
WORDBOOKS_FOLDER_NAME = "wordbooks"
# 默认单词库文件名
DEFAULT_WORDBOOK = "default.csv"

# 标准CSV表头
STANDARD_CSV_HEADERS = [
    "word", "phonetic", "meaning", "example", "example_trans",
    "textbook", "unit", "review_count", "correct_count", "last_review"
]

DEFAULT_ENCODING = "utf-8"

# 空值默认常量字典
DEFAULT_VALUES = {
    "phonetic": "未写入音标",
    "example": "未写入例句",
    "example_trans": "未写入例句翻译",
    "textbook": "未写入来源",
    "unit": "未写入单元信息",
    "last_review": "没有考察记录"
}

# 词性标记最大长度
POS_MAX_LENGTH = 6
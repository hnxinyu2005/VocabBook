# services/word_constants.py

# 单词文件夹（不可修改）
WORDBOOKS_FOLDER_NAME = "wordbooks"
# 默认单词库文件名
DEFAULT_WORDBOOK = "default.csv"

# 标准CSV表头
STANDARD_CSV_HEADERS = [
    "word", "phonetic", "meaning", "example", "example_trans",
    "textbook", "unit", "review_count", "correct_count", "last_review"
]

# 默认兜底文本
# 音标空值默认
DEFAULT_PHONETIC = "未写入音标"
# 例句空值默认
DEFAULT_EXAMPLE = "未写入例句"
# 例句翻译空值默认
DEFAULT_EXAMPLE_TRANS = "未写入例句翻译"
# 教材来源空值默认
DEFAULT_TEXTBOOK = "未写入来源"
# 单元信息空值默认
DEFAULT_UNIT = "未写入单元信息"
# 考察记录空值默认
DEFAULT_LAST_REVIEW = "没有考察记录"

# 词性标记最大长度
POS_MAX_LENGTH = 4
# app/tk/components/main_menu/right_panel/config.py
"""右侧面板样式/常量配置（解耦硬编码）"""

# 颜色配置（匹配左侧配色）
COLORS = {
    "bg_white": "white",
    "title": "#2c3e50",       # 左侧主背景色
    "content": "#34495e",     # 左侧功能条默认色
    "link": "#2980b9",        # 左侧功能条选中色
    "success": "#148f77"      # 左侧欢迎条选中色
}

# 字体配置
FONTS = {
    "title": ("微软雅黑", 24, "bold"),
    "content": ("微软雅黑", 12),
    "tip": ("微软雅黑", 10),
    "placeholder": ("微软雅黑", 16)
}

# 间距配置
PADDING = {
    "container": (60, 40),    # 内容容器上下左右间距
    "title": (0, 20),         # 标题上下间距
    "intro": (0, 20),         # 简介上下间距
    "link_tip": (5, 0)        # 复制提示上下间距
}

# 其他常量
WRAP_LENGTH = 600             # 文本换行宽度
GITHUB_URL = "https://github.com/hnxinyu2005/VocabBook"
GITHUB_TEXT = f"项目GitHub地址：{GITHUB_URL}"
WELCOME_TITLE = "欢迎使用 VocabBook"
INTRO_TEXT = """项目简介：

本项目是一款轻量级桌面单词本学习工具，核心服务于习惯用纸质书籍记单词的朋友们。

·支持全自定义单词库：可按纸质书章节、学习主题等维度自主录入、管理单词，精准匹配个人学习进度；

·主打高效轻量化体验：本地运行无广告，聚焦单词自测、错题复盘等核心功能，快速巩固纸质书记忆的单词，弥补纸质记词 “复习不便、无即时反馈” 的不足；

·交互极简，无需复杂操作，让用户专注于单词记忆本身，是纸质背词场景下的便捷辅助工具。
"""
BOOK_PLACEHOLDER = "我的单词本功能正在开发中..."
SETTING_PLACEHOLDER = "设置功能正在开发中..."
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
    "container": (40, 40),    # 内容容器上下左右间距
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
VocabBook 是一款基于 Python 开发的轻量级桌面单词本学习工具，专注于简洁、高效的单词记忆体验。
单词库全自定义，特别适合使用纸质书籍记单词但需要电子化自测、巩固记忆效果的用户。"""
BOOK_PLACEHOLDER = "我的单词本功能正在开发中..."
SETTING_PLACEHOLDER = "设置功能正在开发中..."
# app/tk/components/main_menu/config.py

#左侧面板配置常量
# 颜色配置
BAR_COLORS = {
    "welcome_normal": "#1abc9c",    # 欢迎条默认色
    "welcome_hover": "#16a085",     # 欢迎条悬浮色
    "welcome_selected": "#148f77",  # 欢迎条选中色
    "func_normal": "#34495e",       # 功能条默认色
    "func_hover": "#4a69bd",        # 功能条悬浮色
    "func_selected": "#2980b9"      # 功能条选中色
}

# 尺寸配置
BAR_SIZES = {
    "welcome_height": 50,           # 欢迎条高度
    "func_height": 50,              # 功能条高度
    "bar_padx": 0,                  # 蓝条左右内边距
    "bar_pady": 2,                  # 蓝条上下间距
    "func_container_pady": 10       # 功能条容器上下间距
}

# 字体配置
BAR_FONTS = {
    "welcome": ("微软雅黑", 12, "bold"),  # 欢迎条字体
    "func": ("微软雅黑", 11, "bold")      # 功能条字体
}

LEFT_PANEL_WIDTH_PERCENT = 0.25  # 左侧宽度占窗口总宽度的x
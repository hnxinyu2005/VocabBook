# app/tk/components/main_menu/__init__.py
"""主菜单组件包：对外统一导出左右面板创建函数"""
from .left_panel import main  # 左侧面板（已拆分到left_panel子包）
from .right_panel import create_right_panel  # 右侧面板（通过right_panel子包导出）
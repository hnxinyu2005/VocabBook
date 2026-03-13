# app/tk/components/main_menu/right_panel/main.py
"""右侧面板入口"""
import tkinter as tk
from .base_panel import BaseRightPanel
from .welcome_panel import WelcomePanel
from .book_panel import BookPanel
from .setting_panel import SettingPanel


def create_right_panel(parent: tk.Frame, width: int) -> tuple[tk.Frame, callable]:
    """
    创建右侧面板
    :param parent: 父容器
    :param width: 右侧面板宽度
    :return: 右侧面板frame + 内容切换函数
    """
    # 初始化基础面板
    base_panel = BaseRightPanel(parent, width)

    # 注册所有面板
    base_panel.register_panel("欢迎使用VocabBook", WelcomePanel)
    base_panel.register_panel("我的单词本", BookPanel)
    base_panel.register_panel("设置", SettingPanel)

    # 初始化显示欢迎面板
    base_panel.switch_content("欢迎使用VocabBook")

    # 返回主框架和切换函数
    return base_panel.main_frame, base_panel.switch_content
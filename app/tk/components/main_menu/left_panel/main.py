# app/tk/components/main_menu/main.py
"""左侧面板主文件"""
import tkinter as tk
from app.tk.components.main_menu.left_panel.func_bar import FuncBar
from app.tk.components.main_menu.left_panel.config import BAR_SIZES


def create_left_panel(parent: tk.Frame, width: int, click_callback: callable = None) -> tk.Frame:
    """
    创建左侧面板
    :param parent: 父容器
    :param width: 左侧面板宽度
    :param click_callback: 蓝条点击回调函数
    :return: 左侧面板frame
    """
    # 左侧主框架
    left_frame = tk.Frame(parent, bg="#2c3e50", width=width)
    left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)
    left_frame.pack_propagate(False)

    # 全局选中条引用（用列表实现可变对象共享）
    selected_bar_ref = [None]

    # 创建欢迎条（默认选中）
    welcome_bar = FuncBar(
        left_frame,
        "欢迎使用VocabBook",
        is_welcome=True,
        selected_bar_ref=selected_bar_ref,
        click_callback=click_callback  # 传递回调
    )
    welcome_bar.set_selected()

    # 创建功能条容器
    func_container = tk.Frame(left_frame, bg="#2c3e50")
    func_container.pack(fill=tk.X, padx=0, pady=BAR_SIZES["func_container_pady"])

    # 创建功能条
    book_bar = FuncBar(
        func_container,
        "我的单词本",
        is_welcome=False,
        selected_bar_ref=selected_bar_ref,
        click_callback=click_callback
    )
    setting_bar = FuncBar(
        func_container,
        "设置",
        is_welcome=False,
        selected_bar_ref=selected_bar_ref,
        click_callback=click_callback
    )

    return left_frame
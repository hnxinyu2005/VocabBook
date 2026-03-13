# app/tk/components/main_menu/left_panel.py
"""左侧面板主文件（仅布局构建）"""
import tkinter as tk
from .func_bar import FuncBar
from .config import BAR_SIZES

def create_left_panel(parent: tk.Frame, width: int) -> tk.Frame:
    """创建左侧面板（解耦后仅负责布局）"""
    # 左侧主框架
    left_frame = tk.Frame(parent, bg="#2c3e50", width=width)
    left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)
    left_frame.pack_propagate(False)

    # 全局选中条引用（用列表实现可变对象共享）
    selected_bar_ref = [None]

    # 创建欢迎条（默认选中）
    welcome_bar = FuncBar(left_frame, "欢迎使用VocabBook", is_welcome=True, selected_bar_ref=selected_bar_ref)
    welcome_bar.set_selected()

    # 创建功能条容器
    func_container = tk.Frame(left_frame, bg="#2c3e50")
    func_container.pack(fill=tk.X, padx=0, pady=BAR_SIZES["func_container_pady"])

    # 创建功能条
    book_bar = FuncBar(func_container, "我的单词本", is_welcome=False, selected_bar_ref=selected_bar_ref)
    setting_bar = FuncBar(func_container, "设置", is_welcome=False, selected_bar_ref=selected_bar_ref)

    return left_frame
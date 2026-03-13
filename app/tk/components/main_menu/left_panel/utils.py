# app/tk/components/main_menu/utils.py

import tkinter as tk
from .config import LEFT_PANEL_WIDTH_PERCENT

# 左侧面板通用工具函数
def update_bar_color(bar: tk.Frame, color: str) -> None:
    """统一更新蓝条和内部Label的背景色"""
    bar.config(bg=color)
    for child in bar.winfo_children():
        if isinstance(child, tk.Label):
            child.config(bg=color)

def calculate_left_width(window_width: int) -> int:
    """根据窗口宽度计算左侧面板宽度（按百分比）"""
    return int(window_width * LEFT_PANEL_WIDTH_PERCENT)
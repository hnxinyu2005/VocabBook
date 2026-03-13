# app/tk/components/main_menu/utils.py


import tkinter as tk

# 左侧面板通用工具函数
def update_bar_color(bar: tk.Frame, color: str) -> None:
    """统一更新蓝条和内部Label的背景色"""
    bar.config(bg=color)
    for child in bar.winfo_children():
        if isinstance(child, tk.Label):
            child.config(bg=color)
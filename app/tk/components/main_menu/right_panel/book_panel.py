# app/tk/components/main_menu/right_panel/book_panel.py
"""我的单词本面板（单一职责：仅处理单词本内容）"""
import tkinter as tk
from .config import COLORS, FONTS, BOOK_PLACEHOLDER

class BookPanel:
    def __init__(self, parent: tk.Frame):
        self.parent = parent

    def render(self) -> None:
        """渲染单词本占位内容"""
        tip_label = tk.Label(
            self.parent,
            text=BOOK_PLACEHOLDER,
            bg=COLORS["bg_white"],
            fg=COLORS["content"],
            font=FONTS["placeholder"]
        )
        tip_label.pack(expand=True)
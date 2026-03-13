# app/tk/components/main_menu/right_panel/setting_panel.py
"""设置面板"""
import tkinter as tk
from .config import COLORS, FONTS, SETTING_PLACEHOLDER

class SettingPanel:
    def __init__(self, parent: tk.Frame):
        self.parent = parent

    def render(self) -> None:
        """渲染设置占位内容"""
        tip_label = tk.Label(
            self.parent,
            text=SETTING_PLACEHOLDER,
            bg=COLORS["bg_white"],
            fg=COLORS["content"],
            font=FONTS["placeholder"]
        )
        tip_label.pack(expand=True)
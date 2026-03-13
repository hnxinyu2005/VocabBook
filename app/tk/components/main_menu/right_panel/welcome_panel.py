# app/tk/components/main_menu/right_panel/welcome_panel.py
"""欢迎面板"""
import tkinter as tk
from .config import COLORS, FONTS, PADDING, WRAP_LENGTH, WELCOME_TITLE, INTRO_TEXT, GITHUB_TEXT, GITHUB_URL

class WelcomePanel:
    def __init__(self, parent: tk.Frame):
        self.parent = parent  # 内容容器

    def render(self) -> None:
        """渲染欢迎面板所有内容"""
        self._render_title()
        self._render_intro()
        self._render_github_link()

    def _render_title(self) -> None:
        """渲染欢迎标题"""
        title_label = tk.Label(
            self.parent,
            text=WELCOME_TITLE,
            bg=COLORS["bg_white"],
            fg=COLORS["title"],
            font=FONTS["title"]
        )
        title_label.pack(anchor="w", pady=PADDING["title"])

    def _render_intro(self) -> None:
        """渲染项目简介"""
        intro_label = tk.Label(
            self.parent,
            text=INTRO_TEXT,
            bg=COLORS["bg_white"],
            fg=COLORS["content"],
            font=FONTS["content"],
            justify="left",
            wraplength=WRAP_LENGTH
        )
        intro_label.pack(anchor="w", pady=PADDING["intro"])

    def _render_github_link(self) -> None:
        """渲染GitHub链接+复制交互"""
        link_label = tk.Label(
            self.parent,
            text=GITHUB_TEXT,
            bg=COLORS["bg_white"],
            fg=COLORS["link"],
            font=FONTS["content"],
            cursor="hand2"
        )
        link_label.pack(anchor="w")
        # 绑定复制交互
        link_label.bind("<Button-1>", self._copy_github_url)

    def _copy_github_url(self, _) -> None:
        """复制GitHub地址（纯业务逻辑）"""
        self.parent.clipboard_clear()
        self.parent.clipboard_append(GITHUB_URL)
        # 渲染复制成功提示
        self._render_copy_tip()

    def _render_copy_tip(self) -> None:
        """渲染复制成功提示"""
        tip_label = tk.Label(
            self.parent,
            text="地址已复制到剪贴板！",
            bg=COLORS["bg_white"],
            fg=COLORS["success"],
            font=FONTS["tip"]
        )
        tip_label.pack(anchor="w", pady=PADDING["link_tip"])
        # 2秒后销毁提示
        self.parent.after(2000, tip_label.destroy)
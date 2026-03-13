# app/tk/components/main_menu/right_panel/base_panel.py
"""右侧面板基础类（封装通用逻辑，解耦重复操作）"""
import tkinter as tk
from .config import COLORS, PADDING


class BaseRightPanel:
    def __init__(self, parent: tk.Frame, width: int):
        # 创建右侧主框架
        self.main_frame = tk.Frame(parent, bg=COLORS["bg_white"], width=width)
        self.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.main_frame.pack_propagate(False)

        # 创建内容容器（用于清空/替换内容）
        self.content_container = tk.Frame(self.main_frame, bg=COLORS["bg_white"])
        self.content_container.pack(
            fill=tk.BOTH, expand=True,
            padx=PADDING["container"][0],
            pady=PADDING["container"][1]
        )

        # 面板注册表
        self.panel_registry = {}
        self.current_panel = None

    def register_panel(self, panel_key: str, panel_class) -> None:
        """注册面板"""
        self.panel_registry[panel_key] = panel_class

    def switch_content(self, panel_key: str) -> None:
        """通用内容切换逻辑"""
        # 清空当前内容
        self.clear_content()
        # 渲染目标面板
        if panel_key in self.panel_registry:
            self.current_panel = self.panel_registry[panel_key](self.content_container)
            self.current_panel.render()

    def clear_content(self) -> None:
        """清空内容容器"""
        for widget in self.content_container.winfo_children():
            widget.destroy()
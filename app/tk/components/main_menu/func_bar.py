# app/tk/components/main_menu/func_bar.py

"""蓝条组件封装（解耦交互逻辑）"""
import tkinter as tk
from .config import BAR_COLORS, BAR_SIZES, BAR_FONTS
from .utils import update_bar_color


class FuncBar:
    """功能蓝条组件类"""

    def __init__(self, parent: tk.Frame, text: str, is_welcome: bool = True, selected_bar_ref: list = None):
        # selected_bar_ref用列表（可变对象）实现全局状态共享（替代nonlocal）
        self.selected_bar_ref = selected_bar_ref or [None]
        self.is_welcome = is_welcome
        self.text = text

        # 创建蓝条容器
        self.frame = tk.Frame(
            parent,
            bg=BAR_COLORS["welcome_normal"] if is_welcome else BAR_COLORS["func_normal"],
            height=BAR_SIZES["welcome_height"] if is_welcome else BAR_SIZES["func_height"],
            cursor="hand2"
        )
        self.frame.pack(fill=tk.X, padx=BAR_SIZES["bar_padx"], pady=BAR_SIZES["bar_pady"])
        self.frame.pack_propagate(False)
        # 绑定组件属性到frame，方便外部访问
        self.frame.is_welcome = is_welcome
        self.frame.text = text

        # 创建文字标签
        self.label = tk.Label(
            self.frame,
            text=text,
            bg=self.frame["bg"],
            fg="white",
            font=BAR_FONTS["welcome"] if is_welcome else BAR_FONTS["func"],
            anchor="center"
        )
        self.label.pack(fill=tk.BOTH, expand=True)

        # 绑定交互事件
        self._bind_events()

    def _bind_events(self) -> None:
        """绑定交互事件（解耦事件逻辑）"""

        # 悬浮事件
        def on_enter(_):
            if self.frame != self.selected_bar_ref[0]:
                target_color = BAR_COLORS["welcome_hover"] if self.is_welcome else BAR_COLORS["func_hover"]
                update_bar_color(self.frame, target_color)

        # 离开事件
        def on_leave(_):
            if self.frame != self.selected_bar_ref[0]:
                target_color = BAR_COLORS["welcome_normal"] if self.is_welcome else BAR_COLORS["func_normal"]
                update_bar_color(self.frame, target_color)

        # 点击事件
        def on_click(_):
            if self.frame == self.selected_bar_ref[0]:
                return
            # 恢复上一个选中条
            if self.selected_bar_ref[0] is not None:
                prev_color = BAR_COLORS["welcome_normal"] if self.selected_bar_ref[0].is_welcome else BAR_COLORS[
                    "func_normal"]
                update_bar_color(self.selected_bar_ref[0], prev_color)
            # 设置当前选中条
            current_color = BAR_COLORS["welcome_selected"] if self.is_welcome else BAR_COLORS["func_selected"]
            update_bar_color(self.frame, current_color)
            # 更新全局选中态
            self.selected_bar_ref[0] = self.frame

        # 绑定到frame和label
        for widget in [self.frame, self.label]:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            widget.bind("<Button-1>", on_click)

    def set_selected(self) -> None:
        """设置当前蓝条为选中态"""
        selected_color = BAR_COLORS["welcome_selected"] if self.is_welcome else BAR_COLORS["func_selected"]
        update_bar_color(self.frame, selected_color)
        self.selected_bar_ref[0] = self.frame
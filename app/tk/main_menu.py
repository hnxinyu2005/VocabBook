# app/tk/main_menu.py
import tkinter as tk
from app.tk.components.main_menu.left_panel.main import create_left_panel
from app.tk.components.main_menu.right_panel import create_right_panel
from app.tk.base_window import BaseCustomWindow  # 导入基类
from utils.constants import DEFAULT_WINDOW_WIDTH_PERCENT, DEFAULT_WINDOW_HEIGHT_PERCENT
from app.tk.components.main_menu.left_panel.utils import calculate_left_width


class MainMenu(BaseCustomWindow):
    """主菜单窗口"""

    def __init__(self, title: str = "VocabBook",
                 width_percent: float = DEFAULT_WINDOW_WIDTH_PERCENT,
                 height_percent: float = DEFAULT_WINDOW_HEIGHT_PERCENT):
        # 创建根窗口
        root = tk.Tk()
        # 调用基类初始化
        super().__init__(
            root=root,
            title=title,
            width_percent=width_percent,
            height_percent=height_percent,
            resizable=(False, False)
        )

        # 创建主容器
        self.main_container = tk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # 先创建右侧面板
        self.right_panel, self.switch_content = create_right_panel(self.main_container, width=0)

        # 延迟计算左侧宽度
        self.root.after(10, self.init_left_panel)  # 延迟10ms，确保窗口已渲染

    def init_left_panel(self):
        """初始化左侧面板（按百分比计算宽度）"""
        # 获取窗口当前宽度
        window_width = self.root.winfo_width()
        left_width = calculate_left_width(window_width)  # 直接调用工具函数
        # 创建左侧面板（传入计算后的宽度）
        self.left_panel = create_left_panel(
            self.main_container,
            width=left_width,
            click_callback=self.switch_content
        )

    def on_window_resize(self, event):
        """窗口缩放时更新左侧宽度"""
        # 避免重复创建：先销毁旧的左侧面板，再重新创建
        if hasattr(self, 'left_panel') and self.left_panel.winfo_exists():
            self.left_panel.destroy()
        # 重新初始化左侧面板
        self.init_left_panel()

    def run(self):
        """启动主菜单窗口"""
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = MainMenu(root)
    root.mainloop()
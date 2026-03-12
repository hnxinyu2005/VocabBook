# app/tk/main_menu.py

import tkinter as tk
from app.tk.base_window import BaseCustomWindow
from utils.constants import DEFAULT_WINDOW_WIDTH_PERCENT, DEFAULT_WINDOW_HEIGHT_PERCENT
from utils.system.file import get_all_wordbooks

from app.tk.components.main_menu.left_panel import create_left_panel
from app.tk.components.main_menu.right_panel import create_right_panel


class MainMenu(BaseCustomWindow):  # 继承通用基类
    """主菜单窗口"""
    def __init__(self,
                 title="VocabBook",
                 width_percent=DEFAULT_WINDOW_WIDTH_PERCENT,
                 height_percent=DEFAULT_WINDOW_HEIGHT_PERCENT):
        root = tk.Tk()
        # 调用父类（BaseCustomWindow）
        super().__init__(root, title, width_percent, height_percent)

        # 数据初始化
        self._init_wordbook_data()
        # 延迟创建布局
        self.root.after(10, self._create_layout)

    def _init_wordbook_data(self):
        """数据初始化"""
        self.wordbooks = get_all_wordbooks()
        self.current_page = 0
        self.words_per_page = 8
        self.total_pages = max(1, (len(self.wordbooks) + self.words_per_page - 1) // self.words_per_page)

    def _create_layout(self):
        """布局整合"""
        # 主容器
        main_container = tk.Frame(self.root, bg="white")
        main_container.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        # 比例计算
        golden_ratio = 0.72
        left_width_ratio = 1 - golden_ratio
        window_width = self.root.winfo_width() if self.root.winfo_width() > 1 else 800
        left_width = int(window_width * left_width_ratio)
        right_width = window_width - left_width

        # 调用组件函数创建左右面板
        self.left_frame = create_left_panel(main_container, left_width)
        self.right_frame = create_right_panel(main_container, right_width)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainMenu()
    app.run()
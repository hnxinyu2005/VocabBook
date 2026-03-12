# app/tk/main_menu.py

import tkinter as tk
from utils.system.screen import get_centered_window_geometry
from utils.constants import DEFAULT_WINDOW_WIDTH_PERCENT, DEFAULT_WINDOW_HEIGHT_PERCENT

class MainMenu:
    def __init__(self,
                 title="VocabBook",
                 width_percent=DEFAULT_WINDOW_WIDTH_PERCENT,
                 height_percent=DEFAULT_WINDOW_HEIGHT_PERCENT): # 窗口高度占屏幕 50%
        self.root = tk.Tk()
        self.root.title(title)

        # 居中+百分比的窗口几何参数
        self.root.geometry(get_centered_window_geometry(width_percent, height_percent))

    def run(self):
        # 启动窗口主循环
        self.root.mainloop()
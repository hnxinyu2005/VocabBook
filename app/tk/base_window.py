# app/tk/base_window.py
import tkinter as tk
from utils.system.screen import get_centered_window_geometry
from utils.constants import DEFAULT_WINDOW_WIDTH_PERCENT, DEFAULT_WINDOW_HEIGHT_PERCENT


class BaseCustomWindow:
    """系统原生窗口基类"""
    def __init__(self, root,
                 title="VocabBook",
                 width_percent=DEFAULT_WINDOW_WIDTH_PERCENT,
                 height_percent=DEFAULT_WINDOW_HEIGHT_PERCENT,
                 resizable=(False, False)):  # 是否允许缩放（宽，高）
        self.root = root  # 接收外部传入的 TK 根窗口（Tk/Toplevel）
        self.root.title(title)

        # 系统窗口 + 居中 + 按屏幕百分比大小
        self.root.geometry(get_centered_window_geometry(width_percent, height_percent))

        # 是否允许缩放
        self.root.resizable(*resizable)

        # 设置窗口最小尺寸 已禁止缩放
        # self._set_min_size(width_percent * 0.5, height_percent * 0.5)

    '''
    def _set_min_size(self, min_width_percent, min_height_percent):
        """设置窗口最小尺寸"""
        screen_w, screen_h = self._get_screen_size()
        min_w = int(screen_w * min_width_percent)
        min_h = int(screen_h * min_height_percent)
        self.root.minsize(min_w, min_h)
    '''

    '''
    def _get_screen_size(self):
        """内部工具：获取屏幕逻辑分辨率（兼容所有系统）"""
        temp_root = tk.Tk()
        temp_root.withdraw()
        w = temp_root.winfo_screenwidth()
        h = temp_root.winfo_screenheight()
        temp_root.destroy()
        return w, h
    '''

    '''
    # 通用窗口控制方法（可选）
    
    def center_window(self):
        """重新居中窗口（比如窗口大小变化后）"""
        current_w = self.root.winfo_width()
        current_h = self.root.winfo_height()
        screen_w, screen_h = self._get_screen_size()
        x = (screen_w - current_w) // 2
        y = (screen_h - current_h) // 2
        self.root.geometry(f"{current_w}x{current_h}+{x}+{y}")
        
    def minimize_window(self):
        """系统原生最小化"""
        self.root.iconify()

    def restore_window(self):
        """恢复最小化窗口"""
        self.root.deiconify()

    def close_window(self):
        """关闭窗口（兼容根窗口/子窗口）"""
        if isinstance(self.root, tk.Tk):
            self.root.quit()
        else:
            self.root.destroy()
    
    '''
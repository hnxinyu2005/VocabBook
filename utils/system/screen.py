# utils/system/screen.py

import sys
import os

def get_screen_size():
    """
    获取逻辑分辨率（包括缩放）
    :return: (width, height)
    """
    # 此处只做了windows系统
    width = height = 0
    if sys.platform == "win32":
        import ctypes
        user32 = ctypes.WinDLL("user32", use_last_error=True)
        width = user32.GetSystemMetrics(0)
        height = user32.GetSystemMetrics(1)
    else:
        width, height = 1920, 1080

    return width, height

def get_centered_window_geometry(width_percent=0.4, height_percent=0.5):
    """
    按屏幕百分比计算窗口大小并居中（基于逻辑分辨率）

    :param width_percent: 窗口宽度占屏幕百分比（0-1）
    :param height_percent: 窗口高度占屏幕百分比（0-1）
    :return: tkinter可用的geometry字符串，如 "800x600+200+150"
    """
    screen_w, screen_h = get_screen_size()
    win_w = int(screen_w * width_percent)
    win_h = int(screen_h * height_percent)
    x = (screen_w - win_w) // 2
    y = (screen_h - win_h) // 2
    return f"{win_w}x{win_h}+{x}+{y}"

if __name__ == '__main__':
    print(f"屏幕逻辑分辨率：{get_screen_size()}")
    print(f"窗口几何参数（40%宽/50%高）：{get_centered_window_geometry()}")
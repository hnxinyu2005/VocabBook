# app/tk/main_menu.py
import tkinter as tk
from app.tk.components.main_menu.left_panel.main import create_left_panel
from app.tk.components.main_menu.right_panel import create_right_panel


class MainMenu:
    """主菜单窗口"""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("VocabBook")
        self.root.geometry("1000x600")  # 设置窗口大小
        self.root.resizable(True, True)  # 允许缩放

        # 主容器
        main_container = tk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True)

        # 创建右侧面板（先创建，获取切换函数）
        right_panel, self.switch_content = create_right_panel(main_container, width=800)

        # 创建左侧面板（传递切换函数作为回调）
        self.left_panel = create_left_panel(main_container, width=200, click_callback=self.switch_content)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainMenu(root)
    root.mainloop()
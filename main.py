# main.py
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.tk.main_menu import MainMenu

if __name__ == "__main__":
    # 方式1：用默认占比（从constants来）
    app = MainMenu(title="VocabBook")

    # 方式2：自定义占比（比如悬浮小窗用20%宽、30%高）
    # app = MainWordWindow(
    #     title="悬浮单词本",
    #     width_percent=0.2,
    #     height_percent=0.3
    # )

    app.run()
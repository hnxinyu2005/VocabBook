# app/tk/components/main_menu/right_panel.py

import tkinter as tk

def create_right_panel(parent, width):
    right_frame = tk.Frame(
        parent,
        bg="#ffffff", # 白色背景
        width=width
    )
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=0, pady=0)
    return right_frame
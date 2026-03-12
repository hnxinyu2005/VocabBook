# app/tk/components/main_menu/left_panel.py

import tkinter as tk

def create_left_panel(parent, width):
    left_frame = tk.Frame(
        parent,
        bg="#2c3e50",
        width=width
    )
    left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)
    left_frame.pack_propagate(False) # 禁止宽度被内容撑开

    return left_frame
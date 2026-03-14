# app/tk/components/main_menu/right_panel/book_panel.py
"""我的单词本面板"""
import tkinter as tk
from tkinter import ttk, messagebox
import os
from utils.system.file import get_all_wordbooks
from core.csv_manager import create_wordbook_csv, delete_wordbook_csv
from utils.constants import DEFAULT_WORDBOOK
from .config import COLORS, FONTS, PADDING


class BookPanel:
    def __init__(self, parent: tk.Frame):
        self.parent = parent
        self.selected_book = tk.StringVar()  # 选中的单词本名称
        # 存储三个信息标签（名称/路径/单词数量）
        self.name_label = None
        self.path_label = None
        self.count_label = None
        # 初始化单词本列表（确保default始终存在）
        self.wordbooks = self._init_wordbooks()

    def _init_wordbooks(self):
        """初始化单词本列表，确保default始终存在"""
        # 调用文件工具获取所有单词本
        book_list = get_all_wordbooks()
        book_names = [book["name"] for book in book_list]

        # 检查default是否存在，不存在则通过csv_manager创建
        if "default" not in book_names:
            is_created, err_msg = create_wordbook_csv(DEFAULT_WORDBOOK)
            if not is_created:
                messagebox.showerror("初始化失败", f"创建默认单词本失败：{err_msg}")
            # 重新获取单词本列表
            book_list = get_all_wordbooks()

        # 缓存单词本详情
        self.book_detail_map = {b["name"]: b for b in book_list}
        # 提取单词本名称
        book_names = ["default"] + [b["name"] for b in book_list if b["name"] != "default"]
        # 设置默认选中default
        self.selected_book.set("default")
        return book_names

    def _format_file_path(self, file_path):
        """将VocabBook文件夹前的路径替换为..."""
        if not file_path or file_path == "无":
            return "无"

        # 匹配VocabBook文件夹
        vocab_book_key = "VocabBook"
        if vocab_book_key in file_path:
            # 找到VocabBook的起始位置，保留后续路径
            idx = file_path.index(vocab_book_key)
            # 兼容Windows(\)和Linux/Mac(/)路径分隔符
            formatted_path = f"...{os.sep}{file_path[idx:]}"
            return formatted_path
        return file_path

    def render(self) -> None:
        """渲染完整单词本界面"""
        self._render_book_selector()  # 单词本选择下拉框
        self._render_book_info()  # 单词本信息（三行展示）
        self._render_operate_buttons()  # 打开单词本+按钮组+新增单词
        self._render_new_book_button()  # 新建/删除单词本按钮

    def _render_book_selector(self):
        """渲染单词本选择下拉框（绑定选中事件）"""
        selector_frame = tk.Frame(self.parent, bg=COLORS["bg_white"])
        selector_frame.pack(anchor="w", pady=PADDING["title"], fill=tk.X)

        # 下拉框标签
        label = tk.Label(
            selector_frame,
            text="选择单词本：",
            bg=COLORS["bg_white"],
            fg=COLORS["content"],
            font=FONTS["content"]
        )
        label.pack(side=tk.LEFT, padx=(0, 10))

        # 下拉选择框
        self.book_combobox = ttk.Combobox(
            selector_frame,
            textvariable=self.selected_book,
            values=self.wordbooks,
            state="readonly",
            font=FONTS["content"],
            width=20
        )
        self.book_combobox.pack(side=tk.LEFT)
        # 绑定选中事件（更新单词本信息）
        self.book_combobox.bind("<<ComboboxSelected>>", self._on_book_selected)

    def _render_book_info(self):
        """渲染单词本信息（拆分为名称、路径、单词数量三行）"""
        info_frame = tk.Frame(self.parent, bg=COLORS["bg_white"])
        info_frame.pack(anchor="w", pady=(0, 20), fill=tk.X)

        # 初始显示default的信息
        default_detail = self.book_detail_map.get("default", {})

        # 单词本名称
        self.name_label = tk.Label(
            info_frame,
            text=f"名称：{default_detail.get('name', '无')}",
            bg=COLORS["bg_white"],
            fg=COLORS["content"],
            font=FONTS["content"]
        )
        self.name_label.pack(anchor="w", pady=(0, 3))

        # 文件路径（自动换行 + 格式化）
        default_path = default_detail.get('path', '无')
        formatted_path = self._format_file_path(default_path)
        self.path_label = tk.Label(
            info_frame,
            text=f"路径：{formatted_path}",
            bg=COLORS["bg_white"],
            fg=COLORS["content"],
            font=FONTS["content"],
            wraplength=600  # 路径过长时自动换行
        )
        self.path_label.pack(anchor="w", pady=(0, 3))

        # 单词数量
        self.count_label = tk.Label(
            info_frame,
            text=f"单词数量：{default_detail.get('word_count', 0)}",
            bg=COLORS["bg_white"],
            fg=COLORS["content"],
            font=FONTS["content"]
        )
        self.count_label.pack(anchor="w")

    def _on_book_selected(self, event):
        """下拉框选中单词本后更新三行信息"""
        selected_name = self.selected_book.get()
        book_detail = self.book_detail_map.get(selected_name, {})

        # 更新名称标签
        self.name_label.config(text=f"名称：{book_detail.get('name', '无')}")

        # 更新路径标签（格式化 + 自动换行）
        book_path = book_detail.get('path', '无')
        formatted_path = self._format_file_path(book_path)
        self.path_label.config(text=f"路径：{formatted_path}")

        # 更新单词数量标签
        self.count_label.config(text=f"单词数量：{book_detail.get('word_count', 0)}")

    def _render_operate_buttons(self):
        """渲染 打开单词本 + 按钮组 + 新增单词按钮"""
        operate_frame = tk.Frame(self.parent, bg=COLORS["bg_white"])
        operate_frame.pack(anchor="w", pady=(0, 20), fill=tk.X)

        # 打开单词本文本
        entry_label = tk.Label(
            operate_frame,
            text="打开单词本：",
            bg=COLORS["bg_white"],
            fg=COLORS["content"],
            font=FONTS["content"]
        )
        entry_label.pack(side=tk.LEFT, padx=(0, 15))

        # 按钮通用样式
        btn_style = {
            "bg": COLORS["link"],
            "fg": "white",
            "font": FONTS["content"],
            "relief": tk.FLAT,
            "padx": 8,
            "pady": 3,
            "cursor": "hand2",
            "width": 8
        }

        # 主界面按钮
        main_btn = tk.Button(operate_frame, text="主界面", **btn_style, command=self._on_main_interface)
        main_btn.pack(side=tk.LEFT, padx=(0, 5))

        # Web界面按钮
        web_btn = tk.Button(operate_frame, text="web界面", **btn_style, command=self._on_web_interface)
        web_btn.pack(side=tk.LEFT, padx=(0, 5))

        # 小窗口按钮
        small_btn = tk.Button(operate_frame, text="小窗口", **btn_style, command=self._on_small_window)
        small_btn.pack(side=tk.LEFT, padx=(0, 15))

        # 新增单词按钮
        add_word_btn = tk.Button(
            operate_frame,
            text="新增单词",
            bg=COLORS["success"],
            fg="white",
            font=FONTS["content"],
            relief=tk.FLAT,
            padx=8,
            pady=3,
            cursor="hand2",
            command=self._on_add_word
        )
        add_word_btn.pack(side=tk.LEFT)

    def _render_new_book_button(self):
        """渲染 新建单词本 + 删除单词本 按钮"""
        new_book_frame = tk.Frame(self.parent, bg=COLORS["bg_white"])
        new_book_frame.pack(anchor="w", pady=(0, 10), fill=tk.X)

        # 新建单词本按钮
        new_book_btn = tk.Button(
            new_book_frame,
            text="新建单词本",
            bg=COLORS["success"],
            fg="white",
            font=FONTS["content"],
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor="hand2",
            command=self._on_new_book
        )
        new_book_btn.pack(side=tk.LEFT)

        # 删除单词本按钮（紧跟新建按钮）
        delete_book_btn = tk.Button(
            new_book_frame,
            text="删除单词本",
            bg="#e74c3c",  # 红色主题，区分删除操作
            fg="white",
            font=FONTS["content"],
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor="hand2",
            command=self._on_delete_book
        )
        delete_book_btn.pack(side=tk.LEFT, padx=(15, 0))

    # 按钮回调函数
    def _on_main_interface(self):
        """点击 主界面 按钮"""
        selected_name = self.selected_book.get()
        print(f"打开【{selected_name}】单词本主界面")

    def _on_web_interface(self):
        """点击 web界面 按钮"""
        selected_name = self.selected_book.get()
        print(f"打开【{selected_name}】Web预览界面")

    def _on_small_window(self):
        """点击 小窗口 按钮"""
        selected_name = self.selected_book.get()
        print(f"打开【{selected_name}】迷你复习窗口")

    def _on_add_word(self):
        """点击 新增单词 按钮"""
        selected_name = self.selected_book.get()
        print(f"为【{selected_name}】新增单词（待实现弹窗）")

    def _on_new_book(self):
        """点击 新建单词本 按钮（调用csv_manager接口）"""
        # 弹窗输入新单词本名称
        new_name = tk.simpledialog.askstring("新建单词本", "请输入单词本名称：")
        if not new_name:
            return

        # 调用csv_manager的创建函数
        is_created, err_msg = create_wordbook_csv(new_name)

        # 仅展示接口返回的信息
        if is_created:
            messagebox.showinfo("成功", err_msg)
            # 刷新单词本列表
            self._refresh_wordbook_list()
        else:
            messagebox.showerror("失败", err_msg)

    def _on_delete_book(self):
        """点击 删除单词本 按钮（调用csv_manager的删除函数）"""
        selected_name = self.selected_book.get()

        # 二次确认删除操作
        confirm = messagebox.askyesno(
            "确认删除",
            f"是否确定删除单词本【{selected_name}】？\n⚠️ 删除后数据将无法恢复！"
        )
        if not confirm:
            return

        # 调用核心层的删除函数
        is_deleted, err_msg = delete_wordbook_csv(selected_name)

        # 根据返回结果处理提示
        if is_deleted:
            messagebox.showinfo("删除成功", err_msg)
            # 刷新列表并选中default
            self._refresh_wordbook_list()
            self.selected_book.set("default")
            self._on_book_selected(None)
        else:
            messagebox.showerror("删除失败", err_msg)

    def _refresh_wordbook_list(self):
        """刷新下拉框的单词本列表"""
        # 重新获取单词本列表
        book_list = get_all_wordbooks()
        book_names = ["default"] + [b["name"] for b in book_list if b["name"] != "default"]
        # 更新缓存和下拉框
        self.book_detail_map = {b["name"]: b for b in book_list}
        self.wordbooks = book_names
        self.book_combobox.config(values=book_names)
        # 选中新创建的单词本（删除时会覆盖此选中）
        self.selected_book.set(book_names[-1])
        # 触发选中事件更新信息
        self._on_book_selected(None)


# 补充导入
import tkinter.simpledialog as simpledialog

tk.simpledialog = simpledialog
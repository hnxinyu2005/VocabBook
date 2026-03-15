# app/tk/components/main_menu/right_panel/book_panel.py
"""我的单词本面板"""
import tkinter as tk
from tkinter import ttk, messagebox
import os
from utils.system.file import get_all_wordbooks
from core.csv_manager import create_wordbook_csv, delete_wordbook_csv, write_processed_csv
from utils.constants import DEFAULT_WORDBOOK
from .config import COLORS, FONTS, PADDING
from utils.system.path import format_file_path_for_display
import tkinter.simpledialog as simpledialog
tk.simpledialog = simpledialog

class BookPanel:
    def __init__(self, parent: tk.Frame):
        self.parent = parent
        self.selected_book = tk.StringVar()  # 选中的单词本名称
        # 存储三个信息标签 名称/路径/单词数量
        self.name_label = None
        self.path_label = None
        self.count_label = None
        # 初始化单词本列表 确保default始终存在
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
        self._render_book_selector_with_new_btn()  # 选择单词本 + 新建按钮（同一行）
        self._render_book_info()  # 单词本信息（名称/路径/单词数量）
        self._render_open_buttons()  # 打开单词本的三个按钮（主界面/web/小窗口）
        self._render_operation_buttons()  # 操作行（新增单词 + 删除单词本）

    def _render_book_selector_with_new_btn(self):
        """渲染：选择单词本标签 + 下拉框 + 新建单词本按钮（同一行）"""
        selector_frame = tk.Frame(self.parent, bg=COLORS["bg_white"])
        selector_frame.pack(anchor="w", pady=PADDING["title"], fill=tk.X)

        # 选择单词本标签
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
        self.book_combobox.pack(side=tk.LEFT, padx=(0, 15))
        # 绑定选中事件
        self.book_combobox.bind("<<ComboboxSelected>>", self._on_book_selected)

        # 新建单词本按钮
        new_book_btn = tk.Button(
            selector_frame,
            text="新建单词本",
            bg=COLORS["success"],
            fg="white",
            font=FONTS["content"],
            relief=tk.FLAT,
            padx=15,
            pady=3,
            cursor="hand2",
            command=self._on_new_book
        )
        new_book_btn.pack(side=tk.LEFT)

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
        formatted_path = format_file_path_for_display(default_path)
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

    def _render_open_buttons(self):
        """渲染：打开单词本标签 + 主界面/web界面/小窗口 三个按钮"""
        open_frame = tk.Frame(self.parent, bg=COLORS["bg_white"])
        open_frame.pack(anchor="w", pady=(0, 15), fill=tk.X)

        # 打开单词本文本标签
        entry_label = tk.Label(
            open_frame,
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
        main_btn = tk.Button(open_frame, text="主界面", **btn_style, command=self._on_main_interface)
        main_btn.pack(side=tk.LEFT, padx=(0, 5))

        # Web界面按钮
        web_btn = tk.Button(open_frame, text="web界面", **btn_style, command=self._on_web_interface)
        web_btn.pack(side=tk.LEFT, padx=(0, 5))

        # 小窗口按钮
        small_btn = tk.Button(open_frame, text="小窗口", **btn_style, command=self._on_small_window)
        small_btn.pack(side=tk.LEFT)

    def _render_operation_buttons(self):
        """渲染：操作标签 + 新增单词 + 删除单词本 按钮"""
        operation_frame = tk.Frame(self.parent, bg=COLORS["bg_white"])
        operation_frame.pack(anchor="w", pady=(0, 10), fill=tk.X)

        # 操作标签
        op_label = tk.Label(
            operation_frame,
            text="操作：",
            bg=COLORS["bg_white"],
            fg=COLORS["content"],
            font=FONTS["content"]
        )
        op_label.pack(side=tk.LEFT, padx=(0, 15))

        # 新增单词按钮
        add_word_btn = tk.Button(
            operation_frame,
            text="新增单词",
            bg=COLORS["success"],
            fg="white",
            font=FONTS["content"],
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor="hand2",
            command=self._on_add_word
        )
        add_word_btn.pack(side=tk.LEFT, padx=(0, 15))

        # 删除单词本按钮
        delete_book_btn = tk.Button(
            operation_frame,
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
        delete_book_btn.pack(side=tk.LEFT)

    def _on_book_selected(self, event):
        """下拉框选中单词本后更新三行信息"""
        selected_name = self.selected_book.get()
        book_detail = self.book_detail_map.get(selected_name, {})

        # 更新名称标签
        self.name_label.config(text=f"名称：{book_detail.get('name', '无')}")

        # 更新路径标签（格式化 + 自动换行）
        book_path = book_detail.get('path', '无')
        formatted_path = format_file_path_for_display(book_path)
        self.path_label.config(text=f"路径：{formatted_path}")

        # 更新单词数量标签
        self.count_label.config(text=f"单词数量：{book_detail.get('word_count', 0)}")

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
        """用户传字典格式txt，直接丢给csvmanager"""
        # 豆包修了一万回 明明manager接口逻辑都写好了 这里硬要搞算法处理文本
        selected_book = self.selected_book.get()

        # 让用户选择自己准备的字典格式txt文件
        import tkinter.filedialog as fd
        file_path = fd.askopenfilename(
            title="选择单词数据文件",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        if not file_path:  # 取消选择
            return

        # 读取文件内容（不做任何处理，原封不动）
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text_data = f.read()  # 纯文本读取，不解析、不处理
        except Exception as e:
            messagebox.showerror("文件读取失败", f"读取文件出错：{str(e)}")
            return

        # 直接丢给你的csvmanager函数（零处理，原封不动传）
        try:
            from core.csv_manager import write_processed_csv
            # 需要用eval转成对应类型
            # 这是唯一的必要操作，否则传的是字符串，会报错
            data = eval(text_data)
            is_done, err_msg = write_processed_csv(data, selected_book)

            # 只接收并展示回传结果，无任何额外逻辑
            if is_done:
                messagebox.showinfo("导入成功", err_msg)
                self._refresh_wordbook_list(selected_book)
            else:
                messagebox.showerror("导入失败", err_msg)
        except Exception as e:
            messagebox.showerror("调用失败", f"传给csvmanager时出错：{str(e)}")

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
            # 刷新单词本列表（自动选中新建的单词本）
            self._refresh_wordbook_list(new_name.strip())  # 传入新建名称确保精准选中
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
            self._refresh_wordbook_list("default")
            self._on_book_selected(None)
        else:
            messagebox.showerror("删除失败", err_msg)

    def _refresh_wordbook_list(self, select_name=None):
        """刷新下拉框的单词本列表（支持指定选中名称）"""
        # 重新获取单词本列表
        book_list = get_all_wordbooks()
        book_names = ["default"] + [b["name"] for b in book_list if b["name"] != "default"]
        # 更新缓存和下拉框
        self.book_detail_map = {b["name"]: b for b in book_list}
        self.wordbooks = book_names
        self.book_combobox.config(values=book_names)

        # 选中指定名称（优先级最高），无则选中最后一个（新建场景）
        if select_name and select_name in book_names:
            self.selected_book.set(select_name)
        else:
            self.selected_book.set(book_names[-1])

        # 触发选中事件更新信息
        self._on_book_selected(None)
from flask import Flask
from routes.word_routes import register_word_routes

# 初始化Flask应用
app = Flask(__name__)

# 注册单词相关路由（仅这一行，路由完全独立）
register_word_routes(app)

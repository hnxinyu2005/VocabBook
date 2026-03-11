"""
单词相关路由：仅负责Flask路由注册、请求处理，无业务逻辑
"""
from flask import Blueprint, jsonify, request, abort
from services.word_flask_service import (
    get_wordbook_data,
    get_random_sample_words as service_random_words,
    list_all_wordbooks as service_list_books,
    get_single_word
)

# 创建蓝图（推荐使用蓝图，便于大型项目路由拆分）
word_bp = Blueprint("word", __name__, url_prefix="/api")


# 路由1：列出所有可用单词库
@word_bp.route("/wordbooks", methods=["GET"])
def list_wordbooks():
    try:
        result = service_list_books()
        return jsonify(result)
    except FileNotFoundError as e:
        abort(404, description=f"错误：{str(e)}")
    except Exception as e:
        abort(500, description=f"列出单词库失败：{str(e)}")


# 路由2：获取指定单词库的所有单词（支持随机排序）
@word_bp.route("/wordbooks/<csv_filename>", methods=["GET"])
def get_wordbook(csv_filename):
    try:
        # 解析请求参数：random（默认false）
        random_mode = request.args.get("random", "false").lower() == "true"
        # 调用业务层
        result = get_wordbook_data(csv_filename, random_mode)
        return jsonify(result)
    except FileNotFoundError as e:
        abort(404, description=f"错误：{str(e)}")
    except ValueError as e:
        abort(400, description=f"错误：{str(e)}")
    except IOError as e:
        abort(500, description=f"错误：{str(e)}")
    except Exception as e:
        abort(500, description=f"获取单词库数据失败：{str(e)}")


# 路由3：从指定单词库随机抽取N个单词
@word_bp.route("/wordbooks/<csv_filename>/random", methods=["GET"])
def get_random_words(csv_filename):
    try:
        # 解析并校验count参数
        count_str = request.args.get("count", "10")
        sample_count = int(count_str)
        # 调用业务层
        result = service_random_words(csv_filename, sample_count)
        return jsonify(result)
    except ValueError as e:
        abort(400, description=f"错误：{str(e)}（count必须是正整数）")
    except FileNotFoundError as e:
        abort(404, description=f"错误：{str(e)}")
    except IOError as e:
        abort(500, description=f"错误：{str(e)}")
    except Exception as e:
        abort(500, description=f"随机抽取单词失败：{str(e)}")


# 路由4：从指定单词库查找单个单词
@word_bp.route("/wordbooks/<csv_filename>/word/<word_name>", methods=["GET"])
def get_single_word_route(csv_filename, word_name):
    try:
        result = get_single_word(csv_filename, word_name)
        return jsonify(result)
    except FileNotFoundError as e:
        abort(404, description=f"错误：{str(e)}")
    except ValueError as e:
        abort(400, description=f"错误：{str(e)}")
    except IOError as e:
        abort(500, description=f"错误：{str(e)}")
    except Exception as e:
        abort(500, description=f"查找单词失败：{str(e)}")


def register_word_routes(app):
    """将单词蓝图注册到Flask应用"""
    app.register_blueprint(word_bp)
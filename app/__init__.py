from flask import Flask
from flask_cors import CORS
from app.utils.db import init_db
from app.routes import folk_culture_bp

def create_app(config_name=None):
    """Flask应用工厂函数"""
    # 创建Flask应用实例
    app = Flask(__name__)
    
    # 启用CORS
    CORS(app)
    
    # 初始化数据库
    init_db(app)
    
    # 注册蓝图
    app.register_blueprint(folk_culture_bp)
    
    # 根路径路由
    @app.route('/')
    def index():
        return {'message': '民俗文化API服务正在运行'}
    
    return app

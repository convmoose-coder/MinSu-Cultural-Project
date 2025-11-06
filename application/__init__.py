from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from .utils.db import db, init_db
from .routes.admin_routes import admin_bp
from .routes.folk_culture_routes import public_bp
from .routes.front_routes import register_front_routes
import os

def create_app():
    # 创建Flask应用实例，指定模板目录
    app = Flask(__name__, template_folder='../templates')
    
    # 加载配置
    app.config.from_object(Config)
    
    # 从环境变量加载数据库URI（如果存在）
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    
    # 初始化扩展
    CORS(app)
    JWTManager(app)
    
    # 注册蓝图
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(public_bp, url_prefix='/api')
    
    # 注册前端路由
    register_front_routes(app)
    
    # 初始化数据库
    with app.app_context():
        init_db(app)
    
    # 健康检查端点
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'timestamp': __import__('datetime').datetime.now().isoformat()}
    
    # API版本信息端点
    @app.route('/api/version')
    def api_version():
        return {
            'version': '1.0.0',
            'name': 'MinSu Cultural API'
        }
    
    return app
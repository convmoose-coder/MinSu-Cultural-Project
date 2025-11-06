from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.utils.db import db, init_db
from app.routes.admin_routes import admin_bp
from app.routes.folk_culture_routes import public_bp
from app.routes.front_routes import register_front_routes

def create_app():
    """应用工厂函数，用于创建和配置Flask应用实例"""
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object('config')
    
    # 初始化扩展
    CORS(app)
    JWTManager(app)
    db.init_app(app)
    
    # 注册蓝图
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(public_bp, url_prefix='/api')
    
    # 注册前端路由
    register_front_routes(app)
    
    # 初始化数据库
    with app.app_context():
        init_db()
    
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
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.routes.admin_routes import admin_bp
from app.routes.folk_culture_routes import public_bp
from app.routes.front_routes import register_front_routes
from app.utils.db import db, init_db
import os

# 创建Flask应用实例
app = Flask(__name__)

# 配置CORS - 支持前后端分离架构
cors_config = {
    "origins": ["http://localhost:5173"],  # 前端开发服务器地址
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"],
    "expose_headers": ["Content-Length"],
    "allow_credentials": True,
    "max_age": 3600
}

# 为不同路由组配置不同的CORS策略
CORS(app, resources={
    r"/api/*": cors_config,  # 前台公开API
    r"/admin/*": cors_config  # 后台管理API
})

# 配置JWT
app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 24 * 60 * 60  # 24小时
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 7 * 24 * 60 * 60  # 7天
app.config['JWT_ERROR_MESSAGE_KEY'] = 'message'
jwt = JWTManager(app)

# 注册路由蓝图
app.register_blueprint(admin_bp)  # 后台管理API，前缀已在蓝图中设置为/api/admin
app.register_blueprint(public_bp)  # 前台公开API，前缀已在蓝图中设置为/api

# 注册前台路由（包括模板渲染路由和API路由）
register_front_routes(app)

# 初始化数据库
init_db(app)

# JWT 回调函数
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({'message': '令牌已过期，请重新登录'}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({'message': '无效的令牌'}), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({'message': '缺少访问令牌'}), 401

# 注意：根路径路由已在前台路由中定义，这里不再重复定义

# 健康检查路由
@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'service': 'folk-culture-api'})

# API版本信息路由
@app.route('/api/version')
def api_version():
    return jsonify({
        'version': '1.0.0',
        'status': 'active',
        'features': [
            '民俗文化信息查询',
            '分类筛选',
            '地区筛选',
            '搜索功能',
            '热门推荐',
            '最新信息'
        ]
    })

# 跨域预检请求处理
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

if __name__ == '__main__':
    # 在开发环境中运行应用
    app.run(debug=True, host='0.0.0.0', port=5000)


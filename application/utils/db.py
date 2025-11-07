from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 初始化数据库实例
db = SQLAlchemy()

def init_db(app: Flask):
    """初始化数据库连接"""
    # 先尝试直接读取DATABASE_URL，如果没有则构建连接字符串
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        # 从单独的环境变量构建数据库连接字符串
        mysql_host = os.getenv('MYSQL_HOST', 'localhost')
        mysql_port = os.getenv('MYSQL_PORT', '3306')
        mysql_user = os.getenv('MYSQL_USER', 'root')
        mysql_password = os.getenv('MYSQL_PASSWORD', '')
        mysql_database = os.getenv('MYSQL_DATABASE', 'MinSu')
        db_url = f'mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # 绑定数据库到应用
    db.init_app(app)
    
    # 创建数据库表
    with app.app_context():
        db.create_all()

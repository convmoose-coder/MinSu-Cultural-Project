#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
初始化管理员用户脚本
用于创建管理员用户表并添加默认的admin用户
"""
import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from application import create_app
from application.models.admin_user import AdminUser
from application.utils.db import db
from werkzeug.security import generate_password_hash

def init_admin_user():
    """初始化管理员用户表并添加默认用户"""
    print("开始初始化管理员用户表...")
    
    # 创建Flask应用实例
    app = Flask(__name__)
    
    # 初始化数据库连接
    init_db(app)
    
    # 确保在应用上下文中创建表和添加数据
    with app.app_context():
        # 创建所有表（包括管理员用户表）
        db.create_all()
        print("数据库表创建成功!")
        
        # 检查是否已存在admin用户
        admin_user = AdminUser.query.filter_by(username='admin').first()
        
        if not admin_user:
            # 创建默认的admin用户
            admin_user = AdminUser(
                username='admin',
                password_hash=generate_password_hash('admin'),
                email='admin@example.com'
            )
            db.session.add(admin_user)
            db.session.commit()
            print("✅ 已成功添加admin用户")
            print("   用户名: admin")
            print("   密码: admin")
            print("   邮箱: admin@example.com")
        else:
            print("⚠️ admin用户已存在，跳过创建")
    
    print("\n管理员用户初始化完成!")

if __name__ == "__main__":
    init_admin_user()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据库初始化脚本
用于连接数据库并创建所有必要的表结构
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from application import create_app
from application.utils.db import db, init_db
from application.models.folk_culture import FolkCulture  # 导入所有模型，确保SQLAlchemy能识别它们
from application.models.admin_user import AdminUser

def create_tables():
    """创建数据库表"""
    print("开始初始化数据库...")
    
    # 创建Flask应用实例
    app = Flask(__name__)
    
    # 初始化数据库连接
    init_db(app)
    
    # 确保在应用上下文中创建表
    with app.app_context():
        # 创建所有表（基于已导入的模型）
        db.create_all()
        print("数据库表创建成功!")
        
        # 打印创建的表信息
        print("已创建的表:")
        for table in db.metadata.tables.keys():
            print(f"- {table}")
    
    print("数据库初始化完成!")

if __name__ == "__main__":
    create_tables()

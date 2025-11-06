#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据库表结构更新脚本
用于添加缺失的view_count列
"""
import os
import sys
# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask import Flask
from app.utils.db import db, init_db
from app.models.folk_culture import FolkCulture
from sqlalchemy import text

def update_database():
    """更新数据库表结构"""
    print("开始更新数据库表结构...")
    
    # 创建Flask应用实例
    app = Flask(__name__)
    
    # 初始化数据库连接
    init_db(app)
    
    # 确保在应用上下文中操作数据库
    with app.app_context():
        # 检查folk_cultures表是否存在
        if 'folk_cultures' in db.metadata.tables:
            # 使用SQLAlchemy的text()方法执行原始SQL
            try:
                # 先检查表中是否已有view_count列
                with db.engine.connect() as conn:
                    result = conn.execute(text("SHOW COLUMNS FROM folk_cultures LIKE 'view_count'")).fetchone()
                    column_exists = result is not None
                    
                    if not column_exists:
                        # 添加view_count列，设置默认值为0
                        conn.execute(text("ALTER TABLE folk_cultures ADD COLUMN view_count INT DEFAULT 0 NOT NULL"))
                        conn.commit()
                        print("成功添加view_count列到folk_cultures表")
                    else:
                        print("view_count列已存在，无需添加")
                
                # 确保表结构与模型同步
                db.create_all()
                print("数据库表结构已同步更新")
                
            except Exception as e:
                print(f"更新数据库时出错: {str(e)}")
        else:
            # 如果表不存在，创建所有表
            print("folk_cultures表不存在，创建所有表...")
            db.create_all()
            print("所有表创建成功")
    
    print("数据库更新完成!")

if __name__ == "__main__":
    update_database()

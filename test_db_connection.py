#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库连接测试脚本
用于诊断和解决数据库连接问题
"""

import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_database_connection():
    """测试数据库连接"""
    print("=== 数据库连接测试 ===\n")
    
    # 读取环境变量
    mysql_host = os.environ.get('MYSQL_HOST', 'localhost')
    mysql_port = os.environ.get('MYSQL_PORT', '3306')
    mysql_user = os.environ.get('MYSQL_USER', 'root')
    mysql_password = os.environ.get('MYSQL_PASSWORD', '')
    mysql_database = os.environ.get('MYSQL_DATABASE', 'test')
    database_url = os.environ.get('DATABASE_URL', '')
    
    print("环境变量配置:")
    print(f"  MYSQL_HOST: {mysql_host}")
    print(f"  MYSQL_PORT: {mysql_port}")
    print(f"  MYSQL_USER: {mysql_user}")
    print(f"  MYSQL_PASSWORD: {'*' * len(mysql_password) if mysql_password else '未设置'}")
    print(f"  MYSQL_DATABASE: {mysql_database}")
    print(f"  DATABASE_URL: {database_url if database_url else '未设置'}")
    print()
    
    # 构建连接字符串
    if database_url:
        connection_string = database_url
        print("使用 DATABASE_URL 连接数据库")
    else:
        connection_string = f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}"
        print("使用环境变量构建连接字符串")
    
    print(f"连接字符串: {connection_string.replace(mysql_password, '*' * len(mysql_password) if mysql_password else '')}")
    print()
    
    try:
        # 导入SQLAlchemy
        from sqlalchemy import create_engine
        from sqlalchemy.exc import SQLAlchemyError
        
        print("正在尝试连接数据库...")
        engine = create_engine(connection_string, echo=False)
        connection = engine.connect()
        print("✓ 数据库连接成功！")
        
        # 执行简单查询测试
        result = connection.execute("SELECT VERSION()")
        version = result.fetchone()
        print(f"✓ MySQL版本: {version[0]}")
        
        connection.close()
        return True
        
    except ImportError as e:
        print(f"✗ 导入SQLAlchemy失败: {e}")
        print("请确保已安装所需依赖:")
        print("  pip install pymysql sqlalchemy")
        return False
        
    except SQLAlchemyError as e:
        print(f"✗ 数据库连接失败: {e}")
        print("\n常见问题及解决方案:")
        print("1. 检查环境变量是否正确设置")
        print("2. 确认MySQL服务正在运行")
        print("3. 验证数据库用户和密码是否正确")
        print("4. 确认用户具有从当前主机连接的权限")
        print("5. 检查防火墙设置")
        return False
        
    except Exception as e:
        print(f"✗ 连接过程中发生未知错误: {e}")
        return False

def check_env_file():
    """检查.env文件是否存在"""
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_file):
        print("✓ 找到 .env 文件")
        return True
    else:
        print("✗ 未找到 .env 文件")
        print("请创建 .env 文件并配置数据库连接信息")
        print("可以复制 .env.example 文件作为模板:")
        print("  cp .env.example .env")
        return False

def main():
    """主函数"""
    print("民俗文化展示系统 - 数据库连接诊断工具\n")
    
    # 检查.env文件
    if not check_env_file():
        sys.exit(1)
    
    print()
    
    # 测试数据库连接
    success = test_database_connection()
    
    print("\n" + "="*50)
    if success:
        print("数据库连接测试完成，一切正常！")
        sys.exit(0)
    else:
        print("数据库连接测试失败，请根据上面的提示进行排查。")
        sys.exit(1)

if __name__ == "__main__":
    main()
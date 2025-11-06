#!/usr/bin/env python3
"""
重置管理员用户密码脚本
"""

from flask import Flask
from werkzeug.security import generate_password_hash

# 创建临时Flask应用来初始化数据库
app = Flask(__name__)

# 配置数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Fzy025897758.@8.138.227.227:3306/MinSu'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
from app.utils.db import db
db.init_app(app)

# 导入模型
from app.models.admin_user import AdminUser

def reset_admin_password():
    """重置管理员用户密码"""
    with app.app_context():
        try:
            # 检查数据库连接
            print("正在连接数据库...")
            
            # 查找管理员用户
            admin_user = AdminUser.query.filter_by(username='admin').first()
            
            if admin_user:
                print(f"找到管理员用户: {admin_user.username}")
                print(f"当前邮箱: {admin_user.email}")
                
                # 重置密码为 admin123
                new_password = 'admin123'
                admin_user.password_hash = generate_password_hash(new_password)
                db.session.commit()
                
                print(f"密码已重置为: {new_password}")
                print("✓ 密码重置成功")
                return True
            else:
                print("未找到管理员用户，创建新用户...")
                
                # 创建新的管理员用户
                new_admin = AdminUser(
                    username='admin',
                    email='admin@example.com',
                    password_hash=generate_password_hash('admin123')
                )
                
                db.session.add(new_admin)
                db.session.commit()
                
                print(f"新管理员用户创建成功！")
                print(f"用户名: {new_admin.username}")
                print(f"邮箱: {new_admin.email}")
                print(f"密码: admin123")
                return True
                
        except Exception as e:
            print(f"操作失败: {e}")
            return False

if __name__ == '__main__':
    print("=== 重置管理员用户密码 ===")
    
    if reset_admin_password():
        print("\n=== 重置完成 ===")
        print("用户名: admin")
        print("密码: admin123")
        print("请重新运行登录测试")
    else:
        print("重置失败")
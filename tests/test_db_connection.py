import os
import pymysql
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 从环境变量获取数据库配置
host = os.getenv('MYSQL_HOST', '8.138.227.227')
port = int(os.getenv('MYSQL_PORT', '3306'))
user = os.getenv('MYSQL_USER', 'root')
password = os.getenv('MYSQL_PASSWORD', 'Fzy025897758.')
database = os.getenv('MYSQL_DATABASE', 'MinSu')

print(f"正在尝试连接到MySQL数据库：{host}:{port}")
print(f"数据库：{database}")
print(f"用户名：{user}")

# 尝试连接数据库
try:
    connection = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    print("✅ 数据库连接成功！")
    
    # 测试数据库操作
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1 as test")
        result = cursor.fetchone()
        print(f"✅ 数据库查询成功：{result}")
    
    connection.close()
    print("✅ 数据库连接已关闭")
    
except Exception as e:
    print(f"❌ 数据库连接失败：{str(e)}")
    print("\n请检查：")
    print("1. 数据库服务器是否正在运行")
    print("2. 连接参数是否正确")
    print("3. 防火墙是否允许连接")
    print("4. 用户是否有权限连接到指定数据库")

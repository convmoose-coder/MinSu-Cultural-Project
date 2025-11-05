import pymysql
import mysql.connector
from sqlalchemy import create_engine

print("测试MySQL库安装状态：")
print(f"pymysql版本: {pymysql.__version__}")
print(f"mysql-connector-python版本: {mysql.connector.__version__}")
print(f"SQLAlchemy版本: {create_engine.__module__.split('.')[0]} {__import__('sqlalchemy').__version__}")
print("\n所有MySQL相关库已成功安装！")

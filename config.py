import os

class Config:
    # 从环境变量获取配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT') or 3306)
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or ''
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE') or 'test'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f"mysql+pymysql://{'root'}:{'Fzy025897758.'}@{'8.138.227.227'}:{'3306'}/{'MinSu'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
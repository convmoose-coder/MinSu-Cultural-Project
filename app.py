from app import create_app

# 创建应用实例（保持向后兼容）
app = create_app()

if __name__ == '__main__':
    import os
    # 从环境变量获取主机和端口，如果没有设置则使用默认值
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"启动服务器: http://{host}:{port}")
    app.run(host=host, port=port, debug=debug)


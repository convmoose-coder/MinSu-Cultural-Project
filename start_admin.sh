#!/bin/bash

echo "=== 启动管理后台系统 ==="

# 检查后端服务是否运行
if ! pgrep -f "python app.py" > /dev/null; then
    echo "启动后端服务..."
    cd /e/pythonProject/MinSu
    python app.py &
    sleep 3
fi

# 注意：用户端前台服务（端口5173）需要在另一个终端中启动
# 启动命令：cd /e/pythonProject/MinSu/frontend && npm run dev

# 启动管理后台前端
echo "启动管理后台前端..."
cd /e/pythonProject\MinSu/frontend
npm run dev:admin

echo "管理后台地址: http://localhost:5174/admin/"
echo "用户端前台地址: http://localhost:5173/"
echo "后端API地址: http://127.0.0.1:5000/"
echo ""
echo "注意：请在另一个终端中启动用户端前台服务："
echo "cd /e/pythonProject/MinSu/frontend && npm run dev"
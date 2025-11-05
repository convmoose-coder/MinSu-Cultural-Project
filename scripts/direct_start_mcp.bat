@echo off

echo 正在直接启动MySQL MCP服务器...
echo 设置环境变量...
set MYSQL_HOST=8.138.227.227
set MYSQL_PORT=3306
set MYSQL_USER=root
set MYSQL_PASSWORD=Fzy025897758.
set MYSQL_DATABASE=MinSu

echo 正在启动mysql_mcp_server.exe...
"%~dp0.venv\Scripts\mysql_mcp_server.exe"

echo MySQL MCP服务器已退出
pause

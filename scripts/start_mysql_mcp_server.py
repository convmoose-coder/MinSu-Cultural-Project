import os
import sys
import subprocess
from pathlib import Path

# 获取当前虚拟环境的Scripts目录
venv_dir = Path(sys.prefix)
scripts_dir = venv_dir / "Scripts"

# 检查mysql_mcp_server.exe是否存在
mysql_mcp_exe = scripts_dir / "mysql_mcp_server.exe"

if not mysql_mcp_exe.exists():
    print(f"错误: 找不到mysql_mcp_server.exe在{scripts_dir}")
    sys.exit(1)

print(f"找到mysql_mcp_server.exe: {mysql_mcp_exe}")
print("正在启动MySQL MCP服务器...")

# 加载环境变量
os.environ["MYSQL_HOST"] = "8.138.227.227"
os.environ["MYSQL_PORT"] = "3306"
os.environ["MYSQL_USER"] = "root"
os.environ["MYSQL_PASSWORD"] = "Fzy025897758."
os.environ["MYSQL_DATABASE"] = "MinSu"

# 直接启动mysql_mcp_server.exe
try:
    subprocess.run([str(mysql_mcp_exe)], check=True)
except subprocess.CalledProcessError as e:
    print(f"MySQL MCP服务器启动失败: {e}")
    sys.exit(1)

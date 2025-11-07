# Linux服务器部署指南

## 项目概述

本项目是一个前后端分离的民俗文化展示系统，包含用户端前台和一个后端API服务。

### 项目架构

1. **用户端前台** (端口5173)
   - 访问地址：http://localhost:5173/
   - 提供民俗文化信息展示功能

2. **后端API服务** (端口5000)
   - API地址：http://localhost:5000/
   - 提供RESTful API接口

## 部署环境要求

### 系统要求
- Linux服务器 (Ubuntu 20.04 LTS 或 CentOS 8 推荐)
- Python 3.8+
- Node.js 16+
- MySQL 8.0+
- Nginx (用于反向代理和静态文件服务)

### 依赖组件
- Gunicorn (Python WSGI HTTP Server)
- PM2 (Node.js进程管理器，可选)

## 部署步骤

### 1. 环境准备

```bash
# 更新系统包
sudo apt update && sudo apt upgrade -y

# 安装基础依赖
sudo apt install -y python3 python3-pip python3-venv nodejs npm git mysql-server nginx

# 安装PM2 (Node.js进程管理器)
sudo npm install -g pm2
```

### 2. 项目获取

```bash
# 克隆项目代码
git clone <项目仓库地址>
cd MinSu

# 创建Python虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 安装Python依赖
pip install -r requirements.txt
```

### 3. 数据库配置

```bash
# 启动MySQL服务
sudo systemctl start mysql
sudo systemctl enable mysql

# 登录MySQL并创建数据库
mysql -u root -p
```

```sql
CREATE DATABASE MinSu CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'minsu_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON MinSu.* TO 'minsu_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 4. 环境变量配置

创建 `.env` 文件：

```bash
# 数据库连接信息
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=minsu_user
MYSQL_PASSWORD=your_secure_password
MYSQL_DATABASE=MinSu
DATABASE_URL=mysql+pymysql://${MYSQL_USER}:${MYSQL_PASSWORD}@${MYSQL_HOST}:${MYSQL_PORT}/${MYSQL_DATABASE}

# Flask配置
FLASK_ENV=production
FLASK_APP=app.py

# 应用密钥 (请更改为安全的随机字符串)
SECRET_KEY=your_production_secret_key_here


```

#### 解决数据库连接问题

如果您遇到类似 `pymysql.err.OperationalError: (1045, "Access denied for user 'root'@'localhost' (using password: NO)")` 的错误，请按照以下步骤排查：

1. **检查环境变量是否正确加载**
   ```bash
   # 在项目根目录下检查环境变量
   cat .env
   
   # 确认环境变量已被正确设置
   echo $MYSQL_HOST
   echo $MYSQL_USER
   echo $MYSQL_PASSWORD
   ```

2. **验证数据库用户权限**
   ```bash
   # 登录MySQL验证用户权限
   mysql -u $MYSQL_USER -p
   
   # 在MySQL中检查用户权限
   SHOW GRANTS FOR CURRENT_USER();
   ```

3. **测试数据库连接**
   ```bash
   # 使用Python测试数据库连接
   python -c "
   import os
   from sqlalchemy import create_engine
   
   # 读取环境变量
   host = os.environ.get('MYSQL_HOST', 'localhost')
   port = os.environ.get('MYSQL_PORT', '3306')
   user = os.environ.get('MYSQL_USER', 'root')
   password = os.environ.get('MYSQL_PASSWORD', '')
   database = os.environ.get('MYSQL_DATABASE', 'test')
   
   # 打印连接信息（注意不要在生产环境中打印密码）
   print(f'Host: {host}')
   print(f'Port: {port}')
   print(f'User: {user}')
   print(f'Database: {database}')
   
   # 尝试连接数据库
   try:
       engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')
       connection = engine.connect()
       print('数据库连接成功！')
       connection.close()
   except Exception as e:
       print(f'数据库连接失败: {e}')
   "
   ```

4. **常见的解决方法**
   - 确保 `.env` 文件中的 `MYSQL_USER` 和 `MYSQL_PASSWORD` 与MySQL中创建的用户和密码一致
   - 如果使用 `root` 用户，请确保其可以从 `localhost` 连接
   - 检查MySQL用户是否具有正确的权限：
     ```sql
     -- 授予所有权限（仅用于开发环境）
     GRANT ALL PRIVILEGES ON MinSu.* TO 'your_user'@'localhost';
     
     -- 或者授予特定权限（推荐用于生产环境）
     GRANT SELECT, INSERT, UPDATE, DELETE ON MinSu.* TO 'your_user'@'localhost';
     
     -- 刷新权限
     FLUSH PRIVILEGES;
     ```

### 5. 数据库初始化

```bash
# 初始化数据库表
python scripts/init_database.py
```

### 6. 前端构建

```bash
# 进入前端目录
cd frontend

# 安装前端依赖
npm install

# 构建用户端前台
npm run build

# 返回项目根目录
cd ..
```

### 7. 后端服务部署

使用Gunicorn启动后端服务：

```bash
# 安装Gunicorn和项目依赖
pip install gunicorn pandas openpyxl

# 启动后端服务（推荐使用应用工厂模式）
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()" --daemon
```

或者使用PM2管理：

```bash
# 安装Gunicorn和项目依赖
pip install gunicorn pandas openpyxl

# 使用PM2启动后端服务（推荐使用应用工厂模式）
pm2 start "gunicorn -w 4 -b 0.0.0.0:5000 \"app:create_app()\"" --name "minsu-backend"
```

> 注意：我们推荐使用应用工厂模式 (`app:create_app()`) 来启动应用，这种方式更加稳定且符合最佳实践。如果你的环境不支持这种模式，也可以使用传统的启动方式：
> 
> ```bash
> gunicorn -w 4 -b 0.0.0.0:5000 app:app --daemon
> ```
```

### 8. 前端服务部署

使用PM2管理前端服务：

```bash
# 进入前端目录
cd frontend

# 启动用户端前台服务
pm2 start "npm run preview" --name "minsu-frontend"
```

### 9. Nginx配置

创建Nginx配置文件 `/etc/nginx/sites-available/minsu`：

```nginx
server {
    listen 80;
    server_name your_domain.com;

    # 用户端前台
    location / {
        proxy_pass http://localhost:5173;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    

    # API服务
    location /api/ {
        proxy_pass http://localhost:5000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

启用配置并重启Nginx：

```bash
# 创建软链接
sudo ln -s /etc/nginx/sites-available/minsu /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重启Nginx
sudo systemctl restart nginx
sudo systemctl enable nginx
```

### 10. 安全配置

1. **SSL证书配置** (推荐使用Let's Encrypt)

```bash
# 安装Certbot
sudo apt install certbot python3-certbot-nginx

# 获取SSL证书
sudo certbot --nginx -d your_domain.com
```

2. **防火墙配置**

```bash
# 启用UFW防火墙
sudo ufw enable

# 允许必要端口
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
```

## 管理命令

### 查看服务状态

```bash
# 查看PM2服务状态
pm2 list

# 查看后端服务日志
pm2 logs minsu-backend

# 查看前端服务日志
pm2 logs minsu-frontend
```

### 重启服务

```bash
# 重启后端服务
pm2 restart minsu-backend

# 重启用户端前台
pm2 restart minsu-frontend
```

### 停止服务

```bash
# 停止所有服务
pm2 stop all

# 停止特定服务
pm2 stop minsu-backend
pm2 stop minsu-frontend

## 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查MySQL服务是否运行：`sudo systemctl status mysql`
   - 检查数据库配置是否正确
   - 检查防火墙设置

2. **前端页面无法访问**
   - 检查前端服务是否运行：`pm2 list`
   - 检查Nginx配置是否正确
   - 检查端口是否被占用

3. **API接口返回403错误**
   - 检查前后端分离安全机制配置
   - 确认Referer头和User-Agent设置正确

### 日志查看

```bash
# 查看后端日志
tail -f /path/to/gunicorn/access.log
tail -f /path/to/gunicorn/error.log

# 查看前端服务日志
pm2 logs minsu-frontend

# 查看Nginx日志
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

## 性能优化建议

1. **数据库优化**
   - 添加适当的数据库索引
   - 定期清理无用数据
   - 使用连接池

2. **前端优化**
   - 启用Gzip压缩
   - 使用CDN加速静态资源
   - 启用浏览器缓存

3. **后端优化**
   - 使用Redis缓存热点数据
   - 优化数据库查询
   - 使用异步任务处理耗时操作

## 备份与恢复

### 数据库备份

```bash
# 备份数据库
mysqldump -u minsu_user -p MinSu > minsu_backup_$(date +%Y%m%d).sql

# 恢复数据库
mysql -u minsu_user -p MinSu < minsu_backup_*.sql
```

### 文件备份

```bash
# 备份项目文件
tar -czf minsu_files_$(date +%Y%m%d).tar.gz /path/to/minsu
```

## 监控与维护

### 系统监控

建议使用以下监控工具：
- **Netdata**: 实时系统监控
- **Uptime Kuma**: 网站可用性监控
- **Prometheus + Grafana**: 高级监控和可视化

### 定期维护任务

1. **日志轮转**
   - 配置logrotate定期清理日志文件

2. **安全更新**
   - 定期更新系统和依赖包

3. **性能检查**
   - 定期检查系统资源使用情况

## 联系信息

如有部署问题，请联系项目维护人员或查看项目文档。
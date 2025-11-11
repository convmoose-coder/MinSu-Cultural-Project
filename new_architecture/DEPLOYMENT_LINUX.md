# Linux服务器部署指南

本文档提供了在Linux服务器上直接部署项目的详细步骤，适用于未安装Docker的环境。

## 1. 环境准备

### 1.1 安装必要软件

```bash
# 更新系统包
apt update && apt upgrade -y

# 安装Python 3.10和pip
apt install python3.10 python3.10-venv python3.10-dev -y

# 安装Node.js 16
curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
apt install nodejs -y

# 安装Nginx
apt install nginx -y

# 安装Git
apt install git -y
```

### 1.2 安装数据库

```bash
# 安装MySQL
apt install mysql-server -y

# 安全配置MySQL
mysql_secure_installation
```

## 2. 后端部署

### 2.1 克隆代码

```bash
# 克隆项目代码
git clone https://your-repo-url/MinSu.git /var/www/minsu
cd /var/www/minsu/new_architecture/backend
```

### 2.2 创建虚拟环境

```bash
# 创建Python虚拟环境
python3.10 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 升级pip
pip install --upgrade pip
```

### 2.3 安装依赖

```bash
# 安装后端依赖
pip install -r requirements.txt
```

### 2.4 配置环境变量

创建`.env`文件：

```bash
cp .env.example .env

# 编辑.env文件，配置数据库连接等信息
nano .env
```

### 2.5 数据库初始化

```bash
# 运行数据库初始化脚本
python -m app.db.init
```

### 2.6 配置Gunicorn

```bash
# 安装Gunicorn
pip install gunicorn

# 创建Gunicorn配置文件
nano /var/www/minsu/new_architecture/backend/gunicorn_config.py
```

Gunicorn配置内容：

```python
bind = "127.0.0.1:8000"
workers = 3
worker_class = "uvicorn.workers.UvicornWorker"
threads = 3
timeout = 120
```

### 2.7 配置Systemd服务

```bash
# 创建后端服务文件
nano /etc/systemd/system/minsu-backend.service
```

服务配置内容：

```
[Unit]
Description=Minsu Backend Service
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/minsu/new_architecture/backend
Environment="PATH=/var/www/minsu/new_architecture/backend/venv/bin"
ExecStart=/var/www/minsu/new_architecture/backend/venv/bin/gunicorn -c gunicorn_config.py app.main:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# 启动服务
systemctl daemon-reload
systemctl enable minsu-backend.service
systemctl start minsu-backend.service
```

## 3. 前端部署

### 3.1 安装依赖

```bash
# 进入前端目录
cd /var/www/minsu/new_architecture/frontend/client

# 安装依赖
npm install
```

### 3.2 构建项目

```bash
# 构建前端项目
npm run build
```

## 4. Nginx配置

```bash
# 创建Nginx配置文件
nano /etc/nginx/conf.d/minsu.conf
```

配置内容：

```nginx
events {
    worker_connections 1024;
}

http {
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    server_tokens off;

    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

    server {
        listen 80;
        server_name your-domain.com;

        # 前端静态文件
        location / {
            root /var/www/minsu/new_architecture/frontend/client/dist;
            try_files $uri $uri/ /index.html;
        }

        # 后端API
        location /api/ {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            proxy_connect_timeout 60s;
            proxy_send_timeout 60s;
            proxy_read_timeout 60s;
            
            proxy_buffers 4 256k;
            proxy_buffer_size 128k;
            proxy_busy_buffers_size 256k;
        }

        error_page 500 502 503 504 /50x.html;
        location = /50x.html {
            root /usr/share/nginx/html;
        }
    }
}
```

```bash
# 检查Nginx配置
inginx -t

# 重载Nginx
systemctl reload nginx
```

## 5. 安全配置

### 5.1 配置防火墙

```bash
# 安装UFW
apt install ufw -y

# 允许SSH、HTTP和HTTPS
ufw allow 22
default deny incoming
default allow outgoing
ufw enable
```

### 5.2 SSL配置（可选）

```bash
# 安装Certbot
apt install certbot python3-certbot-nginx -y

# 申请SSL证书
certbot --nginx -d your-domain.com
```

## 6. 服务监控

### 6.1 配置日志轮转

```bash
# 创建日志轮转配置
nano /etc/logrotate.d/minsu
```

配置内容：

```
/var/log/nginx/access.log /var/log/nginx/error.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data adm
    sharedscripts
    postrotate
        [ -s /run/nginx.pid ] && kill -USR1 `cat /run/nginx.pid`
    endscript
}
```

### 6.2 定期备份数据库

创建备份脚本：

```bash
nano /var/www/minsu/scripts/backup_db.sh
```

脚本内容：

```bash
#!/bin/bash

BACKUP_DIR="/var/backups/minsu"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
mysqldump -u root -p"your-password" minsu_db > "$BACKUP_DIR/minsu_db_$DATE.sql"
gzip "$BACKUP_DIR/minsu_db_$DATE.sql"

# 删除7天前的备份
find $BACKUP_DIR -name "minsu_db_*.sql.gz" -mtime +7 -delete
```

```bash
# 设置执行权限
chmod +x /var/www/minsu/scripts/backup_db.sh

# 添加到定时任务
crontab -e
```

添加：

```
0 2 * * * /var/www/minsu/scripts/backup_db.sh
```

## 7. 故障排查

### 7.1 检查服务状态

```bash
# 检查后端服务状态
systemctl status minsu-backend.service

# 检查Nginx状态
systemctl status nginx

# 查看错误日志
journalctl -u minsu-backend.service --since "1 hour ago"
cat /var/log/nginx/error.log
```

### 7.2 常见问题

- **502 Bad Gateway**: 检查后端服务是否正常运行
- **504 Gateway Timeout**: 增加超时设置
- **连接被拒绝**: 检查防火墙设置和端口监听

## 8. 维护

### 8.1 更新代码

```bash
# 进入项目目录
cd /var/www/minsu

# 拉取最新代码
git pull

# 更新后端
cd /var/www/minsu/new_architecture/backend
source venv/bin/activate
pip install -r requirements.txt
python -m app.db.migrate
deactivate
systemctl restart minsu-backend.service

# 更新前端
cd /var/www/minsu/new_architecture/frontend/client
npm install
npm run build
systemctl reload nginx
```

---

本文档提供了在Linux服务器上直接部署项目的完整流程。如有任何问题，请参考相应的服务文档或联系技术支持。
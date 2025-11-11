# Nginx配置指南

本文档提供了详细的Nginx配置指南，适用于直接部署在服务器上的环境（非Docker环境）。

## 项目技术栈说明

- **前端（client）**: Next.js框架
- **管理后台（admin）**: Vue.js 3 + Vite框架
- **后端**: FastAPI（通过uvicorn运行在端口8000）

## 项目构建指南

在配置Nginx前，请确保已完成项目构建：

### 前端（Next.js）构建

```bash
# 进入前端client目录
cd /var/www/minsu/new_architecture/frontend/client

# 安装依赖
npm install

# 构建项目
npm run build

# 启动Next.js服务（生产环境）
npm start
# 注意：这将在端口3000启动服务，需要保持运行
```

### 管理后台（Vue.js）构建

```bash
# 进入管理后台目录
cd /var/www/minsu/new_architecture/frontend/admin

# 安装依赖
npm install

# 构建项目（将生成dist目录）
npm run build
```

### 后端启动

确保后端服务通过uvicorn运行在端口8000：

```bash
# 进入后端目录
cd /var/www/minsu/new_architecture/backend

# 激活虚拟环境
# source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 启动后端服务
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

使用Systemd或PM2管理服务，确保服务持久运行。

## 1. Nginx安装

### 1.1 在Ubuntu/Debian上安装

```bash
# 更新包列表
apt update

# 安装Nginx
apt install nginx -y

# 检查安装状态
nginx -v

# 启动Nginx服务
systemctl start nginx

# 设置开机自启
systemctl enable nginx
```

### 1.2 在CentOS/RHEL上安装

```bash
# 安装EPEL仓库
yum install epel-release -y

# 安装Nginx
yum install nginx -y

# 启动Nginx服务
systemctl start nginx

# 设置开机自启
systemctl enable nginx
```

## 2. 基本配置结构

Nginx配置文件的基本结构如下：

- `/etc/nginx/nginx.conf`: 主配置文件
- `/etc/nginx/conf.d/`: 额外配置目录，存放站点配置
- `/etc/nginx/sites-enabled/`: 启用的站点配置（Debian/Ubuntu）
- `/etc/nginx/sites-available/`: 可用的站点配置（Debian/Ubuntu）

## 3. 项目Nginx配置

### 3.1 基本配置文件

创建配置文件：

```bash
nano /etc/nginx/conf.d/minsu.conf
```

基本配置内容（仅server块，适合放在conf.d目录）：

```nginx
# 前端静态文件和后端API代理配置 - Next.js版本
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    # 注意：根据项目实际运行环境配置正确的代理地址
    # 以下配置适用于非Docker环境，直接部署在服务器上的情况
    
    # 前端代理
    # 注意：当前前端服务实际运行在5173端口（Vite默认端口），不是3000端口
    # 重要警告：不要将proxy_pass设置为与Nginx监听端口相同的值，这会导致循环代理并产生400错误
    location / {
        # 对于根路径请求，代理到前端服务
        proxy_pass http://127.0.0.1:5173;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 关键设置：502错误常见解决方法
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        
        # 确保代理缓冲区配置正确
        proxy_buffers 4 256k;
        proxy_buffer_size 128k;
        proxy_busy_buffers_size 256k;
        proxy_temp_file_write_size 256k;
    }
    
    # 管理后台代理
    location /admin {
        # 注意：如果管理后台尚未启动，可以先注释此行，避免502错误
        # 管理后台需要单独启动并监听3001端口
        proxy_pass http://127.0.0.1:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 关键设置：502错误常见解决方法
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # 后端API代理
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        
        # 超时设置 - 解决502/504错误
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        
        # 缓冲区设置
        proxy_buffers 4 256k;
        proxy_buffer_size 128k;
        proxy_busy_buffers_size 256k;
        proxy_temp_file_write_size 256k;
    }

    # 错误页面
    error_page 404 /404.html;
    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /usr/share/nginx/html;
    }

    # 非Docker环境重要注意事项：
    # 1. 确保所有代理的服务端口与实际运行端口一致
    #    - 前端Vue项目运行在5173端口（npm run dev的默认端口）
    #    - 管理后台需要运行在3001端口（需单独启动）
    #    - 后端API运行在8000端口
    # 2. 绝对禁止将proxy_pass设置为与Nginx监听端口相同的值（如Nginx监听80端口，就不能代理到80端口）
    #    这会导致循环代理，产生"400 Request Header Or Cookie Too Large"错误
    # 3. 确保只有一个后端服务实例运行，避免端口冲突（目前看到有两个后端实例同时运行在8000端口）
    # 4. 检查防火墙设置，确保端口未被阻止
    # 5. 验证每个服务都能通过curl命令直接访问
    #    - curl http://127.0.0.1:5173 （测试前端服务）
    #    - curl http://127.0.0.1:8000 （测试后端服务）
    # 6. 确保nginx有足够权限访问代理的服务
    # 7. 修改配置后需要重启nginx：nginx -s reload
    # 8. 检查Nginx错误日志排查问题：tail -f /var/log/nginx/error.log
    # 9. 前端构建命令：使用npm而非pm，正确命令为 npm run build
    # 10. 持久化运行前端服务的方法（Linux环境）：
    #     - 使用screen：screen -S frontend npm run dev
    #     - 使用nohup：nohup npm run dev > frontend.log 2>&1 &
    #     - 推荐使用PM2进行管理：npm install -g pm2 && pm2 start npm --name "frontend" -- run dev
    # 
    # Linux环境下检查端口监听状态的命令（替代Windows的findstr）：
    # - 检查80端口：netstat -tuln | grep 80
    # - 检查5173端口：netstat -tuln | grep 5173
    # - 检查8000端口：netstat -tuln | grep 8000
    # 或使用：lsof -i :端口号
    # 
    # 注意：服务器环境似乎是Linux系统（从命令提示符可以看出），请确保所有命令适用于Linux环境
}
```

### 3.2 管理后台配置（可选）

如果需要为管理后台提供单独的服务，可以创建单独的配置文件。请注意，此配置同样只包含server块，适合放在conf.d目录中。

**创建管理后台配置文件：**
```bash
nano /etc/nginx/conf.d/minsu-admin.conf
```

**配置内容：**
```nginx
# 管理后台配置 - Vue.js + Vite项目
server {
    listen 80;
    server_name admin.your-domain.com;
    
    # 重要注意事项：以下有两种配置方式，根据实际部署情况选择
    
    # 方式一：静态文件部署（适用于已构建的Vue.js项目）
    # Vue.js + Vite项目构建后的dist目录
    # 注意：确保此目录存在并且包含构建后的文件
    root /var/www/minsu/new_architecture/frontend/admin/dist;
    index index.html;

    # Vue.js应用的静态文件处理（SPA应用）
    location / {
        try_files $uri $uri/ /index.html;
        expires 7d;
    }

    # 静态资源缓存配置
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg)$ {
        expires 30d;
        add_header Cache-Control "public, max-age=2592000";
    }
    
    # 方式二：开发环境代理方式（可选，如果需要使用开发服务器）
    # 取消下面的注释并注释上面的静态文件配置即可使用
    # 适用于开发环境或需要动态更新的场景
    # location / {
    #     proxy_pass http://127.0.0.1:3001;
    #     proxy_http_version 1.1;
    #     proxy_set_header Upgrade $http_upgrade;
    #     proxy_set_header Connection 'upgrade';
    #     proxy_set_header Host $host;
    #     proxy_set_header X-Real-IP $remote_addr;
    #     proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    #     proxy_set_header X-Forwarded-Proto $scheme;
    #     
    #     # 解决502错误的关键设置
    #     proxy_connect_timeout 60s;
    #     proxy_send_timeout 60s;
    #     proxy_read_timeout 60s;
    # }

    # 后端API代理（管理后台API）
    location /api/ {
        # 非Docker环境必须使用127.0.0.1或localhost
        # 不要使用Docker环境中的容器名称
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 解决502错误的超时设置
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        
        # 缓冲区设置
        proxy_buffers 4 256k;
        proxy_buffer_size 128k;
        proxy_busy_buffers_size 256k;
        proxy_temp_file_write_size 256k;
    }
    
    # 错误页面
    error_page 404 /404.html;
    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /usr/share/nginx/html;
    }
    
    # 非Docker环境重要注意事项：
    # 1. 静态文件方式：确保dist目录存在并包含构建好的Vue.js文件
    # 2. 代理方式：确保Vue.js开发服务器在3001端口正确运行
    # 3. 验证文件权限：确保Nginx用户有权限访问dist目录
    # 4. 检查防火墙设置，确保相关端口未被阻止
}
```

**应用配置：**
```bash
# 验证配置
nginx -t

# 重载配置
systemctl reload nginx
```

## 4. 配置验证与重载

```bash
# 检查配置语法
nginx -t

# 重载配置（不会中断服务）
systemctl reload nginx

# 重启Nginx（会短暂中断服务）
systemctl restart nginx
```

## 5. 解决常见Nginx错误

### 5.0 修复配置重复导致的启动失败

如果遇到`Job for nginx.service failed`错误，很可能是因为配置文件中包含了重复的`events`或`http`块。主配置文件`/etc/nginx/nginx.conf`已经包含了这些块，而conf.d目录中的配置文件只应包含`server`块。

### 5.1 500 Internal Server Error错误

500错误表示服务器内部错误，通常与配置错误有关。根据我们的项目结构，可能的原因包括：

1. **文件路径错误**（常见问题）：
   ```bash
   # 检查前端client构建后的文件是否存在
   ls -la /var/www/minsu/new_architecture/frontend/client/.next
   
   # 检查管理后台构建后的文件是否存在
   ls -la /var/www/minsu/new_architecture/frontend/admin/dist
   ```

2. **Next.js服务未启动**：
   ```bash
   # 检查Next.js服务是否运行在端口3000
   netstat -tulpn | grep 3000
   
   # 如果未运行，启动Next.js服务
   cd /var/www/minsu/new_architecture/frontend/client
   npm start
   ```

3. **文件权限问题**：
   ```bash
   # 设置正确的文件权限
   chown -R www-data:www-data /var/www/minsu/
   chmod -R 755 /var/www/minsu/
   ```

4. **Nginx配置检查**：
   ```bash
   # 检查Nginx配置语法
   nginx -t
   
   # 查看Nginx错误日志中的具体错误信息
   tail -f /var/log/nginx/error.log
   ```

5. **针对Next.js项目的特殊检查**：
   - 确保Next.js服务在端口3000上正常运行
   - 确认Nginx配置中正确代理到了Next.js服务器地址
   - 检查Next.js服务的日志以获取更多信息

修复步骤：

```bash
# 查看当前错误详情
systemctl status nginx.service
journalctl -xe | grep nginx

# 检查配置文件
cat /etc/nginx/conf.d/minsu.conf

# 编辑配置文件，移除重复的events和http块
nano /etc/nginx/conf.d/minsu.conf

# 只保留server块部分，类似以下内容：
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    # 其他配置...
}
```

```bash
# 验证配置
nginx -t

# 重启服务
systemctl restart nginx.service
```

### 5.1 502 Bad Gateway错误

502错误通常表示Nginx无法连接到后端服务。这是代理模式下最常见的错误，**非Docker环境**特别需要注意以下排查步骤：

1. **检查所有被代理的服务是否运行**（前端、管理后台、后端API）：
   ```bash
   # 检查后端API服务（端口8000）
   ps aux | grep uvicorn
   # 或者使用systemctl（如果通过systemd管理）
   systemctl status minsu-backend.service
   
   # 检查前端服务（端口3000）
   ps aux | grep node
   # 检查管理后台服务（端口3001）
   ps aux | grep node
   ```

2. **验证端口是否正确监听**：
   ```bash
   # 检查所有相关端口
   netstat -tulpn | grep -E '3000|3001|8000'
   # 或者使用lsof（如果安装了）
   lsof -i :3000
   lsof -i :3001
   lsof -i :8000
   ```

3. **直接测试服务是否可访问**（关键排查步骤）：
   ```bash
   # 测试前端服务
   curl -I http://127.0.0.1:3000
   # 测试管理后台服务
   curl -I http://127.0.0.1:3001
   # 测试后端API
   curl -I http://127.0.0.1:8000/api/health
   ```

4. **检查防火墙设置**：
   ```bash
   # Ubuntu/Debian系统
   ufw status
   # CentOS/RHEL系统
   firewall-cmd --list-ports
   # 如果需要开放端口
   ufw allow 3000/tcp
   ufw allow 3001/tcp
   ufw allow 8000/tcp
   ```

5. **关键配置：确保所有location块都有适当的超时设置**：
   ```nginx
   # 在每个proxy_pass的location块中添加（前端、管理后台、API）
   proxy_connect_timeout 60s;  # 连接超时时间
   proxy_send_timeout 60s;     # 发送超时时间
   proxy_read_timeout 60s;     # 读取超时时间
   
   # 缓冲区设置也很重要
   proxy_buffers 4 256k;
   proxy_buffer_size 128k;
   proxy_busy_buffers_size 256k;
   proxy_temp_file_write_size 256k;
   ```

6. **检查Nginx错误日志获取详细错误信息**：
   ```bash
   tail -n 100 /var/log/nginx/error.log
   ```

7. **验证Nginx配置语法**：
   ```bash
   nginx -t
   ```

8. **非Docker环境特别注意事项**：
   - 确保使用127.0.0.1或localhost，而不是Docker容器名
   - 检查服务是否绑定到0.0.0.0或127.0.0.1（不是仅绑定到容器内部IP）
   - 确保没有其他服务占用相同端口
   - 检查SELinux设置（如果使用CentOS/RHEL）：
     ```bash
     sestatus
     # 如果需要临时禁用（仅测试）
     setenforce 0
     ```

**502错误快速排查流程**：
1. 首先验证每个被代理的服务单独是否可访问（使用curl命令）
2. 确认端口监听状态（netstat或lsof）
3. 检查防火墙设置
4. 查看Nginx错误日志获取具体错误信息
5. 确保所有代理location块都有超时和缓冲区设置

### 5.2 504 Gateway Timeout错误

504错误表示请求超时。解决方法：

1. 增加超时设置（同上）

2. 检查后端服务性能

3. 增加worker_processes数量：
   ```nginx
   worker_processes auto;  # 或设置为CPU核心数
   ```

### 5.3 403 Forbidden错误

1. 检查文件权限：
   ```bash
   chown -R www-data:www-data /var/www/minsu/new_architecture/frontend/client/dist
   ```

2. 检查SELinux设置（CentOS/RHEL）：
   ```bash
   setenforce 0  # 临时关闭SELinux
   ```

## 6. 性能优化

### 6.1 基本优化

**注意**：以下优化配置应添加到主配置文件`/etc/nginx/nginx.conf`的http块中，而不是conf.d目录下的站点配置文件中：

在`nginx.conf`文件的http块中添加：

```nginx
# 连接处理优化
worker_rlimit_nofile 100000;

# 压缩设置（已在基本配置中）
gzip on;
gzip_comp_level 6;
gzip_min_length 256;
gzip_proxied any;
gzip_vary on;

# 客户端请求缓冲区
client_body_buffer_size 128k;
client_max_body_size 10m;
client_header_buffer_size 1k;
large_client_header_buffers 4 4k;
output_buffers 1 32k;
postpone_output 1460;
```

### 6.2 缓存配置

添加缓存区域：

```nginx
# 在http块中添加
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=api_cache:10m max_size=1g inactive=60m;
proxy_temp_path /var/cache/nginx/temp;

# 在location /api/块中使用缓存
proxy_cache api_cache;
proxy_cache_valid 200 302 10m;
proxy_cache_valid 404 1m;
proxy_cache_use_stale error timeout updating http_500 http_502 http_503 http_504;
add_header X-Cache-Status $upstream_cache_status;
```

## 7. SSL配置

### 7.1 使用Let's Encrypt配置SSL

```bash
# 安装Certbot
apt install certbot python3-certbot-nginx -y

# 申请证书（自动配置Nginx）
certbot --nginx -d your-domain.com -d www.your-domain.com

# 验证证书自动续期
systemctl status certbot.timer
```

### 7.2 手动SSL配置

**注意**：SSL配置同样只包含server块，替换之前的HTTP配置或创建新文件：

```nginx
# SSL配置 - 非Docker环境版本
server {
    listen 443 ssl;
    server_name your-domain.com www.your-domain.com;
    
    # SSL证书配置
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    # SSL优化
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384';
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 1d;
    ssl_session_tickets off;
    
    # OCSP Stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    resolver 8.8.8.8 8.8.4.4 valid=300s;
    resolver_timeout 5s;
    
    # 前端代理 - 非Docker环境配置
    location / {
        # 确保前端服务在3000端口正确运行
        # 非Docker环境必须使用127.0.0.1或localhost
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 解决502错误的关键设置
        # 这些设置确保代理连接稳定，避免超时和连接失败
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        
        # 确保代理缓冲区配置正确
        proxy_buffers 4 256k;
        proxy_buffer_size 128k;
        proxy_busy_buffers_size 256k;
        proxy_temp_file_write_size 256k;
    }
    
    # 管理后台代理 - 非Docker环境配置
    location /admin {
        # 确保管理后台服务在3001端口正确运行
        proxy_pass http://127.0.0.1:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 解决502错误的关键设置
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # 后端API代理 - 非Docker环境配置
    location /api/ {
        # 确保后端API服务在8000端口正确运行
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        
        # 解决502错误的超时设置
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        
        # 缓冲区设置
        proxy_buffers 4 256k;
        proxy_buffer_size 128k;
        proxy_busy_buffers_size 256k;
        proxy_temp_file_write_size 256k;
    }
    
    # HSTS头
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # 错误页面
    error_page 404 /404.html;
    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /usr/share/nginx/html;
    }
    
    # 非Docker环境重要注意事项：
    # 1. 确保所有代理的服务（3000, 3001, 8000端口）都在本地正确运行
    # 2. 检查防火墙设置，确保端口未被阻止
    # 3. 验证每个服务都能通过curl命令直接访问（如：curl http://127.0.0.1:3000）
    # 4. 确保SSL证书路径正确且Nginx用户有权限访问
    # 5. 502错误排查：首先检查被代理的服务是否正常运行，其次检查防火墙设置，最后检查Nginx配置语法
}

# HTTP重定向到HTTPS
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    return 301 https://$host$request_uri;
}
```

## 8. 安全配置

### 8.1 基本安全头

在server块中添加：

```nginx
# 安全响应头
add_header X-Content-Type-Options nosniff;
add_header X-Frame-Options SAMEORIGIN;
add_header X-XSS-Protection "1; mode=block";
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'";
```

### 8.2 限制访问

```nginx
# 限制某些路径访问
location ~ /\.(?!well-known) {
    deny all;
}

# 限制API访问（可选）
location /api/admin/ {
    allow 192.168.1.0/24;  # 允许内网访问
    deny all;  # 拒绝其他所有访问
    
    proxy_pass http://127.0.0.1:8000;
    # 其他代理设置...
}
```

## 9. 日志管理

### 9.1 日志轮转配置

```bash
nano /etc/logrotate.d/nginx
```

配置内容：

```
/var/log/nginx/*.log {
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

### 9.2 自定义日志格式

在nginx.conf的http块中添加自定义日志格式：

```nginx
log_format detailed '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for" '
                    '$request_time $upstream_response_time $pipe $upstream_cache_status';

# 使用自定义格式
access_log /var/log/nginx/access.log detailed;
```

## 10. 监控与维护

### 10.1 检查Nginx状态

```bash
# 检查服务状态
systemctl status nginx

# 查看连接数
netstat -an | grep ESTABLISHED | wc -l

# 查看请求数（实时）
watch -n1 'netstat -an | grep ESTABLISHED | wc -l'
```

### 10.2 常用命令

```bash
# 启动服务
systemctl start nginx

# 停止服务
systemctl stop nginx

# 重启服务
systemctl restart nginx

# 重载配置
systemctl reload nginx

# 查看错误日志
journalctl -u nginx
cat /var/log/nginx/error.log
```

---

本文档提供了详细的Nginx配置指南，重点解决了可能出现的502错误问题，并提供了性能优化和安全配置建议。请根据实际环境调整相关参数。

> **重要说明**：本配置适用于直接部署在服务器上的环境，不依赖Docker容器。确保所有服务（前端静态文件、后端API）都正确安装和运行在指定端口上。
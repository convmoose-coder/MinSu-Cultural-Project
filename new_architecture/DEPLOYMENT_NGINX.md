# Nginx反向代理配置指南

## 配置说明

Nginx作为反向代理服务器，将请求分发到不同的后端服务：

- 用户端前端: http://localhost:3000
- 管理后台前端: http://localhost:3001
- 后端API: http://localhost:8000

## Nginx配置文件

```nginx
events {
    worker_connections 1024;
}

http {
    upstream frontend_client {
        server frontend-client:3000;
    }

    upstream frontend_admin {
        server frontend-admin:3001;
    }

    upstream backend {
        server backend:8000;
    }

    server {
        listen 80;

        location / {
            proxy_pass http://frontend_client;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /admin {
            proxy_pass http://frontend_admin;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /api/ {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

## 部署步骤

1. 将Nginx配置文件复制到服务器的Nginx配置目录中
2. 重启Nginx服务使配置生效：
   ```bash
   sudo systemctl restart nginx
   ```
3. 验证Nginx配置是否正确：
   ```bash
   sudo nginx -t
   ```

## 常用Nginx命令

- 启动Nginx：
  ```bash
  sudo systemctl start nginx
  ```
- 停止Nginx：
  ```bash
  sudo systemctl stop nginx
  ```
- 重新加载Nginx配置：
  ```bash
  sudo systemctl reload nginx
  ```
- 查看Nginx状态：
  ```bash
  sudo systemctl status nginx
  ```
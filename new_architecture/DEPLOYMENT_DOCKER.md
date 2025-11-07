# Docker容器化部署指南

## 项目结构

```
new_architecture/
├── backend/
│   ├── app/
│   ├── requirements.txt
│   └── ...
├── frontend/
│   ├── client/
│   └── admin/
├── docker/
│   ├── docker-compose.yml
│   ├── frontend.Dockerfile
│   ├── backend.Dockerfile
│   └── nginx/
│       ├── Dockerfile
│       └── nginx.conf
```

## 部署步骤

1. 确保已安装Docker和Docker Compose
2. 在项目根目录下运行以下命令启动所有服务：
   ```bash
   docker-compose up -d
   ```
3. 首次部署时，可能需要运行数据库迁移：
   ```bash
   docker-compose exec backend alembic upgrade head
   ```

## 服务访问地址

- 用户端前端: http://localhost:3000
- 管理后台前端: http://localhost:3001
- 后端API: http://localhost:8000
- Nginx代理: http://localhost

## 常用Docker命令

- 查看运行中的容器：
  ```bash
  docker-compose ps
  ```
- 查看容器日志：
  ```bash
  docker-compose logs <service_name>
  ```
- 停止所有服务：
  ```bash
  docker-compose down
  ```
- 重新构建并启动服务：
  ```bash
  docker-compose up -d --build
  ```
# 云服务器部署指南

## 环境要求

- Ubuntu 20.04 LTS 或更高版本
- 至少 2GB RAM, 2 vCPUs
- 至少 20GB 磁盘空间
- 已安装 Docker 和 Docker Compose

## 部署步骤

### 1. 连接到云服务器

使用SSH连接到您的云服务器：
```bash
ssh username@your_server_ip
```

### 2. 安装Docker和Docker Compose

```bash
# 更新包索引
sudo apt update

# 安装必要的包
sudo apt install apt-transport-https ca-certificates curl software-properties-common

# 添加Docker官方GPG密钥
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# 添加Docker官方仓库
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# 更新包索引
sudo apt update

# 安装Docker
sudo apt install docker-ce

# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# 给Docker Compose执行权限
sudo chmod +x /usr/local/bin/docker-compose
```

### 3. 上传项目文件

将项目文件上传到云服务器，可以使用`scp`命令或Git：
```bash
# 使用scp上传（在本地执行）
scp -r /path/to/new_architecture username@your_server_ip:/home/username/

# 或者在服务器上克隆Git仓库
git clone your_repository_url
```

### 4. 配置环境变量

在`new_architecture/backend/app/core/config.py`文件中修改数据库连接信息和其他敏感配置。

### 5. 启动服务

```bash
# 进入项目目录
cd new_architecture/docker

# 启动所有服务
docker-compose up -d
```

### 6. 配置防火墙

```bash
# 允许HTTP和HTTPS流量
sudo ufw allow 80
sudo ufw allow 443

# 启用防火墙
sudo ufw enable
```

### 7. 配置SSL证书（可选但推荐）

使用Let's Encrypt获取免费SSL证书：
```bash
# 安装Certbot
sudo apt install certbot python3-certbot-nginx

# 获取SSL证书
sudo certbot --nginx -d your_domain.com
```

## 监控和维护

### 查看服务状态
```bash
docker-compose ps
```

### 查看日志
```bash
docker-compose logs <service_name>
```

### 更新部署
```bash
# 拉取最新代码
git pull

# 重新构建并启动服务
docker-compose up -d --build
```

## 常见问题

### 1. 服务无法启动
检查Docker和Docker Compose是否正确安装，并查看容器日志。

### 2. 数据库连接失败
检查数据库配置是否正确，确保PostgreSQL容器正常运行。

### 3. Nginx配置问题
检查Nginx配置文件是否正确，确保端口映射无误。
# 推送代码到GitHub的说明

## 步骤1：在GitHub上创建仓库

1. 登录到您的GitHub账户
2. 点击右上角的 "+" 号，选择 "New repository"
3. 仓库名称输入：`MinSu-Cultural-Project`
4. 描述输入：`民族文化展示项目，包含前后端分离的管理系统`
5. 选择公共仓库（Public）
6. 不要初始化README、.gitignore或license
7. 点击 "Create repository"

## 步骤2：推送代码到GitHub

创建仓库后，按照以下步骤推送代码：

```bash
# 添加远程仓库（将YOUR_USERNAME替换为您的GitHub用户名）
git remote add origin https://github.com/YOUR_USERNAME/MinSu-Cultural-Project.git

# 验证远程仓库已添加
git remote -v

# 推送代码到GitHub
git push -u origin master
```

## 项目信息

这个项目是一个完整的民族文化展示系统，包含：

- 前端Vue.js应用程序（用户端和管理后台）
- 后端Flask API服务
- MySQL数据库集成
- 完整的管理员功能（登录、注册、内容管理等）
- 前后端分离的安全机制
- 响应式设计和中国传统风格的UI

## 项目结构

- `app/` - 后端Flask应用程序
- `frontend/` - 前端Vue.js应用程序
- `scripts/` - 数据库初始化和管理脚本
- `templates/` - 传统HTML模板（备用方案）

## 环境要求

- Python 3.8+
- Node.js 16+
- MySQL 8.0+
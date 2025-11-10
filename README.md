# 乘灼展示项目

**最后更新时间：2024年8月15日 10:30:00**
<!-- 此时间会在下次更新时自动更新为本地时间 -->

## 项目状态

🔄 **项目进行中** - 核心功能开发中，持续优化和更新

本项目正在积极开发中，包含传统架构和新架构两种实现。当前已完成基础的前后端分离架构搭建，正在进行功能完善和性能优化。项目提供了完整的部署文档和测试验证脚本，支持多种部署方式。

## 项目简介

这是一个完整的乘灼展示系统，采用前后端分离架构，包含用户端前台。项目融合了中国传统元素与现代Web技术，为用户提供沉浸式的乘灼体验。

## 最新功能更新

### 架构升级
- **新架构实现**：增加了 <mcfolder name="new_architecture" path="e:/ChengZhuo/MinSu-Cultural-Project/new_architecture"></mcfolder> 目录，包含现代化的前后端实现
- **多部署方式支持**：添加Docker、云服务和Nginx三种部署方案

### UI/UX优化
- **内容背景设计**：为内容区域添加了中国传统风格的渐变背景和传统纹样
- **导航栏优化**：调整了导航链接的位置和文本，提升用户体验
- **响应式设计**：确保在不同设备上都能获得良好的浏览体验

### 技术升级
- **前后端分离**：完善的Vue.js前端和Python后端架构
- **TypeScript支持**：增加了TypeScript类型定义，提升代码质量
- **MCP服务集成**：添加MySQL MCP服务支持，增强数据库交互能力

## 项目结构

```
MinSu-Cultural-Project/
├── .env.example                 # 环境变量示例文件
├── .gitignore                   # Git忽略配置
├── README.md                    # 项目说明文档
├── frontend/                    # 前端Vue.js应用程序
│   ├── index.html               # HTML入口文件
│   ├── package-lock.json        # npm依赖锁定文件
│   ├── package.json             # npm依赖配置
│   ├── src/                     # 前端源代码
│   │   ├── App.vue              # 主应用组件
│   │   ├── main.js              # 应用入口文件
│   │   ├── api/                 # API请求定义
│   │   ├── assets/              # 静态资源文件
│   │   ├── components/          # 可复用组件
│   │   ├── composables/         # 组合式函数
│   │   ├── router/              # 路由配置
│   │   ├── stores/              # 状态管理
│   │   ├── types/               # TypeScript类型定义
│   │   ├── utils/               # 工具函数
│   │   └── views/               # 页面组件
│   ├── tsconfig.json            # TypeScript配置
│   ├── tsconfig.node.json       # Node环境TypeScript配置
│   └── vite.config.js           # Vite构建配置
├── new_architecture/            # 新架构实现
│   ├── DEPLOYMENT_CLOUD.md      # 云部署文档
│   ├── DEPLOYMENT_DOCKER.md     # Docker部署文档
│   ├── DEPLOYMENT_NGINX.md      # Nginx部署文档
│   ├── README.md                # 新架构说明
│   ├── backend/                 # 新后端服务
│   │   ├── app/                 # 后端应用代码
│   │   └── requirements.txt     # Python依赖
│   ├── docker/                  # Docker配置
│   │   ├── backend.Dockerfile   # 后端Dockerfile
│   │   ├── docker-compose.yml   # Docker Compose配置
│   │   ├── frontend.Dockerfile  # 前端Dockerfile
│   │   └── nginx/               # Nginx配置
│   └── frontend/                # 新前端实现
│       ├── admin/               # 管理端
│       └── client/              # 客户端
├── scripts/                     # 系统管理脚本
│   ├── direct_start_mcp.bat     # MCP直接启动脚本
│   ├── start_mysql_mcp_server.py# MySQL MCP服务启动
│   └── update_database.py       # 数据库更新脚本
├── tests/                       # 测试文件
│   ├── test_db_connection.py    # 数据库连接测试
│   ├── test_mcp_client.py       # MCP客户端测试
│   └── test_mysql.py            # MySQL测试
└── test_db_connection.py        # 根目录数据库连接测试
```

## 技术栈

### 后端
- Python 3.8+
- Flask Web框架
- MySQL 8.0+ 数据库
- SQLAlchemy ORM
- Pydantic 数据验证


### 前端
- Vue 3 (Composition API)
- Vue Router
- Pinia 状态管理
- Sass 样式预处理器
- Axios HTTP客户端
- Vite 构建工具

## 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+ 或 18+
- MySQL 8.0+
- Docker (可选，用于容器化部署)

### 后端设置

1. 安装Python依赖：

```bash
pip install -r requirements.txt
```

2. 配置环境变量：

确保`.env`文件中包含正确的数据库连接信息：

```
MYSQL_HOST=8.138.227.227
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=Fzy025897758.
MYSQL_DATABASE=MinSu
```

3. 启动后端服务：

### 开发环境启动

```bash
python app.py
```

后端服务将在 http://localhost:5000 上运行。

### 生产环境部署

项目提供多种部署方式，请参考对应的部署文档：

1. **Docker部署**：查看 <mcfile name="DEPLOYMENT_DOCKER.md" path="e:/ChengZhuo/MinSu-Cultural-Project/new_architecture/DEPLOYMENT_DOCKER.md"></mcfile>
2. **云服务部署**：查看 <mcfile name="DEPLOYMENT_CLOUD.md" path="e:/ChengZhuo/MinSu-Cultural-Project/new_architecture/DEPLOYMENT_CLOUD.md"></mcfile>
3. **Nginx部署**：查看 <mcfile name="DEPLOYMENT_NGINX.md" path="e:/ChengZhuo/MinSu-Cultural-Project/new_architecture/DEPLOYMENT_NGINX.md"></mcfile>

对于传统部署，可以使用Gunicorn：

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### 前端设置

1. 安装Node.js依赖：

```bash
cd frontend
npm install
```

2. 启动用户端前台服务：

```bash
npm run dev
```

用户端前台服务将在 http://localhost:5173 上运行。

#### 新架构前端设置

1. 客户端设置：

```bash
cd new_architecture/frontend/client
npm install
npm run dev
```

2. 管理端设置：

```bash
cd new_architecture/frontend/admin
npm install
npm run dev
```

### 常见问题解决

1. **数据库连接问题**：
   - 使用专门的数据库连接测试工具诊断问题：
     ```bash
     python test_db_connection.py
     ```
   - 检查环境变量配置是否正确（参考 `.env.example`）
   - 确认MySQL用户权限设置
   - 运行测试脚本验证连接：`python tests/test_db_connection.py`

2. **图片加载问题**：
   - 确保图片路径使用正确的格式
   - 检查文件权限设置
   - 清除浏览器缓存后重试

3. **启动错误**：
   - 确认依赖安装完整：`npm install` 和 `pip install -r requirements.txt`
   - 检查端口是否被占用
   - 查看详细错误日志进行排查

## API接口

### 用户端前台API (前缀: /api)

- `GET /api/folkcultures` - 获取所有民俗文化列表（支持分页、搜索和筛选）
- `GET /api/folkcultures/<id>` - 获取指定ID的民俗文化详情
- `GET /api/regions` - 获取所有地区列表
- `GET /api/categories` - 获取所有分类列表

## 功能特点

### 用户端前台
- 民俗文化展示与浏览
- 按地区和分类筛选查看
- 搜索功能，支持关键词搜索
- 文化详情页面，展示完整信息
- 响应式设计，适配各种设备
- 中国传统风格UI设计，展现民俗文化特色
- 加载动画和错误处理机制

## 核心功能模块

### 传统架构功能
- **民俗文化展示与浏览**：包含列表页和详情页
- **搜索与筛选**：支持按名称搜索、按地区和分类筛选
- **传统风格UI**：中国传统元素融合现代设计
- **响应式布局**：适配不同设备屏幕

### 新架构功能
- **前后端完全分离**：现代化的API设计和前端实现
- **管理端功能**：提供内容管理和系统配置能力
- **Docker支持**：简化部署和环境配置
- **多环境适配**：开发、测试、生产环境配置

## 注意事项

1. 确保MySQL数据库已启动并创建了对应的数据库
2. 首次运行时，需要执行数据库初始化脚本：
   ```bash
   python scripts/init_database.py
   ```
   或使用Flask应用自动创建所需的数据表
3. 前端开发服务器通过代理将API请求转发到后端服务
4. 项目支持热模块替换(HMR)，开发过程中修改代码会自动刷新

## 开发指南

### 后端开发

1. **传统后端开发**：
   - 添加新的数据模型：在相关目录下创建模型文件
   - 添加新的API路由：定义路由函数
   - 实现业务逻辑：创建对应的服务
   - 数据验证：定义请求和响应模式

2. **新架构后端开发**：
   - 参考 `new_architecture/backend/app/` 目录结构
   - 遵循Flask应用工厂模式
   - 使用蓝图组织路由
   - 实现RESTful API设计

### 前端开发

1. **传统前端开发**：
   - 添加新的页面：在`src/views/`目录下创建Vue组件
   - 注册路由：在`src/router/index.js`中添加路由配置
   - 创建可复用组件：在`src/components/`目录下开发组件
   - 添加状态管理：在`src/stores/`目录下定义Pinia store
   - 添加业务逻辑：在`src/composables/`目录下创建组合式函数

2. **新架构前端开发**：
   - 客户端开发：`new_architecture/frontend/client/`
   - 管理端开发：`new_architecture/frontend/admin/`
   - 遵循组件化开发规范
   - 使用TypeScript确保类型安全

## 部署

### 前端构建
1. 构建用户端前台：
   ```bash
   cd frontend
   npm run build
   ```

### 后端部署
1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 设置环境变量（参考 `.env.example` 文件）
   
   在Linux服务器上，请确保正确配置数据库连接信息：
   ```bash
   # 创建 .env 文件并根据实际情况修改以下配置
   cp .env.example .env
   nano .env  # 或使用其他文本编辑器编辑
   
   # 确保设置了正确的数据库凭据
   MYSQL_HOST=localhost           # Linux服务器上的数据库主机
   MYSQL_PORT=3306               # 数据库端口
   MYSQL_USER=your_linux_user    # Linux服务器上的数据库用户名
   MYSQL_PASSWORD=your_password  # 对应用户的数据库密码
   MYSQL_DATABASE=MinSu          # 数据库名称
   SECRET_KEY=your_secret_key    # Flask密钥，应更改为强随机字符串
   ```

3. 初始化数据库：
   ```bash
   python init_db.py
   ```



5. 运行应用：
   ```bash
   python app.py
   ```
### 部署选项

项目提供三种主要部署方式：

1. **Docker容器化部署**
   - 最推荐的部署方式
   - 包含完整的Docker配置
   - 一键部署整个应用栈
   - 适合开发、测试和生产环境

2. **云服务部署**
   - 支持主流云服务提供商
   - 包含云服务特定的配置指南
   - 适合生产环境

3. **Nginx反向代理部署**
   - 传统部署方式
   - 提供完整的Nginx配置示例
   - 适合需要自定义服务器配置的场景

详细部署指南请参考 <mcfolder name="new_architecture" path="e:/ChengZhuo/MinSu-Cultural-Project/new_architecture"></mcfolder> 目录下的对应文档。

## 性能优化

- 前端使用懒加载和代码分割
- 图片资源优化
- API响应数据缓存
- 数据库查询优化

## License

MIT
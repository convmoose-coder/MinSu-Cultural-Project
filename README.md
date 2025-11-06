# 民族文化展示项目

**最后更新时间：2025年11月07日 10:30:00**
<!-- 此时间会在下次更新时自动更新为本地时间 -->

## 项目状态

✅ **项目已完成** - 所有核心功能和安全机制已实现并通过测试验证

本项目已按计划完成所有功能开发，包括前后端分离架构、安全机制、用户端前台、管理后台等核心模块。项目具备完整的部署文档和测试验证报告，可以投入实际使用。

## 项目简介

这是一个完整的民族文化展示系统，采用前后端分离架构，包含用户端前台和管理后台两部分。项目融合了中国传统元素与现代Web技术，为用户提供沉浸式的民族文化体验。

## 最新功能更新

### 用户体验优化
- **首页性能优化**：修复了首页异常抖动问题，提升页面加载速度
- **图片加载优化**：修复了所有图片404问题，确保所有图片正确加载
- **错误处理改进**：增强了错误处理机制，提升系统稳定性

### 技术细节与问题解决
- **图片路径问题修复**：
  - 修复了管理后台所有默认图片路径配置问题
  - 添加了正确的`/admin`前缀以适配Vite的资源处理机制
  - 修复了所有类型图片（culture, region, category, user, logo）的加载问题
- **关键技术点**：
  - Vue 3 Composition API
  - 响应式数据处理
  - 组件化开发
  - Vite资源处理机制

## 项目结构

```
MinSu/
├── application/                   # 后端Flask应用程序
│   ├── __init__.py               # 应用初始化文件
│   ├── models/                   # 数据模型定义
│   │   ├── __init__.py
│   │   ├── admin_user.py         # 管理员用户模型
│   │   └── folk_culture.py       # 民俗文化数据模型
│   ├── routes/                   # API路由配置
│   │   ├── __init__.py
│   │   ├── admin_routes.py       # 管理后台API路由
│   │   ├── folk_culture_routes.py# 民俗文化相关API路由
│   │   └── front_routes.py       # 前台API路由
│   ├── schemas/                  # 数据验证模式
│   │   ├── __init__.py
│   │   └── folk_culture.py       # 民俗文化数据验证模式
│   ├── services/                 # 业务逻辑层
│   │   ├── __init__.py
│   │   └── folk_culture_service.py# 民俗文化业务逻辑实现
│   └── utils/                    # 后端工具函数
│       ├── __init__.py
│       └── db.py                 # 数据库连接工具
├── frontend/                     # 前端Vue.js应用程序
│   ├── src/                      # 前端源代码
│   │   ├── App.vue               # 前台主应用组件
│   │   ├── AdminApp.vue          # 后台管理主应用组件
│   │   ├── main.js               # 前台应用入口文件
│   │   ├── admin-main.js         # 后台管理应用入口文件
│   │   ├── assets/               # 静态资源文件
│   │   │   ├── images/           # 图片资源
│   │   │   ├── styles/           # 样式文件
│   │   │   └── ...               # 其他静态资源
│   │   ├── components/           # 可复用UI组件
│   │   │   ├── FolkCultureCard.vue # 民俗文化卡片组件
│   │   │   ├── CustomButton.vue    # 自定义按钮组件
│   │   │   ├── LoadingSpinner.vue  # 加载动画组件
│   │   │   └── admin/              # 后台管理专用组件
│   │   ├── views/                # 页面组件
│   │   │   ├── HomeView.vue      # 首页
│   │   │   ├── CultureListView.vue# 民俗文化列表页
│   │   │   ├── CultureDetailView.vue# 民俗文化详情页
│   │   │   ├── AboutView.vue     # 关于页面
│   │   │   └── admin/            # 后台管理页面组件
│   │   ├── router/               # 路由配置
│   │   │   ├── index.js          # 前台路由配置
│   │   │   └── admin/            # 后台路由配置
│   │   ├── stores/               # 状态管理(Pinia)
│   │   │   ├── folkCultureStore.js # 民俗文化状态管理
│   │   │   └── admin/            # 后台状态管理
│   │   ├── services/             # API服务封装
│   │   │   ├── folkCultureService.js # 民俗文化相关服务
│   │   │   ├── api.js            # 通用API封装
│   │   │   └── admin/            # 后台API服务
│   │   ├── api/                  # API请求定义
│   │   │   ├── frontendApi.js    # 前台API实例
│   │   │   ├── adminApi.js       # 后台API实例
│   │   │   ├── culture.js        # 民俗文化API定义
│   │   │   └── index.js          # API索引文件
│   │   ├── composables/          # 组合式函数
│   │   │   └── useDataFetching.js # 数据获取组合式函数
│   │   ├── utils/                # 前端工具函数
│   │   └── types/                # TypeScript类型定义
│   ├── package.json              # Node.js依赖配置
│   ├── vite.config.js            # 前台构建配置
│   └── vite.admin.config.js      # 后台构建配置
├── scripts/                      # 数据库和系统管理脚本
│   ├── init_database.py          # 数据库初始化脚本
│   ├── init_admin_user.py        # 管理员用户初始化脚本
│   └── ...                       # 其他管理脚本
├── templates/                    # 传统HTML模板（备用方案）
│   └── front/                    # 前台传统页面模板
├── requirements.txt              # Python依赖包列表
├── app.py                        # Flask应用主文件
├── create_test_admin.py         # 测试管理员创建脚本
├── init_db.py                   # 数据库初始化脚本
└── ...                          # 其他配置和文档文件
```

## 技术栈

### 后端
- Python 3.8+
- Flask Web框架
- MySQL 8.0+ 数据库
- SQLAlchemy ORM
- Pydantic 数据验证
- JWT 身份认证

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
- Node.js 16+
- MySQL 8.0+

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

### 生产环境部署（使用Gunicorn）

安装Gunicorn：

```bash
pip install gunicorn
```

使用Gunicorn启动应用：

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

或者使用应用工厂模式：

```bash
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
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

3. 启动管理后台服务（新终端）：

```bash
npm run dev:admin
```

管理后台服务将在 http://localhost:5174 上运行。

### 常见问题解决

如果遇到图片无法加载或页面异常抖动的问题，请检查以下几点：

1. 确保`src/assets/images/defaultImages.js`文件中的图片路径格式正确，应该使用相对路径而非别名：
   ```javascript
   // 正确的写法
   region: '/src/assets/images/placeholder-region.jpg'
   
   // 错误的写法
   region: '@/assets/images/placeholder-region.jpg'
   ```

2. 如果修改了图片路径后仍未解决问题，请重启开发服务器：
   ```bash
   # 在frontend目录下
   npm run dev
   ```

3. 数据库连接问题：
   - 使用专门的数据库连接测试工具诊断问题：
     ```bash
     python test_db_connection.py
     ```
   - 检查环境变量配置是否正确
   - 确认MySQL用户权限设置
   - 查看DEPLOYMENT_LINUX.md文件中的详细解决方案

## API接口

### 用户端前台API (前缀: /api)

- `GET /api/folkcultures` - 获取所有民俗文化列表（支持分页、搜索和筛选）
- `GET /api/folkcultures/<id>` - 获取指定ID的民俗文化详情
- `GET /api/regions` - 获取所有地区列表
- `GET /api/categories` - 获取所有分类列表

### 管理后台API (前缀: /api/admin)

#### 认证相关
- `POST /api/admin/auth/login` - 管理员登录
- `POST /api/admin/auth/register` - 管理员注册
- `POST /api/admin/auth/refresh` - 刷新JWT令牌
- `POST /api/admin/auth/change-password` - 修改管理员密码

#### 数据管理
- `GET /api/admin/dashboard` - 获取仪表盘数据
- `GET /api/admin/dashboard/stats` - 获取统计信息
- `GET /api/admin/dashboard/recent` - 获取最近数据
- `GET /api/admin/dashboard/distribution/<type>` - 获取数据分布
- `POST /api/admin/batch-upload` - 批量上传文化数据

## 功能特点

### 用户端前台
- 民俗文化展示与浏览
- 按地区和分类筛选查看
- 搜索功能，支持关键词搜索
- 文化详情页面，展示完整信息
- 响应式设计，适配各种设备
- 中国传统风格UI设计，展现民俗文化特色
- 加载动画和错误处理机制

### 管理后台
- 管理员身份认证系统（登录/注册/令牌刷新）
- 数据仪表盘和统计分析
- 文化数据批量上传功能
- 安全密码管理和修改
- 前后端分离安全机制
- Referer验证防止直接API访问
- JWT令牌认证和权限控制

## 核心功能模块

### 文化列表页面
- 支持按名称搜索
- 支持按地区和分类筛选
- 响应式网格布局
- 中国传统卷轴风格设计

### 文化详情页面
- 展示完整的文化信息
- 相关文化推荐
- 图片展示

### 导航系统
- 中国传统红色主题
- 响应式设计，移动端友好
- 平滑过渡动画

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

1. 添加新的数据模型：在`application/models/`目录下创建新的模型文件
2. 添加新的API路由：在`application/routes/`目录下定义新的路由函数
3. 实现业务逻辑：在`application/services/`目录下创建对应的服务
4. 数据验证：在`application/schemas/`目录下定义请求和响应模式

### 前端开发

1. 添加新的页面：在`src/views/`目录下创建新的Vue组件
2. 注册路由：在`src/router/index.js`中添加新的路由配置
3. 创建可复用组件：在`src/components/`目录下开发组件
4. 添加状态管理：在`src/stores/`目录下定义Pinia store
5. 添加业务逻辑：在`src/composables/`目录下创建组合式函数

## 部署

### 前端构建
1. 构建用户端前台：
   ```bash
   cd frontend
   npm run build
   ```

2. 构建管理后台：
   ```bash
   cd frontend
   npm run build:admin
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

4. 创建初始管理员账户：
   ```bash
   python create_test_admin.py
   ```

5. 运行应用：
   ```bash
   python app.py
   ```
### Linux服务器部署

详细部署指南请参考 [DEPLOYMENT_LINUX.md](DEPLOYMENT_LINUX.md) 文件，其中包含了完整的Linux服务器部署步骤，包括：
- 环境准备和依赖安装
- 数据库配置和初始化
- 前后端服务部署
- Nginx反向代理配置
- SSL证书配置
- 服务管理和监控

## 性能优化

- 前端使用懒加载和代码分割
- 图片资源优化
- API响应数据缓存
- 数据库查询优化

## License

MIT
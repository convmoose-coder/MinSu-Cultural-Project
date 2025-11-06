# 中国民俗文化网站

**最后更新时间：2025年11月06日 13:22:21**
<!-- 此时间会在下次更新时自动更新为本地时间 -->

这是一个展示中国民俗文化的全栈网站，使用Vue 3作为前端框架，Flask作为后端API框架，专注于中国传统民俗文化的展示与传播。

## 🚀 最新功能更新

### 安全机制增强
- ✅ **前后端分离安全机制**：实现用户端前台和管理后台的完全分离
- ✅ **独立端口部署**：前台服务(5173)和管理后台服务(5174)独立运行
- ✅ **Referer验证中间件**：防止直接通过URL访问管理后台API
- ✅ **JWT令牌认证**：管理员身份验证和权限控制

### 管理后台功能
- ✅ **管理员登录/注册系统**：完整的身份验证流程
- ✅ **数据仪表盘**：统计信息展示和数据分析
- ✅ **批量上传功能**：支持文化数据的批量导入
- ✅ **安全密码管理**：密码哈希存储和修改功能

### 用户体验优化
- ✅ **首页性能优化**：修复页面异常抖动问题，提升加载速度
- ✅ **图片加载优化**：修复默认图片路径问题，确保图片正确显示
- ✅ **错误处理改进**：增强组件的错误处理机制，提高应用稳定性

## 技术细节与问题解决

### 首页异常抖动问题修复

**问题描述**：首页在加载过程中出现明显的异常抖动现象，影响用户体验。

**解决方案**：
1. **路径别名问题修复**：修正了`defaultImages.js`中使用`@`别名的图片路径，将其改为以`/src/assets/images/`开头的相对路径，确保Vite能够正确解析静态资源。
2. **图片错误处理优化**：完善了`HomeView.vue`和`FolkCultureCard.vue`组件中的图片加载错误处理逻辑，确保当图片加载失败时能够正确显示占位图。
3. **组件生命周期修复**：修复了`HomeView.vue`中`onMounted`和`onUnmounted`钩子函数的语法错误，确保滚动事件监听器能够正确添加和移除。

### 关键技术点

1. **Vue 3 Composition API**：充分利用Composition API的优势，提高代码的可读性和可维护性。
2. **响应式数据处理**：使用Vue 3的响应式系统处理复杂的用户交互和数据展示。
3. **Vite构建优化**：针对Vite的特性优化资源配置，提升开发和生产环境的构建效率。
4. **错误边界处理**：建立完善的错误处理机制，提升应用的健壮性。

## 项目结构

```
├── app/              # 后端Flask应用模块
│   ├── models/       # 数据模型
│   ├── routes/       # API路由
│   ├── schemas/      # 数据验证模式
│   ├── services/     # 业务逻辑服务
│   └── utils/        # 工具函数
├── frontend/         # 前端Vue应用
│   ├── src/
│   │   ├── assets/   # 静态资源
│   │   ├── components/ # Vue组件
│   │   ├── views/    # 页面视图
│   │   ├── router/   # 路由配置
│   │   ├── api/      # API客户端
│   │   ├── stores/   # 状态管理
│   │   ├── composables/ # 可复用逻辑
│   │   ├── types/    # TypeScript类型
│   │   ├── utils/    # 工具函数
│   │   ├── App.vue   # 根组件
│   │   └── main.js   # 入口文件
│   ├── index.html    # HTML模板
│   ├── package.json  # npm配置
│   └── vite.config.js # Vite配置
├── scripts/          # 初始化和工具脚本
├── tests/            # 测试脚本
├── .env              # 环境变量配置
├── app.py            # 后端应用入口
└── requirements.txt  # Python依赖
```

## 技术栈

- **前端**：Vue 3、Vue Router、Pinia、Axios、Vite、TypeScript
- **后端**：Flask、SQLAlchemy
- **数据库**：MySQL
- **项目管理**：npm、pip

## 快速开始

### 开发环境设置

#### 后端设置

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

```bash
python app.py
```

后端服务将在 http://localhost:5000 上运行。

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

1. 添加新的数据模型：在`app/models/`目录下创建新的模型文件
2. 添加新的API路由：在`app/routes/`目录下定义新的路由函数
3. 实现业务逻辑：在`app/services/`目录下创建对应的服务
4. 数据验证：在`app/schemas/`目录下定义请求和响应模式

### 前端开发

1. 添加新的页面：在`src/views/`目录下创建新的Vue组件
2. 注册路由：在`src/router/index.js`中添加新的路由配置
3. 创建可复用组件：在`src/components/`目录下开发组件
4. 添加状态管理：在`src/stores/`目录下定义Pinia store
5. 添加业务逻辑：在`src/composables/`目录下创建组合式函数

## 部署

### 前端构建

```bash
cd frontend
npm run build
```

构建产物将生成在`frontend/dist`目录中。

### 后端部署

1. 使用Gunicorn部署（推荐）：

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

2. 也可以使用Docker容器化部署，创建Dockerfile：

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## 性能优化

- 前端使用懒加载和代码分割
- 图片资源优化
- API响应数据缓存
- 数据库查询优化

## License

MIT
# 中国民俗文化网站

这是一个展示中国民俗文化的全栈网站，使用Vue 3作为前端框架，Flask作为后端API框架，专注于中国传统民俗文化的展示与传播。

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

2. 启动前端开发服务器：

```bash
npm run dev
```

前端服务将在 http://localhost:5173 上运行。

## API接口

### 民俗文化相关

- `GET /api/folkcultures` - 获取所有民俗文化列表（支持分页、搜索和筛选）
- `GET /api/folkcultures/<id>` - 获取指定ID的民俗文化详情
- `POST /api/folkcultures` - 创建新的民俗文化记录
- `GET /api/regions` - 获取所有地区列表
- `GET /api/categories` - 获取所有分类列表

## 功能特点

- 民俗文化展示与浏览
- 按地区和分类筛选查看
- 搜索功能，支持关键词搜索
- 文化详情页面，展示完整信息
- 响应式设计，适配各种设备
- 中国传统风格UI设计，展现民俗文化特色
- 加载动画和错误处理机制

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
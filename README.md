# 民族文化展示项目

**最后更新时间：2025年11月07日 18:30:00**
<!-- 此时间会在下次更新时自动更新为本地时间 -->

## 项目状态

🚀 **项目已优化升级** - 现代化UI设计全面升级，用户体验大幅提升

本项目已完成现代化UI设计升级，采用最新的前端设计理念和技术栈，为用户提供更加现代化、交互性更强的民族文化展示体验。项目具备完整的现代化UI组件库和响应式设计，可以投入实际使用。

## 项目简介

这是一个完整的民族文化展示系统，采用前后端分离架构，包含用户端前台。项目融合了中国传统元素与现代Web技术，为用户提供沉浸式的民族文化体验。

## 最新功能更新

### 🎨 现代化UI设计升级
- **全新视觉设计**：采用深色渐变背景搭配蓝青色系，营造科技感与现代感
- **现代化组件库**：重新设计所有UI组件，包含毛玻璃效果、阴影、渐变等现代设计元素
- **交互体验优化**：实现悬停效果、动态按钮、卡片动画等现代化交互设计

### 用户体验优化
- **首页性能优化**：修复了首页异常抖动问题，提升页面加载速度
- **图片加载优化**：修复了所有图片404问题，确保所有图片正确加载
- **错误处理改进**：增强了错误处理机制，提升系统稳定性

### 技术细节与问题解决
- **关键技术点**：
  - Vue 3 Composition API
  - 响应式数据处理
  - 组件化开发
  - Vite资源处理机制
  - Tailwind CSS现代化样式框架
  - CSS Grid和Flexbox布局

## 项目结构

```
MinSu/
├── application/                   # 后端Flask应用程序
│   ├── __init__.py               # 应用初始化文件
│   ├── models/                   # 数据模型定义
│   │   ├── __init__.py
│   │   └── folk_culture.py       # 民俗文化数据模型
│   ├── routes/                   # API路由配置
│   │   ├── __init__.py
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
│   │   ├── main.js               # 前台应用入口文件
│   │   ├── assets/               # 静态资源文件
│   │   │   ├── images/           # 图片资源
│   │   │   ├── styles/           # 样式文件
│   │   │   └── ...               # 其他静态资源
│   │   ├── components/           # 可复用UI组件
│   │   │   ├── FolkCultureCard.vue # 民俗文化卡片组件
│   │   │   ├── CustomButton.vue    # 自定义按钮组件
│   │   │   ├── LoadingSpinner.vue  # 加载动画组件
│   │   ├── views/                # 页面组件
│   │   │   ├── HomeView.vue      # 首页
│   │   │   ├── CultureListView.vue# 民俗文化列表页
│   │   │   ├── CultureDetailView.vue# 民俗文化详情页
│   │   │   ├── AboutView.vue     # 关于页面
│   │   ├── router/               # 路由配置
│   │   │   └── index.js          # 前台路由配置
│   │   ├── stores/               # 状态管理(Pinia)
│   │   │   └── folkCultureStore.js # 民俗文化状态管理
│   │   ├── services/             # API服务封装
│   │   │   ├── folkCultureService.js # 民俗文化相关服务
│   │   │   └── api.js            # 通用API封装
│   │   ├── api/                  # API请求定义
│   │   │   ├── frontendApi.js    # 前台API实例
│   │   │   ├── culture.js        # 民俗文化API定义
│   │   │   └── index.js          # API索引文件
│   │   ├── composables/          # 组合式函数
│   │   │   └── useDataFetching.js # 数据获取组合式函数
│   │   ├── utils/                # 前端工具函数
│   │   └── types/                # TypeScript类型定义
│   ├── package.json              # Node.js依赖配置
│   └── vite.config.js            # 前台构建配置
├── scripts/                      # 数据库和系统管理脚本
│   ├── init_database.py          # 数据库初始化脚本
│   └── ...                       # 其他管理脚本
├── templates/                    # 传统HTML模板（备用方案）
│   └── front/                    # 前台传统页面模板
├── requirements.txt              # Python依赖包列表
├── app.py                        # Flask应用主文件
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


### 前端
- Vue 3 (Composition API)
- Vue Router
- Pinia 状态管理
- Tailwind CSS 现代化CSS框架
- Sass 样式预处理器
- Axios HTTP客户端
- Vite 构建工具
- CSS Grid & Flexbox 现代布局
- CSS动画与过渡效果

## 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+
- MySQL 5.7+

### 安装步骤

1. **克隆项目**
```bash
git clone <项目地址>
cd MinSu
```

2. **后端环境配置**
```bash
cd backend
pip install -r requirements.txt
```

3. **数据库配置**
```bash
# 创建数据库
mysql -u root -p
CREATE DATABASE minsu CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 配置数据库连接
# 修改 backend/config.py 中的数据库连接信息
```

4. **前端环境配置**
```bash
cd frontend
npm install
```

5. **启动服务**
```bash
# 启动后端服务 (backend目录下)
python app.py

# 启动前端服务 (frontend目录下)
npm run dev
```

6. **访问应用**
- **前端预览地址**: http://localhost:5173 (现代化UI设计)
- **后端API服务**: http://localhost:8000
- **API文档**: http://localhost:8000/docs

### 🎯 现代化UI预览
项目已完成全面的现代化UI设计升级，访问前端地址即可体验：
- **深色渐变背景**：科技感与现代感并存的视觉设计
- **动态交互效果**：悬停动画、按钮效果、卡片过渡
- **响应式布局**：适配各种设备的现代化界面
- **现代化组件**：毛玻璃效果、阴影、渐变等现代设计元素

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

## 功能特点

### 🎨 现代化UI设计特点

#### 视觉设计
- **色彩方案**：深色渐变背景搭配蓝青色系，营造科技感与现代感
- **视觉层次**：毛玻璃效果、阴影、渐变提升视觉深度
- **组件设计**：圆角设计、卡片式布局、现代化图标
- **字体排版**：渐变文字效果、合理的字体层次结构

#### 交互体验
- **悬停效果**：卡片悬停上移、缩放、背景过渡动画
- **按钮交互**：动态按钮效果、滑动光效、状态变化
- **表单交互**：聚焦状态高亮、输入框动态背景
- **响应式设计**：适配不同屏幕尺寸的布局调整

#### 页面区域优化
- **英雄区域**：动态背景粒子、渐变文字、交互式按钮组
- **民族文化展示区**：现代化卡片设计，包含渐变背景、装饰标签
- **地区风情区**：深色渐变背景搭配紫色/青色装饰元素
- **文化展示区**：现代化图片网格，分类标签、悬停显示内容
- **联系我们区域**：现代化联系表单和信息卡片

### 用户端前台核心功能
- 民俗文化展示与浏览
- 按地区和分类筛选查看
- 搜索功能，支持关键词搜索
- 文化详情页面，展示完整信息
- 响应式设计，适配各种设备
- **中国传统元素融合**：在现代化设计中融入传统文化特色
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
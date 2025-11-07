# 民俗文化展示项目 - 新架构

## 项目结构

```
new_architecture/
├── frontend/                     # 前端应用
│   ├── client/                  # Next.js 15 用户端
│   │   ├── app/                 # 应用路由和页面
│   │   ├── components/          # 共享组件
│   │   ├── lib/                 # 工具库和客户端库
│   │   ├── public/              # 静态资源
│   │   ├── styles/              # 全局样式
│   │   └── package.json         # 依赖配置
│   └── admin/                  # Vue 3 管理后台
│       ├── src/                 # 源代码
│       │   ├── assets/          # 静态资源
│       │   ├── components/      # 组件
│       │   ├── composables/     # 组合式函数
│       │   ├── layouts/         # 布局组件
│       │   ├── pages/           # 页面
│       │   ├── plugins/         # 插件
│       │   ├── router/          # 路由配置
│       │   ├── services/        # API服务
│       │   ├── stores/          # 状态管理
│       │   └── styles/          # 样式
│       ├── package.json         # 依赖配置
│       └── vite.config.js       # 构建配置
├── backend/                     # 后端应用
│   ├── app/                     # FastAPI应用
│   │   ├── api/                 # API路由
│   │   ├── core/                # 核心配置和安全
│   │   ├── models/              # 数据模型
│   │   ├── schemas/             # 数据验证模式
│   │   ├── services/            # 业务逻辑
│   │   ├── utils/               # 工具函数
│   │   ├── database.py          # 数据库配置
│   │   └── main.py              # 应用入口
│   ├── tests/                   # 测试文件
│   ├── requirements.txt         # Python依赖
│   └── alembic/                 # 数据库迁移
├── docker/                      # Docker配置
│   ├── nginx/                  # Nginx配置
│   │   ├── conf.d/             # 站点配置
│   │   └── nginx.conf          # 主配置文件
│   ├── docker-compose.yml       # Docker Compose配置
│   ├── backend.Dockerfile       # 后端Dockerfile
│   └── frontend.Dockerfile      # 前端Dockerfile
└── README.md                   # 项目说明
```
# 🤖 AI Novel Writer - AI 小说创作平台

一个基于 AI 的智能小说创作平台，帮助作者进行小说创作、章节管理和 AI 辅助写作。

## ✨ 功能特性

### 🎯 核心功能
- **📚 小说项目管理** - 创建、编辑、删除小说项目，支持项目模板（备忘录、大纲、设定、章节）
- **📝 章节编辑器** - 三栏布局：章节树目录、文本编辑、AI 对话
- **🌳 多级章节目录** - 树状结构支持文件夹/章节节点，拖拽排序、右键菜单（重命名/复制/删除/添加子节点）、折叠/展开
- **🤖 AI 辅助创作** - 集成 OpenAI 兼容 API，支持流式输出，提供智能写作建议
- **💬 实时对话** - 与 AI 进行创作相关的对话交流
- **⚙️ API 配置管理** - 多模型配置管理，支持自定义 API 地址、密钥、模型参数，一键测试连接

### 🔧 辅助功能
- **🔐 用户认证** - JWT 认证系统，支持注册、登录
- **📁 代码片段管理** - 保存和管理常用代码片段
- **💡 提示词广场** - 预设的 AI 提示词模板
- **📊 字数统计** - 实时统计章节和项目总字数
- **🚀 一键启动** - Windows 批处理脚本一键启动前后端服务

## 🛠️ 技术栈

### 后端 (`ai-novel-backend/`)
| 技术 | 用途 |
|------|------|
| **FastAPI** | Web 框架 |
| **PostgreSQL** | 数据库 |
| **SQLAlchemy 2.0** | ORM (异步) |
| **Alembic** | 数据库迁移 |
| **Pydantic v2** | 数据验证 |
| **JWT** | 用户认证 |
| **OpenAI API** | AI 服务 (支持任意 OpenAI 兼容 API) |
| **Loguru** | 日志管理 |
| **httpx / aiohttp** | 异步 HTTP 客户端 |

### 前端 (`vue-project/`)
| 技术 | 用途 |
|------|------|
| **Vue 3** | 前端框架 (Composition API + `<script setup>`) |
| **TypeScript** | 类型安全 |
| **Vite 8** | 构建工具 |
| **Vue Router 4** | 路由管理 |
| **Pinia 3** | 状态管理 |

## 🚀 快速开始

### 环境要求
- Python 3.10+
- Node.js 22.18.0+ 或 24.12.0+
- PostgreSQL 14+
- npm 或 yarn

### 1. 克隆项目
```bash
git clone https://github.com/SergeXie/ai-novel-writer.git
cd ai-novel-writer
```

### 2. 启动后端服务

```bash
cd ai-novel-backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，配置数据库和 API 密钥

# 运行数据库迁移
alembic upgrade head

# 启动服务
python -m app.main
# 或
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. 启动前端服务

```bash
cd vue-project

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 4. 访问应用
- **前端**: http://localhost:5173/novel
- **后端 API**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs (Swagger UI)
- **ReDoc 文档**: http://localhost:8000/redoc

### 🚀 一键启动 (Windows)

双击 `start-all.bat` 即可同时启动前后端服务，无需手动分别启动。

| 脚本 | 说明 |
|------|------|
| `start-all.bat` | 一键启动前后端 |
| `start-backend.bat` | 仅启动后端 API |
| `start-frontend.bat` | 仅启动前端开发服务器 |

## ⚙️ 环境配置

### 后端环境变量 (`ai-novel-backend/.env`)

```env
# 数据库配置
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/ai_novel

# AI 服务配置
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_BASE_URL=https://api.openai.com/v1
DEFAULT_MODEL=gpt-4

# 认证配置
SECRET_KEY=your-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS 配置
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]
```

## 📁 项目结构

```
ai-novel-writer/
├── ai-novel-backend/          # 后端服务
│   ├── app/
│   │   ├── api/v1/           # API 路由
│   │   │   ├── api_configs.py  # API 配置管理
│   │   │   ├── auth.py         # 用户认证
│   │   │   ├── chat.py         # AI 聊天
│   │   │   ├── novels.py       # 小说项目/章节
│   │   │   ├── prompts.py      # 提示词管理
│   │   │   └── snippets.py     # 代码片段
│   │   ├── core/             # 核心配置
│   │   ├── models/           # 数据库模型
│   │   ├── schemas/          # Pydantic 模型
│   │   ├── services/         # 业务逻辑
│   │   └── middleware/       # 中间件
│   ├── alembic/              # 数据库迁移
│   ├── .env.example          # 环境变量模板
│   └── requirements.txt      # Python 依赖
├── vue-project/               # 前端应用
│   ├── src/
│   │   ├── api/              # API 调用 (novel.ts, apiConfig.ts)
│   │   ├── components/       # Vue 组件
│   │   │   ├── AppSidebar.vue    # 侧边栏导航
│   │   │   ├── ApiSettingsModal.vue # API 配置弹窗
│   │   │   └── ChapterTree.vue   # 树状章节目录
│   │   ├── router/           # 路由配置
│   │   ├── stores/           # Pinia 状态
│   │   └── views/            # 页面视图
│   └── package.json          # npm 依赖
├── start-all.bat              # 一键启动脚本
├── start-backend.bat          # 后端启动脚本
├── start-frontend.bat         # 前端启动脚本
└── README.md                  # 项目说明
```

## 📖 功能页面

| 页面 | 路径 | 说明 |
|------|------|------|
| 首页 | `/` | 欢迎页面和导航入口 |
| 小说列表 | `/novel` | 管理所有小说项目 |
| 小说编辑器 | `/novel/:id` | 三栏编辑界面（树状目录 + 编辑器 + AI 对话） |
| 拆书 | `/split-book` | 文本拆分分析工具 |
| 代码片段 | `/snippets` | 代码片段管理 |
| 提示词广场 | `/prompts` | AI 提示词模板 |
| 工具箱 | `/toolbox` | 实用工具集合 |
| 讨论区 | `/discuss` | 用户交流讨论 |
| 使用指南 | `/guide` | 平台使用说明 |
| 关于平台 | `/about-platform` | 平台介绍 |

## 🔌 API 接口

### 认证接口
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/v1/auth/register` | 用户注册 |
| POST | `/api/v1/auth/login` | 用户登录 |
| GET | `/api/v1/auth/me` | 获取当前用户 |

### 小说项目接口
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/projects` | 获取项目列表 |
| POST | `/api/v1/projects` | 创建项目 |
| GET | `/api/v1/projects/{id}` | 获取项目详情 |
| PUT | `/api/v1/projects/{id}` | 更新项目 |
| DELETE | `/api/v1/projects/{id}` | 删除项目 |

### AI 聊天接口
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/v1/chat` | 发送聊天消息 |
| POST | `/api/v1/chat/stream` | 流式聊天 |

### API 配置接口
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/api-configs` | 获取配置列表 |
| POST | `/api/v1/api-configs` | 创建配置 |
| GET | `/api/v1/api-configs/{id}` | 获取配置详情 |
| PUT | `/api/v1/api-configs/{id}` | 更新配置 |
| DELETE | `/api/v1/api-configs/{id}` | 删除配置 |
| POST | `/api/v1/api-configs/{id}/test` | 测试配置连接 |

## 🚦 开发指南

### 代码规范
- 后端使用 Black 格式化代码
- 前端使用 ESLint + Prettier
- 提交信息遵循 [Conventional Commits](https://www.conventionalcommits.org/zh-hans/)

### 分支管理
- `main` - 生产分支
- `develop` - 开发分支
- `feature/*` - 功能分支
- `fix/*` - 修复分支

### 测试
```bash
# 后端测试
cd ai-novel-backend
pytest

# 前端测试
cd vue-project
npm run test
```

## 📝 更新日志

### v1.1.0 (2026-07-23)
- ✨ 新增 API 配置管理 - 支持多模型配置、自定义 API 地址和参数
- ✨ 新增树状章节目录 - 文件夹/章节节点、右键菜单、折叠/展开
- ✨ 新增一键启动脚本 (`start-all.bat`)
- 🎨 优化编辑器界面布局和交互体验
- 🔧 移除旧版 Counter/Todo 示例页面

### v1.0.0 (2026-07-20)
- ✨ 初始版本发布
- 🎯 小说项目管理功能
- 📝 三栏编辑器
- 🤖 AI 辅助创作
- 🔐 用户认证系统

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目使用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 👥 作者

- **SergeXie** - [GitHub](https://github.com/SergeXie)

## 🙏 致谢

- [FastAPI](https://fastapi.tiangolo.com/) - 现代高性能 Web 框架
- [Vue.js](https://vuejs.org/) - 渐进式 JavaScript 框架
- [OpenAI](https://openai.com/) - AI 服务提供

---

⭐ 如果这个项目对你有帮助，请给个 Star 支持一下！

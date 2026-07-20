# AI Novel Backend

## 项目结构

```
ai-novel-backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # 应用入口
│   ├── core/
│   │   ├── config.py        # 配置管理
│   │   ├── database.py      # 数据库连接
│   │   ├── logging.py       # 日志配置
│   │   └── security.py      # 认证与安全
│   ├── models/
│   │   ├── user.py          # 用户模型
│   │   ├── novel.py         # 小说项目模型
│   │   ├── chapter.py       # 章节模型
│   │   └── conversation.py  # 对话记录模型
│   ├── schemas/
│   │   ├── user.py          # 用户请求/响应模型
│   │   ├── novel.py         # 小说项目模型
│   │   ├── conversation.py  # 对话模型
│   │   └── common.py        # 通用响应模型
│   ├── services/
│   │   ├── user_service.py  # 用户业务逻辑
│   │   ├── novel_service.py # 小说项目逻辑
│   │   └── ai_service.py    # AI 服务封装
│   ├── api/
│   │   └── v1/
│   │       ├── router.py    # v1 路由聚合
│   │       ├── auth.py      # 认证接口
│   │       ├── novels.py    # 小说项目接口
│   │       ├── chat.py      # AI 聊天接口
│   │       └── system.py    # 系统接口
│   ├── middleware/
│   │   ├── logging.py       # 请求日志中间件
│   │   └── context.py       # 请求上下文中间件
│   └── utils/
│       └── helpers.py       # 工具函数
├── alembic/                 # 数据库迁移
├── tests/                   # 测试用例
├── requirements.txt         # Python 依赖
├── .env.example             # 环境变量示例
├── alembic.ini              # Alembic 配置
└── README.md                # 项目说明
```

## 快速开始

### 1. 安装依赖

```bash
cd ai-novel-backend
python -m venv venv

# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，配置数据库连接等信息
```

### 3. 启动服务

```bash
# 开发模式
python -m app.main

# 或使用 uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. 访问 API 文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 技术栈

- **Web 框架**: FastAPI
- **数据库**: PostgreSQL + SQLAlchemy 2.0 (异步)
- **迁移工具**: Alembic
- **数据验证**: Pydantic v2
- **认证**: JWT (python-jose)
- **AI 服务**: OpenAI API
- **日志**: Loguru

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/v1/auth/register` | 用户注册 |
| POST | `/api/v1/auth/login` | 用户登录 |
| GET | `/api/v1/auth/me` | 获取当前用户 |
| GET | `/api/v1/projects` | 获取项目列表 |
| POST | `/api/v1/projects` | 创建项目 |
| GET | `/api/v1/projects/{id}` | 获取项目详情 |
| PUT | `/api/v1/projects/{id}` | 更新项目 |
| DELETE | `/api/v1/projects/{id}` | 删除项目 |
| POST | `/api/v1/chat` | 发送聊天消息 |
| POST | `/api/v1/chat/stream` | 流式聊天 |
| GET | `/api/v1/health` | 健康检查 |

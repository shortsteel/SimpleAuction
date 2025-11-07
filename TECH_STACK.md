# 简单拍卖系统技术方案

## 1. 技术栈选型

### 1.1 后端技术栈

#### 核心框架
- **Python 3.11+** - 主要编程语言
- **FastAPI** - 现代、高性能的 Web 框架
  - 自动生成 API 文档（Swagger/OpenAPI）
  - 基于 Python 类型提示，类型安全
  - 异步支持，性能优秀
  - AI 编辑器对 FastAPI 支持良好

#### 数据库
- **SQLite** - 轻量级关系型数据库
  - 无需单独安装数据库服务
  - 适合中小型应用和快速开发
  - 文件存储，易于备份和迁移
  - 使用 SQLAlchemy ORM 进行数据库操作

#### ORM 和数据访问
- **SQLAlchemy 2.0+** - Python ORM 框架
  - 类型安全，支持 Python 类型提示
  - 支持异步操作
  - 数据库迁移工具 Alembic
  - AI 编辑器能很好地理解 SQLAlchemy 模型

#### 认证和安全
- **python-jose[cryptography]** - JWT 令牌处理
- **passlib[bcrypt]** - 密码加密
- **python-multipart** - 文件上传支持

#### 数据验证
- **Pydantic** - 数据验证和序列化
  - 与 FastAPI 深度集成
  - 基于 Python 类型提示
  - AI 编辑器能很好地生成 Pydantic 模型

#### 定时任务
- **APScheduler** - 高级 Python 调度器
  - 用于拍卖自动结算
  - 支持多种调度方式

#### 其他工具
- **python-dotenv** - 环境变量管理
- **uvicorn** - ASGI 服务器（用于运行 FastAPI）

### 1.2 前端技术栈

#### 核心框架
- **Vue 3** - 渐进式 JavaScript 框架
  - Composition API（推荐使用 `<script setup>`）
  - 响应式系统优秀
  - 组件化开发
  - AI 编辑器对 Vue 3 支持良好

#### 构建工具
- **Vite** - 下一代前端构建工具
  - 极速的开发服务器
  - 快速的热模块替换（HMR）
  - 优化的生产构建

#### UI 框架
- **Element Plus** 或 **Vuetify 3** - Vue 3 UI 组件库
  - 提供丰富的组件（表格、表单、对话框等）
  - 减少样式编写工作
  - AI 编辑器能很好地生成组件代码

#### 状态管理
- **Pinia** - Vue 官方推荐的状态管理库
  - 类型安全（配合 TypeScript 使用）
  - 简单易用
  - 替代 Vuex

#### 路由
- **Vue Router 4** - Vue 官方路由管理器

#### HTTP 客户端
- **Axios** - 基于 Promise 的 HTTP 客户端
  - 请求/响应拦截器
  - 自动 JSON 转换

#### 实时更新（可选）
- **Socket.io-client** - WebSocket 客户端
  - 用于实时显示出价和倒计时

#### 类型支持（可选但推荐）
- **TypeScript** - 为 Vue 3 添加类型支持
  - 更好的代码提示和错误检查
  - AI 编辑器能生成更准确的代码

### 1.3 开发工具

#### 代码质量
- **Black** - Python 代码格式化工具
- **flake8** 或 **ruff** - Python 代码检查工具
- **mypy** - Python 静态类型检查
- **ESLint** + **Prettier** - 前端代码质量和格式化

#### 测试框架
- **pytest** - Python 测试框架
- **pytest-asyncio** - 异步测试支持
- **Vitest** - Vue 前端单元测试框架

#### API 文档
- **FastAPI 自动生成** - Swagger UI 和 ReDoc
  - 访问 `/docs` 查看 Swagger UI
  - 访问 `/redoc` 查看 ReDoc

## 2. 架构设计

### 2.1 整体架构

```
┌─────────────────┐
│   Vue 3 前端    │
│   (Vite + Pinia)│
└────────┬────────┘
         │ HTTP/REST API
         │ (JSON)
┌────────▼────────┐
│  FastAPI 后端   │
│  (Python 3.11+) │
└────────┬────────┘
         │ ORM
┌────────▼────────┐
│   SQLite 数据库 │
│   (文件存储)     │
└─────────────────┘
```

### 2.2 后端架构

采用分层架构：

```
backend/
├── app/
│   ├── main.py              # FastAPI 应用入口
│   ├── config.py            # 配置管理
│   ├── database.py          # 数据库连接和会话管理
│   ├── models/              # SQLAlchemy 数据模型
│   │   ├── user.py
│   │   ├── auction.py
│   │   └── bid.py
│   ├── schemas/             # Pydantic 模式（请求/响应）
│   │   ├── user.py
│   │   ├── auction.py
│   │   └── bid.py
│   ├── api/                 # API 路由
│   │   ├── deps.py          # 依赖注入（认证等）
│   │   ├── auth.py          # 认证相关路由
│   │   ├── auctions.py      # 拍卖相关路由
│   │   └── bids.py          # 出价相关路由
│   ├── services/            # 业务逻辑层
│   │   ├── auth_service.py
│   │   ├── auction_service.py
│   │   └── bid_service.py
│   ├── utils/               # 工具函数
│   │   ├── security.py      # 密码加密、JWT
│   │   └── scheduler.py     # 定时任务
│   └── migrations/          # Alembic 数据库迁移
└── tests/                   # 测试文件
```

### 2.3 前端架构

采用组件化架构：

```
frontend/
├── src/
│   ├── main.js              # 应用入口
│   ├── App.vue              # 根组件
│   ├── router/              # 路由配置
│   │   └── index.js
│   ├── stores/              # Pinia 状态管理
│   │   ├── auth.js
│   │   └── auction.js
│   ├── api/                 # API 请求封装
│   │   └── client.js
│   ├── views/               # 页面组件
│   │   ├── Home.vue         # 首页（拍卖列表）
│   │   ├── Login.vue        # 登录页
│   │   ├── Register.vue     # 注册页
│   │   ├── AuctionDetail.vue # 拍卖详情
│   │   ├── CreateAuction.vue # 发布拍卖
│   │   ├── MyAuctions.vue   # 我的拍卖
│   │   └── MyBids.vue       # 我的竞拍
│   ├── components/          # 可复用组件
│   │   ├── AuctionCard.vue
│   │   ├── BidHistory.vue
│   │   └── CountdownTimer.vue
│   ├── utils/               # 工具函数
│   │   └── format.js
│   └── assets/              # 静态资源
├── public/                  # 公共文件
└── package.json
```

## 3. 数据库设计

### 3.1 数据库文件
- 使用 SQLite，数据库文件存储在 `backend/data/auction.db`
- 使用 Alembic 进行数据库迁移管理

### 3.2 数据表设计

#### users 表
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### auctions 表
```sql
CREATE TABLE auctions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    starting_price DECIMAL(10, 2) NOT NULL,
    current_price DECIMAL(10, 2) NOT NULL,
    current_bidder_id INTEGER,
    seller_id INTEGER NOT NULL,
    end_time DATETIME NOT NULL,
    status VARCHAR(20) DEFAULT 'active',  -- active, ended, no_bid
    images TEXT,  -- JSON 数组存储图片路径
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (seller_id) REFERENCES users(id),
    FOREIGN KEY (current_bidder_id) REFERENCES users(id)
);
```

#### bids 表
```sql
CREATE TABLE bids (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    auction_id INTEGER NOT NULL,
    bidder_id INTEGER NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (auction_id) REFERENCES auctions(id),
    FOREIGN KEY (bidder_id) REFERENCES users(id)
);

CREATE INDEX idx_bids_auction_id ON bids(auction_id);
CREATE INDEX idx_bids_bidder_id ON bids(bidder_id);
CREATE INDEX idx_auctions_status ON auctions(status);
CREATE INDEX idx_auctions_end_time ON auctions(end_time);
```

## 4. API 设计

### 4.1 API 基础信息
- **Base URL**: `http://localhost:8000/api`
- **认证方式**: Bearer Token (JWT)
- **数据格式**: JSON

### 4.2 API 端点列表

#### 认证相关
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `POST /api/auth/logout` - 用户登出
- `GET /api/auth/me` - 获取当前用户信息

#### 拍卖相关
- `POST /api/auctions` - 创建拍卖（需认证）
- `GET /api/auctions` - 获取拍卖列表（公开）
  - 查询参数: `status`, `page`, `limit`, `sort`
- `GET /api/auctions/{id}` - 获取拍卖详情（公开）
- `GET /api/auctions/my/listings` - 获取我发布的拍卖（需认证）

#### 出价相关
- `POST /api/auctions/{id}/bids` - 创建出价（需认证）
- `GET /api/auctions/{id}/bids` - 获取拍卖的出价历史（公开）
- `GET /api/auctions/my/bids` - 获取我的竞拍记录（需认证）

### 4.3 响应格式

#### 成功响应
```json
{
  "success": true,
  "data": { ... },
  "message": "操作成功"
}
```

#### 错误响应
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "错误描述"
  }
}
```

## 5. 开发环境配置

### 5.1 Python 环境
- Python 3.11 或更高版本
- 使用 `venv` 或 `conda` 创建虚拟环境
- 使用 `requirements.txt` 管理依赖

### 5.2 Node.js 环境
- Node.js 18+ 或更高版本
- 使用 `npm` 或 `yarn` 或 `pnpm` 管理依赖

### 5.3 环境变量

#### 后端 (.env)
```env
# 应用配置
APP_NAME=SimpleAuction
DEBUG=True
SECRET_KEY=your-secret-key-here

# 数据库配置
DATABASE_URL=sqlite:///./data/auction.db

# JWT 配置
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# CORS 配置
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

#### 前端 (.env)
```env
VITE_API_BASE_URL=http://localhost:8000/api
```

## 6. 开发流程

### 6.1 初始化项目

#### 后端初始化
```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
alembic init migrations
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

# 运行开发服务器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 前端初始化
```bash
# 安装依赖
npm install  # 或 yarn install

# 运行开发服务器
npm run dev  # 或 yarn dev
```

### 6.2 开发规范

#### Python 代码规范
- 使用 Black 格式化代码
- 使用 flake8 检查代码质量
- 使用类型提示（Type Hints）
- 遵循 PEP 8 规范

#### Vue 代码规范
- 使用 `<script setup>` 语法
- 组件名使用 PascalCase
- 文件名使用 PascalCase（组件）或 kebab-case（工具文件）
- 使用 ESLint 和 Prettier

## 7. 部署方案

### 7.1 开发环境
- 后端: `uvicorn` 开发服务器
- 前端: `vite` 开发服务器
- 数据库: SQLite 文件

### 7.2 生产环境（建议）

#### 后端部署
- 使用 `gunicorn` + `uvicorn workers` 或直接使用 `uvicorn`
- 使用 Nginx 作为反向代理
- 使用 Supervisor 或 systemd 管理进程

#### 前端部署
- 使用 `npm run build` 构建生产版本
- 部署到 Nginx 或 CDN
- 或使用 Vercel/Netlify 等平台

#### 数据库
- 生产环境可考虑迁移到 PostgreSQL
- 或继续使用 SQLite（适合中小型应用）

## 8. 为什么这个技术栈适合 AI 编辑器？

### 8.1 Python + FastAPI
- **类型提示支持好**: Python 3.11+ 的类型系统完善，AI 能理解代码结构
- **Pydantic 模型**: AI 能很好地生成数据验证模型
- **SQLAlchemy**: AI 对 ORM 模式理解深入，能生成正确的查询代码
- **FastAPI 文档丰富**: AI 训练数据中 FastAPI 示例多

### 8.2 Vue 3
- **Composition API**: `<script setup>` 语法简洁，AI 能生成清晰的组件代码
- **类型支持**: 配合 TypeScript 使用，AI 能生成类型安全的代码
- **组件模式**: AI 对 Vue 组件模式理解好
- **生态成熟**: Element Plus/Vuetify 等 UI 库，AI 能生成标准组件代码

### 8.3 SQLite
- **简单直接**: 无需复杂配置，AI 能生成正确的数据库操作代码
- **SQLAlchemy 支持**: 通过 ORM 操作，AI 能生成类型安全的查询

## 9. 依赖包清单

### 9.1 后端依赖 (requirements.txt)
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
alembic==1.12.1
pydantic==2.5.0
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
python-dotenv==1.0.0
apscheduler==3.10.4
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
```

### 9.2 前端依赖 (package.json 核心依赖)
```json
{
  "dependencies": {
    "vue": "^3.3.8",
    "vue-router": "^4.2.5",
    "pinia": "^2.1.7",
    "axios": "^1.6.2",
    "element-plus": "^2.4.4"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^4.5.0",
    "vite": "^5.0.0",
    "typescript": "^5.3.2",
    "@vue/tsconfig": "^0.4.0"
  }
}
```

## 10. 下一步行动

1. 初始化后端项目结构
2. 初始化前端项目结构
3. 配置开发环境
4. 创建数据库模型
5. 实现认证模块
6. 实现拍卖核心功能
7. 实现前端界面
8. 集成测试

---

**注意**: 本技术方案基于 AI 编辑器的特点进行了优化，确保 AI 能更好地理解和生成代码。


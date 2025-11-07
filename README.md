# 简单拍卖系统

一个基于 Python Flask + Vue.js 的在线拍卖系统。

## 技术栈

### 后端
- Python 3.8+
- Flask 3.0.0
- SQLite 数据库
- Flask-JWT-Extended (JWT认证)
- APScheduler (定时任务)

### 前端
- Vue 3
- Vue Router 4
- Element Plus (UI组件库)
- Axios (HTTP客户端)

## 项目结构

```
SimpleAuction/
├── backend/              # 后端代码
│   ├── app.py           # Flask应用入口
│   ├── config.py        # 配置文件
│   ├── database.py      # 数据库初始化
│   ├── models.py        # 数据模型
│   ├── auth.py          # 认证API
│   ├── auction.py       # 拍卖API
│   ├── bid.py           # 竞拍API
│   ├── scheduler.py     # 定时任务
│   └── requirements.txt # Python依赖
├── frontend/            # 前端代码
│   ├── src/
│   │   ├── api/         # API接口
│   │   ├── router/      # 路由配置
│   │   ├── store/       # 状态管理
│   │   ├── views/       # 页面组件
│   │   ├── App.vue      # 根组件
│   │   └── main.js      # 入口文件
│   ├── package.json     # 前端依赖
│   └── vue.config.js    # Vue配置
└── REQUIREMENTS.md      # 需求文档
```

## 功能特性

### 用户认证
- ✅ 用户注册（用户名、邮箱、密码）
- ✅ 用户登录（用户名/邮箱登录）
- ✅ 用户登出
- ✅ JWT Token认证

### 拍卖管理
- ✅ 发布拍卖标的
- ✅ 查看拍卖列表（支持筛选和排序）
- ✅ 查看拍卖详情
- ✅ 查看我的拍卖

### 竞拍功能
- ✅ 参与竞拍（出价）
- ✅ 查看我的竞拍记录
- ✅ 实时显示剩余时间
- ✅ 出价历史记录

### 拍卖结算
- ✅ 自动结算到期拍卖
- ✅ 标记流拍（无出价）
- ✅ 确定获胜者（最高出价者）

## 安装和运行

### 快速启动（推荐）

#### 方式一：同时启动前后端（后台运行）

**Linux/Mac:**
```bash
# 启动服务（后台运行）
./start.sh

# 停止服务
./stop.sh
```

**Windows:**
```batch
# 启动服务（新窗口运行）
start.bat

# 停止服务：关闭对应的命令行窗口
```

启动脚本会自动：
- 检查Python和Node.js环境
- 创建并激活Python虚拟环境
- 安装后端和前端依赖
- 启动后端服务（http://localhost:3000）
- 启动前端服务（http://localhost:8080）

#### 方式二：分别启动前后端（推荐用于开发调试）

**Linux/Mac:**
```bash
# 终端1：启动后端
./start-backend.sh

# 终端2：启动前端
./start-frontend.sh
```

**Windows:**
```batch
# 窗口1：启动后端
start-backend.bat

# 窗口2：启动前端
start-frontend.bat
```

这种方式可以分别查看前后端的日志输出，便于调试。

### 手动启动

#### 后端

1. 进入后端目录：
```bash
cd backend
```

2. 创建虚拟环境（推荐）：
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 运行后端服务：
```bash
python app.py
```

后端服务将在 `http://localhost:3000` 启动。

#### 前端

1. 进入前端目录：
```bash
cd frontend
```

2. 安装依赖：
```bash
npm install
```

3. 运行开发服务器：
```bash
npm run serve
```

前端应用将在 `http://localhost:8080` 启动。

## API接口

### 认证接口
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `POST /api/auth/logout` - 用户登出
- `GET /api/auth/me` - 获取当前用户信息

### 拍卖接口
- `POST /api/auctions` - 发布拍卖标的（需登录）
- `GET /api/auctions` - 获取拍卖列表（公开）
- `GET /api/auctions/:id` - 获取拍卖详情（公开）
- `GET /api/auctions/my/listings` - 获取我发布的拍卖（需登录）

### 竞拍接口
- `POST /api/auctions/:id/bids` - 参与竞拍（需登录）
- `GET /api/auctions/my/bids` - 获取我的竞拍记录（需登录）

## 数据库

系统使用 SQLite 数据库，数据库文件会自动创建在 `backend/auction.db`。

### 数据表
- `users` - 用户表
- `auctions` - 拍卖标地表
- `bids` - 出价记录表

## 注意事项

1. **密码要求**：密码至少8位，必须包含字母和数字
2. **拍卖结束时间**：必须至少在未来1小时后
3. **出价规则**：出价金额必须大于当前最高价
4. **定时任务**：系统每30秒检查一次到期拍卖并自动结算

## 开发说明

### 后端开发
- 使用 Flask 蓝图组织路由
- 使用 JWT 进行身份验证
- 使用 APScheduler 执行定时任务
- 数据库操作使用 SQLite

### 前端开发
- 使用 Vue 3 Composition API
- 使用 Element Plus 组件库
- 使用 Axios 进行 API 调用
- 响应式设计，支持移动端和桌面端

## 许可证

MIT License


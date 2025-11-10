> 🤖 **本项目完全由 AI 开发**  
> 这是一个展示 AI 编程能力的示例项目，从需求分析、架构设计、代码实现到文档编写，全程由 AI 完成。

# 简单拍卖系统

一个基于 Python Flask + Vue.js 的在线拍卖系统。支持用户注册登录、发布拍卖、参与竞拍、自动结算等完整功能。

## 技术栈

### 后端
- Python 3.11
- Flask 3.0.0 (Web框架)
- Flask-CORS 4.0.0 (跨域支持)
- Flask-JWT-Extended 4.6.0 (JWT认证)
- SQLite (数据库)
- APScheduler 3.10.4 (定时任务)
- Werkzeug 3.0.1 (密码加密)
- python-dotenv 1.0.0 (环境变量管理)

### 前端
- Vue 3.3.4
- Vue Router 4.2.5
- Element Plus 2.4.4 (UI组件库)
- Axios 1.6.0 (HTTP客户端)
- @element-plus/icons-vue 2.3.1 (图标库)

### 部署
- Docker (容器化部署)
- Nginx (反向代理)
- Supervisor (进程管理)

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
  - 用户名和邮箱唯一性验证
  - 邮箱格式验证
  - 密码强度验证（至少8位，包含字母和数字）
  - 密码加密存储（Werkzeug）
- ✅ 用户登录（支持用户名/邮箱登录）
- ✅ 用户登出
- ✅ JWT Token认证（有效期24小时）
- ✅ 获取当前用户信息

### 拍卖管理
- ✅ 发布拍卖标的
  - 标的名称、描述、起拍价
  - 拍卖结束时间（必须至少在未来1小时后）
  - 标的图片（支持多张，JSON数组存储）
  - 最低加价幅度设置
- ✅ 查看拍卖列表
  - 分页显示（可配置每页数量）
  - 按状态筛选（全部/进行中/已结束/流拍）
  - 按时间排序（最新/最早）
  - 显示竞拍者数量、剩余时间
- ✅ 查看拍卖详情
  - 完整标的信息
  - 实时剩余时间倒计时
  - 当前最高价和最高出价者（部分隐藏）
  - 完整出价历史记录
  - 卖家可查看完整竞拍者信息
- ✅ 查看我的拍卖
  - 我发布的所有拍卖列表
  - 每个拍卖的竞拍者数量
  - 当前状态和最高价

### 竞拍功能
- ✅ 参与竞拍（出价）
  - 出价金额验证（必须大于当前最高价+最低加价幅度）
  - 防止对自己的拍卖出价
  - 拍卖状态和时间检查
  - 实时更新当前最高价
- ✅ 查看我的竞拍记录
  - 我参与的所有竞拍列表
  - 显示是否是当前最高出价者
  - 显示是否中标（已结束拍卖）
  - 按时间倒序排列
- ✅ 实时显示剩余时间
- ✅ 完整出价历史记录

### 拍卖结算
- ✅ 自动结算到期拍卖（定时任务每30秒检查）
- ✅ 标记流拍（无出价的拍卖）
- ✅ 确定获胜者（最高出价者）
- ✅ 拍卖状态管理（active/ended/no_bid）

### 安全与日志
- ✅ 密码加密存储
- ✅ JWT Token认证和授权
- ✅ CORS跨域配置
- ✅ 完整的请求日志（包括客户端IP追踪）
- ✅ 错误处理和友好提示

## 安装和运行

### 方式一：Docker部署（推荐用于生产环境）

使用Docker可以一键启动完整的应用（包括前端、后端、Nginx），无需手动配置环境。

#### 前置要求
- 已安装 Docker

#### 启动服务

```bash
# Linux/Mac
chmod +x start-docker.sh  # 添加执行权限（首次运行）
./start-docker.sh
```

启动脚本会自动：
1. 创建数据目录（database、uploads、logs）
2. 构建Docker镜像（包含前端构建和后端环境）
3. 启动容器（默认端口18080）
4. 配置Nginx反向代理
5. 启动Flask后端服务

访问地址：`http://localhost:18080`

#### 停止服务

```bash
./stop-docker.sh
```

停止脚本提供三个选项：
1. 仅停止容器（保留容器，可快速重启）
2. 停止并删除容器
3. 停止并删除容器和镜像（彻底清理）

#### 重启服务

```bash
./restart-docker.sh
```

#### 其他Docker命令

```bash
# 查看容器日志
docker logs -f simple-auction-app

# 查看容器状态
docker ps

# 进入容器
docker exec -it simple-auction-app /bin/bash

# 停止容器
docker stop simple-auction-app

# 启动已有容器
docker start simple-auction-app
```

### 方式二：手动启动（推荐用于开发调试）

手动启动适合开发调试，可以分别查看前后端的日志输出。

#### 前置要求
- Python 3.11+
- Node.js 18+
- npm

#### 后端启动

1. 进入后端目录：
```bash
cd backend
```

2. 创建并激活虚拟环境（推荐）：
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

后端API服务将在 `http://localhost:3000` 启动。

#### 前端启动

打开新的终端窗口：

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

#### 构建生产版本

```bash
cd frontend
npm run build
```

构建后的文件将输出到 `frontend/dist` 目录。

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

系统使用 SQLite 数据库，数据库文件会自动创建。

### 数据库位置
- 开发模式：`backend/auction.db`
- Docker模式：`data/database/auction.db`（持久化挂载）

### 数据表结构

#### users - 用户表
- `id` - 用户ID（主键）
- `username` - 用户名（唯一）
- `email` - 邮箱（唯一）
- `password` - 密码（加密存储）
- `created_at` - 创建时间
- `updated_at` - 更新时间

#### auctions - 拍卖标的表
- `id` - 拍卖ID（主键）
- `title` - 标的名称
- `description` - 标的描述
- `starting_price` - 起拍价
- `current_price` - 当前最高价
- `min_increment` - 最低加价幅度（默认0.01）
- `current_bidder_id` - 当前最高出价者ID（外键）
- `seller_id` - 发布者ID（外键）
- `end_time` - 拍卖结束时间
- `status` - 状态（active/ended/no_bid）
- `images` - 标的图片（JSON数组）
- `created_at` - 创建时间
- `updated_at` - 更新时间

#### bids - 出价记录表
- `id` - 出价ID（主键）
- `auction_id` - 拍卖标的ID（外键）
- `bidder_id` - 出价者ID（外键）
- `amount` - 出价金额
- `created_at` - 出价时间

### 索引
- `idx_auctions_status` - 拍卖状态索引
- `idx_auctions_end_time` - 拍卖结束时间索引
- `idx_bids_auction_id` - 出价拍卖ID索引
- `idx_bids_bidder_id` - 出价者ID索引

## 注意事项

1. **密码要求**：密码至少8位，必须包含字母和数字
2. **拍卖结束时间**：必须至少在未来1小时后
3. **出价规则**：出价金额必须大于当前最高价加上最低加价幅度
4. **最低加价幅度**：发布拍卖时可自定义，默认为0.01
5. **定时任务**：系统每30秒检查一次到期拍卖并自动结算
6. **拍卖状态**：
   - `active` - 拍卖进行中
   - `ended` - 拍卖已结束（有出价）
   - `no_bid` - 拍卖流拍（无出价）
7. **JWT Token**：有效期24小时，过期后需重新登录
8. **文件上传**：最大文件大小16MB
9. **数据持久化**：Docker模式下数据保存在data目录，删除容器不会丢失数据

## 开发说明

### 后端开发
- **框架**：Flask 3.0.0
- **架构**：使用蓝图（Blueprint）组织路由
  - `auth_bp` - 认证相关路由
  - `auction_bp` - 拍卖相关路由
  - `bid_bp` - 竞拍相关路由
- **认证**：Flask-JWT-Extended，Token有效期24小时
- **定时任务**：APScheduler后台任务，每30秒检查一次
- **数据库**：SQLite with Row Factory（字典模式）
- **密码加密**：Werkzeug的generate_password_hash/check_password_hash
- **跨域处理**：Flask-CORS，支持所有API路由
- **日志记录**：标准logging模块，记录请求和响应信息
- **IP追踪**：支持X-Forwarded-For和X-Real-IP头

### 前端开发
- **框架**：Vue 3.3.4
- **UI组件库**：Element Plus 2.4.4
- **路由**：Vue Router 4.2.5
- **HTTP客户端**：Axios 1.6.0
- **状态管理**：Vuex（轻量级使用）
- **图标**：@element-plus/icons-vue
- **响应式设计**：支持移动端和桌面端
- **页面组件**：
  - Login.vue - 登录页面
  - Register.vue - 注册页面
  - Home.vue - 首页/拍卖列表
  - AuctionDetail.vue - 拍卖详情
  - CreateAuction.vue - 发布拍卖
  - MyAuctions.vue - 我的拍卖
  - MyBids.vue - 我的竞拍

### 项目特点
- **前后端分离**：完全独立的前后端架构
- **RESTful API**：标准的REST接口设计
- **容器化部署**：完整的Docker支持
- **数据持久化**：支持数据卷挂载
- **日志管理**：完整的请求日志和错误日志
- **安全性**：密码加密、JWT认证、CORS配置

## 许可证

MIT License


# HealthData-Valuator | 医疗数据资产价值计量器

本项目旨在构建一套标准化的医疗数据资产价值评估系统。通过科学的指标体系与加权算法，为全国各级医院提供数据资产估值服务。

## 项目定位

* **当前版本**: V2.0.0 (功能完善版)
* **核心目标**: 实现"指标输入 -> 自动计算 -> 结果展示"的闭环流程
* **交付日期**: 2026年3月

---

## 技术选型

为了兼顾开发效率与系统稳定性，本项目采用全栈分离架构：

### 前端技术栈
* **框架**: Vue 3 (Composition API)
* **UI 组件库**: Element Plus
* **构建工具**: Vite 5.0
* **状态管理**: Pinia
* **路由管理**: Vue Router 4
* **数据可视化**: ECharts + vue-echarts
* **HTTP 客户端**: Axios

### 后端技术栈
* **Web 框架**: FastAPI 0.104.1
* **ASGI 服务器**: Uvicorn
* **ORM**: SQLAlchemy 2.0
* **数据验证**: Pydantic 2.5
* **数据库**: MySQL 8.0 (使用 PyMySQL 驱动)
* **配置管理**: Pydantic Settings (支持环境变量)

### 开发工具
* **版本控制**: Git (Gitee/GitHub)
* **API 调试**: Apifox
* **IDE**: Cursor / VS Code

---

## 核心功能特性

### 用户功能
* ✅ **用户注册与登录**: 支持医院用户自助注册，JWT Token 认证
* ✅ **数据录入**: 9大类成本指标在线录入，支持折叠式表单和实时计算
* ✅ **评估报告**: 自动生成可视化评估报告，包含雷达图、饼图、柱状图等
* ✅ **历史记录**: 查看和管理历史评估记录
* ✅ **个人中心**: 个人信息管理和评估历史查看

### 管理员功能
* ✅ **数据看板**: 系统全量数据统计和可视化展示
* ✅ **权重配置**: 动态调整9大类指标的测算权重系数
* ✅ **评估管理**: 查看所有用户的评估记录，支持搜索和筛选

### 技术特性
* ✅ **响应式设计**: 适配PC端和移动端浏览器
* ✅ **路由守卫**: 基于Token的权限控制和页面访问控制
* ✅ **数据持久化**: SQLite数据库存储，支持数据持久化
* ✅ **API文档**: FastAPI自动生成交互式API文档

---

## 项目路线

### 阶段一：需求对齐与脚手架搭建 ✅

> **目标：** 环境统一，实现团队成员本地代码跑通，明确开发规范。

* **负责人 (组长)：**
* [√] 搭建 Git 仓库 (Gitee/GitHub) 并配置团队权限。
* [√] 初始化前后端脚手架：`FastAPI` (后端) + `Vue3 Vite` (前端)。
* [√] 设计初步数据库模型 (ER图) 与 API 基础规范。

* **组员：**
* [√] 配置本地开发环境。
* [√] 熟悉 Git 基础指令 (Clone, Pull, Push)。
* [√] 熟悉选定的技术栈基础架构。

---

### 阶段二：基础设施与认证联通 ✅

> **目标：** 解决"进得去"的问题，确保前后端握手成功。

* **前端：**
* [√] 初始化 Vue3 + Vite 项目，引入 Element Plus。
* [√] 封装 Axios 请求拦截器（处理 Token 和 401 跳转）。
* [√] 完成登录页与注册页 UI，实现对接后端登录接口。
* [√] 配置 Vue Router 路由管理和 Pinia 状态管理。

* **后端：**
* [√] 初始化 FastAPI 项目结构，配置 SQLite 数据库连接。
* [√] 编写 `User` 模型，实现 `Register`（注册）与 `Login`（登录）接口，完成联调。
* [√] 实现 Token 生成与验证机制。

---

### 阶段三：完成数据采集与测算 ✅

**目标：** 实现从"前端填表"到"后端计算"到"前端展示"

* **前端：**
* [√] 开发表单组件（折叠式），对应 9 类成本指标。
* [√] 实现表单前端校验（如金额必填、非负数）。
* [√] 对接提交接口，用户点击"提交"后，前端立即获取后端算出的结果，并跳转至报告页。
* [√] 实现评估结果展示页面，包含可视化图表（雷达图、饼图、柱状图）。

* **后端：**
* [√] 编写 `Evaluation`（主表）和 `IndicatorData`（明细表）的 SQLAlchemy 模型。
* [√] 开发 `POST /evaluations` 接口（接收 9 类指标数据并入库）。
* [√] 开发 `GET /evaluations` 接口（返回历史列表）。
* [√] 开发 `GET /evaluations/{id}` 接口（返回单次评估的完整明细，供前端渲染报告）。
* [√] 开发 `DELETE /evaluations/{id}` 接口（删除评估记录）。

---

### 阶段四：管理员看板与系统封版 ✅

**目标：** 解决"管得好"的问题，完成最后交付。

* **后端：**
* [√] 实现 `GET /admin/stats` 接口（全量数据汇总）。
* [√] 实现 `PUT /admin/weights` 接口（动态权重调整）。
* [ ] 全量接口压力测试与 Bug 修复。

* **前端：**
* [√] 开发管理员专属看板（Dashboard）和权重设置页。
* [√] 整体 UI 细节优化，处理响应式适配。
* [√] 评估报告可视化：引入 Echarts。雷达图：展示 9 类指标的分布情况。饼图/柱状图：展示各项指标在总资产价值中的占比。
* [√] 准备演示 Demo 数据。

---

## 快速开始

### 环境要求

* Python 3.11+
* Node.js 16+
* npm 或 yarn

### 推荐：一键启动（单终端）

在项目**根目录**执行（只需开一个终端）：

```bash
# 首次：安装根目录工具 + 前端依赖（后端依赖见下一步）
npm install
npm run install:all

# 首次：生成 backend/.env（从模板复制，不会覆盖已有文件）
npm run init-env
# 然后编辑 backend/.env，填写 DB_PASSWORD 等 MySQL 配置

# 首次：安装 Python 依赖（建议在 backend 下使用虚拟环境）
cd backend
pip install -r requirements.txt
cd ..

# 每次开发：同时启动后端(8000) + 前端(3000)，按 Ctrl+C 可一并结束
npm run dev
```

访问：**http://localhost:3000**（前端通过代理访问 `/api`，无需再单独开终端）。

> **说明**：`npm run dev` 依赖本机已安装 `python` 且能在命令行执行（Windows 可装 Python 并勾选「Add to PATH」）。若 `python` 不可用，可尝试将根目录 `package.json` 里 `dev:api` 中的 `python` 改为 `py`。

---

### 安装步骤（分步 / 与上文等价）

```bash
# 1. 克隆项目
git clone [项目地址]
cd HealthData-Valuator

# 2. 配置数据库
# 2.1 安装并启动 MySQL 8.0
# 2.2 创建数据库
mysql -u root -p
CREATE DATABASE healthdata_valuator CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;

# 2.3 配置环境变量（也可用根目录 npm run init-env 自动生成）
cd backend
# 复制环境变量示例文件为 .env（必须在 backend 目录下执行，任选一种）
cp .env.example .env                    # Linux / macOS / Git Bash
#   Copy-Item .env.example .env             # Windows PowerShell
#   copy .env.example .env                  # Windows CMD
# 编辑 .env 文件，填入你的 MySQL 配置信息
# DB_HOST=localhost
# DB_PORT=3306
# DB_USER=root
# DB_PASSWORD=your_password
# DB_NAME=healthdata_valuator

# 3. 后端启动
pip install -r requirements.txt
# 数据库表会自动创建（通过 SQLAlchemy）
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000

# 后端 API 默认运行在 http://localhost:8000
# API 文档访问地址: http://localhost:8000/docs

# 4. 前端启动（新开一个终端；若已用根目录 npm run dev 则无需此步）
cd frontend
npm install
npm run dev

# 前端开发服务器默认运行在 http://localhost:3000
```

### 访问地址

* **前端应用**: http://localhost:3000
* **后端 API**: http://localhost:8000
* **API 文档**: http://localhost:8000/docs
* **API 交互式文档**: http://localhost:8000/redoc

### 前后端联调说明

1. **启动方式**：推荐在项目根目录执行 **`npm run dev`**（同时起后端与前端）；或分两个终端分别启动后端、前端。
2. **后端**：需运行在 **8000** 端口（`python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000`）。
3. **前端**：运行在 **3000** 端口（`cd frontend && npm run dev`）。
4. **代理**：`vite.config.js` 已将 `/api` 代理到 `http://localhost:8000`，前端请求 `axios.get('/api/xxx')` 会转发到 `http://localhost:8000/api/xxx`。
5. **若出现 404**：检查后端是否已启动、端口是否为 8000；检查请求路径是否与后端路由一致（如 `/api/user/info`、`/api/evaluations` 等）。

### 管理员登录与入口

1. **管理员账号**：用户名为 **admin** 的账号视为管理员（与普通用户同一套登录接口）。
2. **如何获得 admin 账号**：
   - 方式一：在前端首页或任意页面，若项目提供「演示数据初始化」入口，执行一次即可创建测试用户，其中包括 **admin / admin123**。
   - 方式二：调用后端接口 `POST /api/demo/init`，会创建 admin、doctor_zhang、nurse_li 等测试账号及示例评估数据。
   - 方式三：在数据库中手动插入一条用户记录，用户名为 `admin`，密码自设（当前为明文存储）。
3. **登录步骤**：打开登录页 → 用户名输入 **admin**，密码输入 **admin123**（若通过演示数据初始化创建）→ 登录。
4. **进入管理员端**：登录成功后，点击右上角 **用户名下拉菜单** → 选择 **「管理员看板」**，或浏览器直接访问 **http://localhost:3000/admin/dashboard**。
5. **管理员功能**：**管理员看板**（`/admin/dashboard`）查看系统统计与评估列表；**权重设置**（`/admin/weights`）调整 9 大类成本权重。非 admin 用户访问上述地址会被重定向到个人中心。

---

## 项目结构

```
HealthData-Valuator/
├── package.json               # 根目录：npm run dev 一键启动前后端；npm run init-env 生成 .env
├── scripts/
│   └── copy-env.js            # 复制 backend/.env.example → backend/.env（不存在时）
├── backend/                    # 后端项目目录
│   ├── main.py                # FastAPI 应用入口（简化版）
│   ├── requirements.txt       # Python 依赖列表
│   ├── sql_app.db            # SQLite 数据库文件（自动生成）
│   └── app/                   # 应用主目录
│       ├── __init__.py
│       ├── api/               # API 路由目录
│       │   ├── __init__.py
│       │   └── api.py        # 主要 API 路由实现
│       ├── models/            # 数据库模型目录
│       │   ├── __init__.py
│       │   └── models.py     # SQLAlchemy 模型定义
│       ├── schemas/           # Pydantic 模式目录
│       │   ├── __init__.py
│       │   └── schemas.py    # 数据验证模式
│       ├── crud/              # 数据库操作目录
│       │   ├── __init__.py
│       │   └── crud.py       # CRUD 操作函数
│       └── core/              # 核心配置目录
│           ├── __init__.py
│           ├── config.py      # 应用配置（数据库等）
│           └── database.py    # 数据库连接配置
│
└── frontend/                  # 前端项目目录
    ├── package.json           # Node.js 项目配置
    ├── vite.config.js         # Vite 构建配置
    ├── index.html             # HTML 入口文件
    └── src/                   # 源代码目录
        ├── main.js            # Vue 应用入口
        ├── App.vue            # 根组件
        ├── api/               # API 接口目录
        │   ├── request.js    # Axios 封装
        │   ├── user.js       # 用户相关 API
        │   └── evaluation.js # 评估相关 API
        ├── router/            # 路由配置
        │   └── index.js      # Vue Router 配置
        ├── store/             # 状态管理目录
        │   ├── index.js      # Pinia 初始化
        │   ├── user.js       # 用户状态管理
        │   └── admin.js      # 管理员状态管理
        ├── views/             # 页面视图目录
        │   ├── Home.vue      # 首页
        │   ├── Login.vue     # 登录页
        │   ├── Register.vue  # 注册页
        │   ├── DataInput.vue # 数据录入页
        │   ├── ResultDisplay.vue # 结果展示页
        │   ├── PersonalCenter.vue # 个人中心
        │   └── admin/         # 管理员页面
        │       ├── Dashboard.vue # 管理员看板
        │       └── WeightSetting.vue # 权重设置
        └── components/        # 组件目录
            └── charts/        # 图表组件
                ├── BaseChart.vue
                └── RadarChart.vue
```

---

## API 接口说明

详细的 API 接口文档请参考 [API.md](./API.md)

### 主要接口

* **认证模块**: `/api/auth/register`, `/api/auth/login`
* **评估模块**: `/api/evaluations` (GET, POST), `/api/evaluations/{id}` (GET, DELETE)
* **管理模块**: `/api/admin/stats` (GET), `/api/admin/weights` (PUT)

---

## 数据库设计

### 主要数据表

* **users**: 用户信息表
* **evaluations**: 评估任务主表
* **indicator_data**: 指标明细表

详细的数据模型定义请参考 `backend/app/models/models.py`

---

## 开发规范

* **代码风格**: 遵循 PEP 8 (Python) 和 ESLint (JavaScript)
* **提交规范**: 使用有意义的 commit message
* **分支管理**: main 分支为稳定版本，开发在 feature 分支进行

---

## 阿里云公网部署

面向仅有公网 IP 的部署方案（Nginx 反代前端 + 反代 `/api` 到后端，后端用 systemd 守护进程）。

参考文档：
* `DEPLOY_ALIYUN_PUBLIC.md`
* `deploy_nginx_public.conf`
* `deploy_backend_systemd.service`

## 注意事项

1. **数据库配置**: 
   - 项目已配置为使用 MySQL 8.0
   - 数据库配置通过 `.env` 文件管理，请参考 `backend/.env.example`
   - 首次运行前需要创建数据库：`CREATE DATABASE healthdata_valuator CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`
   - 数据库表会在应用启动时自动创建（通过 SQLAlchemy）
2. **环境变量**: 
   - 后端配置通过 `.env` 文件管理
   - 请复制 `backend/.env.example` 为 `backend/.env` 并填入实际配置
   - `.env` 文件已添加到 `.gitignore`，不会提交到版本控制
3. **Token 安全**: 当前 Token 生成使用简单随机字符串，生产环境建议使用 JWT
4. **密码安全**: 当前密码以明文存储，生产环境必须使用哈希加密
5. **CORS 配置**: 当前允许所有来源访问，生产环境应限制为特定域名
6. **数据库连接池**: 默认连接池大小为 5，最大溢出为 10，可在 `.env` 文件中配置

---

## 许可证

本项目采用 MIT 许可证。

---

## 联系方式

如有问题或建议，请通过以下方式联系：

* 邮箱: xxx
* 电话: xxx

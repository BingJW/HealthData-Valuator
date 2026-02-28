# 项目文件结构说明

本文档详细说明了 HealthData-Valuator 项目中每个文件的作用和内容。

---

## 📁 后端项目 (backend/)

### 根目录文件

#### `main.py`
- **作用**: FastAPI 应用的主入口文件
- **内容说明**:
  - 创建 FastAPI 应用实例，设置标题和版本号
  - 配置 CORS 中间件，允许所有来源访问（方便前端联调）
  - 定义根路由 `/`，返回 API 运行状态信息
- **启动方式**: `uvicorn main:app --reload`

#### `requirements.txt`
- **作用**: Python 项目依赖管理文件
- **包含的包**:
  - `fastapi==0.104.1` - Web 框架
  - `uvicorn[standard]==0.24.0` - ASGI 服务器
  - `sqlalchemy==2.0.23` - ORM 数据库操作库
  - `pydantic==2.5.0` - 数据验证库
  - `pydantic-settings==2.1.0` - 配置管理扩展
- **安装方式**: `pip install -r requirements.txt`

---

### `app/` 目录结构

#### `app/__init__.py`
- **作用**: Python 包标识文件，使 `app` 目录成为一个 Python 包

#### `app/api/__init__.py`
- **用途**: 后续在此目录下创建各个 API 路由文件（如 `users.py`, `indicators.py` 等）

#### `app/models/__init__.py`
- **用途**: 后续在此目录下使用 SQLAlchemy 定义数据库模型（如 `User`, `Indicator` 等）

#### `app/schemas/__init__.py`
- **用途**: 后续在此目录下定义 API 请求/响应的数据验证模式（如 `UserCreate`, `IndicatorResponse` 等）

#### `app/core/__init__.py`
- **用途**: 后续在此目录下存放核心配置文件（如 `config.py`, `security.py`, `database.py` 等）
- **内容**: 空文件

---

## 📁 前端项目 (frontend/)

### 根目录文件

#### `package.json`
- **作用**: Node.js 项目配置文件，定义项目元数据和依赖
- **内容说明**:
  - **scripts**: 
    - `dev` - 启动开发服务器
    - `build` - 构建生产版本
    - `preview` - 预览生产构建
  - **dependencies**: 生产依赖
    - `vue@^3.3.4` - Vue 3 框架
    - `element-plus@^2.4.4` - UI 组件库
    - `axios@^1.6.2` - HTTP 请求库
  - **devDependencies**: 开发依赖
    - `@vitejs/plugin-vue@^4.5.0` - Vite 的 Vue 插件
    - `vite@^5.0.0` - 构建工具

#### `vite.config.js`
- **作用**: Vite 构建工具配置文件
- **内容说明**:
  - 配置 Vue 插件
  - 设置开发服务器端口为 5173
  - 配置代理：将 `/api` 请求代理到 `http://localhost:8000`（后端 API 地址）
  - 自动重写路径，去除 `/api` 前缀

#### `index.html`
- **作用**: HTML 入口文件
- **内容说明**:
  - 定义页面基本结构
  - 设置页面标题为"医疗数据资产价值计量器"
  - 引入 Vue 应用的挂载点 `<div id="app"></div>`
  - 通过 `<script>` 标签引入 `main.js` 作为应用入口

#### `.gitignore`
- **作用**: Git 版本控制忽略文件配置
- **忽略内容**: 
  - `node_modules/` - 依赖包目录
  - `dist/` - 构建输出目录
  - 日志文件、编辑器配置文件等

---

### `src/` 目录结构

#### `src/main.js`
- **作用**: Vue 应用的入口文件
- **内容说明**:
  - 使用 `createApp` 创建 Vue 应用实例
  - 引入并注册 Element Plus 组件库
  - 引入 Element Plus 的样式文件
  - 挂载 `App.vue` 组件到 `#app` 元素

#### `src/App.vue`
- **作用**: Vue 应用的根组件
- **内容说明**:
  - 使用 Composition API (`<script setup>`)
  - 展示 Element Plus 的 `el-card` 组件
  - 显示欢迎信息："医疗数据资产价值计量器 - 欢迎体验"
  - 包含样式定义，实现居中布局和卡片样式

#### `src/api/request.js`
- **作用**: Axios 请求封装文件
- **内容说明**:
  - 创建 Axios 实例，配置基础 URL 为 `/api`，超时时间为 10 秒
  - **请求拦截器**: 在发送请求前进行处理（可在此添加 token、请求头等）
  - **响应拦截器**: 统一处理响应数据，直接返回 `response.data`
  - 导出封装好的 `request` 对象，供其他模块使用

---

### `src/` 子目录说明

#### `src/views/`
- **作用**: 存放页面级组件（路由对应的视图组件）
- **当前状态**: 空目录，使用 `.gitkeep` 保持目录结构
- **后续用途**: 存放如 `Home.vue`, `Login.vue`, `Dashboard.vue` 等页面组件

#### `src/components/`
- **作用**: 存放可复用的通用组件
- **当前状态**: 空目录，使用 `.gitkeep` 保持目录结构
- **后续用途**: 存放如 `Header.vue`, `Footer.vue`, `DataTable.vue` 等组件

#### `src/store/`
- **作用**: 存放状态管理相关文件（如 Vuex 或 Pinia）
- **当前状态**: 空目录，使用 `.gitkeep` 保持目录结构
- **后续用途**: 存放全局状态管理逻辑，如用户信息、应用配置等

---

## 目录结构总览

```
HealthData-Valuator/
├── backend/                    # 后端项目目录
│   ├── main.py                # FastAPI 应用入口
│   ├── requirements.txt       # Python 依赖列表
│   └── app/                   # 应用主目录
│       ├── __init__.py
│       ├── api/               # API 路由目录
│       │   └── __init__.py
│       ├── models/            # 数据库模型目录
│       │   └── __init__.py
│       ├── schemas/           # Pydantic 模式目录
│       │   └── __init__.py
│       └── core/              # 核心配置目录
│           └── __init__.py
│
└── frontend/                  # 前端项目目录
    ├── package.json           # Node.js 项目配置
    ├── vite.config.js         # Vite 构建配置
    ├── index.html             # HTML 入口文件
    ├── .gitignore            # Git 忽略配置
    └── src/                   # 源代码目录
        ├── main.js            # Vue 应用入口
        ├── App.vue            # 根组件
        ├── api/               # API 接口目录
        │   └── request.js    # Axios 封装
        ├── views/             # 页面视图目录
        ├── components/        # 组件目录
        └── store/             # 状态管理目录
```


## 注意事项

1. **后端 CORS 配置**: 当前配置允许所有来源访问，生产环境应限制为特定域名
2. **前端代理配置**: 开发环境下，前端通过 `/api` 前缀访问后端，Vite 会自动代理到 `http://localhost:8000`
3. **目录结构**: 使用 `.gitkeep` 文件保持空目录在 Git 中的存在
4. **依赖版本**: 建议使用固定版本号以确保团队环境一致

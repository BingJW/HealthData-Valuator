# 本地开发、数据库配置与验证

命令未特别注明时均从项目根目录执行。本指南合并原 README 启动章节和后端快速开始、数据库配置说明。

## 本地启动

环境：Python 3.11+、Node.js 20（本机验证为 20.20.0）、MySQL。前端锁定 Vite 6.4.3，后端默认使用 MySQL；SQLite 仅用于隔离测试。

在项目根目录执行：

```powershell
# 首次安装；已有 .venv 时不要重复创建
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend/requirements.txt
npm ci
npm ci --prefix frontend
npm run init-env
```

编辑 `backend/.env` 填写本机数据库配置，不要把密码提交 Git。先用数据库管理工具创建 `healthdata_valuator`（utf8mb4），再运行：

```powershell
npm run dev
```

启动脚本优先使用项目 `.venv` 中的 Python，也可用 `PYTHON` 环境变量指定解释器。首次启动会创建缺失的表，**不会自动改写旧表结构**。启动时若报告缺少字段，请阅读[更新说明](../releases/2026-09-08.md)后迁移，不要删库重建。

- 网站：http://127.0.0.1:3000/
- API 文档：http://127.0.0.1:8000/docs
- 操作指引：http://127.0.0.1:3000/documents/user-guide.pdf
- 在启动终端按 Ctrl+C 停止前后端。

普通用户在网站注册。现有管理员继续使用原账号；新环境只允许在服务器/本机终端创建初始管理员：

```powershell
cd backend
..\.venv\Scripts\python.exe -B create_admin.py
```

脚本通过隐藏输入读取密码，不提供公开管理员注册或默认密码。已有管理员时不会覆盖。

## 验证

从项目根目录执行：

```powershell
.\.venv\Scripts\python.exe -B -m unittest discover -s backend/tests -v
npm run lint --prefix frontend
node --test frontend/tests/export.test.mjs
npm run build --prefix frontend
npm audit --prefix frontend
```

后端测试自行创建临时数据库和本地 HTTP 服务，不使用实际业务数据。`npm run lint` 只检查，不再自动修改源文件。前端构建产物在 `frontend/dist`，操作指引会随构建一起复制进去。


## 单独启动后端

在项目根目录打开终端，进入后端目录执行：

```powershell
cd backend
..\.venv\Scripts\python.exe -B -m uvicorn main:app --host 127.0.0.1 --port 8000
```

## 数据库配置与兼容

默认数据库为MySQL。复制backend/.env.example为.env并填写DB_HOST、DB_PORT、DB_USER、DB_PASSWORD、DB_NAME；连接地址已支持密码中的特殊符号。

先在MySQL管理工具执行：

```sql
CREATE DATABASE healthdata_valuator CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

仅在数据库尚不存在时创建。已有数据库不要删除。

在项目根目录运行 `.\.venv\Scripts\python.exe -B backend/init_db.py`，或启动 `main:app`，会使用 `app/models/models.py` 中同一套模型创建缺失表：users、evaluations、login_sessions、weight_settings。

`create_all`不会迁移已有列。旧原型evaluation_name/user_id结构不能与当前name/username/indicators结构混用，启动会检查必要字段。字段不足时应先备份并分析实际结构，不能通过删表来绕过错误。

DATABASE_URL用于显式连接覆盖；自动回归测试使用一次性SQLite文件，不访问实际MySQL数据。实际部署和回退说明见[更新说明](../releases/2026-09-08.md)。

## 后续部署

生产环境部署 frontend/dist 并配置 /api 反向代理；不使用 Vite 开发服务器作为生产服务。发布前阅读[更新说明中的兼容、备份和回退事项](../releases/2026-09-08.md)。本文不是已验证的服务器部署操作手册。

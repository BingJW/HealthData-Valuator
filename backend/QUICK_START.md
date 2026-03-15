# 快速开始指南

## 数据库已创建后的操作步骤

### ✅ 步骤 1: 创建 `.env` 配置文件

在 `backend` 目录下创建 `.env` 文件，填入你的 MySQL 配置：

**Windows PowerShell:**
```powershell
cd backend
notepad .env
```

**Windows CMD:**
```cmd
cd backend
notepad .env
```

**macOS/Linux:**
```bash
cd backend
nano .env
```

在 `.env` 文件中填入以下内容（**重要：必须填写你的 MySQL root 密码**）：

```env
# MySQL 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=你的MySQL密码
DB_NAME=healthdata_valuator

# 数据库连接池配置
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10
```

**⚠️ 重要提示：**
- `DB_PASSWORD` 必须填写你安装 MySQL 时设置的 root 密码
- 如果密码为空，也要确保这一行存在：`DB_PASSWORD=`
- 保存文件后关闭编辑器

---

### ✅ 步骤 2: 安装 Python 依赖

在 `backend` 目录下执行：

```bash
pip install -r requirements.txt
```

**如果使用虚拟环境（推荐）：**

```bash
# 创建虚拟环境（如果还没有）
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

这会安装以下新添加的包：
- `pymysql` - MySQL 驱动
- `cryptography` - 加密库（PyMySQL 的依赖）

---

### ✅ 步骤 3: 初始化数据库表

有两种方式：

#### 方式一：使用初始化脚本（推荐）

```bash
python init_db.py
```

如果成功，你会看到：
```
正在连接到数据库: localhost:3306/healthdata_valuator
正在创建数据表...
数据库初始化完成！
已创建以下表:
  - users
  - evaluations
  - indicator_data
```

#### 方式二：启动应用自动创建

```bash
uvicorn main:app --reload
```

应用启动时会自动创建表结构。

---

### ✅ 步骤 4: 验证数据库连接

启动应用后，打开浏览器访问：

**http://localhost:8000**

如果看到：
```json
{
  "status": "online",
  "message": "MySQL 数据库连接已启用"
}
```

说明数据库连接成功！🎉

你也可以访问 API 文档：
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 常见问题

### ❌ 问题 1: 连接失败

**错误信息：** `Can't connect to MySQL server` 或 `Access denied`

**解决方案：**
1. 检查 `.env` 文件中的 `DB_PASSWORD` 是否正确
2. 检查 MySQL 服务是否正在运行
3. 确认数据库名称 `healthdata_valuator` 已创建

### ❌ 问题 2: 找不到 pymysql 模块

**错误信息：** `ModuleNotFoundError: No module named 'pymysql'`

**解决方案：**
```bash
pip install pymysql cryptography
```

### ❌ 问题 3: 表创建失败

**错误信息：** `Table 'xxx' already exists`

**解决方案：**
如果表已存在，可以忽略这个错误，或者先删除旧表：
```sql
mysql -u root -p
USE healthdata_valuator;
DROP TABLE IF EXISTS indicator_data;
DROP TABLE IF EXISTS evaluations;
DROP TABLE IF EXISTS users;
EXIT;
```
然后重新运行 `python init_db.py`

---

## 下一步

数据库配置完成后，你可以：

1. **测试注册功能**：访问 http://localhost:8000/docs，尝试调用 `/api/auth/register` 接口
2. **启动前端**：在 `frontend` 目录下运行 `npm run dev`
3. **开始开发**：参考 [API.md](../API.md) 了解接口规范

---

## 完整命令清单（复制粘贴）

```bash
# 1. 进入后端目录
cd backend

# 2. 创建 .env 文件（手动编辑，填入密码）
notepad .env

# 3. 安装依赖
pip install -r requirements.txt

# 4. 初始化数据库表
python init_db.py

# 5. 启动应用
uvicorn main:app --reload
```

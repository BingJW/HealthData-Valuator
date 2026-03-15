# 数据库配置说明

本项目使用 MySQL 8.0 作为数据库。

## 快速开始

### 1. 安装 MySQL

确保你的系统已安装 MySQL 8.0 或更高版本。

**Windows 系统：**
- 下载 MySQL Installer: https://dev.mysql.com/downloads/installer/
- 运行安装程序，选择 "Developer Default" 或 "Server only"
- 记住设置的 root 密码

**macOS 系统：**
```bash
brew install mysql
brew services start mysql
```

**Linux 系统：**
```bash
sudo apt-get update
sudo apt-get install mysql-server
sudo systemctl start mysql
```

### 2. 创建数据库

有两种方式创建数据库：

#### 方式一：使用 MySQL 命令行（终端）

1. **打开终端/命令提示符**

   **Windows:**
   - 按 `Win + R`，输入 `cmd` 或 `powershell`
   - 或者在开始菜单搜索 "命令提示符" 或 "PowerShell"

   **macOS/Linux:**
   - 打开终端应用

2. **登录 MySQL**

   ```bash
   mysql -u root -p
   ```
   
   输入你安装 MySQL 时设置的 root 密码

3. **创建数据库**

   ```sql
   CREATE DATABASE healthdata_valuator CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

4. **验证数据库是否创建成功**

   ```sql
   SHOW DATABASES;
   ```
   
   你应该能看到 `healthdata_valuator` 在列表中

5. **退出 MySQL**

   ```sql
   EXIT;
   ```


### 3. 配置环境变量

在 `backend` 目录下创建 `.env` 文件：

**Windows PowerShell:**
```powershell
cd backend
Copy-Item .env.example .env
notepad .env
```

**Windows CMD:**
```cmd
cd backend
copy .env.example .env
notepad .env
```

**macOS/Linux:**
```bash
cd backend
cp .env.example .env
nano .env  # 或使用 vim .env
```

编辑 `.env` 文件，填入你的 MySQL 配置：

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

**重要提示：**
- `DB_PASSWORD` 必须填写你安装 MySQL 时设置的 root 密码
- 如果密码包含特殊字符，不需要转义，直接填写即可
- `.env` 文件不会被提交到 Git（已在 .gitignore 中）

### 4. 安装 Python 依赖

在 `backend` 目录下执行：

```bash
pip install -r requirements.txt
```

如果使用虚拟环境（推荐）：

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

### 5. 初始化数据库表

有两种方式初始化数据库表：

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

应用启动时会自动创建表结构。如果看到错误，请检查：
1. MySQL 服务是否正在运行
2. `.env` 文件中的配置是否正确
3. 数据库是否已创建

### 6. 验证数据库连接

启动应用后，访问 http://localhost:8000，如果看到：
```json
{
  "status": "online",
  "message": "MySQL 数据库连接已启用"
}
```
说明数据库连接成功！

## 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 | 必填 |
|--------|------|--------|------|
| DB_HOST | MySQL 服务器地址 | localhost | 是 |
| DB_PORT | MySQL 端口 | 3306 | 否 |
| DB_USER | MySQL 用户名 | root | 是 |
| DB_PASSWORD | MySQL 密码 | （空） | **是** |
| DB_NAME | 数据库名称 | healthdata_valuator | 是 |
| DB_POOL_SIZE | 连接池大小 | 5 | 否 |
| DB_MAX_OVERFLOW | 最大溢出连接数 | 10 | 否 |

### 连接字符串格式

```
mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4
```

## 数据表结构

数据库表会在首次运行时自动创建，包括：

- `users`: 用户信息表
- `evaluations`: 评估任务主表
- `indicator_data`: 指标明细表

详细的数据模型定义请参考 `app/models/models.py`。

## 故障排查

### 问题 1: 无法连接到 MySQL

**错误信息：** `Can't connect to MySQL server`

**解决方案：**
1. 检查 MySQL 服务是否运行：
   - **Windows:** 打开"服务"应用，查找 "MySQL80"，确保状态为"正在运行"
   - **macOS:** `brew services list` 查看 MySQL 状态
   - **Linux:** `sudo systemctl status mysql`
2. 检查端口是否正确（默认 3306）
3. 检查防火墙设置

### 问题 2: 认证失败

**错误信息：** `Access denied for user 'root'@'localhost'`

**解决方案：**
1. 检查 `.env` 文件中的 `DB_PASSWORD` 是否正确
2. 尝试重置 MySQL root 密码
3. 检查用户名是否正确

### 问题 3: 数据库不存在

**错误信息：** `Unknown database 'healthdata_valuator'`

**解决方案：**
1. 按照步骤 2 创建数据库
2. 检查 `.env` 文件中的 `DB_NAME` 是否正确

### 问题 4: 字符编码问题

**错误信息：** 中文乱码

**解决方案：**
确保数据库使用 `utf8mb4` 字符集：

```sql
ALTER DATABASE healthdata_valuator CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 问题 5: 表创建失败

**错误信息：** `Table 'xxx' already exists` 或其他表相关错误

**解决方案：**
1. 检查数据库中是否已有表：
   ```sql
   USE healthdata_valuator;
   SHOW TABLES;
   ```
2. 如果需要重新创建，先删除旧表：
   ```sql
   DROP TABLE IF EXISTS indicator_data;
   DROP TABLE IF EXISTS evaluations;
   DROP TABLE IF EXISTS users;
   ```
3. 然后运行 `python init_db.py`

### 问题 6: 找不到 mysql 命令

**Windows 解决方案：**
1. 将 MySQL 的 bin 目录添加到系统 PATH
2. 默认路径：`C:\Program Files\MySQL\MySQL Server 8.0\bin`
3. 或者在 MySQL Command Line Client 中执行命令

**macOS/Linux 解决方案：**
```bash
# 查找 MySQL 安装路径
which mysql

# 如果找不到，可能需要添加到 PATH
export PATH=$PATH:/usr/local/mysql/bin
```

## 常用 MySQL 命令参考

```sql
-- 查看所有数据库
SHOW DATABASES;

-- 使用数据库
USE healthdata_valuator;

-- 查看所有表
SHOW TABLES;

-- 查看表结构
DESCRIBE users;

-- 查看表中的数据
SELECT * FROM users;

-- 删除数据库（谨慎使用！）
DROP DATABASE healthdata_valuator;
```

## 生产环境建议

1. **使用独立的数据库用户**
   ```sql
   CREATE USER 'app_user'@'localhost' IDENTIFIED BY 'strong_password';
   GRANT ALL PRIVILEGES ON healthdata_valuator.* TO 'app_user'@'localhost';
   FLUSH PRIVILEGES;
   ```
   然后在 `.env` 中使用 `app_user` 而不是 `root`

2. **设置强密码**
   - 至少 12 个字符
   - 包含大小写字母、数字和特殊字符

3. **配置适当的连接池大小**
   - 根据应用负载调整 `DB_POOL_SIZE` 和 `DB_MAX_OVERFLOW`

4. **启用 MySQL 的慢查询日志**
   - 监控性能问题

5. **定期备份数据库**
   ```bash
   mysqldump -u root -p healthdata_valuator > backup.sql
   ```

6. **使用 SSL 连接**（如果数据库在远程服务器）
   - 在连接字符串中添加 SSL 参数

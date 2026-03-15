# 查看数据库内容指南

本文档介绍如何查看 MySQL 数据库中的数据。

## 方法一：使用 Python 脚本（最简单）⭐

### 查看所有数据

```bash
cd d:\Python-Projects\HealthData-Valuator\backend
python view_database.py
```

这会显示：
- 所有用户数据
- 所有评估记录
- 所有指标明细
- 统计信息

### 自定义查询

编辑 `query_examples.py` 文件，添加你自己的查询逻辑，然后运行：

```bash
python query_examples.py
```

---

## 方法二：使用 MySQL 命令行

### Windows

1. **打开命令提示符或 PowerShell**

2. **登录 MySQL**
   ```bash
   mysql -u root -p
   ```
   输入你的 MySQL root 密码

3. **选择数据库**
   ```sql
   USE healthdata_valuator;
   ```

4. **查看所有表**
   ```sql
   SHOW TABLES;
   ```
   应该看到：
   - users
   - evaluations
   - indicator_data

5. **查看表数据**

   **查看用户表：**
   ```sql
   SELECT * FROM users;
   ```

   **查看评估表：**
   ```sql
   SELECT * FROM evaluations;
   ```

   **查看指标明细表：**
   ```sql
   SELECT * FROM indicator_data;
   ```

6. **查看表结构**
   ```sql
   DESCRIBE users;
   DESCRIBE evaluations;
   DESCRIBE indicator_data;
   ```

7. **条件查询示例**
   ```sql
   -- 查询特定用户
   SELECT * FROM users WHERE username = 'testuser';
   
   -- 查询特定评估的指标
   SELECT * FROM indicator_data WHERE evaluation_id = 1;
   
   -- 统计查询
   SELECT COUNT(*) FROM users;
   SELECT SUM(total_value) FROM evaluations;
   ```

8. **退出 MySQL**
   ```sql
   EXIT;
   ```

### 如果找不到 mysql 命令

**Windows 解决方案：**

1. 使用 MySQL Command Line Client：
   - 在开始菜单搜索 "MySQL Command Line Client"
   - 直接输入密码登录
   - 然后执行 SQL 命令

2. 或者将 MySQL 添加到 PATH：
   - MySQL 默认路径：`C:\Program Files\MySQL\MySQL Server 8.0\bin`
   - 将这个路径添加到系统环境变量 PATH 中

---

## 方法三：使用图形化工具（推荐新手）

### MySQL Workbench（官方工具）

1. **下载安装**
   - 访问：https://dev.mysql.com/downloads/workbench/
   - 下载 Windows 版本并安装

2. **连接数据库**
   - 打开 MySQL Workbench
   - 点击 "MySQL Connections" 下的连接（通常是 localhost）
   - 输入 root 密码，点击 "OK"

3. **查看数据**
   - 在左侧 "SCHEMAS" 面板中找到 `healthdata_valuator`
   - 展开数据库，可以看到所有表
   - 右键点击表名 → "Select Rows - Limit 1000"
   - 或者双击表名，在右侧查看数据

4. **执行 SQL 查询**
   - 点击工具栏的 "SQL Editor" 图标
   - 在查询窗口中输入 SQL 语句
   - 点击执行按钮（⚡）或按 `Ctrl+Enter`

### DBeaver（免费，功能强大）

1. **下载安装**
   - 访问：https://dbeaver.io/download/
   - 下载 Community Edition（免费版）

2. **连接数据库**
   - 打开 DBeaver
   - 点击 "新建数据库连接"
   - 选择 "MySQL"
   - 填写连接信息：
     - Host: localhost
     - Port: 3306
     - Database: healthdata_valuator
     - Username: root
     - Password: 你的密码
   - 点击 "测试连接"，成功后点击 "完成"

3. **查看数据**
   - 在左侧数据库导航器中找到 `healthdata_valuator`
   - 展开可以看到所有表
   - 双击表名即可查看数据
   - 可以编辑、添加、删除数据

---

## 常用 SQL 查询命令

### 查看所有数据

```sql
-- 查看所有用户
SELECT * FROM users;

-- 查看所有评估
SELECT * FROM evaluations;

-- 查看所有指标明细
SELECT * FROM indicator_data;
```

### 条件查询

```sql
-- 查询特定用户
SELECT * FROM users WHERE username = 'testuser';

-- 查询特定评估的所有指标
SELECT * FROM indicator_data WHERE evaluation_id = 1;

-- 查询价值大于某个值的评估
SELECT * FROM evaluations WHERE total_value > 100000;
```

### 统计查询

```sql
-- 用户总数
SELECT COUNT(*) FROM users;

-- 评估总数
SELECT COUNT(*) FROM evaluations;

-- 总价值
SELECT SUM(total_value) FROM evaluations;

-- 平均价值
SELECT AVG(total_value) FROM evaluations;

-- 按类别统计指标数量
SELECT category, COUNT(*) FROM indicator_data GROUP BY category;
```

### 关联查询

```sql
-- 查看评估及其所属用户
SELECT e.id, e.evaluation_name, e.total_value, u.username, u.hospital
FROM evaluations e
JOIN users u ON e.user_id = u.id;

-- 查看评估及其所有指标明细
SELECT e.evaluation_name, i.category, i.item_name, i.amount
FROM evaluations e
JOIN indicator_data i ON e.id = i.evaluation_id
WHERE e.id = 1;
```

### 排序和限制

```sql
-- 按创建时间倒序查看评估（最新的在前）
SELECT * FROM evaluations ORDER BY created_at DESC;

-- 查看前 10 条评估记录
SELECT * FROM evaluations LIMIT 10;

-- 查看价值最高的评估
SELECT * FROM evaluations ORDER BY total_value DESC LIMIT 5;
```

---

## 快速查看脚本

运行以下命令快速查看数据库内容：

```bash
# Windows PowerShell
cd d:\Python-Projects\HealthData-Valuator\backend
python view_database.py
```

---

## 注意事项

1. **数据安全**：在生产环境中，不要直接在生产数据库上执行删除或修改操作
2. **备份**：重要操作前建议先备份数据库
3. **权限**：确保你有足够的权限访问数据库
4. **编码**：如果看到中文乱码，确保数据库和连接都使用 `utf8mb4` 字符集

---

## 故障排查

### 问题：无法连接到数据库

**解决方案：**
- 检查 MySQL 服务是否运行
- 检查 `.env` 文件中的配置是否正确
- 检查防火墙设置

### 问题：看不到数据

**解决方案：**
- 确认数据库名称正确：`healthdata_valuator`
- 确认表已创建（运行 `python init_db.py`）
- 检查是否有数据（可能表是空的，这是正常的）

### 问题：中文显示乱码

**解决方案：**
```sql
-- 设置数据库字符集
ALTER DATABASE healthdata_valuator CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 设置连接字符集
SET NAMES utf8mb4;
```

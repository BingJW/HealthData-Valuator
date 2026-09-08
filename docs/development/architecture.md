# 项目结构与业务数据流

此文档描述当前实际运行代码，替代原型阶段的结构说明。

## 请求入口

浏览器 → Vue Router → 页面/Pinia → Axios `/api` → Vite 本地代理（生产环境为反向代理）→ `backend/main.py` → 输入校验/身份/归属检查 → SQLAlchemy → MySQL。

数据库记录的金额按成本直接相加。参考权重单独存储，修改权重不重算当前或历史报告。

## 前端

下表路径相对于 `frontend/`。

| 文件/目录 | 职责 |
|---|---|
| `src/main.js`、`App.vue` | Vue、Element Plus、图标、状态管理与共享样式入口 |
| `src/router/index.js` | 页面路由、登录跳转、前端管理员入口限制；真正权限由后端决定 |
| `src/api/request.js` | 相对地址 `/api`、令牌请求头、401清理状态与错误消息整理 |
| `src/api/user.js`、`evaluation.js`、`admin.js` | 与实际后端接口对应的请求封装 |
| `src/store/user.js` | 登录状态、用户信息、退出登录 |
| `src/store/admin.js` | 管理员统计与参考权重 |
| `views/Home.vue` | 首页、登录/个人中心入口、操作指引阅读和下载 |
| `views/Login.vue`、`Register.vue` | 用户认证表单；不会自动创建演示账号 |
| `views/PersonalCenter.vue` | 个人中心外壳、导航、帮助入口 |
| `views/PersonalCenter*.vue` | 个人统计、历史列表、本机草稿、个人资料 |
| `views/DataInput.vue` | 36 个成本子项录入、新建/编辑、校验、草稿、离开提醒 |
| `views/ResultDisplay.vue` | 真实报告、分类明细、打印/PDF、CSV、复制链接与评估 |
| `views/admin/*` | 全局统计、全量评估管理、用户管理、参考权重 |
| `components/charts/BaseChart.vue` | ECharts 生命周期、选项更新、容器尺寸变化处理 |
| `components/charts/RadarChart.vue` | 雷达图包装组件，当前主报告未挂载它 |
| `components/DemoDataPanel.vue` | 备用演示对话框，当前主页面未挂载；已修复导入与旧说明 |
| `utils/responsive.js`、`assets/styles/responsive.css` | 断点与共享手机样式 |
| `utils/export.js` | CSV 单元格转义、公式防护和剪贴板兼容处理 |
| `public/documents/user-guide.pdf` | 原样保存的用户操作指引，构建时复制到 dist |
| `tests/export.test.mjs` | CSV 正常数据和公式注入回归测试 |

## 后端

下表路径相对于 `backend/`。

| 文件/目录 | 职责 |
|---|---|
| `main.py` | 唯一活动 HTTP 入口 `main:app`，生命周期、权限依赖、接口与错误处理 |
| `app/models/models.py` | 唯一运行表模型：User、Evaluation、LoginSession、WeightSetting |
| `app/schemas/schemas.py` | 用户、资料、金额、评估创建与部分更新的输入限制 |
| `app/crud/crud.py` | 评估归属查询、Decimal 求和、重复项和存储长度检查 |
| `app/core/database.py` | 引擎与会话；默认 MySQL，测试可用 SQLite |
| `app/core/config.py` | 固定从 backend/.env 读取配置，安全构造含特殊字符密码的连接地址 |
| `app/core/security.py` | PBKDF2 密码处理与会话令牌摘要 |
| `app/core/indicator_labels.py` | 历史英文成本字段到中文展示名称的映射 |
| `init_db.py` | 使用同一模型初始化表；不删除、不重建旧表 |
| `create_admin.py` | 隐藏密码输入的初始管理员创建工具 |
| `query_examples.py` | 与现有表结构一致的只读查询示例 |
| `app/api/api.py` | 旧原型路由已退役，只保留说明，禁止重新挂载无归属校验的原型接口 |
| `tests/test_api.py` | 临时 SQLite + 独立 HTTP 进程的回归测试 |

## 数据归属和状态

- `users.username` 是当前业务所有者标识；本轮没有引入新的角色表或改变为 user_id 关联。
- `evaluations.username` 记录归属。普通用户不能读取/修改他人的记录；管理员可管理全量记录。
- `login_sessions` 只保存令牌摘要、用户名和到期时间；退出、改密码、删除账号使会话失效。
- `weight_settings` 保存 1–9 类参考权重；默认值为 1，数据库保存后可跨重启读取。
- 草稿不是服务端评估记录，保存在当前浏览器的 `evaluationDraft:<用户名>`；服务器“草稿状态”不是这个本机草稿箱。
- 评估提交时就持久化，不依赖是否导出报告。新提交默认完成状态。

## 关键路径

1. 注册 → 密码哈希保存 → 登录 → 会话入库 → 前端携带令牌。
2. 新建 → 36 个字段转换为指标列表 → Decimal 求和 → 记录入库 → 按 ID 读取报告。
3. 编辑 → 根据 `?edit=ID` 加载原值 → PUT 同一记录 → 返回原报告；不会再生成一条新记录。
4. 复制 → 校验原记录访问权 → 创建属于当前操作者的副本 → 路由参数变化后重新加载报告。
5. 草稿 → 按账号保存 → 继续编辑时恢复；历史未知字段保留，避免编辑时静默丢项。
6. 报告 → 真实 API 数据 → 中文成本名称与类别明细 → 打印完整表格/导出 CSV/复制受权限保护的链接。

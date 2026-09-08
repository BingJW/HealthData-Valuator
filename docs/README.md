# 项目文档目录

## 按用途阅读

| 分类 | 文档 | 内容 |
|---|---|---|
| 使用 | [用户操作指引](usage/user-guide.md) | 首页阅读、下载、PDF 与当前功能说明 |
| 开发 | [本地开发与数据库](development/local-setup.md) | 环境安装、启动、数据库、管理员、验证命令 |
| 开发 | [项目架构与业务流程](development/architecture.md) | 文件职责、数据归属、关键业务链路 |
| 开发 | [接口与权限](development/api.md) | 接口清单、字段约束、认证和访问范围 |
| 开发 | [Git 与团队协作](development/git-workflow.md) | 同步、提交、审查及冲突处理 |
| 更新 | [2026年9月8日更新说明](releases/2026-09-08.md) | 手机适配、代码修复、用户指引、验证和回退 |

## 部署

- [阿里云宝塔服务器更新方式](deployment/server-update.md)
- [2026年9月8日实际发布记录](deployment/release-2026-09-08.md)

## 原文档迁移对照

| 原位置 | 现位置 / 合并方式 |
|---|---|
| `MOBILE_ADAPTATION.md` | 合并至更新说明第 11 节 |
| `PROJECT_REVIEW_AND_CHANGES.md` | 合并至 2026年9月8日更新说明，保留详细修复与验证记录 |
| `PROJECT_STRUCTURE.md` | `docs/development/architecture.md` |
| `API.md` | `docs/development/api.md` |
| `GITHUB_GUIDE.md` | `docs/development/git-workflow.md`，更新协作步骤 |
| `backend/QUICK_START.md` | 合并至 `docs/development/local-setup.md` |
| `backend/DATABASE_SETUP.md` | 合并至 `docs/development/local-setup.md` |
| 根目录 `README.md` | 保留为项目入口，启动细节移至本地开发指南 |
| `frontend/public/documents/user-guide.pdf` | 原位置保留，使用文档链接到同一文件 |

## 文档维护约定

- 根目录 README 只保留项目简介和常用入口；详细内容按用途存放。
- 文件名采用小写英文和连字符，标题使用中文；更新说明采用 `YYYY-MM-DD.md`。
- 使用与开发指南描述当前行为，日期更新说明保留当时修改和验证范围。
- 同一主题只维护一份详细文档，通过相对链接引用；不要复制 PDF 或维护重复启动步骤。
- 修改功能时同步对应指南；验证结果注明实际执行范围，历史结果不当作新一次检查结论。

[返回项目首页](../README.md)

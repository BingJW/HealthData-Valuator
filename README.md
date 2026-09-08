# HealthData-Valuator

医疗数据资产价值计量器，使用 Vue 3、Element Plus、FastAPI 和 SQLAlchemy。当前报告按 9 大类成本直接相加；管理员参考权重独立保存，暂不参与报告金额计算。

## 文档入口

- [全部文档与分类目录](docs/README.md)
- [本地安装、启动、数据库配置与验证](docs/development/local-setup.md)
- [用户操作指引与 PDF 下载](docs/usage/user-guide.md)
- [项目架构与业务流程](docs/development/architecture.md)
- [接口与权限说明](docs/development/api.md)
- [Git 与团队协作](docs/development/git-workflow.md)
- [2026年9月8日更新说明](docs/releases/2026-09-08.md)：手机适配、代码修复、操作指引接入及兼容事项。

## 已配置环境启动

在项目根目录运行：

```powershell
npm run dev
```

首次使用请先完成[本地开发指南](docs/development/local-setup.md)中的环境和数据库配置。

- 网站：http://127.0.0.1:3000/
- API 文档：http://127.0.0.1:8000/docs
- 操作指引：http://127.0.0.1:3000/documents/user-guide.pdf

2026年9月8日更新在本地完成，尚未推送或部署到服务器。后续发布前请阅读更新说明中的数据库兼容、密码升级和备份回退事项。

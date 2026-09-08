# Git 与团队协作

## 获取项目

```powershell
git clone https://github.com/BingJW/HealthData-Valuator.git
cd HealthData-Valuator
```

环境安装见[本地开发指南](local-setup.md)。

## 日常修改

先用 `git status` 检查本地状态。有未提交修改时先确认内容并妥善保存，不直接覆盖。工作区干净时可用 `git pull --ff-only origin main` 同步；出现分叉时先分析差异再处理。

每个独立功能使用独立分支，例如 `git switch -c codex/update-docs`。修改后检查差异，运行与改动相关的验证。仅暂存本次需要的文件，避免无差别加入环境文件、密码、数据库备份或生成目录。

```powershell
git diff
git add docs/README.md
git diff --cached
git commit -m "docs: 整理项目文档目录"
```

以上路径仅为示例，请替换为实际文件。确认需要发布远程分支后再推送，并按团队流程审查合并；本地修改不会自动更新 GitHub 或服务器。

## 提交命名与冲突

| 前缀 | 用途 |
|---|---|
| feat | 新功能 |
| fix | 问题修复 |
| docs | 文档 |
| style | 不影响逻辑的格式调整 |
| refactor | 代码重构 |
| test | 测试 |

遇到冲突时先读取双方修改，逐项解决并重新验证，不强制推送覆盖他人的提交。后端使用项目 `.venv`；接口以[接口与权限说明](api.md)及运行服务的 `/docs` 为准。

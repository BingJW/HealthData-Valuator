# 用户操作指引

在网站首页“用户操作指引”模块，点击“在线阅读”在新窗口查看，或点击“下载指引”保存 PDF。个人中心“使用帮助”也可打开该文件，无需额外下载软件即可使用支持 PDF 的浏览器阅读。

- [打开操作指引 PDF](../../frontend/public/documents/user-guide.pdf)
- 网站发布路径：`/documents/user-guide.pdf`
- 下载文件名：`医疗数据资产价值计量器_操作指引.pdf`

PDF 保留用户提供的原文件内容，共 5 页。页面不再显示页数或“新窗口”提示文字。

## 与当前功能对应

报告的 PDF 导出通过浏览器打印窗口“另存为 PDF”完成；复制报告链接仍要求原账号或管理员登录。评估提交时即保存到数据库，导出不是保存的前提。本机草稿仅保存在当前浏览器，不跨设备同步。

## 维护

PDF 仅保留一份源文件在 `frontend/public/documents/user-guide.pdf`，构建自动复制到 `frontend/dist/documents/user-guide.pdf`。更新文件时保持该路径可避免破坏首页链接；发布构建产物时应包含 documents 目录。接入细节见[2026年9月8日更新说明](../releases/2026-09-08.md)。

# 服务器更新方式（阿里云 + 宝塔）

本项目使用 GitHub 管理源代码，在本地构建前端，通过 SSH 更新服务器。本次更新执行结果另见同目录发布记录。以下步骤按顺序执行；任何检查失败应停止，不直接跳到重启。

## 1. 已核对的部署信息

| 项目 | 实际配置 |
|---|---|
| 服务器 | Ubuntu 22.04，47.93.192.190 |
| SSH | admin，22 端口，专用密钥，具备 sudo 权限 |
| 项目 | /www/wwwroot/HealthData-Valuator |
| GitHub | BingJW/HealthData-Valuator，main 分支 |
| 网站目录 | /www/wwwroot/HealthData-Valuator/frontend/dist |
| 网站配置 | /www/server/panel/vhost/nginx/47.93.192.190.conf |
| 后端管理 | 宝塔生成的 /etc/init.d/Valuator_pymanager |
| 后端 Python | backend/1b18d84016ab807531b98de7e2f8cb15_venv/bin/python3，3.11.4 |
| 启动方式 | 使用上述解释器执行 backend/main.py |
| 数据库 | MySQL，healthdata_valuator；连接配置保留服务器 backend/.env |

不要把本机 .env、虚拟环境、数据库备份或 SSH 私钥提交 GitHub。服务器备份放在网站目录之外，只有管理员可读取。

## 2. 本地检查与发布 GitHub

在项目根目录执行：

```powershell
.\.venv\Scripts\python.exe -B -m unittest discover -s backend/tests -v
npm run lint --prefix frontend
node --test frontend/tests/export.test.mjs
npm run build --prefix frontend
git diff --check
git status --short
git fetch origin
```

逐项检查变更文件，提交本次更新及文档，再推送 main；有远程新提交时先整合，不强推。记录完整提交 ID，后面所有构建与服务器更新以这个 ID 为准。dist 是构建产物，不放入 Git；将 frontend/dist 打包并记录 SHA256，上传后再校验。

## 3. 更新前检查与备份

检查服务器工作区干净、当前提交、Python 版本、磁盘空间、服务启动方式、Nginx 规则及数据库结构。数据库只输出结构和数量，不输出个人资料或密码。

更新窗口内先暂停网站业务请求并优雅停止后端，确保备份后没有新记录写入。用服务器数据库凭据在服务器本地运行 mysqldump；凭据通过权限为 600 的临时配置文件传递，不放在命令行或聊天中。备份成功后检查退出码、文件大小与摘要。

备份至少包含：数据库 SQL、旧 Git 提交 ID、旧 frontend/dist、backend/.env、宝塔 Nginx 配置、后端服务脚本。备份期间若数据库导出失败，不继续更新。不要把本地数据库导入服务器。

## 4. 获取同一版本

优先在服务器获取 GitHub：

```bash
cd /www/wwwroot/HealthData-Valuator
sudo git fetch origin
sudo git merge --ff-only origin/main
sudo git rev-parse HEAD
```

实际执行前确认 origin/main 就是本次已审核发布提交。如服务器无法连接 GitHub，可在本机从已经推送并核对的提交生成 Git bundle，经 SSH 上传后在服务器 fetch bundle，再快进到同一提交。bundle 只传输版本历史，不包含服务器环境或数据库；这只是网络传输替代，GitHub 仍是版本来源。禁止 git reset --hard 覆盖服务器未保存修改。

上传本地构建包到临时目录，核对 SHA256 后解包到新目录；检查 index.html、assets 和 documents/user-guide.pdf，再切换网站 dist，保留旧目录供回退。

## 5. 后端与数据库兼容

用宝塔当前 Python 解释器检查并安装 backend/requirements.txt，不使用系统 Python 或 Windows .venv。保留原环境，避免覆盖已有服务路径。

本版新增 login_sessions 和 weight_settings 表；启动会创建缺失表，不删除 users 或 evaluations。检查旧表必需字段及额外列约束；有缺失或非空额外列阻碍写入时，先单独制定迁移，不能删表绕过。

密码首次正确登录后升级为哈希，旧会话不迁移，发布后用户需重新登录。参考权重不参与报告金额，原有数据不重算。

## 6. 宝塔 Nginx 配置与切换

本版前端请求相对 /api 地址，必须让 Nginx 转发到本机后端，并为 Vue 页面刷新设置回退：

```nginx
location /api/ {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
location / {
    try_files $uri $uri/ /index.html;
}
```

proxy_pass 后不要追加斜杠，否则会丢失 /api 前缀。规则写入已包含的宝塔扩展目录，先检查是否存在重复 location。保留宝塔原证书、日志和其他规则。新后端只监听 127.0.0.1:8000，通过 80 端口网站访问。

用 /www/server/nginx/sbin/nginx -t 验证配置，通过后 reload。服务仍使用原宝塔启动脚本启动；停机时优先对已确认的后端 PID 发送 TERM，避免原脚本 kill -9 中断写入。避免同时启动两个后端。

## 7. 上线验证

核对服务器 HEAD 与发布提交一致；后端健康检查、/openapi.json 版本、网站首页、/api/indicators、登录页刷新、PDF 下载都应正常。未登录访问个人评估应返回 401，不能暴露数据。比较数据库原表记录数量，核对 PDF SHA256。

自动验证不使用真实账号密码；真实账号登录、手机操作和真实报告由用户复核。若需要创建线上测试数据，明确标记并在验证后清理。上线后刷新网页并重新登录。

## 8. 回退

切换失败时保持维护状态，读取错误日志定位。数据库密码升级后不能只回退旧代码：旧后端不认识哈希密码。应使用匹配的部署前数据库和代码备份，或保留兼容哈希的新后端。恢复数据库前必须确认备份时间及是否有上线后新数据；恢复会覆盖这段期间的写入，不能自动盲目执行。

前端可切回已备份的 dist，Nginx 可恢复对应备份并测试后 reload。后端用保存的版本和原运行环境启动；验证通过后解除维护。不要删除备份直到用户完成验收。

## 9. 本次额外发现

发布前回归暴露 Windows 虚拟环境子进程仍占用测试日志的问题，已改为终止测试进程树；该改动仅影响测试清理。现网初始 /api/indicators 返回 404，需补充反向代理后才能使用新前端。

[返回文档目录](../README.md) · [2026年9月8日功能更新](../releases/2026-09-08.md)

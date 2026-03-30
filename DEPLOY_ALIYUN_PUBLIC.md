# 阿里云公网部署（Nginx + FastAPI）

目标：仅配置云服务器公网 IP，外部用户通过 `http://公网IP` 访问前端页面，同时 `/api` 被 Nginx 反向代理到后端。

假设：
- 前后端已在你的服务器同目录运行：`/opt/HealthData-Valuator`
- 前端生产构建输出目录为默认的 `frontend/dist`
- 后端 API 在 `127.0.0.1:8000` 上运行（不直接对公网开放）

---

## 1. 服务器准备

1. 安装依赖（Ubuntu 示例）：
   - `sudo apt update`
   - `sudo apt install -y nginx python3 python3-venv python3-pip`
2. 创建部署目录：
   - `sudo mkdir -p /opt/HealthData-Valuator`
3. 上传/同步代码到服务器的 `/opt/HealthData-Valuator`

---

## 2. 配置后端（FastAPI）

1. 创建虚拟环境并安装依赖：
   - `cd /opt/HealthData-Valuator/backend`
   - `python3 -m venv venv`
   - `source venv/bin/activate`
   - `pip install -r requirements.txt`
2. 生成并编辑数据库配置：
   - `cp .env.example .env`（首次运行）
   - 编辑 `.env` 中 `DB_PASSWORD` 等
3. 启动后端（systemd）：
   - 将仓库里的 `deploy_backend_systemd.service` 复制为系统服务文件：
     - `sudo cp deploy_backend_systemd.service /etc/systemd/system/healthdata-backend.service`
   - 按需要修改 `ExecStart` / 路径（模板内已用 `/opt/HealthData-Valuator` 举例）
   - 执行：
     - `sudo systemctl daemon-reload`
     - `sudo systemctl enable --now healthdata-backend`
4. 检查：
   - `sudo systemctl status healthdata-backend --no-pager`

---

## 3. 构建前端并交给 Nginx

1. 构建前端：
   - `cd /opt/HealthData-Valuator/frontend`
   - `npm ci`
   - `npm run build`
2. 准备 Nginx 的站点目录（模板中默认为 `/var/www/healthdata`）：
   - `sudo mkdir -p /var/www/healthdata`
   - `sudo cp -r dist/* /var/www/healthdata/`

---

## 4. 配置 Nginx 反代

1. 将仓库里的 `deploy_nginx_public.conf` 复制到 Nginx：
   - `sudo cp deploy_nginx_public.conf /etc/nginx/conf.d/healthdata.conf`
2. 校验并重载：
   - `sudo nginx -t`
   - `sudo systemctl reload nginx`

---

## 5. 安全组/防火墙建议

- 云安全组只需要放行：
  - `22`（SSH，做运维）
  - `80`（对外访问）
- 不建议对公网直接开放 `8000`（由 Nginx 代理即可）

---

## 6. 访问方式

- 访问：`http://你的公网IP`
- 如果前端需要登录：
  - 先用后端的 `POST /api/demo/init` 初始化演示数据（页面里如果有入口也可点）
  - 默认演示管理员账号：`admin / admin123`


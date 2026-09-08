# API 与权限说明

活动入口为 `backend/main.py` 的 `main:app`。完整字段定义可在本地 `/docs` 或 `/openapi.json` 查看。本文件替代原型版 API 说明。

## 通用约定

- 成功：HTTP 200，JSON 含 `code: 0`，数据在 `data`，操作提示在 `message`。
- 失败：HTTP 400/401/403/404/409/422/503，JSON 含 `detail`。422 可能是字段错误列表。
- 登录后：请求头 `Authorization: Bearer <token>`。令牌默认 12 小时过期；服务端存摘要和到期时间。
- 普通用户只能操作自己的评估。管理员可访问全部评估；“我的评估”默认仍只显示当前账号。
- 列表 `page >= 1`，`1 <= pageSize <= 100`。关键字按字面值筛选。

## 路由清单

| 方法 | 路径 | 权限/作用 |
|---|---|---|
| GET | `/` | 数据库健康检查，无业务数据 |
| POST | `/api/auth/register` | 公开注册普通账号；保留 admin，密码至少6位 |
| POST | `/api/auth/login` | 校验账号、创建会话；旧明文密码成功登录后升级 |
| POST | `/api/auth/logout` | 注销所带会话；无会话时也返回成功 |
| GET/PUT | `/api/user/info` | 当前用户读取/更新医院、手机、邮箱 |
| GET | `/api/indicators` | 公开读取9类成本目录 |
| POST | `/api/evaluations` | 登录用户创建属于自己的评估 |
| GET | `/api/evaluations` | 默认 `scope=mine`；`scope=all` 仅管理员 |
| GET | `/api/evaluations/stats` | 当前用户统计，未登录不可读 |
| GET/PUT/DELETE | `/api/evaluations/{id}` | 所有者或管理员读取、部分更新、删除 |
| GET | `/api/evaluations/{id}/result` | 所有者或管理员读取真实报告 |
| POST | `/api/evaluations/{id}/submit` | 所有者或管理员标记完成 |
| POST | `/api/evaluations/{id}/duplicate` | 所有者或管理员复制；副本归当前操作者 |
| GET/POST | `/api/admin/users` | 管理员列表/新增用户 |
| GET/PUT/DELETE | `/api/admin/users/{id}` | 管理员读取/更新/删除；禁止删除 admin 或仍有评估的用户 |
| GET | `/api/admin/stats` | 管理员全局统计 |
| GET/PUT | `/api/admin/weights` | 管理员读取/保存参考权重；不改报告算法 |
| POST | `/api/demo/init` | 管理员且 `ENABLE_DEMO=true` 才能创建幂等示例；不创建默认密码账号 |

## 新建与编辑示例

```json
{
  "name": "2026年度成本评估",
  "description": "示例",
  "indicators": [
    { "category": 1, "item_name": "strategicPlanning", "amount": 120.25 },
    { "category": 2, "item_name": "dataPurchase", "amount": 79.75 }
  ]
}
```

POST 返回 `data.id` 和 `data.total_value`，上述总值为200。PUT同一记录可只传要改的 `name`、`description`、`indicators`。

- 名称去首尾空格，不可为空，最多200字；说明最多500字。
- 类别1至9；单项金额非负、有限数，最多两位小数，单项上限1万亿元。
- 指标列表1至100项；同类别同名子项不能重复；至少一项为正数。
- 序列化后不能超过当前5000字符字段容量；超限返回422，不截断数据。
- 服务端用Decimal求和，最终兼容已有Float总额字段。没有擅自修改现有数据库金额类型。
- `item_name`保留稳定字段键用于编辑，报告通过映射显示中文标签；未知历史字段原样保留。

## 报告与导出

报告包含稳定的 `REPORT-{id}`、所属医院、分类汇总、分类下的明细、全量明细与百分比。

CSV和浏览器打印/PDF在前端完成，没有虚构的服务器导出接口。本机草稿使用浏览器存储，没有服务器草稿接口。复制报告链接不改变访问权限，不等于匿名公开分享。

## 配置与兼容

默认MySQL，从backend/.env读取。新会话、参考权重使用新增的 `login_sessions`、`weight_settings` 表。旧 `users` 和 `evaluations` 表不自动重建。旧原型 `user_id/evaluation_name/indicator_data` 模型不再是活动模型，不能与本接口混用。

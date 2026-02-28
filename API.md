# 🩺 HealthData-Valuator API 接口规范 (V1.0)

本项目采用 **RESTful API** 设计风格，前后端通过 **JSON** 进行数据交换。

## 1. 基础信息

* **Base URL**: `http://localhost:8000/api/v1`
* **内容类型**: `Content-Type: application/json`
* **字符编码**: `UTF-8`
* **认证方式**: `Bearer Token (JWT)`。除登录/注册外，所有请求需在 Header 中携带 `Authorization: Bearer <token>`。

---

## 2. 统一响应格式

所有接口必须返回统一的 JSON 结构，方便前端拦截器处理：

```json
{
  "code": 200,          // 业务状态码：200-成功, 401-未授权, 403-无权限, 500-服务器错误
  "message": "success",  // 提示信息
  "data": null          // 核心业务数据
}

```

---

## 3. 核心接口清单

### 🔑 认证模块 (Auth)

| 接口名称 | 方法 | 路径 | 说明 |
| --- | --- | --- | --- |
| 用户注册 | `POST` | `/auth/register` | 医院用户自助注册，默认角色为 `hospital` |
| 用户登录 | `POST` | `/auth/login` | 返回 JWT Token 及用户信息 |

### 📊 评估模块 (Evaluation)

| 接口名称 | 方法 | 路径 | 说明 |
| --- | --- | --- | --- |
| 获取列表 | `GET` | `/evaluations` | 获取当前医院的所有历史测算记录 |
| 提交测算 | `POST` | `/evaluations` | 提交 9 类指标数据，触发 P3 引擎计算并入库 |
| 详情报告 | `GET` | `/evaluations/{id}` | 获取单次测算的明细数据与价值结论 |
| 删除记录 | `DELETE` | `/evaluations/{id}` | 删除评估记录（级联删除指标明细） |

### ⚙️ 管理模块 (Admin)

| 接口名称 | 方法 | 路径 | 说明 |
| --- | --- | --- | --- |
| 全局统计 | `GET` | `/admin/stats` | 管理员获取全量数据的可视化看板数据 |
| 权重配置 | `PUT` | `/admin/weights` | 动态调整 9 大类指标的测算权重系数 |

---

## 4. 关键数据结构示例

### 9 类指标提交格式 (JSON)

当调用 `POST /evaluations` 时，Payload 结构如下：

```json
{
  "evaluation_name": "2026年度上半年资产评估",
  "indicators": [
    {
      "category": 1, 
      "item_name": "战略规划成本",
      "amount": 50000.00
    },
    {
      "category": 7,
      "item_name": "安全防护成本",
      "amount": 120000.00
    }
    // ... 对应老师给出的 9 类指标明细
  ]
}

```

---
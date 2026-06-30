# 个人记账本 (Personal Ledger)

> 基于 **FastAPI + Vue3 + SQLite** 的轻量级 Web 记账应用，移动端优先，支持多用户数据隔离。

---

## 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| 前端 | Vue 3 + Vite + TypeScript | SPA 单页应用 |
| 状态管理 | Pinia | Vue3 官方推荐 |
| 路由 | Vue Router 4 | 页面导航 |
| 图表 | ECharts + vue-echarts | 分类支出饼图 |
| HTTP | Axios | API 请求封装 |
| 后端 | FastAPI (Python) | 异步 Web 框架 |
| ORM | SQLAlchemy 2.0 | 数据库模型 |
| 数据库 | SQLite | 单文件部署 |
| 认证 | PyJWT + passlib[bcrypt] | JWT Token + 密码哈希 |

---

## 功能特性

### 注册与登录
- 邮箱验证码注册（开发环境验证码固定为 `123456`）
- 密码登录 / 验证码登录
- 未注册邮箱 + 验证码自动创建账号
- JWT Token 认证（有效期 7 天）
- 退出登录 / 注销账户（物理删除所有数据）

### 收支记录
- 新增账单（金额 + 分类 + 备注 + 日期）
- 账单列表（按月份倒序，支持收入/支出筛选）
- 编辑账单（点击账单行进入编辑）
- 删除账单（点击删除按钮 + 确认）

### 分类管理
- 新用户注册自动获得 6 个预设分类：餐饮、交通、购物、娱乐、住房、收入
- 新增/删除自定义分类
- 收入/支出分类独立管理
- 分类数据严格按用户隔离

### 月度报表
- 月度收支概览（收入合计、支出合计、结余）
- 分类支出占比环形图（ECharts）
- 月份切换（左右箭头，不可超过当前月份）

---

## 本地开发

### 环境要求
- Python 3.11+
- Node.js 18+

### 启动后端

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

后端运行在 http://localhost:8000

### 启动前端

```bash
cd frontend
npm install
npm run dev
```

前端运行在 http://localhost:3000

### 访问应用

浏览器打开 http://localhost:3000

---

## 项目结构

```
├── backend/                  # FastAPI 后端
│   ├── app/
│   │   ├── main.py           # 入口
│   │   ├── models/           # 数据模型
│   │   ├── schemas/          # Pydantic 请求/响应模型
│   │   ├── routers/          # API 路由
│   │   ├── services/         # 业务逻辑
│   │   ├── middleware/       # JWT 认证中间件
│   │   └── utils/            # 密码哈希、JWT、验证码
│   ├── requirements.txt
│   └── seed.py               # 数据库初始化
├── frontend/                 # Vue3 + Vite 前端
│   ├── src/
│   │   ├── views/            # 页面组件
│   │   ├── components/       # 通用组件
│   │   ├── stores/           # Pinia 状态管理
│   │   ├── api/              # Axios 请求封装
│   │   └── router/           # Vue Router
│   ├── package.json
│   └── vite.config.ts
└── start.sh                  # CloudStudio 一键启动脚本
```

---

## CloudStudio 部署

1. 在 CloudStudio 中从 Git 仓库导入项目
2. 在终端执行：

```bash
sh start.sh
```

3. CloudStudio 会自动生成外部访问链接（端口 3000）

---

## API 文档

后端自动生成 OpenAPI 文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 主要接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/auth/send-code | 发送验证码 |
| POST | /api/auth/register | 注册 |
| POST | /api/auth/login/password | 密码登录 |
| POST | /api/auth/login/code | 验证码登录 |
| GET | /api/categories | 获取分类列表 |
| POST | /api/categories | 创建分类 |
| GET | /api/bills | 获取账单列表 |
| POST | /api/bills | 创建账单 |
| GET | /api/reports/monthly-summary | 月度概览 |
| GET | /api/reports/category-breakdown | 分类占比 |

---

## 开发说明

- **验证码**：开发环境固定为 `123456`，有效期 5 分钟
- **密码**：bcrypt 哈希存储，前端最小 6 位
- **数据隔离**：所有数据查询均携带 `user_id` 过滤
- **响应格式**：统一 `{ code, message, data }`

---

## 作者

June-Yan

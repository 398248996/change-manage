<!-- markdownlint-disable MD033 MD041 -->

<p align="center">
  <a href="https://github.com/398248996/change-manage/"><img src="web/public/favicon.svg" width="180" height="180" alt="变更管理系统"></a>
</p>

<div align="center">

# 变更管理系统

[![license](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)
![python](https://img.shields.io/badge/python-3.12+-blue?logo=python&logoColor=edb641)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?logo=fastapi&logoColor=edb641)
![Pydantic](https://img.shields.io/badge/Pydantic_v2-e92063?logo=pydantic&logoColor=edb641)
![uv](https://img.shields.io/badge/uv-managed-blueviolet)
[![basedpyright](https://img.shields.io/badge/types-basedpyright-797952.svg?logo=python&logoColor=edb641)](https://github.com/DetachHead/basedpyright)
[![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

**化工企业变更管理系统 - FastAPI + Vue3 全栈应用**

</div>

## 简介

化工企业变更管理系统，用于管理化工企业的变更需求、变更申请、风险评估、审批、实施投用、验收和关闭等全流程管理。

- **后端** — FastAPI · Pydantic v2 · Tortoise ORM · Redis
- **前端** — Vue3 · Vite8 · TypeScript · Naive UI · UnoCSS · Pinia · Alova · Elegant Router
- **基础设施** — Docker Compose（Nginx + FastAPI + Redis）、多 worker 启动锁、fastapi-guard 限流、内置 Radar 监控面板
- **代码生成器** — `cli-init` 起骨架，编辑 `models.py`，`cli-crud` 一键产出前后端 CRUD

## 特性

- **变更管理** — 变更需求、变更申请、风险评估、审批、实施投用、验收、关闭全流程
- **一键 CRUD** — Tortoise 模型生成前后端 CRUD、类型与 i18n
- **可覆写路由工厂** — `CRUDRouter` 生成标准接口，`@crud.override` 按需定制
- **模块化业务** — `app/business/<name>/` 自动发现，跨模块走事件总线
- **多数据库支持** — PostgreSQL / SQLite / MySQL / SQL Server / Oracle
- **RBAC 权限体系** — 菜单 / API / 按钮 + 行级 `data_scope`
- **IaC 初始化对账** — 菜单、角色、API 启动时可声明式同步
- **统一接口契约** — `{code, msg, data}`、camelCase、Sqid 对外 ID
- **全栈类型检查** — basedpyright + vue-tsc + 静态 i18n 校验
- **内置运维能力** — Radar 监控、Redis 缓存降级、限流与 IP 封禁
- **Docker 部署** — Nginx + FastAPI + Redis 开箱即用

## 快速开始

### 环境要求

| 工具             | 版本     |
| ---------------- | -------- |
| Python           | >= 3.12  |
| Node.js          | >= 20.19 |
| uv · pnpm · just | 最新     |

### Docker 部署（推荐）

```bash
git clone https://github.com/398248996/change-manage.git
cd change-manage
just docker-db-init  # 首次先启动依赖服务并初始化数据库
just up              # 启动完整栈并写入默认/业务种子数据
```

访问 `http://localhost:1880`。

### 本地开发

```bash
git clone https://github.com/398248996/change-manage.git
cd change-manage
just install          # 后端 uv sync + 前端 pnpm install
cp .env.example .env  # 复制环境变量模板，按需修改 SECRET_KEY / DB_URL / REDIS_URL 等
just db-init          # 首次建表 + 基础数据
just run              # 并行启动后端(:9999) + 前端(:9527)，Ctrl+C 一起停
```

## 常用命令

全部命令封装在 `justfile`，运行 `just --list` 查看完整列表。

| 命令                                         | 作用                                      |
| -------------------------------------------- | ----------------------------------------- |
| `just install`                               | 安装后端 + 前端依赖                       |
| `just run`                                   | 同时启动后端 + 前端开发服务器             |
| `just run backend` / `just run frontend`     | 仅启动后端 / 前端                         |
| `just check`                                 | 跑完后端 + 前端所有质量检查（提交前必跑） |
| `just check backend` / `just check frontend` | 仅检查后端 / 前端                         |
| `just mm`                                    | `makemigrations` + `migrate`              |
| `just cli-init xxx`                          | 创建业务模块骨架                          |
| `just cli-gen xxx`                           | 选择模型与模糊/精确查询字段，生成后端代码 |
| `just cli-gen-web xxx 中文名`                | 选择模型与列表/搜索字段，生成前端代码     |
| `just cli-gen-all xxx 中文名`                | 一次选择并生成前后端代码                  |
| `just cli-crud xxx 中文名`                   | 同上，完整 CRUD 生成别名                  |
| `just up` / `just down` / `just logs`        | Docker 启停与日志                         |

## 新增业务模块

以 `change`（变更管理）为例：

```bash
just cli-init change                   # 1. 创建模块骨架
$EDITOR app/business/change/models.py  # 2. 定义 Tortoise 模型
just cli-crud change 变更管理          # 3. 生成前后端 CRUD（i18n 自动并入）
just mm                                   # 4. 迁移
just run                                  # 5. 启动验证
just check                                # 6. 提交前检查
```

## 架构

```
app/
├── core/           # 框架基础设施（CRUDBase / CRUDRouter / Schema / 鉴权 / 缓存 / 事件 / Sqids）
├── system/         # 系统模块（auth / user / role / menu / api / dictionary / radar）
├── business/       # 业务模块（autodiscover 自动加载）
├── cli/            # 代码生成器
└── utils/          # 业务模块对外统一 import 入口
web/src/
├── views/          # 页面（Elegant Router 源）
├── service/api/    # Alova HTTP 封装
├── typings/api/    # TS 类型
├── store/modules/  # Pinia
├── router/         # Elegant Router + 守卫
└── locales/        # vue-i18n
```

分层：`api/` → `services/` → `controllers/` → `models + schemas`。业务模块**禁止**反向 import `app.system.*`（少数显式暴露的 service 除外），**禁止**互相 import；跨模块走事件总线。

## 响应码

所有接口返回 `{"code": "xxxx", "msg": "...", "data": ...}`，HTTP 状态恒 200。

| 段          | 含义                               | 前端典型行为           |
| ----------- | ---------------------------------- | ---------------------- |
| `0000`      | 成功                               | 正常处理               |
| `1xxx`      | 系统内部错误 / 序列化失败          | 框架自动弹错           |
| `21xx`      | 认证失败（token / session）        | 登出 / 弹窗 / 自动刷新 |
| `22xx`      | 授权失败（RBAC / 按钮 / 角色）     | 显示错误消息           |
| `23xx`      | 资源冲突（唯一键）                 | 显示错误消息           |
| `24xx`      | 通用业务失败                       | 显示错误消息           |
| `25xx`      | 限流 / 安全策略                    | 显示错误消息           |
| `26xx`      | Schema 必填兜底                    | 显示错误消息           |
| `4000–9999` | 用户自定义（业务模块从 `4000` 起） | 业务自行处理           |

## 开源协议

[MIT © 2026](./LICENSE)
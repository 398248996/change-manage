<!-- markdownlint-disable MD033 MD041 -->

<p align="center">
  <a href="https://github.com/398248996/change-manage/"><img src="web/public/favicon.svg" width="180" height="180" alt="Change Management System"></a>
</p>

<div align="center">

# Change Management System

[![license](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)
![python](https://img.shields.io/badge/python-3.12+-blue?logo=python&logoColor=edb641)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?logo=fastapi&logoColor=edb641)
![Pydantic](https://img.shields.io/badge/Pydantic_v2-e92063?logo=pydantic&logoColor=edb641)
![uv](https://img.shields.io/badge/uv-managed-blueviolet)
[![basedpyright](https://img.shields.io/badge/types-basedpyright-797952.svg?logo=python&logoColor=edb641)](https://github.com/DetachHead/basedpyright)
[![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

<span>English | <a href="./README.md">中文</a></span>

**Chemical Enterprise Change Management System - FastAPI + Vue3 Full-stack Application**

</div>

## Overview

Chemical enterprise change management system, used to manage the full process of change requests, change applications, risk assessment, approval, implementation, acceptance and closure in chemical enterprises.

- **Backend** — FastAPI · Pydantic v2 · Tortoise ORM · Redis
- **Frontend** — Vue3 · Vite8 · TypeScript · Naive UI · UnoCSS · Pinia · Alova · Elegant Router
- **Infra** — Docker Compose (Nginx + FastAPI + Redis), multi-worker startup lock, fastapi-guard, built-in Radar dashboard
- **Code generator** — `cli-init` to scaffold, write `models.py`, `cli-crud` to emit backend + frontend CRUD

## Highlights

- **Change Management** — Full process of change requests, change applications, risk assessment, approval, implementation, acceptance and closure
- **One-command CRUD** — Tortoise models generate backend, frontend, types, and i18n
- **Overridable route factory** — `CRUDRouter` for standard APIs, `@crud.override` for custom behavior
- **Modular business apps** — `app/business/<name>/` autodiscovery with event-bus integration
- **Multi-database support** — PostgreSQL / SQLite / MySQL / SQL Server / Oracle
- **RBAC permissions** — menu / API / button checks plus row-level `data_scope`
- **IaC-style bootstrap** — menus, roles, and APIs can be reconciled on startup
- **Unified API contract** — `{code, msg, data}`, camelCase, and Sqid public IDs
- **Full-stack type checks** — basedpyright + vue-tsc + static i18n validation
- **Ops built in** — Radar dashboard, Redis fallback, rate limiting, and IP banning
- **Docker-ready** — Nginx + FastAPI + Redis pre-wired

## Getting Started

### Requirements

| Tool             | Version |
| ---------------- | ------- |
| Python           | >= 3.12 |
| Node.js          | >= 20.19 |
| uv · pnpm · just | latest  |

### Docker (recommended)

```bash
git clone https://github.com/398248996/change-manage.git
cd change-manage
just docker-db-init  # first start dependencies and initialize the database
just up              # start the full stack and write default/business seeds
```

Open `http://localhost:1880`.

### Local development

```bash
git clone https://github.com/398248996/change-manage.git
cd change-manage
just install          # uv sync + pnpm install
cp .env.example .env  # copy env template; update SECRET_KEY / DB_URL / REDIS_URL as needed
just db-init          # first-time: create tables + seed
just run              # backend (:9999) + frontend (:9527) in parallel, Ctrl+C stops both
```

## Common Commands

All commands are wrapped in `justfile`. Run `just --list` for the full list.

| Command                                | Purpose                                               |
| -------------------------------------- | ----------------------------------------------------- |
| `just install`                         | Install backend + frontend dependencies               |
| `just run`                             | Run backend + frontend dev servers together           |
| `just run backend` / `just run frontend` | Run backend / frontend only                         |
| `just check`                           | Run all backend + frontend quality gates (pre-commit) |
| `just check backend` / `just check frontend` | Check backend / frontend only                  |
| `just mm`                              | `makemigrations` + `migrate`                          |
| `just cli-init xxx`                | Scaffold a new business module                        |
| `just cli-gen xxx`                 | Choose models and fuzzy/exact search fields; generate backend code |
| `just cli-gen-web xxx name`     | Choose models and list/search fields; generate frontend code |
| `just cli-gen-all xxx name`     | Choose and generate both at once                      |
| `just cli-crud xxx name`        | Alias for full CRUD generation                        |
| `just up` / `just down` / `just logs`  | Docker lifecycle                                      |

## Adding a new business module

```bash
just cli-init change                   # 1. scaffold the module
$EDITOR app/business/change/models.py  # 2. define Tortoise models
just cli-crud change ChangeManagement  # 3. generate backend + frontend CRUD (i18n auto-merged)
just mm                                   # 4. run migrations
just run                                  # 5. verify
just check                                # 6. pre-commit
```

## Architecture

```
app/
├── core/           # Framework infra (CRUDBase / CRUDRouter / Schema / auth / cache / events / Sqids)
├── system/         # System modules (auth / user / role / menu / api / dictionary / radar)
├── business/       # Business modules (autodiscovered)
├── cli/            # Code generator
└── utils/          # Unified re-export surface for business modules
web/src/
├── views/          # Pages (Elegant Router source)
├── service/api/    # Alova HTTP wrappers
├── typings/api/    # TS types
├── store/modules/  # Pinia
├── router/         # Elegant Router + guards
└── locales/        # vue-i18n
```

Layers: `api/` → `services/` → `controllers/` → `models + schemas`. Business modules **must not** reverse-import `app.system.*` (except a few explicitly exposed services) and **must not** import sibling modules — cross-module talk uses the event bus.

## Response Codes

All endpoints return `{"code": "xxxx", "msg": "...", "data": ...}` with HTTP status always 200.

| Range       | Meaning                                  | Typical frontend behavior           |
| ----------- | ---------------------------------------- | ----------------------------------- |
| `0000`      | Success                                  | Normal processing                   |
| `1xxx`      | Internal / serialization error           | Auto-toasted by the framework       |
| `21xx`      | Auth failure (token / session)           | Logout / modal / auto token refresh |
| `22xx`      | Authorization failure (RBAC / button)    | Show error toast                    |
| `23xx`      | Resource conflict (unique constraint)    | Show error toast                    |
| `24xx`      | Generic business failure                 | Show error toast                    |
| `25xx`      | Rate-limit / security                    | Show error toast                    |
| `26xx`      | Schema required-field fallback           | Show error toast                    |
| `4000–9999` | User-defined (modules start at `4000`)   | Handled by callers                  |

## License

[MIT © 2026](./LICENSE)
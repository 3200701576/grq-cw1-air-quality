# Air Quality API (CW1)

城市级空气质量数据分析 API 服务，基于 Django + Django REST Framework 构建。

## 项目介绍

本项目是一个用于分析和展示城市空气质量数据的 RESTful API 服务，主要功能包括：

- **空气质量记录管理** - 提供空气质量记录的增删改查（CRUD）接口
- **城市趋势分析** - 支持查询指定城市特定污染物的时间趋势数据
- **数据筛选** - 支持按城市名称、日期范围筛选记录
- **自动文档** - 基于 OpenAPI 3.0 规范提供 Swagger UI 在线文档

### 技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| Python | 3.13+ | 编程语言 |
| Django | 5.x | Web 框架 |
| Django REST Framework | 3.15+ | RESTful API 框架 |
| drf-spectacular | 0.27+ | OpenAPI 3.0 文档生成 |

### 数据说明

数据源文件位于 `data/` 目录：

- **city_day.csv** - 城市每日空气质量数据（已纳入版本控制）
- city_hour.csv、station_day.csv、station_hour.csv、stations.csv 为本地数据集（未纳入版本控制）

---

## 快速开始

### 环境要求

- Python 3.13 或更高版本
- Windows PowerShell / Linux / macOS 终端

### 运行步骤

```bash
# 1. 创建虚拟环境
python -m venv .venv

# 2. 激活虚拟环境（Windows PowerShell）
.\.venv\Scripts\Activate.ps1

# 3. 安装依赖
pip install -r requirements.txt

# 4. 执行数据库迁移
python manage.py migrate

# 5. 导入初始数据（可选）
python manage.py import_data

# 6. 启动开发服务器
python manage.py runserver
```

服务器启动后，访问 http://127.0.0.1:8000/

---

## 部署地址

| 环境 | 地址 | 说明 |
|------|------|------|
| 本地开发 | http://127.0.0.1:8000/ | 默认开发服务器 |
| 生产部署 | 待配置 | 请根据实际服务器地址更新 |

> 如需部署到云服务器，建议使用 Gunicorn + Nginx 或 Docker 容器化部署。

---

## API 文档

### 在线文档

| 文档类型 | 地址 | 说明 |
|----------|------|------|
| Swagger UI | http://127.0.0.1:8000/api/docs/ | 交互式 API 文档 |
| ReDoc | http://127.0.0.1:8000/api/redoc/ | 另一种 API 文档风格 |
| OpenAPI Schema | http://127.0.0.1:8000/api/schema/ | OpenAPI 3.0 JSON/YAML |

### 健康检查

```
GET http://127.0.0.1:8000/api/health/
```

响应示例：

```json
{
  "status": "ok",
  "service": "air-quality-api"
}
```

### 可用端点

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/api/records/` | 获取空气质量记录列表 |
| POST | `/api/records/` | 创建新的空气质量记录 |
| GET | `/api/records/<id>/` | 获取单条记录详情 |
| PUT | `/api/records/<id>/` | 更新记录 |
| DELETE | `/api/records/<id>/` | 删除记录 |
| GET | `/api/analytics/city-trend/` | 获取城市污染物趋势分析 |

### 查询参数

**列表查询** (`GET /api/records/`)

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| city | string | 否 | 城市名称（不区分大小写） |
| start_date | date | 否 | 开始日期（YYYY-MM-DD） |
| end_date | date | 否 | 结束日期（YYYY-MM-DD） |

**趋势分析** (`GET /api/analytics/city-trend/`)

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| city | string | 是 | 城市名称 |
| pollutant | string | 是 | 污染物类型 |

**pollutant 可选值**：`pm25`、`pm10`、`no2`、`co`、`aqi`

---

## 项目结构

```
code/
├── api/                      # API 应用
│   ├── models.py             # 数据模型
│   ├── views.py              # 视图逻辑
│   ├── serializers.py        # 序列化器
│   ├── urls.py               # URL 路由
│   ├── tests.py              # 单元测试
│   └── management/
│       └── commands/
│           ├── import_data.py    # 数据导入命令
│           └── renumber_records.py # 记录重编号命令
├── data/                     # 数据文件目录
│   └── city_day.csv          # 城市每日数据
├── db.sqlite3                # SQLite 数据库
├── manage.py                 # Django 管理脚本
├── requirements.txt          # Python 依赖
└── README.md                 # 项目文档
```

---

## Git 使用规范

### 首次提交到 GitHub

```bash
git init
git add .
git commit -m "chore: initialize django drf project skeleton"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

### 每个 API 功能提交

```bash
git add .
git commit -m "feat(api): add <endpoint-name> endpoint"
git push
```

---

## 常见问题

### 导入数据失败

确保 `data/city_day.csv` 文件存在且格式正确：

```bash
python manage.py import_data
```

### 大文件推送问题

如果首次推送因 CSV 文件过大失败：

```bash
git reset --soft HEAD~1
git restore --staged data/city_hour.csv data/station_day.csv data/station_hour.csv data/stations.csv
git add .
git commit -m "chore: initialize django drf project skeleton"
git push -u origin main --force
```

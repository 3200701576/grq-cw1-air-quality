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

- **city_day.csv** - 城市每日空气质量数据

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

| 环境 | 地址 |
|------|------|
| 本地开发 | http://127.0.0.1:8000/ |
| PythonAnywhere | https://grq.pythonanywhere.com/ |

---

## PythonAnywhere 部署指南

### 1. 准备代码

在本地完成开发后，将代码推送到 GitHub 仓库。

### 2. 在 PythonAnywhere 上克隆代码

打开 PythonAnywhere 的 Bash 终端：

```bash
cd ~
git clone https://github.com/<your-username>/<your-repo>.git grq
cd ~/grq
```

### 3. 创建虚拟环境

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. 配置数据库

```bash
python manage.py migrate
python manage.py import_data
```

### 5. 配置 Web App

1. 进入 **Web** 页面
2. 点击 **Add a new web app**
3. 选择 **Manual configuration**
4. 选择 Python 版本
5. 在 **WSGI configuration file** 中编辑，替换为 Django 的 WSGI 配置：

```python
import os
import sys

path = '/home/grq/grq'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

6. 配置静态文件：

| 设置 | 值 |
|------|------|
| URL | `/static/` |
| Directory | `/home/grq/grq/static/` |

### 6. 重启 Web App

点击 **Reload** 按钮使配置生效。

### 7. 验证部署

访问 https://grq.pythonanywhere.com/api/health/ 确认服务正常运行。

---

## API 文档

### 在线文档

| 文档类型 | 地址 | 说明 |
|----------|------|------|
| Swagger UI | /api/docs/ | 交互式 API 文档 |
| OpenAPI Schema | /api/schema/ | OpenAPI 3.0 JSON/YAML |

### 健康检查

```
GET /api/health/
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


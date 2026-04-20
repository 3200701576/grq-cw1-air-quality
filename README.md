# Air Quality API (CW1)

A RESTful API service for city-level air quality data analysis, built with Django + Django REST Framework.

## Project Overview

This project provides a RESTful API service for analyzing and displaying urban air quality data, featuring:

- **Air Quality Record Management** - CRUD operations for air quality records
- **City Trend Analytics** - Time-series trend analysis for specific pollutants in a given city
- **Data Filtering** - Filter records by city name and date range
- **Auto-generated Documentation** - Swagger UI and OpenAPI 3.0 specification

### Tech Stack

| Technology | Version | Description |
|------------|---------|-------------|
| Python | 3.13+ | Programming Language |
| Django | 5.x | Web Framework |
| Django REST Framework | 3.15+ | RESTful API Framework |
| drf-spectacular | 0.27+ | OpenAPI 3.0 Documentation |

### Data Sources

Data files are located in the `data/` directory:

- **city_day.csv** - City daily air quality data 

---

## Quick Start

### Requirements

- Python 3.13 or higher
- Windows PowerShell / Linux / macOS terminal

### Setup Steps

```bash
# 1. Create virtual environment
python -m venv .venv

# 2. Activate virtual environment (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run database migrations
python manage.py migrate

# 5. Import initial data (optional)
python manage.py import_data

# 6. Start development server
python manage.py runserver
```

After starting, visit http://127.0.0.1:8000/

---

## Deployment

| Environment | URL |
|-------------|-----|
| Local Dev | http://127.0.0.1:8000/ |
| PythonAnywhere | https://grq.pythonanywhere.com/ |

---

## PythonAnywhere Deployment Guide

### 1. Prepare Your Code

Push your completed code to a GitHub repository.

### 2. Clone Code on PythonAnywhere

Open PythonAnywhere Bash terminal:

```bash
cd ~
git clone https://github.com/<your-username>/<your-repo>.git grq
cd ~/grq
```

### 3. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. Configure Database

```bash
python manage.py migrate
python manage.py import_data
```

### 5. Configure Web App

1. Go to the **Web** page
2. Click **Add a new web app**
3. Select **Manual configuration**
4. Choose Python version
5. Edit the **WSGI configuration file**, replace with Django WSGI config:

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

6. Configure static files:

| Setting | Value |
|---------|-------|
| URL | `/static/` |
| Directory | `/home/grq/grq/static/` |

### 6. Reload Web App

Click the **Reload** button to apply changes.

### 7. Verify Deployment

Visit https://grq.pythonanywhere.com/api/health/ to confirm the service is running.

---

## API Documentation

### Online Docs

| Doc Type | URL | Description |
|----------|-----|-------------|
| Swagger UI | /api/docs/ | Interactive API documentation |
| OpenAPI Schema | /api/schema/ | OpenAPI 3.0 JSON/YAML spec |

### Health Check

```
GET /api/health/
```

Response:

```json
{
  "status": "ok",
  "service": "air-quality-api"
}
```

### Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/records/` | List air quality records |
| POST | `/api/records/` | Create a new record |
| GET | `/api/records/<id>/` | Retrieve a single record |
| PUT | `/api/records/<id>/` | Update a record |
| DELETE | `/api/records/<id>/` | Delete a record |
| GET | `/api/analytics/city-trend/` | Get city pollutant trend analysis |

### Query Parameters

**List Records** (`GET /api/records/`)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| city | string | No | City name (case-insensitive) |
| start_date | date | No | Start date (YYYY-MM-DD) |
| end_date | date | No | End date (YYYY-MM-DD) |

**Trend Analytics** (`GET /api/analytics/city-trend/`)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| city | string | Yes | City name |
| pollutant | string | Yes | Pollutant type |

**Valid pollutant values**: `pm25`, `pm10`, `no2`, `co`, `aqi`

---

## Project Structure

```
code/
├── api/                      # API app
│   ├── models.py             # Data models
│   ├── views.py              # View logic
│   ├── serializers.py         # Serializers
│   ├── urls.py               # URL routing
│   ├── tests.py              # Unit tests
│   └── management/
│       └── commands/
│           ├── import_data.py          # Data import command
│           └── renumber_records.py     # Record renumbering command
├── data/                     # Data files directory
│   └── city_day.csv          # City daily data
├── db.sqlite3                # SQLite database
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

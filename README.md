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

- **city_day.csv** - City daily air quality data (tracked in Git)
- city_hour.csv, station_day.csv, station_hour.csv, stations.csv - Local datasets (not tracked)

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

| Environment | URL | Notes |
|-------------|-----|-------|
| Local Dev | http://127.0.0.1:8000/ | Default development server |
| Production | TBD | Update with your server address |

> For cloud deployment, consider using Gunicorn + Nginx or Docker containers.

---

## API Documentation

### Online Docs

| Doc Type | URL | Description |
|----------|-----|-------------|
| Swagger UI | http://127.0.0.1:8000/api/docs/ | Interactive API documentation |
| ReDoc | http://127.0.0.1:8000/api/redoc/ | Alternative API documentation style |
| OpenAPI Schema | http://127.0.0.1:8000/api/schema/ | OpenAPI 3.0 JSON/YAML spec |

### Health Check

```
GET http://127.0.0.1:8000/api/health/
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

---

## Git Workflow

### First Commit to GitHub

```bash
git init
git add .
git commit -m "chore: initialize django drf project skeleton"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

### Per-Feature Commit

```bash
git add .
git commit -m "feat(api): add <endpoint-name> endpoint"
git push
```

---

## FAQ

### Data Import Fails

Ensure `data/city_day.csv` exists and has correct format:

```bash
python manage.py import_data
```

### Large File Push Issues

If first push fails due to large CSV files:

```bash
git reset --soft HEAD~1
git restore --staged data/city_hour.csv data/station_day.csv data/station_hour.csv data/stations.csv
git add .
git commit -m "chore: initialize django drf project skeleton"
git push -u origin main --force
```

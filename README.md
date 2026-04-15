# Air Quality API (CW1)

Coursework API project for city-level air quality analytics using Django and DRF.

## Tech Stack

- Python 3.13+
- Django
- Django REST Framework
- drf-spectacular (OpenAPI + Swagger UI)

## Project Setup

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Useful Endpoints

- Health check: `http://127.0.0.1:8000/api/health/`
- OpenAPI schema: `http://127.0.0.1:8000/api/schema/`
- Swagger docs: `http://127.0.0.1:8000/api/docs/`

## Data Folder

Put source datasets under `data/`:

- tracked in GitHub: `city_day.csv` (recommended first import target)
- local only (not tracked): `city_hour.csv`, `station_day.csv`, `station_hour.csv`, `stations.csv`

This repository intentionally tracks only `city_day.csv` to keep pushes stable on GitHub.

## GitHub First Commit Template

After creating an empty GitHub repository:

```bash
git init
git add .
git commit -m "chore: initialize django drf project skeleton"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

## GitHub Push Fix (if first push failed with large CSV files)

If you accidentally committed large files first, run:

```bash
# uncommit the last commit but keep files in working directory
git reset --soft HEAD~1

# unstage all large dataset files
git restore --staged data/city_hour.csv data/station_day.csv data/station_hour.csv data/stations.csv

# recommit with current .gitignore strategy (only city_day.csv tracked)
git add .
git commit -m "chore: initialize django drf project skeleton"
git push -u origin main --force
```

## Per-API Commit Template

Use one commit per feature unit (endpoint + serializer + route + docs/test update):

```bash
git add .
git commit -m "feat(api): add <endpoint-name> endpoint"
git push
```

## Next Step

Implement `AirQualityRecord` model and CRUD endpoints based on `city_day.csv`.

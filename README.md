# StudentDining

Browse Copenhagen restaurants with student-friendly prices, menus, and reviews — built for University of Copenhagen students.

## Requirements

- Python 3.14
- PostgreSQL

## Setup

```powershell
# 1. Create virtual environment and install dependencies
py -3.14 -m venv .venv
.venv\Scripts\pip.exe install -r requirements.txt

# 2. Create the database and user (run as postgres superuser)
psql -U postgres -c "CREATE USER studentdining WITH PASSWORD 'studentdining';"
psql -U postgres -c "CREATE DATABASE studentdining OWNER studentdining;"

# 3. Configure environment
cp .env.example .env   # then edit .env if your DB credentials differ

# 4. Run migrations
.venv\Scripts\flask.exe --app app db migrate -m "initial schema"
.venv\Scripts\flask.exe --app app db upgrade

# 5. Seed data
.venv\Scripts\python.exe seed.py

# 6. Start the dev server
.venv\Scripts\flask.exe --app app run --debug
```

App runs at http://127.0.0.1:5000

# StudentDining

Browse Copenhagen restaurants with student-friendly prices, menus, and reviews — built for University of Copenhagen students.

## Requirements

- Python
- PostgreSQL

## Setup

```powershell
# 1. Create virtual environment and install dependencies
python -m venv .venv
.venv\Scripts\pip.exe install -r requirements.txt

# 2. Create the database and user
psql -U postgres -c "CREATE USER studentdining WITH PASSWORD 'studentdining';"
psql -U postgres -c "CREATE DATABASE studentdining OWNER studentdining;"

# 3. Configure environment
cp .env.example .env

# 4. Run migrations
.venv\Scripts\flask.exe --app app db upgrade

# 5. Seed data (100 restaurants, 5 demo users, 175 reviews)
.venv\Scripts\python.exe seed.py

# 6. Start the dev server
.venv\Scripts\flask.exe --app app run --debug
```

App runs at http://127.0.0.1:5000

## Demo accounts

| Email | Password |
|---|---|
| alice@alumni.ku.dk | password123 |
| bob@alumni.ku.dk | password123 |
| charlie@alumni.ku.dk | password123 |
| diana@alumni.ku.dk | password123 |
| erik@alumni.ku.dk | password123 |

Registration is restricted to `@alumni.ku.dk` email addresses.

## Database schema

| Table | Description |
|---|---|
| `category` | Restaurant categories (Asian, Italian, Café, …) |
| `restaurant` | 100 Copenhagen restaurants with address and price tier |
| `item` | Parent table for menu items (ISA hierarchy) |
| `food_item` | Food items with dietary info and meal type |
| `beverage` | Drinks with alcohol/hot/volume metadata |
| `user` | Registered students |
| `review` | Star ratings and comments, one per user per restaurant |

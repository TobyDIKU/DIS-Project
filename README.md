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
| alc123@alumni.ku.dk | password123 |
| bob456@alumni.ku.dk | password123 |
| chr789@alumni.ku.dk | password123 |
| din012@alumni.ku.dk | password123 |
| erk345@alumni.ku.dk | password123 |

Registration is restricted to `@alumni.ku.dk` email addresses.

Regex (`re.fullmatch`) is used in `app/auth.py` to validate registration input — the email format (3 letters + 3 digits `@alumni.ku.dk`), username (3-20 chars and only certain characters) and password strength (minimum 8 chars + 1 digit).

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

## Interaction Instructions

1. **Browse** — open http://127.0.0.1:5000 to see all 100 restaurants. Each card shows the average rating, review count, and cheapest alcoholic drink price.
2. **Filter & sort** — narrow the list by category (Asian, Italian, Café, …) and by drink price (under 30/40/50 kr), and sort by name (A–Z) or rating (high↔low).
3. **View a restaurant** — click a restaurant to see its menu grouped by meal type, beverages with badges (Vegan, Vegetarian, Allergens, Hot, Alcoholic, Volume), and its reviews (filterable by stars and recency).
4. **Log in / register** — sign in with a demo account from the table above, or register a new `@alumni.ku.dk` account from the navbar.
5. **Post a review** — once logged in, give a restaurant a 1–5 star rating and an optional comment. One review per user per restaurant.
6. **Log out** — via the navbar button.

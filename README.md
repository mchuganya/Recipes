# Recipes API (Flask + SQLite)

This project implements the assessment: parse a recipes JSON, store it in a database, and provide REST APIs with pagination, sorting and searching. A minimal frontend is included.

Requirements
- Python 3.10+

Setup
1. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/Scripts/activate   # on Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

2. Prepare your recipes JSON file (the assessment provides this). Place it somewhere accessible, e.g. `recipes.json` in the project root.

3. Load data into the database:

```bash
python load_data.py recipes.json
```

This will create `recipes.db` (SQLite) by default.

Run

```bash
python app.py
```

The API will be available at `http://localhost:5000`.

APIs

1. GET /api/recipes?page=1&limit=10
- Returns paginated recipes sorted by rating descending.

2. GET /api/recipes/search?calories=<=400&title=pie&rating=>=4.5
- Supports filters: `calories` (operators <=,>=,<,>,=), `title` (partial match), `cuisine` (exact), `total_time` and `rating`.

Frontend
Open `http://localhost:5000` to see a minimal UI that lists recipes and shows details in a drawer.

Notes and assumptions
- Database uses SQLite for simplicity. The `nutrients` field is stored as JSON text. A derived numeric `calories` column is stored for efficient filtering.
- Numeric "NaN" values are converted to NULL during import.
- If your dataset uses different field names, update `load_data.py` extraction logic accordingly.

Submission

This workspace is ready to be submitted as a git repository. Included artifacts:

- Source code: `app.py`, `models.py`, `load_data.py` (API and loader)
- Frontend: `frontend/index.html`, `frontend/app.js`
- Database schema: `schema.sql`
- DB helper: `create_db.py` (creates SQLite DB from `schema.sql`)
- Smoke test: `smoke_test.py` (uses Flask test client to verify endpoints without network)
- Sample data: `recipes.json`

Suggested git commands to create the repo and make an initial commit:

```bash
git init
git add .
git commit -m "Add Recipes API implementation, schema, loader, and frontend"
```

How to prepare the database (two options):

1) Use the loader (recommended - will parse and handle NaN values):

```bash
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
python load_data.py recipes.json
```

2) Or create the DB from the provided SQL schema (creates empty DB):

```bash
python create_db.py
```

Run the app (non-debug by default):

```bash
python app.py
```

API testing

Manual tests (curl):

```bash
curl "http://127.0.0.1:5000/api/recipes?page=1&limit=10"
curl "http://127.0.0.1:5000/api/recipes/search?calories=%3C%3D400&title=pie&rating=%3E%3D4.5"
```

Automated smoke test (no network required):

```bash
venv/Scripts/python smoke_test.py
```

Example sample response for `GET /api/recipes?page=1&limit=10` (sample data loaded):

```json
{ "page":1, "limit":10, "total":5, "data":[ /* ... sample recipes ... */ ] }
```

Deliverables checklist

- [x] Source code (backend, loader, frontend)
- [x] Database schema (`schema.sql`)
- [x] Sample data (`recipes.json`)
- [x] DB helper script (`create_db.py`)
- [x] Smoke test script (`smoke_test.py`)
- [x] README with run and submission instructions

If you'd like, I can also:
- Add a small `pytest` suite for the API endpoints.
- Provide a Dockerfile and docker-compose (with PostgreSQL) for production-like setup.

Choose any of the above and I'll implement it.


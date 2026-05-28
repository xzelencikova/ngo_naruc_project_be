# NGO Náruč REST API

**This project is a modular Flask API with a clean separation between:**

- API layer (Flask-RESTX namespaces)
- Service layer (business logic)
- Repository layer (database access)
- Database initialization service (singleton engine + session factory)
- DTOs & validation (Pydantic)
- SQL queries (stored in a dedicated module)

---

## API Structure

    app/
    │
    ├── api/
    │   ├── namespaces/
    │   │   ├── users_namespace.py      # Flask-RESTX endpoints
    │   │   └── ...
    │   │
    │   ├── services/
    │   │   ├── users_service.py        # Business logic for Users
    │   │   └── ...
    │   │
    │   ├── db/
    │   │   ├── database.py             # Database engine + session singleton
    │   │   ├── repositories/
    │   │   │   ├── base_repo.py        # Shared helpers (execute, load_to_db, etc.)
    │   │   │   ├── users_repo.py       # User repository
    │   │   │   └── ...
    │   │   ├── data/
    │   │   │   ├── queries.py          # Raw SQL queries
    │   │   │   └── ...
    │   │   └── ...
    │   │
    │   ├── models/
    │   │   ├── users_models.py         # Marshal schemas for requests input/output
    │   │   └── ...
    |   |__ dto/
    │   │   ├── users.py                # Custom Data Type models for params and return values
    │   │   └── ...
    │   │
    │   ├── utils/
    │   │   └── auth_token.py           # Token encoding/decoding utilities
    │   │
    │   └── __init__.py                 # create_app(), namespace registration
    │
    ├── config.py                       # Environment & DB config
    └── main.py                         # Flask API declaration

---

## Key Concepts

### Database Initialization

Database is a singleton responsible for creating and exposing:

- SQLAlchemy engine
- SQLAlchemy SessionLocal factory

Services and repositories never create engines themselves—they call:

    from app.api.db.database import Database

    engine = Database.get_engine()
    session = Database.get_session()

---

### Services

Business logic layer.
Each service loads its repository and DB engine internally:

    class UsersService:
        def __init__(self):
            self.engine = Database.get_engine()
            self.repo = UsersRepository(self.engine)

---

### Repositories

Contain only data operations (SQL queries, selects, inserts, updates):

- BaseRepository provides \_execute_query() and \_load_data_to_db().
- Each child repository implements domain-specific DB operations.

---

## Installing libraries

To create a virtual environment:

    python -m venv venv

To activate a virtual environment:

    venv\Scripts\activate

To install library:

    pip install <library>

To install libraries from requirements.txt file:

    pip install -r requirements.txt

---

## Running the application

To run the application:

    python run.py

or:

    python runWaitressServer.py

---

## Application Deployment

https://github.com/JeevanSandhu/Documentation/blob/master/Flask%20API%20on%20IIS.md

## Requirements

- Python >= 3.12
- Python Formatter Black (Nice to have for code formatting purpose)

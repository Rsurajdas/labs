# FastAPI

A books API built twice: first with an in-memory list and raw dict bodies, then again on PostgreSQL with SQLAlchemy models and Pydantic schemas.

## What's here

| Path                     | Covers                                                                         |
| ------------------------ | ------------------------------------------------------------------------------ |
| `project_one/books.py`   | First version: CRUD on an in-memory list, path params, an optional query param |
| `project_one/data.py`    | Seed data: 10 books as plain dicts                                             |
| `main.py`                | Second version: routes backed by PostgreSQL, `response_model`, 404 handling    |
| `database.py`            | Engine, `SessionLocal`, and the declarative `Base`                             |
| `models.py`              | SQLAlchemy `Books` table with a `CHECK` on rating                              |
| `schema.py`              | Pydantic `BookCreate`, `BookResponse`, and the `BookResponseWrapper` envelope  |

### Version 1: in-memory (project_one/)

| Method   | Path          | Notes                                                       |
| -------- | ------------- | ----------------------------------------------------------- |
| `GET`    | `/books`      | Optional `?in_stock=true/false` filter                      |
| `GET`    | `/books/{id}` |                                                             |
| `POST`   | `/books`      | Body is any JSON object; must include `id` and `title`      |
| `PUT`    | `/books/{id}` | Replaces the whole book with the request body               |
| `DELETE` | `/books/{id}` |                                                             |

Data lives in the `BOOKS` list, so every change is lost on restart.

### Version 2: PostgreSQL (main.py)

| Method | Path                      | Notes                                         |
| ------ | ------------------------- | --------------------------------------------- |
| `GET`  | `/books`                  | Optional `?rating=1..5` filter                |
| `POST` | `/books`                  | Body validated by `BookCreate`                |
| `GET`  | `/books/{id}`             | `id > 0`, 404 if not found                    |
| `GET`  | `/books/published/{year}` | Filters on `published_date`                   |

Every response is wrapped in `BookResponseWrapper`:

```json
{ "status": "success", "length": 2, "data": [ { "id": 1, "title": "...", ... } ] }
```

`length` is only set on list endpoints; `data` is a list there and a single book otherwise.

### What changed between the two

|                  | Version 1                              | Version 2                                                    |
| ---------------- | -------------------------------------- | ------------------------------------------------------------ |
| Storage          | Python list                            | PostgreSQL via SQLAlchemy                                    |
| Request body     | `Body()`, an untyped dict              | `BookCreate` Pydantic model with `min_length`, `ge` / `le`   |
| Response shape   | Hand-built dict                        | `response_model=BookResponseWrapper`, ORM objects converted via `from_attributes=True` |
| Not found        | `200` with `"status": "failed"`        | `HTTPException(status_code=404)`                             |
| Param validation | None                                   | `Path(gt=0)`, `Query(gt=0, lt=6)`                            |
| DB session       | n/a                                    | `get_db()` generator + `Annotated[Session, Depends(get_db)]` |
| Book fields      | `year`, float `rating`, `genre`, `price`, `in_stock` | `published_date`, integer `rating` 1–5, `description` |

## Running

Needs a local PostgreSQL with a database called `books`. The table is created on startup by `Base.metadata.create_all`.

```bash
cd fastapi
python -m venv venv
venv\Scripts\activate             # Windows; source venv/bin/activate elsewhere
pip install "fastapi[standard]" sqlalchemy "psycopg[binary]"

createdb -U postgres books        # or CREATE DATABASE books; in psql

uvicorn main:app --reload         # version 2
cd project_one && uvicorn books:app --reload   # version 1, no database needed
```

Interactive docs at <http://127.0.0.1:8000/docs>. The `json_schema_extra` example in `schema.py` pre-fills the `POST /books` body there.

The local venv (ignored by git through the `.gitignore` that `venv` creates inside it) has FastAPI 0.141.1, SQLAlchemy 2.0.54, Pydantic 2.13.5, psycopg 3.3.5, on Python 3.14.

## Other notes

- **`BookResponse` breaks on NULL columns.** It redeclares `description: str` and `published_date: int`, overriding the optional versions from `BookBase`. The database allows NULL in both, and `BookCreate` lets you omit them. So a book created without a description is saved fine, but every endpoint that returns it fails response validation with a `500`, including the `POST` that created it. Deleting the redeclared fields (they're inherited from `BookBase` already) fixes it.
- **The database password is in `database.py`**, and in git history. Fine for a local throwaway, but if `suraj123` is used anywhere else, change it there. Reading the URL from an environment variable (`os.environ["DATABASE_URL"]`, or `pydantic-settings`, which is already installed) keeps it out of the repo.
- **`async def` with a sync session blocks the event loop.** `db.query(...)` is a blocking call. FastAPI runs plain `def` endpoints in a thread pool, but `async def` endpoints run on the event loop, so a slow query stalls every other request. Use `def` with the sync `Session`, or switch to SQLAlchemy's async engine and `AsyncSession`.
- `create_all` only creates tables that don't exist. Changing `models.py` (say, a new column or constraint) does nothing to an existing `books` table; drop it or use migrations (Alembic).
- `from sqlalchemy.ext.declarative import declarative_base` is the pre-2.0 import path. In SQLAlchemy 2.0 it lives in `sqlalchemy.orm`, or use `class Base(DeclarativeBase): pass`.
- `POST /books` returns `200`. `@app.post(..., status_code=201)` is the usual code for a created resource.
- `Query(gt=0, lt=6)` on `rating` and `Field(ge=1, le=5)` in the schema express the same range two ways.
- In version 1:
  - `POST` doesn't check that `id` is unique, so two books can share one.
  - `PUT` stores the body as-is. Leave out `id` and the book can no longer be found by its old one.
  - `in_stock == None` works, but `is None` is the idiom; `None` is a singleton.
  - Failures return `200`. Version 2 fixes that for the 404 case.

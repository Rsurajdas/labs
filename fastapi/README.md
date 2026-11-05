# FastAPI

FastAPI projects, one per folder, each with its own virtual environment.

| Folder   | Status                                                                                    |
| -------- | ----------------------------------------------------------------------------------------- |
| `books/` | A books API built twice: in-memory first, then on PostgreSQL with SQLAlchemy and Pydantic |
| `todo/`  | A todo API on PostgreSQL with JWT auth, per-user todos, and an admin-only delete          |

## books

A books API built twice: first with an in-memory list and raw dict bodies, then again on PostgreSQL with SQLAlchemy models and Pydantic schemas. Paths below are relative to `books/`.

### What's here

| Path                     | Covers                                                                         |
| ------------------------ | ------------------------------------------------------------------------------ |
| `project_one/books.py`   | First version: CRUD on an in-memory list, path params, an optional query param |
| `project_one/data.py`    | Seed data: 10 books as plain dicts                                             |
| `main.py`                | Second version: routes backed by PostgreSQL, `response_model`, 404 handling    |
| `database.py`            | Engine, `SessionLocal`, and the declarative `Base`                             |
| `models.py`              | SQLAlchemy `Books` table with a `CHECK` on rating                              |
| `schema.py`              | Pydantic `BookCreate`, `BookResponse`, and the `BookResponseWrapper` envelope  |

#### Version 1: in-memory (project_one/)

| Method   | Path          | Notes                                                       |
| -------- | ------------- | ----------------------------------------------------------- |
| `GET`    | `/books`      | Optional `?in_stock=true/false` filter                      |
| `GET`    | `/books/{id}` |                                                             |
| `POST`   | `/books`      | Body is any JSON object; must include `id` and `title`      |
| `PUT`    | `/books/{id}` | Replaces the whole book with the request body               |
| `DELETE` | `/books/{id}` |                                                             |

Data lives in the `BOOKS` list, so every change is lost on restart.

#### Version 2: PostgreSQL (main.py)

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

#### What changed between the two

|                  | Version 1                              | Version 2                                                    |
| ---------------- | -------------------------------------- | ------------------------------------------------------------ |
| Storage          | Python list                            | PostgreSQL via SQLAlchemy                                    |
| Request body     | `Body()`, an untyped dict              | `BookCreate` Pydantic model with `min_length`, `ge` / `le`   |
| Response shape   | Hand-built dict                        | `response_model=BookResponseWrapper`, ORM objects converted via `from_attributes=True` |
| Not found        | `200` with `"status": "failed"`        | `HTTPException(status_code=404)`                             |
| Param validation | None                                   | `Path(gt=0)`, `Query(gt=0, lt=6)`                            |
| DB session       | n/a                                    | `get_db()` generator + `Annotated[Session, Depends(get_db)]` |
| Book fields      | `year`, float `rating`, `genre`, `price`, `in_stock` | `published_date`, integer `rating` 1–5, `description` |

### Running

Needs a local PostgreSQL with a database called `books`. The table is created on startup by `Base.metadata.create_all`.

```bash
cd fastapi/books
python -m venv venv
venv\Scripts\activate             # Windows; source venv/bin/activate elsewhere
pip install "fastapi[standard]" sqlalchemy "psycopg[binary]"

createdb -U postgres books        # or CREATE DATABASE books; in psql

uvicorn main:app --reload         # version 2
cd project_one && uvicorn books:app --reload   # version 1, no database needed
```

Interactive docs at <http://127.0.0.1:8000/docs>. The `json_schema_extra` example in `schema.py` pre-fills the `POST /books` body there.

The local venv at `books/venv` (ignored by git through the `.gitignore` that `venv` creates inside it) has FastAPI 0.141.1, SQLAlchemy 2.0.54, Pydantic 2.13.5, psycopg 3.3.5, on Python 3.14.

### Other notes

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

## todo

A todo API on PostgreSQL with JWT authentication. Each todo belongs to a user, and a user only sees and edits their own; deleting is restricted to admins. Paths below are relative to `todo/`.

### What's here

| Path                   | Covers                                                                        |
| ---------------------- | ----------------------------------------------------------------------------- |
| `main.py`              | App entry: creates tables and mounts the `auth` and `todo` routers            |
| `database.py`          | Engine, `SessionLocal`, `Base`, and the `DB_DEPENDENCY` session dependency    |
| `models/auth.py`       | SQLAlchemy `User` table                                                       |
| `models/todo.py`       | SQLAlchemy `Todo` table with an `owner_id` foreign key to `users.id`          |
| `routers/auth.py`      | Register, login, sign-in, list users, plus password hashing and JWT helpers   |
| `routers/todo.py`      | CRUD on todos, each scoped to the authenticated user                          |
| `schemas/auth.py`      | Pydantic request/response models for users and tokens                         |
| `schemas/todo.py`      | Pydantic request/response models for todos                                    |

### Auth endpoints (`/auth`)

| Method | Path             | Auth | Notes                                                                 |
| ------ | ---------------- | ---- | --------------------------------------------------------------------- |
| `GET`  | `/auth/users`    | none | Lists all users                                                       |
| `POST` | `/auth/register` | none | Creates a user; password is bcrypt-hashed before saving               |
| `POST` | `/auth/login`    | none | JSON body (`email` + `password`); returns the token in the envelope   |
| `POST` | `/auth/sign_in`  | none | OAuth2 form (`username` + `password`); returns `access_token`         |

`login` and `sign_in` do the same thing two ways: `login` takes a custom JSON model and authenticates by **email**, while `sign_in` takes the standard `OAuth2PasswordRequestForm` and authenticates by **username**. `sign_in` is the one wired to the Swagger "Authorize" button (`tokenUrl="auth/sign_in"`), so use it to get a token in `/docs`.

Tokens are HS256 JWTs carrying `sub` (username), `id`, and `role`, and expire after 30 minutes.

### Todo endpoints (`/todos`)

All require a bearer token. Every query is filtered by `owner_id`, so one user cannot read or change another's todos.

| Method   | Path           | Notes                                                        |
| -------- | -------------- | ------------------------------------------------------------ |
| `GET`    | `/todos/`      | Lists the caller's todos                                     |
| `GET`    | `/todos/{id}`  | `id > 0`, 404 if not found or not owned                      |
| `POST`   | `/todos/`      | Body validated by `TodoRequest`; `owner_id` set from token   |
| `PUT`    | `/todos/{id}`  | Replaces the todo's fields, 404 if not found or not owned    |
| `DELETE` | `/todos/{id}`  | **Admin only** (`role == "admin"`); `204` on success         |

List responses are wrapped like the books API — `{ "status", "length", "data": [...] }` — and single-todo responses as `{ "status", "message", "data": {...} }`.

A `Todo` has `title` (min 3 chars), optional `description` (3–280 chars), `priority` (1–5), and `complete`.

### Running

Needs a local PostgreSQL with a database called `todo`. Tables are created on startup by `Base.metadata.create_all`.

```bash
cd fastapi/todo
python -m venv .venv
.venv\Scripts\activate            # Windows; source .venv/bin/activate elsewhere
pip install "fastapi[standard]" sqlalchemy "psycopg[binary]" bcrypt "python-jose[cryptography]"

createdb -U postgres todo         # or CREATE DATABASE todo; in psql

uvicorn main:app --reload
```

Interactive docs at <http://127.0.0.1:8000/docs>. Register a user, authorize with `sign_in`, then call the `/todos` routes.

### Other notes

- **`is_active=body.is_active or True` can never store an inactive user.** When `is_active` is `False` the `or` falls through to `True`, and when it's omitted it also becomes `True`. Use `body.is_active if body.is_active is not None else True`, or just a column default.
- **`register` doesn't check for an existing user.** `email` and `username` are `unique`, so a duplicate raises an `IntegrityError` that surfaces as a `500`. Look the user up first and return a `409`, or catch the integrity error.
- **`GET /auth/users` is unauthenticated** and returns every user. The response model also declares a `password` field, which the ORM object doesn't have; it comes back `null`, but it's better left off the response schema entirely.
- **`decode_jwt` passes the exception object as `detail`.** On a bad token, `HTTPException(..., detail=e)` hands FastAPI a `JWTError` to serialize, which itself errors; pass a string like `"Token is invalid"` instead.
- **Secrets are hardcoded.** The JWT `SECRET_KEY` is in `routers/auth.py` and the database password is in `database.py`, both in git history. Load them from environment variables (`os.environ`, or `pydantic-settings`) for anything beyond a local throwaway.
- `ALGORIHM` is a typo for `ALGORITHM`, and `jwt.decode(..., algorithms=ALGORIHM)` passes a string where a list is expected — it happens to work but `["HS256"]` is the intended form.
- `async def` endpoints run blocking `db.query(...)` calls on the event loop; the same note as the books API applies (use `def`, or an async engine).
- `DELETE /todos/{id}` deletes by `id` alone once the caller is an admin, so an admin can delete any user's todo. That's intentional here, but unlike the other todo routes it isn't owner-scoped.

# Labs

My personal playground for learning.

Whenever I pick up something new, a language, a framework, a tool, a concept, I create a directory for it here and practice inside it. Notes, snippets, small experiments, half-finished ideas: everything lives in one place so I can come back and look it up later instead of hunting through scattered folders and bookmarks.

This is a scratchpad, not a portfolio. Code here is written to understand something, not to ship it.

## Currently working on

- **FastAPI auth (todo API):** `fastapi/todo/` is split into `models/`, `schemas/`, and `routers/` packages, with `APIRouter` prefixes (`/auth`, `/todos`) and a shared `DB_DEPENDENCY = Annotated[Session, Depends(get_db)]`.
  - **Users:** `POST /auth/register` hashes passwords with `bcrypt`, and `GET /auth/users` lists users.
  - **Two ways to log in:** `POST /auth/login` takes a custom Pydantic body (email + password), and `POST /auth/sign_in` takes an `OAuth2PasswordRequestForm` (username + password). Both go through `authenticate_user`, which only matches active users and returns `401` on bad credentials.
  - **JWTs:** a successful login returns a 30-minute HS256 token from `python-jose` (`sub`, `id`, `exp`). `decode_jwt` validates it through `OAuth2PasswordBearer`.
  - **Todos:** full CRUD on `/todos`, with `Field` validation (priority 1–5, length limits), `Path(gt=0)`, 404s, and a `204` on delete. Todos have an `owner_id` foreign key to `users`, but the routes don't depend on `decode_jwt` yet and nothing fills in `owner_id`.
- **Self-assessments:** graded question sets in `Technical Learning & Assessments/` to check what has stuck. Each has a `Questions.md`, my answer files, and an `Answers.md` evaluation report with an explanation for every question (see [Assessments](#assessments)).
- **SQL many-to-many:** a company schema (`sql/relations_company.sql`) with `buildings → teams → employees`, a `projects_employees` junction table, `ON DELETE SET NULL` vs `ON DELETE CASCADE`, and a foreign key that references a `UNIQUE` non-PK column (`internet_accounts.email → employees.email`).
- **Advanced React + TypeScript:** a second Vite app (`typescript/react-ts-advance/`) about wrapper components.
  - `Inputs` extends `ComponentPropsWithoutRef<"input">` and forwards the remaining props with `...props`.
  - `Button` is a discriminated union on `tag` (`"button"` or `"anchor"`), so it renders either a `<button>` or an `<a>`.
  - `PolymorphicComponent` takes an `el: ElementType` prop and renders whatever element it's given.

## Recently covered

- **React + TypeScript basics:** a Vite course-goals app (`typescript/rect-ts-basics/`): typed props with `PropsWithChildren`, `children`, lifting state up, typed callbacks for adding and deleting goals, typed form events, and shared types in a separate `types/` file. `InfoBox` uses a discriminated union on `mode`, so `severity` is required only on warnings.
- **SQL assessment drills:** `sql/Assessment/` has a bookstore schema (`authors`, `genres`, `books`) with `CHECK`, `DEFAULT`, and `UNIQUE` constraints and an `ALTER TABLE ... ADD CONSTRAINT`. It also has CRUD with `UPDATE`/`DELETE`, joins that find books with no author, and `LIMIT ... OFFSET` paging, plus the `products` / `employees` CRUD tasks.
- **SQL relationships:** a PostgreSQL `relations` database (`sql/relations.sql`) with `cities`, `addresses`, and `users` linked by foreign keys and `SERIAL` primary keys. Seed data lives in its own file (`sql/relations_insert_data_query.sql`), with some `NULL` foreign keys on purpose. The queries use multi-table `INNER JOIN`s and `LEFT JOIN`s, plus `IS NOT NULL` filters to drop the unmatched rows.
- **SQL joins:** `departments` and `employees` (`sql/practice_data_normalization.sql`): `INNER JOIN` vs `LEFT JOIN`, finding employees with no department, and top-N by salary.
- **FastAPI books API:** `fastapi/books/` is backed by PostgreSQL through SQLAlchemy with Pydantic schemas. It covers `response_model` with a `BookResponseWrapper` envelope, a 404 `HTTPException` for missing IDs, `GET /books/published/{year}`, and an optional `rating` filter (1–5) on `GET /books`.
- **TypeScript:** type aliases, union types, interfaces and interface merging, literal-union "enums", and generics.
- **SQL CRUD:** practice tasks on `products`, `sales`, and `employees` tables: filtering, `ORDER BY`, `LIMIT`, `DISTINCT`, subqueries, and views.

## Assessments

Each set is answered without running the code first, then graded. The scores are kept as a baseline to measure against.

| #  | Date       | Topic                                              | Score        |
| -- | ---------- | -------------------------------------------------- | ------------ |
| 01 | 2026-10-17 | Mixed: SQL, TypeScript, Python, JS, FastAPI, React | 3 / 12 (25%) |
| 02 | 2026-10-17 | TypeScript: aliases, interfaces, unions, generics  | 9 / 12 (75%) |
| 03 | 2026-10-20 | PostgreSQL: company projects database              | 7 / 12 (58%) |

Where points were lost:

- **#01:** two unanswered (React + TS, FastAPI), and several answers that missed one requirement or edge case.
- **#02:** typed functions, debugging literal types, and combining generics with typed functions.
- **#03:** constraints and FKs, finding unmatched records, debugging, views with `DISTINCT`, and cascading deletes.

## Structure

One top-level directory per topic. Inside it, whatever structure makes sense for that topic.

```
labs/
├── Technical Learning & Assessments/  # Graded self-assessments
│   ├── Assessment #01/            # Mixed topics: Questions.md, answer files, Answers.md report
│   ├── Assessment #02/            # TypeScript
│   └── Assessment #03/            # PostgreSQL company projects database
├── fastapi/                       # FastAPI projects, one per folder
│   ├── README.md
│   ├── books/                     # Books API, built twice
│   │   ├── main.py                # Routes backed by PostgreSQL, 404 handling
│   │   ├── database.py            # Engine and session setup
│   │   ├── models.py              # SQLAlchemy models
│   │   ├── schema.py              # Pydantic schemas and response wrappers
│   │   └── project_one/           # First version: in-memory CRUD books API
│   └── todo/                      # Todo API with users, bcrypt, and JWT login
│       ├── main.py                # App setup, includes the routers
│       ├── database.py            # Engine, session, DB_DEPENDENCY
│       ├── models/                # SQLAlchemy User and Todo
│       ├── schemas/               # Pydantic request/response models
│       └── routers/               # auth.py (/auth), todo.py (/todos)
├── js/                            # JavaScript practice problems
│   ├── codeWars.js                # Codewars katas
│   └── pracHub.js                 # Algorithm practice (two-sum, etc.)
├── python/                        # Python basics
│   ├── README.md
│   ├── dict.py, list.py, imports.py
│   └── oop/                       # Classes and inheritance (Enemy, Zombie, Ogre, Weapon)
├── rust/                          # Rust course projects
│   ├── hello_world/
│   ├── variables-and-mutability/
│   ├── data-types/
│   └── doc/                       # Course slides
├── sql/                           # MySQL and PostgreSQL scripts
│   ├── README.md
│   ├── mysql.sql, postgres.sql    # Same schema in both dialects
│   ├── practice_crud.sql          # Products table: inserts and basic queries
│   ├── crud.sql                   # CRUD practice on sales
│   ├── practice_data_normalization.sql  # departments ↔ employees: INNER vs LEFT JOIN
│   ├── relations.sql              # Foreign keys and JOINs: cities → addresses → users
│   ├── relations_insert_data_query.sql  # Seed data for relations.sql
│   ├── relations_company.sql      # Company schema: many-to-many, ON DELETE rules
│   └── Assessment/                # Bookstore schema, constraints, CRUD, joins, CRUD tasks
├── typescript/                    # TypeScript fundamentals
│   ├── README.md
│   ├── basic.ts                   # Source
│   ├── basic.js                   # Compiled output
│   ├── rect-ts-basics/            # React + TypeScript (Vite) course-goals app
│   │   └── src/
│   │       ├── App.tsx            # Goal state, add/delete handlers
│   │       ├── components/        # Header, CourseGoal, CourseGoalList, AddNewGoal, InfoBox
│   │       └── types/goal.ts      # Goal interface and handler types
│   └── react-ts-advance/          # React + TypeScript (Vite): wrapper and polymorphic components
│       └── src/components/        # Inputs, Button, PolymorphicComponent
└── package.json                   # Node tooling (TypeScript compiler)
```

| Directory                                                                         | What's in it                                                                              |
| --------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| [`Technical Learning & Assessments/`](./Technical%20Learning%20%26%20Assessments) | Graded self-assessments with per-question evaluation reports                              |
| [`fastapi/`](./fastapi)                                                           | REST APIs with FastAPI: CRUD, SQLAlchemy, response models, routers, bcrypt, JWT auth      |
| [`js/`](./js)                                                                     | JavaScript problem solving from Codewars and other practice sites                         |
| [`python/`](./python)                                                             | Python data structures, imports, and object-oriented programming                          |
| [`rust/`](./rust)                                                                 | Rust fundamentals: variables, mutability, and data types                                  |
| [`sql/`](./sql)                                                                   | SQL in MySQL and PostgreSQL: schema design, constraints, CRUD, views, JOINs, many-to-many |
| [`typescript/`](./typescript)                                                     | TypeScript types, interfaces, unions, generics, and two React + TS apps                   |

## Conventions

A few rules I try to stick to, so this stays useful six months from now:

- **One topic per top-level directory.** If a topic gets big enough, split it into subdirectories by subtopic.
- **Every directory gets its own `README.md`** with what I was learning, where I learned it from, and anything that tripped me up.
- **Keep the "why" with the code.** A comment explaining why something works is worth more than the working code by itself.
- **Don't delete the broken attempts.** The thing that didn't work is often the more useful note.
- **Small and runnable.** Each experiment should stand on its own and run without much setup.

## Running things

Each directory has its own setup, since the stacks are different. Check the README inside the directory where there is one. In general:

```bash
# JavaScript
cd js && node <file>.js

# TypeScript (compiler installed via npm at the repo root)
npm install
npx tsc typescript/basic.ts

# React + TypeScript (Vite)
cd typescript/rect-ts-basics && npm install && npm run dev
cd typescript/react-ts-advance && npm install && npm run dev

# Python
cd python && python <file>.py
cd python/oop && python main.py

# FastAPI (needs fastapi, uvicorn, sqlalchemy, psycopg, and a local PostgreSQL "books" database)
# Full setup in fastapi/README.md
cd fastapi/books && uvicorn main:app --reload
cd fastapi/books/project_one && uvicorn books:app --reload

# Todo API (also needs bcrypt, python-jose[cryptography], and a local "todo" database)
createdb -U postgres todo
cd fastapi/todo && uvicorn main:app --reload

# Rust
cd rust/<project> && cargo run

# SQL
mysql -u root -p < sql/mysql.sql
psql -U postgres -f sql/postgres.sql

# relations.sql and practice_data_normalization.sql are PostgreSQL (SERIAL keys).
# relations.sql doesn't switch databases itself, so create it first and point psql at it
# (its own CREATE DATABASE line then just errors and psql carries on):
createdb -U postgres relations
psql -U postgres -d relations -f sql/relations.sql
psql -U postgres -d relations -f sql/relations_insert_data_query.sql
# The SELECTs in relations.sql run before the seed data goes in, so rerun them afterwards

# relations_company.sql is tables only; the seed data is in Assessment #03/Questions.md
createdb -U postgres company
psql -U postgres -d company -f sql/relations_company.sql
```

## Adding a new topic

```bash
mkdir <topic>
cd <topic>
touch README.md
```

Then note down what I'm learning and why, and start experimenting.

## A note for visitors

If you found this repo, you're welcome to look around, but the code is written for me. It's rough, it's inconsistent, and some of it is wrong on purpose because that's how I was thinking about the problem at the time.

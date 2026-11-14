# Labs

My personal playground for learning.

Whenever I pick up something new, a language, a framework, a tool, a concept, I create a directory for it here and practice inside it. Notes, snippets, small experiments, half-finished ideas: everything lives in one place so I can come back and look it up later instead of hunting through scattered folders and bookmarks.

This is a scratchpad, not a portfolio. Code here is written to understand something, not to ship it.

## Currently working on

- **Full-stack room-booking app (FastAPI + React/TS):** `technical_learning_and_assessments/assessment-06-fullstack/` is the project behind [Assessment #06](#assessments) — a "Study Room Booking" app where users book study rooms by day and hourly slot. This is the first assessment that spans a backend and a frontend together.
  - **Backend (`backend/`):** a FastAPI API over `users`, `rooms`, and `bookings` on PostgreSQL, with flat imports (`from database import ...`) like the todo API, plus `models/`, `schemas/`, and `routers/` packages. `config.py` reads secrets from the environment via `pydantic-settings` (`settings.secret_key`/`database_url`, no hardcoded fallback, so a missing variable fails at startup). `security.py` hashes with `bcrypt` and issues 30-minute HS256 JWTs; `dependencies.py` turns a token into the SQLAlchemy `User` (`get_current_user`, `require_admin`, and the `CurrentUser`/`AdminUser` aliases). `POST /auth/register` returns 409 on a duplicate username/email, room management is admin-only, bookings are owner-scoped (403/404/409/204), and `Booking.room_id`/`user_id` cascade on delete.
  - **Frontend (`frontend/`):** React 19 + `react-router-dom` v7 (declarative `<Routes>`) + typed `axios`, no context. Shared types in `types.ts` (including a generic `FetchState<T>` discriminated union), a typed API client in `api.ts` (axios generics plus a `getErrorMessage` helper), a `Layout` with `NavLink`s and `<Outlet />`, a protected `/bookings` route, and pages for the room list (`useMemo` filtering), room detail (URL params + booking form), my bookings (fetch-with-cleanup + cancel), and login.
  - The code here is the submission, with post-grading fixes applied — the frontend route/hook fixes are in (logout navigation, room-id validation, the `MyBookingsPage` rewrite), and the backend fixes are in too (`algorithms` passed as a list in `get_current_user`, `GET /bookings` admin scoping, a room-existence check before booking, and the stray `from turtle import st` import removed from `routers/bookings.py`).
- **Self-assessments:** graded question sets to check what has stuck. Each has a `Questions.md`, my answer files, and an `Answers.md` evaluation report with an explanation for every question (see [Assessments](#assessments)). Most live in `technical_learning_and_assessments/` (including the full-stack Assessment #06, a complete project of its own under `assessment-06-fullstack/`); the other project-based ones live inside the project they cover — Assessment #04 in `fastapi/assessment-04-expense-tracker/` and Assessment #05 in `typescript/assessment-05-react-ts/`.
- **SQL aggregates & grouping:** `sql/aggregate_and_grouping/` is a new `restaurants` schema split across three files (`create_queries.sql`, `insert_queries.sql`, `queries.sql`) with `payment_methods`, `tables`, and a `bookings` fact table (`NUMERIC(6, 2)` money columns, a nullable `amount_tipped`, and `payment_id`/`table_id` foreign keys). The queries so far are `COUNT`-based — `COUNT(*)` vs `COUNT(column)` (which skips the `NULL` tips) and `COUNT(DISTINCT booking_date)` — as a lead-in to `GROUP BY` and the other aggregates.
- **SQL many-to-many:** a company schema (`sql/relations_company.sql`) with `buildings → teams → employees`, a `projects_employees` junction table with a composite primary key (`employee_id`, `project_id`), a self-referencing foreign key (`employees.supervisor_id → employees.id`) for the reporting hierarchy, `ON DELETE SET NULL` vs `ON DELETE CASCADE`, and a foreign key that references a `UNIQUE` non-PK column (`internet_accounts.email → employees.email`).
- **Advanced React + TypeScript:** a second Vite app (`typescript/react-ts-advance/`) that started as a set of wrapper/forwarded-ref components (now under `src/components/UI/`) and grew into a "ReactTimer" app reusing them, with a Context + `useReducer` store.
  - **Reusable UI (`components/UI/`):** `Inputs` extends `ComponentPropsWithoutRef<"input">`, forwards the remaining props with `...props`, and uses `forwardRef<HTMLInputElement>` to pass a ref down to the `<input>`. `Button` is a discriminated union on `tag` (`"button"` or `"anchor"`), so it renders either a `<button>` or an `<a>`. `PolymorphicComponent` takes an `el: ElementType` prop and renders whatever element it's given. `Form` wraps a `<form>` (extending `ComponentPropsWithoutRef<"form">`), handles `onSubmit` by collecting `FormData` into an object and passing it to an `onSave` callback, and exposes an imperative `clear()` method to the parent via `forwardRef` + `useImperativeHandle` (typed by the `FormHandleRef` interface).
  - **Timer store (`store/timers-context.tsx`):** a `createContext` provider backed by `useReducer`, with a discriminated-union `Action` type (`ADD_TIMER`, `START_TIMERS`, `STOP_TIMERS`) and immutable reducer updates. The context value bundles state (`timers`, `isRunning`) with `addTimer`/`startTimers`/`stopTimers` dispatchers, and a typed `useTimersContext` hook throws if the context is `null` so consumers get a non-null value.
  - **Timer app:** `App` wraps everything in the provider; `AddTimer` reuses `Form` + `Input` + `Button` (and the form ref) to add a timer; `Header` flips one `Button` between Start/Stop from `isRunning`; `Timers` maps the list and `Timer` renders each one through `PolymorphicComponent` as an `<article>`. Each `Timer` runs its own countdown: it holds `remainingTime` in `useState`, and a `useEffect` keyed on `isRunning` starts a 50ms `setInterval` (tracked in a `useRef` so it survives re-renders), decrements the time, and clears the interval when it stops or the component unmounts. The remaining time drives a `<progress>` bar and a `toFixed(2)` seconds readout.

## Recently covered

- **React + TypeScript assessment app:** `typescript/assessment-05-react-ts/`, a "Workshop Registration Desk" Vite app built over the 12 questions of [Assessment #05](#assessments): shared types, a `Card`/`Button`/polymorphic `Container`, a discriminated-union `TicketDetails`, a `TextField` with `forwardRef`, a `RegistrationForm` exposing `clear()` via `useImperativeHandle`, and `App` owning all state. Submission plus post-grading fixes.
- **FastAPI expense tracker:** `fastapi/assessment-04-expense-tracker/`, a standalone app (`users`, `categories`, `expenses` on PostgreSQL) behind [Assessment #04](#assessments): tables from `schema.sql`, bcrypt/JWT auth under `/auth`, category CRUD, and filtered expense listing wrapped in `ExpenseListResponse`. Submission plus post-grading fixes.
- **FastAPI auth (todo API):** `fastapi/todo/`, split into `models/`, `schemas/`, and `routers/` packages: bcrypt registration, two login routes (custom body + `OAuth2PasswordRequestForm`) issuing 30-minute HS256 JWTs, and user-scoped CRUD on `/todos` with admin-only delete.
- **React + TypeScript basics:** a Vite course-goals app (`typescript/rect-ts-basics/`): typed props with `PropsWithChildren`, `children`, lifting state up, typed callbacks for adding and deleting goals, typed form events, and shared types in a separate `types/` file. `InfoBox` uses a discriminated union on `mode`, so `severity` is required only on warnings.
- **SQL assessment drills:** `sql/Assessment/` has a bookstore schema (`authors`, `genres`, `books`) with `CHECK`, `DEFAULT`, and `UNIQUE` constraints and an `ALTER TABLE ... ADD CONSTRAINT`. It also has CRUD with `UPDATE`/`DELETE`, joins that find books with no author, and `LIMIT ... OFFSET` paging, plus the `products` / `employees` CRUD tasks.
- **SQL relationships:** a PostgreSQL `relations` database (`sql/relations.sql`) with `cities`, `addresses`, and `users` linked by foreign keys and `SERIAL` primary keys. Seed data lives in its own file (`sql/relations_insert_data_query.sql`), with some `NULL` foreign keys on purpose. The queries use multi-table `INNER JOIN`s and `LEFT JOIN`s, plus `IS NOT NULL` filters to drop the unmatched rows.
- **SQL joins:** `departments` and `employees` (`sql/practice_data_normalization.sql`): `INNER JOIN` vs `LEFT JOIN`, finding employees with no department, and top-N by salary.
- **FastAPI books API:** `fastapi/books/` is backed by PostgreSQL through SQLAlchemy with Pydantic schemas. It covers `response_model` with a `BookResponseWrapper` envelope, a 404 `HTTPException` for missing IDs, `GET /books/published/{year}`, and an optional `rating` filter (1–5) on `GET /books`.
- **TypeScript:** type aliases, union types, interfaces and interface merging, literal-union "enums", and generics.
- **SQL CRUD:** practice tasks on `products`, `sales`, and `employees` tables: filtering, `ORDER BY`, `LIMIT`, `DISTINCT`, subqueries, and views.

## Assessments

Each set is answered without running the code first, then graded. The scores are kept as a baseline to measure against.

| #  | Date       | Topic                                                 | Score        |
| -- | ---------- | ----------------------------------------------------- | ------------ |
| 01 | 2026-10-17 | Mixed: SQL, TypeScript, Python, JS, FastAPI, React    | 3 / 12 (25%) |
| 02 | 2026-10-17 | TypeScript: aliases, interfaces, unions, generics     | 9 / 12 (75%) |
| 03 | 2026-10-20 | PostgreSQL: company projects database                 | 7 / 12 (58%) |
| 04 | 2026-10-31 | FastAPI: expense tracker (SQLAlchemy, Pydantic, auth) | 4 / 12 (33%) |
| 05 | 2026-11-01 | React + TypeScript: workshop registration app         | 3 / 12 (25%) |
| 06 | 2026-11-12 | Full stack: FastAPI + React/TS room booking           | 4 / 12 (33%) |

Where points were lost:

- **#01:** two unanswered (React + TS, FastAPI), and several answers that missed one requirement or edge case.
- **#02:** typed functions, debugging literal types, and combining generics with typed functions.
- **#03:** constraints and FKs, finding unmatched records, debugging, views with `DISTINCT`, and cascading deletes.
- **#04:** auth (bcrypt/login/JWT) went 0/3, plus `NULL`/optional handling, missed status codes, and `ON DELETE` behaviour. Most answers were almost right but missed a single stated requirement — the same pattern as #01.
- **#05:** first dedicated React assessment. The architecture was right almost everywhere; the marks went on spread/prop order, how `&&` renders a falsy `0`, which element an attribute belongs on, validating `FormData` values, and React 18 event types (`SubmitEvent` doesn't exist). 7 of the 8 wrong answers had the right structure but missed a stated detail — the same requirement-completeness pattern as #01 and #04.
- **#06:** first full-stack assessment (backend and frontend together). The structure was right almost everywhere; the marks went on auth failure paths (`None` vs `return None`, a missing `is_active` check, `algorithms` passed as a string not a list), existence checks before insert (checking `is None` on a required field instead of querying the DB), the Rules of Hooks (an early return before `useEffect`) and `useMemo` deps, a missing `api.post<Booking>` axios generic, and HTTP response prediction (unanswered again, as in #04). 6 of the 7 wrong answers had the right shape but missed a stated detail — the same requirement-completeness pattern as #01, #04, and #05.

## Structure

One top-level directory per topic. Inside it, whatever structure makes sense for that topic.

```
labs/
├── technical_learning_and_assessments/  # Graded self-assessments (#04 and #05 live inside the projects they cover)
│   ├── Assessment #01/            # Mixed topics: Questions.md, answer files, Answers.md report
│   ├── Assessment #02/            # TypeScript
│   ├── Assessment #03/            # PostgreSQL company projects database
│   └── assessment-06-fullstack/   # Full-stack room booking (Assessment #06): FastAPI backend/ + React frontend/
│       ├── ASSESSMENT.md          # Brief (12 questions: 6 backend, 6 frontend)
│       ├── ANSWERS.md             # Written answers
│       ├── RESULT.md              # Evaluation report (4/12)
│       ├── learning-scope.md      # Topic scope snapshot
│       ├── backend/               # FastAPI API: config.py, security.py, dependencies.py, seed.py, models/, schemas/, routers/
│       └── frontend/              # React 19 + Vite: api.ts, types.ts, components/ (Layout), pages/ (Rooms, RoomDetail, MyBookings, Login)
├── fastapi/                       # FastAPI projects, one per folder
│   ├── README.md
│   ├── books/                     # Books API, built twice
│   │   ├── main.py                # Routes backed by PostgreSQL, 404 handling
│   │   ├── database.py            # Engine and session setup
│   │   ├── models.py              # SQLAlchemy models
│   │   ├── schema.py              # Pydantic schemas and response wrappers
│   │   └── project_one/           # First version: in-memory CRUD books API
│   ├── todo/                      # Todo API with users, bcrypt, and JWT login
│   │   ├── main.py                # App setup, includes the routers
│   │   ├── database.py            # Engine, session, DB_DEPENDENCY
│   │   ├── models/                # SQLAlchemy User and Todo
│   │   ├── schemas/               # Pydantic request/response models
│   │   └── routers/               # auth.py (/auth), todo.py (/todos)
│   └── assessment-04-expense-tracker/  # Expense tracker API (Assessment #04)
│       ├── README.md             # Assessment #04 brief (questions)
│       ├── Answers.md             # Assessment #04 evaluation report (4/12)
│       ├── schema.sql             # PostgreSQL tables + seed data
│       ├── main.py, database.py   # App setup and session/DB_DEPENDENCY
│       ├── models/                # SQLAlchemy User, Category, Expense
│       ├── schemas/               # auth, categories, expenses Pydantic models
│       └── routers/               # auth.py, categories.py, expenses.py
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
│   ├── aggregate_and_grouping/    # restaurants schema: create/insert/queries, COUNT aggregates
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
│   ├── react-ts-advance/          # React + TypeScript (Vite): wrapper/polymorphic/ref components + a ReactTimer app
│   │   └── src/
│   │       ├── App.tsx            # Wraps the app in TimersContextProvider
│   │       ├── components/        # Header, AddTimer, Timers, Timer + UI/ (Inputs, Button, PolymorphicComponent, Form)
│   │       └── store/             # timers-context.tsx: createContext + useReducer store
│   └── assessment-05-react-ts/    # Workshop Registration Desk app (Assessment #05)
│       ├── ASSESSMENT.md          # Assessment #05 brief (12 questions)
│       ├── ANSWERS.md             # Written answers (Q6, Q7, Q12)
│       ├── RESULT.md              # Assessment #05 evaluation report (3/12)
│       └── src/
│           ├── App.tsx            # Lifted state, duplicate check, form ref
│           ├── components/        # Card, Button, Container, TicketDetails, Summary, SearchBox, TextField, RegistrationForm, AttendeeList
│           └── types.ts           # TicketType, AttendeeFormValues, Attendee, FormHandleRef
└── package.json                   # Node tooling (TypeScript compiler)
```

| Directory                                                                     | What's in it                                                                                          |
| ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| [`technical_learning_and_assessments/`](./technical_learning_and_assessments) | Graded self-assessments with per-question evaluation reports, plus the #06 project                    |
| [`fastapi/`](./fastapi)                                                       | REST APIs with FastAPI: CRUD, SQLAlchemy, response models, routers, bcrypt, JWT auth                  |
| [`js/`](./js)                                                                 | JavaScript problem solving from Codewars and other practice sites                                     |
| [`python/`](./python)                                                         | Python data structures, imports, and object-oriented programming                                      |
| [`rust/`](./rust)                                                             | Rust fundamentals: variables, mutability, and data types                                              |
| [`sql/`](./sql)                                                               | SQL in MySQL and PostgreSQL: schema design, constraints, CRUD, views, JOINs, many-to-many, aggregates |
| [`typescript/`](./typescript)                                                 | TypeScript types, interfaces, unions, generics, and three React + TS apps                             |

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
cd typescript/assessment-05-react-ts && npm install && npm run dev  # npm run typecheck for tsc --noEmit

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

# Expense tracker API (needs bcrypt, python-jose[cryptography]; tables come from schema.sql, not create_all)
createdb -U postgres expenses
psql -U postgres -d expenses -f fastapi/assessment-04-expense-tracker/schema.sql
cd fastapi/assessment-04-expense-tracker && uvicorn main:app --reload

# Room booking API (Assessment #06; deps in backend/requirements.txt; reads SECRET_KEY + DATABASE_URL from .env)
cd technical_learning_and_assessments/assessment-06-fullstack/backend
pip install -r requirements.txt
cp .env.example .env            # then set SECRET_KEY and DATABASE_URL
createdb -U postgres room_booking
python seed.py                  # admin/adminpass123 + three rooms
uvicorn main:app --reload       # http://localhost:8000/docs

# Room booking frontend (React 19 + Vite, talks to the API at :8000)
cd technical_learning_and_assessments/assessment-06-fullstack/frontend && npm install && npm run dev

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

# aggregate_and_grouping is the "restaurants" database (PostgreSQL, SERIAL keys).
# create_queries.sql has a CREATE DATABASE line that errors once the db exists, then psql carries on.
createdb -U postgres restaurants
psql -U postgres -d restaurants -f sql/aggregate_and_grouping/create_queries.sql
psql -U postgres -d restaurants -f sql/aggregate_and_grouping/insert_queries.sql
psql -U postgres -d restaurants -f sql/aggregate_and_grouping/queries.sql
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

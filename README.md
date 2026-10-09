# Labs

My personal playground for learning.

Whenever I pick up something new, a language, a framework, a tool, a concept, I create a directory for it here and practice inside it. Notes, snippets, small experiments, half-finished ideas: everything lives in one place so I can come back and look it up later instead of hunting through scattered folders and bookmarks.

This is a scratchpad, not a portfolio. Code here is written to understand something, not to ship it.

## Currently working on

- **React + TypeScript:** a Vite course-goals app (`typescript/rect-ts-basics/`): typed props with `PropsWithChildren`, `children`, lifting state up, typed callbacks for adding and deleting goals, typed form events, and shared types in a separate `types/` file.
- **SQL relationships:** a PostgreSQL `relations` database (`sql/relations.sql`) with `cities`, `addresses`, and `users` linked by foreign keys and `SERIAL` primary keys. Seed data lives in its own file (`sql/relations_insert_data_query.sql`), with some `NULL` foreign keys on purpose. The queries use multi-table `INNER JOIN`s and `LEFT JOIN`s, plus `IS NOT NULL` filters to drop the unmatched rows.
- **SQL joins:** `departments` and `employees` (`sql/practice_data_normalization.sql`): `INNER JOIN` vs `LEFT JOIN`, finding employees with no department, and top-N by salary.
- **FastAPI:** a books API (`fastapi/books/`) backed by PostgreSQL through SQLAlchemy with Pydantic schemas: `response_model` with a `BookResponseWrapper` envelope, a 404 `HTTPException` for missing IDs, `GET /books/published/{year}`, and an optional `rating` filter (1–5) on `GET /books`. A `todo/` project has been started next to it (no code yet).
- **TypeScript:** type aliases, union types, interfaces and interface merging, literal-union "enums", and generics.
- **SQL CRUD:** practice tasks on `products`, `sales`, and `employees` tables: filtering, `ORDER BY`, `LIMIT`, `DISTINCT`, subqueries, and views.

## Structure

One top-level directory per topic. Inside it, whatever structure makes sense for that topic.

```
labs/
├── fastapi/                       # FastAPI projects, one per folder
│   ├── README.md
│   ├── books/                     # Books API, built twice
│   │   ├── main.py                # Routes backed by PostgreSQL, 404 handling
│   │   ├── database.py            # Engine and session setup
│   │   ├── models.py              # SQLAlchemy models
│   │   ├── schema.py              # Pydantic schemas and response wrappers
│   │   └── project_one/           # First version: in-memory CRUD books API
│   └── todo/                      # Just started, no code yet
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
├── shopify/                       # Shopify theme / Liquid notes
│   └── notes.md
├── sql/                           # MySQL and PostgreSQL scripts
│   ├── README.md
│   ├── mysql.sql, postgres.sql    # Same schema in both dialects
│   ├── practice_crud.sql          # Products table: inserts and basic queries
│   ├── crud.sql, crud_task*.sql   # CRUD practice tasks (sales, products, employees)
│   ├── practice_data_normalization.sql  # departments ↔ employees: INNER vs LEFT JOIN
│   ├── relations.sql              # Foreign keys and JOINs: cities → addresses → users
│   └── relations_insert_data_query.sql  # Seed data for relations.sql
├── typescript/                    # TypeScript fundamentals
│   ├── README.md
│   ├── basic.ts                   # Source
│   ├── basic.js                   # Compiled output
│   └── rect-ts-basics/            # React + TypeScript (Vite) course-goals app
│       └── src/
│           ├── App.tsx            # Goal state, add/delete handlers
│           ├── components/        # Header, CourseGoal, CourseGoalList, AddNewGoal
│           └── types/goal.ts      # Goal interface and handler types
└── package.json                   # Node tooling (TypeScript compiler)
```

| Directory                     | What's in it                                                                    |
| ----------------------------- | ------------------------------------------------------------------------------- |
| [`fastapi/`](./fastapi)       | REST APIs with FastAPI: path/query params, CRUD, SQLAlchemy, response models    |
| [`js/`](./js)                 | JavaScript problem solving from Codewars and other practice sites               |
| [`python/`](./python)         | Python data structures, imports, and object-oriented programming                |
| [`rust/`](./rust)             | Rust fundamentals: variables, mutability, and data types                        |
| [`shopify/`](./shopify)       | Shopify theme structure and Liquid templating notes                             |
| [`sql/`](./sql)               | SQL in MySQL and PostgreSQL: schema design, constraints, CRUD, views, JOINs     |
| [`typescript/`](./typescript) | TypeScript types, interfaces, unions, generics, and a React + TS app            |

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

# Python
cd python && python <file>.py
cd python/oop && python main.py

# FastAPI (needs fastapi, uvicorn, sqlalchemy, psycopg, and a local PostgreSQL "books" database)
# Full setup in fastapi/README.md
cd fastapi/books && uvicorn main:app --reload
cd fastapi/books/project_one && uvicorn books:app --reload

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

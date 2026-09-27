# Labs

My personal playground for learning.

Whenever I pick up something new, a language, a framework, a tool, a concept, I create a directory for it here and practice inside it. Notes, snippets, small experiments, half-finished ideas: everything lives in one place so I can come back and look it up later instead of hunting through scattered folders and bookmarks.

This is a scratchpad, not a portfolio. Code here is written to understand something, not to ship it.

## Currently working on

- **TypeScript:** type aliases, union types, interfaces and interface merging, literal-union "enums", and generics.
- **SQL:** CRUD practice tasks on `products`, `sales`, and `employees` tables: filtering, `ORDER BY`, `LIMIT`, `DISTINCT`, and views.
- **FastAPI:** a books API, first with an in-memory list and now backed by PostgreSQL through SQLAlchemy with Pydantic response schemas.

## Structure

One top-level directory per topic. Inside it, whatever structure makes sense for that topic.

```
labs/
├── fastapi/                       # FastAPI + SQLAlchemy books API
│   ├── main.py                    # App and routes backed by PostgreSQL
│   ├── database.py                # Engine and session setup
│   ├── models.py                  # SQLAlchemy models
│   ├── schema.py                  # Pydantic schemas and response wrappers
│   └── project_one/               # First version: in-memory CRUD books API
├── js/                            # JavaScript practice problems
│   ├── codeWars.js                # Codewars katas
│   └── pracHub.js                 # Algorithm practice (two-sum, etc.)
├── python/                        # Python basics
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
│   ├── practice.sql               # Products table with constraints
│   └── crud.sql, crud_task*.sql   # CRUD practice tasks
├── typescript/                    # TypeScript fundamentals
│   ├── basic.ts                   # Source
│   └── basic.js                   # Compiled output
└── package.json                   # Node tooling (TypeScript compiler)
```

| Directory                     | What's in it                                                                    |
| ----------------------------- | ------------------------------------------------------------------------------- |
| [`fastapi/`](./fastapi)       | REST APIs with FastAPI: path/query params, CRUD endpoints, SQLAlchemy, Pydantic |
| [`js/`](./js)                 | JavaScript problem solving from Codewars and other practice sites               |
| [`python/`](./python)         | Python data structures, imports, and object-oriented programming                |
| [`rust/`](./rust)             | Rust fundamentals: variables, mutability, and data types                        |
| [`shopify/`](./shopify)       | Shopify theme structure and Liquid templating notes                             |
| [`sql/`](./sql)               | SQL in MySQL and PostgreSQL: schema design, constraints, CRUD queries, views    |
| [`typescript/`](./typescript) | TypeScript types, interfaces, unions, and generics                              |

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

# Python
cd python && python <file>.py
cd python/oop && python main.py

# FastAPI (needs fastapi, uvicorn, sqlalchemy, psycopg, and a local PostgreSQL "books" database)
cd fastapi && uvicorn main:app --reload
cd fastapi/project_one && uvicorn books:app --reload

# Rust
cd rust/<project> && cargo run

# SQL
mysql -u root -p < sql/mysql.sql
psql -U postgres -f sql/postgres.sql
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

# SQL

The same toy schema built twice, once in MySQL and once in PostgreSQL, so the dialect differences sit side by side.

## What's here

| File           | Dialect    |
| -------------- | ---------- |
| `mysql.sql`    | MySQL      |
| `postgres.sql` | PostgreSQL |

Both scripts build a small job-board database called `talently`:

- `users`: name, salary, employment status
- `employers`: company name, address, revenue, hiring flag
- `conversations`: messages between a user and an employer

They walk through `CREATE`, `INSERT`, `SELECT`, `DELETE`, then a series of `ALTER TABLE` statements that add primary keys, `NOT NULL`, defaults, `CHECK` constraints, and foreign keys.

## Running

These are scripts to read and run top to bottom, not migrations. They aren't idempotent, so re-running against an existing database will fail. Drop and recreate instead.

```bash
mysql -u root -p < mysql.sql
psql -U postgres -f postgres.sql
```

## Dialect differences worth remembering

|                                  | MySQL                                                        | PostgreSQL                                                              |
| -------------------------------- | ------------------------------------------------------------ | ----------------------------------------------------------------------- |
| Enums                            | Inline: `ENUM('a','b')` on the column                        | Named type first: `CREATE TYPE ... AS ENUM (...)`                       |
| Auto-increment PK                | `INT PRIMARY KEY AUTO_INCREMENT`                             | `SERIAL PRIMARY KEY`                                                    |
| Change a column                  | `MODIFY COLUMN name TYPE ...` (restate the whole definition) | `ALTER COLUMN name SET ...` / `SET DATA TYPE ...` (change one property) |
| Set NOT NULL                     | Part of `MODIFY COLUMN`, so the type has to be repeated      | `ALTER COLUMN name SET NOT NULL` on its own                             |
| Add a CHECK during a type change | Can be inlined in `MODIFY COLUMN`                            | Needs a separate `ADD CONSTRAINT`                                       |
| Create if absent                 | `CREATE DATABASE IF NOT EXISTS`                              | No `IF NOT EXISTS` on `CREATE DATABASE` in the same form                |

The MySQL `MODIFY COLUMN` requirement is the one that keeps catching me: forget to repeat the type and the column quietly changes type instead of just gaining a constraint.

## Other notes

- `CREATE TABLE conversations (...)` is missing its trailing semicolon in both files. Some clients tolerate it, some don't.
- The `CHECK (yearly_salary > 0)` constraint is added _after_ rows with `0` and `NULL` already exist. Existing rows aren't validated retroactively in the same way new ones are, and `NULL` passes a `CHECK` because the comparison evaluates to unknown, not false. Then `INSERT INTO users VALUES ('John Doe', 0, 'unemployed')` is deliberately there to watch the constraint reject it.
- `conversations` starts with names as plain text columns, then gets refactored to `user_id` / `employer_id` foreign keys. That refactor is the point of the exercise, not an afterthought.
- In MySQL, `REFERENCES` written inline on `ADD COLUMN` is parsed but ignored by InnoDB. A real foreign key needs `ADD CONSTRAINT ... FOREIGN KEY (...) REFERENCES ...`. Postgres honours the inline form.
- The `INSERT INTO employers VALUES (...)` statements rely on column order because no column list is given. Fine for a scratch file, bad habit for anything real.

## To do

- Joins across the three tables, which is the actual reason for the foreign keys.
- Indexes and `EXPLAIN`.
- Aggregate functions and `GROUP BY`.

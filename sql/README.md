# SQL

Practice scripts for MySQL and PostgreSQL: a schema built twice so the dialect differences sit side by side, a set of CRUD drills, and a first pass at relationships and joins.

## What's here

| File              | Dialect                           | Database    | Covers                                                                             |
| ----------------- | --------------------------------- | ----------- | ---------------------------------------------------------------------------------- |
| `mysql.sql`       | MySQL                             | `talently`  | `CREATE`, `INSERT`, `ALTER TABLE`, constraints, foreign keys                       |
| `postgres.sql`    | PostgreSQL                        | `talently`  | Same as above, Postgres syntax                                                     |
| `practice.sql`    | Both (labelled per statement)     | `shop`      | `products` table, then `ALTER` for `NOT NULL`, `CHECK`, and an added primary key   |
| `crud.sql`        | MySQL (Postgres line commented)   | —           | `sales` table: filtering, date ranges, `ORDER BY` / `LIMIT`, `DISTINCT`, a `VIEW`  |
| `crud_task.sql`   | MySQL (Postgres line commented)   | —           | `products` exercise: select, filter, sort, paginate, `UPDATE`, `DELETE`            |
| `crud_task_2.sql` | PostgreSQL (MySQL line commented) | —           | `employees` exercise: same drills plus `AND` / `OR` filters                        |
| `relations.sql`   | MySQL (Postgres line commented)   | `relations` | `cities` → `addresses` → `users` with foreign keys, and a three-table `INNER JOIN` |

Where a file is "MySQL (Postgres line commented)", the only difference is the `id` column: swap `INT PRIMARY KEY AUTO_INCREMENT` for the commented `SERIAL PRIMARY KEY` to run it on Postgres.

### `talently` (mysql.sql / postgres.sql)

A small job-board database:

- `users`: name, salary, employment status
- `employers`: company name, address, revenue, hiring flag
- `conversations`: messages between a user and an employer

The scripts walk through `CREATE`, `INSERT`, `SELECT`, `DELETE`, then a series of `ALTER TABLE` statements that add primary keys, `NOT NULL`, defaults, `CHECK` constraints, and foreign keys.

### CRUD drills (crud.sql, crud_task.sql, crud_task_2.sql)

Each one creates a single table, seeds it, and then works through a list of queries:

- `WHERE` with comparisons, `<>`, `AND` / `OR`, `BETWEEN`, and `IS TRUE` / `IS FALSE` on booleans
- `ORDER BY ... ASC/DESC`, `LIMIT`, and `LIMIT ... OFFSET` for pagination
- `UPDATE` and `DELETE` with a `WHERE` clause
- `SELECT DISTINCT` and a `CREATE VIEW` that later queries select from (`crud.sql`)

### Relationships (relations.sql)

Two one-to-many links: a city has many addresses, an address has many users.

```text
cities (id, name)
  └── addresses (id, house_name, street, city_id → cities.id)
        └── users (id, first_name, last_name, email UNIQUE, address_id → addresses.id)
```

Seeds 10 cities, 10 addresses and 10 users, then joins all three to list each user with their street and city name, filtered to two cities and ordered by `u.id DESC`.

## Running

These are scripts to read and run top to bottom, not migrations. They aren't idempotent, so re-running against an existing database will fail. Drop and recreate instead.

```bash
mysql -u root -p < mysql.sql
psql -U postgres -f postgres.sql
```

For the other files, create or pick a database first and run them against it with the client for the dialect listed above. `practice.sql` has both dialects in one file, so run only the blocks for the one you're using.

## Dialect differences worth remembering

|                                  | MySQL                                                        | PostgreSQL                                                              |
| -------------------------------- | ------------------------------------------------------------ | ----------------------------------------------------------------------- |
| Enums                            | Inline: `ENUM('a','b')` on the column                        | Named type first: `CREATE TYPE ... AS ENUM (...)`                       |
| Auto-increment PK                | `INT PRIMARY KEY AUTO_INCREMENT`                             | `SERIAL PRIMARY KEY`                                                    |
| Change a column                  | `MODIFY COLUMN name TYPE ...` (restate the whole definition) | `ALTER COLUMN name SET ...` / `SET DATA TYPE ...` (change one property) |
| Set NOT NULL                     | Part of `MODIFY COLUMN`, so the type has to be repeated      | `ALTER COLUMN name SET NOT NULL` on its own                             |
| Add a CHECK during a type change | Can be inlined in `MODIFY COLUMN`                            | Needs a separate `ADD CONSTRAINT`                                       |
| Create if absent                 | `CREATE DATABASE IF NOT EXISTS`                              | No `IF NOT EXISTS` on `CREATE DATABASE` in the same form                |
| Expression default               | `DEFAULT (CURRENT_DATE)` needs the parentheses (8.0.13+)     | `DEFAULT CURRENT_DATE` works with or without them                       |
| `date - date`                    | Converts both to numbers like `20260131`, not days           | Returns an integer number of days                                       |

The MySQL `MODIFY COLUMN` requirement is the one that keeps catching me: forget to repeat the type and the column quietly changes type instead of just gaining a constraint.

## Other notes

- `CREATE TABLE conversations (...)` is missing its trailing semicolon in both `talently` files. Some clients tolerate it, some don't.
- The `CHECK (yearly_salary > 0)` constraint is added _after_ rows with `0` and `NULL` already exist. Existing rows aren't validated retroactively in the same way new ones are, and `NULL` passes a `CHECK` because the comparison evaluates to unknown, not false. Then `INSERT INTO users VALUES ('John Doe', 0, 'unemployed')` is deliberately there to watch the constraint reject it.
- `conversations` starts with names as plain text columns, then gets refactored to `user_id` / `employer_id` foreign keys. That refactor is the point of the exercise, not an afterthought.
- In MySQL, `REFERENCES` written inline on `ADD COLUMN` is parsed but ignored by InnoDB. A real foreign key needs `ADD CONSTRAINT ... FOREIGN KEY (...) REFERENCES ...`. Postgres honours the inline form. `relations.sql` uses the table-level `FOREIGN KEY (...) REFERENCES ...` form, which InnoDB does enforce.
- The `INSERT INTO employers VALUES (...)` and `INSERT INTO products VALUES (...)` statements rely on column order because no column list is given. Fine for a scratch file, bad habit for anything real. The CRUD drills and `relations.sql` list their columns.
- `crud.sql` line 516 reads `Subqueries CREATE VIEW base_result AS`. The stray `Subqueries` makes that statement a syntax error, so the view and the query after it won't run until it's removed or commented out (`-- Subqueries`).
- `crud.sql` filters with `date_fulfiled - date_created <= 2`. On Postgres that's "fulfilled within two days". On MySQL it's numeric subtraction, so it only gives the right answer when both dates are in the same month; use `DATEDIFF(date_fulfiled, date_created) <= 2` instead.
- `crud.sql` sets `date_fulfiled = NULL` for disputed sales, which is a reminder that `NULL` needs `IS NULL`, not `= NULL`, when filtering on it later.
- `practice.sql` stores `price` as `FLOAT`. The later scripts switch to `DECIMAL` / `NUMERIC`, which is the right type for money.
- `relations.sql` filters with `c.id = 5 OR c.id = 7`; `c.id IN (5, 7)` says the same thing and scales better.

## To do

- Joins across the three `talently` tables, which is the actual reason for the foreign keys there.
- `LEFT JOIN` / `RIGHT JOIN` in `relations.sql`, e.g. cities with no addresses.
- A many-to-many relationship with a junction table.
- Subqueries (started in `crud.sql`, see the note above).
- Aggregate functions and `GROUP BY`.
- Indexes and `EXPLAIN`.

# Assessment 07 — PostgreSQL: Library Database

**Date:** 2026-11-16
**Questions:** 15 · **Marks:** 1 each · no partial marks
**State:** Active. No solutions until you say **"Evaluate My Answers"**.

Every listed requirement is graded, so one missed item scores 0 for that question. Read each list to the end: requirement completeness is still your biggest weak area (#01, #04, #05, #06).

## Rules

- PostgreSQL. Use only what you've practised: CRUD, `WHERE`, `ORDER BY`, `LIMIT`/`OFFSET`, `DISTINCT`, `IS NULL`, subqueries, views, constraints, `ALTER TABLE`, `INNER`/`LEFT JOIN`, junction tables, `ON DELETE`, aggregates, and single-column `GROUP BY`.
- Not allowed: `HAVING`, CTEs (`WITH`), window functions, `COALESCE`, `CASE`.
- **Don't hardcode ids** unless a question gives you one. If a question names a member by email or a book by title, filter on that column.
- Unless a question says otherwise, every query runs against a **freshly loaded** database. Q4 and Q5 change the schema and Q13 changes data, so reload before you test the next question:
  `dropdb library_07 && createdb library_07 && psql -d library_07 -f library_setup.sql`
- Submit answers in one `ANSWERS.md` (or paste them here), one section per question number.

## Setup — `library_setup.sql`

```sql
CREATE TABLE branches (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(60) NOT NULL UNIQUE,
    city VARCHAR(40) NOT NULL
);

CREATE TABLE members (
    id             SERIAL PRIMARY KEY,
    full_name      VARCHAR(80)  NOT NULL,
    email          VARCHAR(120) NOT NULL UNIQUE,
    phone          VARCHAR(15),                                   -- optional
    home_branch_id INT REFERENCES branches ON DELETE SET NULL,    -- optional
    joined_on      DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE authors (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(80) NOT NULL UNIQUE
);

CREATE TABLE books (
    id             SERIAL PRIMARY KEY,
    isbn           CHAR(13)    NOT NULL UNIQUE,
    title          VARCHAR(120) NOT NULL,
    genre          VARCHAR(30),                                   -- optional
    published_year INT CHECK (published_year BETWEEN 1800 AND 2100),
    price          NUMERIC(6, 2) NOT NULL CHECK (price > 0)
);

-- many-to-many: a book can have several authors, an author several books
CREATE TABLE book_authors (
    book_id   INT REFERENCES books   ON DELETE CASCADE,
    author_id INT REFERENCES authors ON DELETE CASCADE,
    PRIMARY KEY (book_id, author_id)
);

CREATE TABLE loans (
    id          SERIAL PRIMARY KEY,
    book_id     INT NOT NULL REFERENCES books,                    -- no ON DELETE clause
    member_id   INT NOT NULL REFERENCES members ON DELETE CASCADE,
    loaned_on   DATE NOT NULL,
    returned_on DATE,                                             -- NULL = still out
    fine        NUMERIC(6, 2)                                     -- NULL = no fine charged
);

INSERT INTO branches (name, city) VALUES
    ('Indiranagar', 'Bengaluru'),
    ('Koramangala', 'Bengaluru'),
    ('Andheri',     'Mumbai');

INSERT INTO members (full_name, email, phone, home_branch_id, joined_on) VALUES
    ('Asha Rao',     'asha@mail.in',   '9800000001', 1,    '2025-01-10'),
    ('Vikram Shah',  'vikram@mail.in', NULL,         1,    '2025-03-02'),
    ('Neha Iyer',    'neha@mail.in',   '9800000003', 2,    '2025-06-15'),
    ('Rahul Menon',  'rahul@mail.in',  NULL,         2,    '2025-08-20'),
    ('Priya Das',    'priya@mail.in',  '9800000005', NULL, '2026-01-05'),
    ('Arjun Nair',   'arjun@mail.in',  '9800000006', 3,    '2026-02-11'),
    ('Kavya Pillai', 'kavya@mail.in',  NULL,         3,    '2026-04-01'),
    ('Sameer Khan',  'sameer@mail.in', '9800000008', NULL, '2026-09-30');

INSERT INTO authors (name) VALUES
    ('R. K. Narayan'),          -- 1
    ('Ruskin Bond'),            -- 2
    ('Amitav Ghosh'),           -- 3
    ('Sudha Murty'),            -- 4
    ('A. P. J. Abdul Kalam'),   -- 5
    ('Arun Tiwari'),            -- 6
    ('Jhumpa Lahiri');          -- 7

INSERT INTO books (isbn, title, genre, published_year, price) VALUES
    ('9780000000001', 'Malgudi Days',           'Fiction',     1943, 299.00),  -- 1
    ('9780000000002', 'The Guide',              'Fiction',     1958, 350.00),  -- 2
    ('9780000000003', 'Swami and Friends',      'Fiction',     1935, 250.00),  -- 3
    ('9780000000004', 'The Blue Umbrella',      'Children',    1980, 150.00),  -- 4
    ('9780000000005', 'Rusty Runs Away',        'Children',    2002, 199.00),  -- 5
    ('9780000000006', 'The Hungry Tide',        'Fiction',     2004, 499.00),  -- 6
    ('9780000000007', 'Wise and Otherwise',     'Non-fiction', 2002, 250.00),  -- 7
    ('9780000000008', 'Wings of Fire',          'Non-fiction', 1999, 399.00),  -- 8
    ('9780000000009', 'Gun Island',             NULL,          2019, 599.00),  -- 9
    ('9780000000010', 'The Room on the Roof',   NULL,          1956, 299.00),  -- 10
    ('9780000000011', 'Local History Pamphlet', 'Non-fiction', 2020,  99.00);  -- 11

INSERT INTO book_authors (book_id, author_id) VALUES
    (1, 1), (2, 1), (3, 1),
    (4, 2), (5, 2), (10, 2),
    (6, 3), (9, 3),
    (7, 4),
    (8, 5), (8, 6);
-- book 11 has no author listed; author 7 has no books

INSERT INTO loans (book_id, member_id, loaned_on, returned_on, fine) VALUES
    (1, 1, '2026-09-01', '2026-09-14', NULL),   -- 1
    (2, 1, '2026-10-02', '2026-10-20', 20.00),  -- 2
    (6, 2, '2026-10-05', '2026-10-28', 45.00),  -- 3
    (1, 3, '2026-10-10', '2026-10-18', NULL),   -- 4
    (4, 3, '2026-10-15', NULL,         NULL),   -- 5
    (8, 4, '2026-10-21', '2026-11-02', 10.00),  -- 6
    (2, 4, '2026-11-01', NULL,         NULL),   -- 7
    (9, 4, '2026-11-03', NULL,         NULL),   -- 8
    (7, 5, '2026-10-25', '2026-10-30', NULL),   -- 9
    (3, 5, '2026-11-05', NULL,         NULL),   -- 10
    (6, 6, '2026-11-02', '2026-11-12', 0.00),   -- 11
    (1, 7, '2026-11-08', NULL,         NULL),   -- 12
    (2, 2, '2026-09-10', '2026-09-25', 15.00),  -- 13
    (8, 6, '2026-11-10', NULL,         NULL);   -- 14
```

---

### Question 1 — Paginated catalogue

**Difficulty:** Easy · **Type:** SQL · **Marks:** 1

**Problem:** The catalogue page shows books 4 at a time, most expensive first.

**Requirements:**
1. Return `title` and `price` only.
2. Sort by `price`, highest first. Books with the same price are sorted by `title`, A to Z.
3. Return **page 2** (the 5th to 8th books in that order).

---

### Question 2 — Predict the aggregates

**Difficulty:** Easy · **Type:** Output Prediction · **Marks:** 1 (all 7 values must be right)

**Problem:** Without running it, write the value each column returns, and one line on why for each.

```sql
SELECT COUNT(*)                  AS a,
       COUNT(returned_on)        AS b,
       COUNT(fine)               AS c,
       COUNT(DISTINCT member_id) AS d,
       SUM(fine)                 AS e,
       ROUND(AVG(fine), 2)       AS f,
       MIN(fine)                 AS g
FROM loans;
```

---

### Question 3 — Debug the follow-up list

**Difficulty:** Easy · **Type:** Debugging · **Marks:** 1

**Problem:** Staff want every member who joined **on or after 1 January 2026** and is missing contact details: **either** no phone **or** no home branch (or both). This query returns 0 rows.

```sql
SELECT full_name, email
FROM members
WHERE phone = NULL
   OR home_branch_id = NULL
  AND joined_on >= '2026-01-01'
ORDER BY full_name;
```

**Requirements:**
1. List **every** bug, with a one-line reason.
2. Write the fixed query. Keep the same columns and order.

---

### Question 4 — Create the reviews table

**Difficulty:** Medium · **Type:** SQL (DDL) + Conceptual · **Marks:** 1

**Problem:** Members can review books.

**Requirements — `CREATE TABLE reviews`:**
1. `member_id`: required, refers to `members`. Deleting a member deletes their reviews.
2. `book_id`: required, refers to `books`. Deleting a book deletes its reviews.
3. `rating`: required whole number from 1 to 5 inclusive, enforced by the database.
4. `comment`: optional text, at most 500 characters.
5. `reviewed_on`: required date, filled in with today's date when an insert leaves it out.
6. A member can review the same book **only once**. Enforce this without adding a surrogate `id` column.

**Requirements — written:** Your table is empty. These four inserts run one at a time, in order. For each, say whether it succeeds or fails. If it fails, name the constraint that rejects it.

```sql
INSERT INTO reviews (member_id, book_id, rating) VALUES (1, 2, 5);                               -- (i)
INSERT INTO reviews (member_id, book_id, rating, comment) VALUES (1, 2, 4, 'Changed my mind');   -- (ii)
INSERT INTO reviews (member_id, book_id, rating) VALUES (3, 4, 0);                               -- (iii)
INSERT INTO reviews (member_id, book_id, rating) VALUES (2, 99, 3);                              -- (iv)
```

---

### Question 5 — Tighten the loans table

**Difficulty:** Medium · **Type:** SQL (DDL) + Conceptual · **Marks:** 1

**Problem:** Add rules to the **existing** `loans` table without recreating it.

**Requirements — `ALTER TABLE` statements:**
1. A constraint named `chk_returned_after_loaned`: a loan can't be returned before the day it was loaned.
2. A constraint named `chk_fine_not_negative`: a fine can't be below zero. A fine of `0.00` is allowed.
3. A new optional column `due_on` of type `DATE`.

**Requirements — written, 1–2 sentences each:**

4. (a) Loan 5 has `returned_on = NULL`. Does it break constraint 1? Why or why not?
   (b) Suppose one existing row had `loaned_on = '2026-10-15'` and `returned_on = '2026-10-01'` when you ran statement 1. What happens, and does the constraint get added?

---

### Question 6 — Books currently out

**Difficulty:** Medium · **Type:** SQL · **Marks:** 1

**Problem:** The front desk needs a list of every loan that hasn't been returned yet.

**Requirements:**
1. Columns, in this order: loan `id`, the member's `full_name`, the book's `title`, the member's home branch name as `branch_name`, and `loaned_on`.
2. Only loans that are still out.
3. **Every** such loan appears, including loans by members with no home branch. For those, `branch_name` is `NULL`.
4. Sort by `loaned_on`, oldest first, then by loan `id`.

---

### Question 7 — Unmatched records

**Difficulty:** Medium · **Type:** SQL · **Marks:** 1 (both parts)

**Requirements:**
1. **(a)** Books that have **never** been loaned. Return `title` and `isbn`, sorted by `title`. Use a `LEFT JOIN`.
2. **(b)** Members who have **no book out right now**. That includes members who've never borrowed anything, and members whose loans are all returned. Return `full_name`, sorted by `full_name`. Use either a `LEFT JOIN` or a subquery.

---

### Question 8 — Many-to-many with DISTINCT

**Difficulty:** Medium · **Type:** SQL + Conceptual · **Marks:** 1

**Problem:** The library is running an R. K. Narayan reading event and wants to invite past readers.

**Requirements:**
1. Return `full_name` and `email` of every member who has **ever** borrowed at least one book written by `'R. K. Narayan'` (returned or not).
2. Filter on the author's name. Go through `book_authors`; don't hardcode book or author ids.
3. Each member appears **once**, even if they borrowed several of his books or the same book twice.
4. Sort by `full_name`.
5. **Written:** without `DISTINCT`, how many rows would your query return, and why are there more?

---

### Question 9 — Above-average books, NULL trap

**Difficulty:** Medium · **Type:** SQL · **Marks:** 1

**Problem:** Marketing wants the books that cost more than the average price of **all** books, but not Fiction.

**Requirements:**
1. Return `title`, `genre` and `price`.
2. Price is greater than the average price of every book in `books`. Get the average with a **subquery**; don't type the number in.
3. Exclude books whose genre is `'Fiction'`. Books with **no genre** count as "not Fiction" and **must** appear if they pass rule 2.
4. Sort by `price`, highest first.

---

### Question 10 — Branch fine report

**Difficulty:** Medium · **Type:** SQL · **Marks:** 1

**Problem:** One summary row for loans that are **returned** and belong to members whose home branch is **Indiranagar**.

**Requirements:**
1. Filter on the branch **name** `'Indiranagar'`, not its id.
2. Only returned loans.
3. One row with these columns and aliases:
   - `total_fines`: the sum of fines
   - `avg_fine`: the average fine, rounded to 2 decimal places
   - `fined_loans`: the number of those loans that have a fine recorded (a `0.00` fine counts as recorded)
   - `first_loan`: the earliest `loaned_on`
   - `last_return`: the latest `returned_on`

---

### Question 11 — Books per genre

**Difficulty:** Medium · **Type:** SQL + Conceptual · **Marks:** 1

**Requirements:**
1. One row per genre with columns `genre` and `book_count` (the number of books in that genre).
2. Sort by `genre`, A to Z.
3. **Written:**
   (a) How many rows does your query return, and what does the row with an empty `genre` represent?
   (b) If you replaced `COUNT(*)` with `COUNT(genre)`, which row's count would change, and to what? Why?

---

### Question 12 — Current borrowers view

**Difficulty:** Medium · **Type:** SQL + Conceptual · **Marks:** 1

**Requirements:**
1. Create a view named `current_borrowers` with columns `id`, `full_name` and `phone` from `members`.
2. It contains every member who has **at least one book out right now**, **one row per member** (Rahul has two books out and must appear once).
3. Write a query **on the view** that returns the `full_name` of current borrowers with **no phone number**, sorted by `full_name`.
4. **Written:** Kavya returns her book with an `UPDATE` on `loans`. Without re-creating the view, does `SELECT * FROM current_borrowers` still include her? Why?

---

### Question 13 — Update and delete with subqueries

**Difficulty:** Medium · **Type:** SQL · **Marks:** 1 (both parts)

**Requirements:**
1. **(a)** The member with email `'rahul@mail.in'` returns **every book he currently has out** on `'2026-11-16'`. Write one `UPDATE`:
   - find the member by email with a subquery (no hardcoded member id)
   - set `returned_on` for his open loans only. His already-returned loan must keep its original `returned_on`.
   - write the number of rows it updates
2. **(b)** Remove members who have **no home branch** and have **never borrowed a book**. Write one `DELETE`:
   - no hardcoded ids or emails
   - write the number of rows it deletes and the name(s) of the member(s) removed

---

### Question 14 — Predict the ON DELETE effects

**Difficulty:** Challenging · **Type:** Output Prediction + Conceptual · **Marks:** 1 (everything must be right)

**Problem:** On a freshly loaded database, these four statements run **one at a time**, in order. Each runs on its own (autocommit), so if one fails, the others still run.

```sql
DELETE FROM branches WHERE name = 'Koramangala';   -- (1)
DELETE FROM members  WHERE email = 'vikram@mail.in'; -- (2)
DELETE FROM books    WHERE title = 'Malgudi Days'; -- (3)
DELETE FROM authors  WHERE name = 'Ruskin Bond';   -- (4)
```

**Requirements:**
1. For each statement, one line: does it succeed or fail? What happens to rows in **other** tables, and which part of the schema causes it?
2. After all four, give the result of each count:

| # | Count |
|---|---|
| a | rows in `branches` |
| b | rows in `members` |
| c | members with `home_branch_id IS NULL` |
| d | rows in `loans` |
| e | loans with `returned_on IS NULL` |
| f | rows in `books` |
| g | rows in `book_authors` |
| h | rows in `authors` |

---

### Question 15 — Debug a schema script

**Difficulty:** Challenging · **Type:** Debugging (DDL) · **Marks:** 1

**Problem:** A colleague wrote this script for staff and their skills. It doesn't run, and even the parts that do run break the requirements.

```sql
CREATE TABLE staff (
    id            INT PRIMARY KEY,
    employee_code VARCHAR(10),
    full_name     VARCHAR(80) NOT NULL,
    branch_id     SERIAL REFERENCES branches(id),
    manager_id    INT REFERENCES staff ON DELETE CASCADE,
    hourly_rate   NUMERIC(6, 2) CHECK (hourly_rate > 0) DEFAULT 0,
    joined_on     DATE DEFAULT CURRENT_DATE
);

CREATE TABLE staff_skills (
    id         SERIAL PRIMARY KEY,
    staff_code VARCHAR(10) REFERENCES staff(employee_code),
    skill      VARCHAR(40) NOT NULL
);
```

**Requirements the tables must meet:**

`staff`:
1. `id` is generated by the database on insert.
2. `employee_code` is required, at most 10 characters, and no two staff share one.
3. `full_name` is required.
4. `branch_id` is required and refers to `branches`. A branch that still has staff **can't be deleted**. The value is always supplied by the insert; the database must never make one up.
5. `manager_id` is optional and refers to another row in `staff`. When a manager is deleted, the people they managed **stay**, with `manager_id` cleared.
6. `hourly_rate` is required, must be greater than 0, and defaults to `250.00`.
7. `joined_on` defaults to today.

`staff_skills`:

8. Each row links a staff member, **by `employee_code`**, to a skill.
9. Both `staff_code` and `skill` are required.
10. The same skill can't be listed twice for the same staff member.
11. Deleting a staff member deletes their skills.

**Answer with:**
1. **Every** bug, with a one-line reason. Include the error message the original script gives and which line causes it.
2. The corrected script. It must run on the setup database.

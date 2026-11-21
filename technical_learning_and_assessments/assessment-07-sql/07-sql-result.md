# Assessment 07 — PostgreSQL Library Database — Evaluation

**Date evaluated:** 2026-11-21 · **Submission:** one `.sql` file with answers for Q1–Q13 and Q15
**What was run:** I loaded `library_setup.sql` fresh on PostgreSQL 16 before each answer and ran every submitted statement. I also ran extra checks on Q5, Q10 and Q13b, which are shown below. Written answers were read, not run.

## A. Overall Results

| Metric | Result |
|---|---|
| Total Questions | 15 |
| Correct Answers | 4 |
| Incorrect Answers | 10 |
| Unanswered | 1 |
| Final Score | 4/15 |
| Percentage | 27% |

**The main finding:** your SQL is much stronger than 27% suggests. In **Q4, Q8 and Q15 the SQL was fully correct**, and the mark was lost only on the written part. Q2 has no predictions. Counting just whether the code met the requirements, you got about 8 of 14 right. Requirement completeness has now cost marks in **five assessments in a row**.

## B. Question-Wise Scorecard

| Q | Topic | Result | Marks | Lost on |
|---|---|---|---|---|
| 1 | Pagination | Correct | 1 | — |
| 2 | Aggregate output prediction | Incorrect (no predictions) | 0 | the whole task |
| 3 | Debug NULL filter + AND/OR | Correct | 1 | — |
| 4 | CREATE TABLE reviews | Incorrect | 0 | (i) not answered, missing `;` |
| 5 | ALTER TABLE constraints | Incorrect | 0 | `>` instead of `>=`, 4a reason, 4b incomplete |
| 6 | Current loans join | Incorrect | 0 | `DESC` instead of oldest first |
| 7 | Unmatched records | Correct | 1 | — |
| 8 | Many-to-many + DISTINCT | Incorrect | 0 | written part: no row count |
| 9 | Subquery + NULL trap | Correct | 1 | — |
| 10 | Branch fine report | Incorrect | 0 | no "returned only" filter |
| 11 | GROUP BY genre | Incorrect | 0 | `COUNT(genre)` → NULL group shows 0 |
| 12 | View with DISTINCT | Incorrect | 0 | LEFT JOIN, no `id`, no phone filter, no written answer |
| 13 | UPDATE / DELETE with subqueries | Incorrect | 0 | (b) deletes the wrong members |
| 14 | ON DELETE prediction | Unanswered | 0 | — |
| 15 | Debug schema script | Incorrect | 0 | no bug list (the script itself is correct) |

## C. Detailed Evaluation

### Q1 — Paginated catalogue — Correct (1/1)
**Your answer:** `ORDER BY price DESC, title ASC OFFSET 4 LIMIT 4`
**Why it works:** The `title` tie-breaker makes the order stable. It returned Malgudi Days, The Room on the Roof, Swami and Friends, and Wise and Otherwise, which is right. PostgreSQL accepts `OFFSET` before `LIMIT`, but `LIMIT 4 OFFSET 4` is the usual order and is easier to read.

### Q2 — Predict the aggregates — Incorrect (0/1)
**Your answer:** the query copied out again, with the aliases' case changed. No values and no reasons.
**Mistake:** The question asked you to predict each value *without running it* and to explain why. Nothing that was asked for was submitted.
**Correct answer:**

| Col | Value | Why |
|---|---|---|
| a | 14 | `COUNT(*)` counts every row |
| b | 8 | `COUNT(returned_on)` skips the 6 open loans, where it's NULL |
| c | 5 | `COUNT(fine)` skips NULL fines. The `0.00` fine is a value, so it's counted |
| d | 7 | members 1–7 have loans. Member 8 has none |
| e | 90.00 | 20 + 45 + 10 + 0 + 15 |
| f | 18.00 | `AVG` divides by the 5 non-NULL fines (90 / 5), not by 14 |
| g | 0.00 | `MIN` ignores NULLs, and 0.00 is a real value |

**Improvement:** an output-prediction question is graded on the values. Trace the rows by hand first, then check your answer by running the query.

### Q3 — Debug the follow-up list — Correct (1/1)
**Why it works:** You found both bugs. `= NULL` is never true, so you need `IS NULL`. And `AND` binds tighter than `OR`, so the `OR` group needs parentheses. It returned Kavya, Priya and Sameer, which is right.

### Q4 — Create the reviews table — Incorrect (0/1)
**What's right:** the table meets all six requirements. `NOT NULL` FKs with `CASCADE`, `CHECK (rating > 0 AND rating <= 5)` (correct for `INT`), `VARCHAR(500)`, `DEFAULT CURRENT_DATE`, and a composite PK. Your constraint names for (ii)–(iv) are the ones PostgreSQL generates.
**Mistakes:**
1. You didn't answer **(i)**. The question said "for each, say whether it succeeds or fails", and you only listed the three failures.
2. There's no `;` after the `CREATE TABLE`. When I ran your file, PostgreSQL gave `syntax error at or near "INSERT"`, so the table was never created and every insert after it failed with `relation "reviews" does not exist`.

**Correct written answer:** (i) **succeeds**, and `reviewed_on` is filled in with today's date. (ii) fails on `reviews_pkey` because (1, 2) already exists. (iii) fails on `reviews_rating_check`. (iv) fails on `reviews_book_id_fkey` because book 99 doesn't exist.
**Improvement:** answer every listed item, including the one that seems obvious. End every statement with `;`.

### Q5 — Tighten the loans table — Incorrect (0/1)
**Mistakes:**
1. `CHECK (returned_on > loaned_on)` rejects a **same-day return**. The requirement was "can't be returned *before* the day it was loaned", so returning on the same day must be allowed. I tested it: inserting `loaned_on = returned_on = '2026-11-20'` failed with `violates check constraint "chk_returned_after_loaned"`.
2. **4a:** the answer ("no") is right, but the reason isn't. `NULL >= '2026-10-15'` is neither true nor false; it's **unknown (NULL)**. A `CHECK` rejects a row only when the result is *false*, so a NULL result passes.
3. **4b:** you said it errors, but you didn't answer whether the constraint gets added.

**Correct solution:**
```sql
ALTER TABLE loans ADD CONSTRAINT chk_returned_after_loaned CHECK (returned_on >= loaned_on);
ALTER TABLE loans ADD CONSTRAINT chk_fine_not_negative CHECK (fine >= 0);
ALTER TABLE loans ADD COLUMN due_on DATE;
```
- 4a: The comparison with NULL gives NULL (unknown), and CHECK only rejects *false*, so loan 5 passes.
- 4b: `ALTER TABLE` checks every existing row first. If one row fails, the statement errors and **the constraint isn't added**. You have to fix the bad row first.

**Improvement:** turn "not before" into `>=` and "after" into `>`. Read the boundary words in the requirement carefully.

### Q6 — Books currently out — Incorrect (0/1)
**What's right:** `LEFT JOIN branches` keeps Priya's loan with `branch_name` NULL. This was the main point of the question, and you got it right: all 6 rows are there.
**Mistake:** `ORDER BY l.loaned_on DESC` lists the newest first. The requirement was "oldest first". Your output starts with loan 14; the correct output starts with loan 5.
**Correct solution:** `ORDER BY l.loaned_on ASC, l.id ASC;` (`ASC` is the default).
**Improvement:** this was the same kind of slip as in #06: almost everything right, one detail wrong. Compare your output's first and last rows against the requirement before you submit.

### Q7 — Unmatched records — Correct (1/1)
**Why it works:** (a) `LEFT JOIN … WHERE l.book_id IS NULL` works because `book_id` is `NOT NULL` in `loans`, so it can only be NULL when no loan matched. It returned the 3 never-loaned books. (b) Putting `l.returned_on IS NULL` **in the `ON` clause** is the key step. It matches only open loans, so members with no open loan end up with NULLs and are kept. It returned Asha, Sameer and Vikram, which is right. Well done: this is the hardest unmatched-records pattern.

### Q8 — Many-to-many + DISTINCT — Incorrect (0/1)
**What's right:** the query is correct and returned the right 6 members. The author subquery filters on the name with no hardcoded ids, and `DISTINCT` removes duplicates. Joining `books` isn't needed (`ba.book_id = l.book_id` is enough), but it does no harm.
**Mistake:** written part 5 asked *how many* rows the query returns without `DISTINCT`. You didn't give a number, and "one row per matching record" doesn't say what's duplicated.
**Correct answer:** **7 rows**. The join gives one row per *loan* of a Narayan book (loans 1, 2, 4, 7, 10, 12, 13). Asha borrowed two of his books (loans 1 and 2), so she appears twice. With 6 members and 7 loans, there's one duplicate.
**Improvement:** when a question asks "how many", answer with a number.

### Q9 — Above-average books — Correct (1/1)
**Why it works:** The subquery average is 308.45. `(genre != 'Fiction' OR genre IS NULL)` keeps Gun Island, whose genre is NULL; `!=` alone would have dropped it. It returned Gun Island and Wings of Fire, which is right. Last time NULL handling was a weak area; this time you handled it correctly.

### Q10 — Branch fine report — Incorrect (0/1)
**Mistake:** there's no `l.returned_on IS NOT NULL` filter. Requirement 2 was "only returned loans". Your output matches the expected numbers **only because every Indiranagar loan in the seed data happens to be returned**. I tested it: after adding one open Indiranagar loan from 2026-08-01, your query reported `first_loan = 2026-08-01`, which is wrong.
**Also:** `LEFT JOIN members` followed by `INNER JOIN branches` behaves as an inner join anyway. Use `INNER JOIN` for both so the query says what it does.
**Correct solution:**
```sql
SELECT SUM(l.fine)           AS total_fines,
       ROUND(AVG(l.fine), 2) AS avg_fine,
       COUNT(l.fine)         AS fined_loans,
       MIN(l.loaned_on)      AS first_loan,
       MAX(l.returned_on)    AS last_return
FROM loans AS l
    INNER JOIN members  AS m ON l.member_id = m.id
    INNER JOIN branches AS b ON m.home_branch_id = b.id
WHERE b.name = 'Indiranagar'
  AND l.returned_on IS NOT NULL;
```
**Improvement:** a query that gives the right output on one dataset can still be wrong. Write each requirement as a condition in the query, even when the current data doesn't need it.

### Q11 — Books per genre — Incorrect (0/1)
**Mistake:** `COUNT(genre)` gives **0** for the NULL group, but the requirement was the number of books in each genre, which is **2** for the books with no genre. Your 11b answer shows you know why (`COUNT(column)` skips NULLs), but you used the version that skips them. 11a is fine.
**Correct solution:**
```sql
SELECT genre, COUNT(*) AS book_count
FROM books
GROUP BY genre
ORDER BY genre;
```
11b: replacing `COUNT(*)` with `COUNT(genre)` changes the NULL row from 2 to 0, because `COUNT(genre)` counts only non-NULL values, and every value in that group is NULL.
**Improvement:** use `COUNT(*)` to count rows, and `COUNT(column)` to count rows where that column has a value.

### Q12 — Current borrowers view — Incorrect (0/1)
**Mistakes:**
1. **`LEFT JOIN` + `WHERE l.returned_on IS NULL` includes Sameer**, who has never borrowed anything. A member with no loans gets `l.returned_on = NULL` from the LEFT JOIN, so they pass the filter. Your view returned 6 people; it should return 5. You need an `INNER JOIN` here, because you *want* only members who have a loan.
2. The view has no `id` column (requirement 1).
3. The query on the view has no `WHERE phone IS NULL` (requirement 3).
4. You didn't answer the written part (4).

**Correct solution:**
```sql
CREATE VIEW current_borrowers AS
SELECT DISTINCT m.id, m.full_name, m.phone
FROM members AS m
    INNER JOIN loans AS l ON l.member_id = m.id
WHERE l.returned_on IS NULL;

SELECT full_name
FROM current_borrowers
WHERE phone IS NULL
ORDER BY full_name;      -- Kavya Pillai, Rahul Menon
```
4: **No**, she drops out. A view stores the query, not the result, so each `SELECT` runs it again on the current data.
**Why it was wrong:** In Q7b you used `LEFT JOIN … IS NULL` correctly to *find* unmatched rows. Here the same pattern *added* an unmatched row where you didn't want one. With a LEFT JOIN, a NULL in the right-hand table can mean "this column is NULL" or "there was no match".
**Improvement:** use a LEFT JOIN only when you want to keep rows that have no match.

### Q13 — UPDATE / DELETE with subqueries — Incorrect (0/1)
**(a) Correct:** finding the member by email with `IN (subquery)` and filtering `returned_on IS NULL` updated 2 rows and left loan 6 alone. (`=` would also work here, because `email` is UNIQUE.)
**(b) Wrong:**
1. `OR` should be `AND`. The requirement was no home branch **and** never borrowed.
2. `id IN (SELECT member_id FROM loans WHERE member_id IS NULL)` can never match. `member_id` is `NOT NULL`, so the subquery returns no rows. "Never borrowed" means `id NOT IN (SELECT member_id FROM loans)`.
3. Because of this, **Priya was deleted**, and `ON DELETE CASCADE` also deleted her 2 loans (I checked: loans went from 14 to 12). Your own answer said Priya would be deleted, even though she has borrowed books. A quick check against the data would have caught this.

**Correct solution:**
```sql
DELETE FROM members
WHERE home_branch_id IS NULL
  AND id NOT IN (SELECT member_id FROM loans);
-- DELETE 1 — Sameer Khan
```
**Improvement:** before any `DELETE`, run the same `WHERE` as a `SELECT` and check every row it returns.

### Q14 — ON DELETE prediction — Unanswered (0/1)
**Correct answer:**
1. **Succeeds.** Members 3 and 4 get `home_branch_id = NULL` because of `members.home_branch_id … ON DELETE SET NULL`.
2. **Succeeds.** Vikram's loans 3 and 13 are deleted because of `loans.member_id … ON DELETE CASCADE`.
3. **Fails:** `violates foreign key constraint "loans_book_id_fkey"`. `loans.book_id` has **no ON DELETE clause**, so the default (NO ACTION) blocks deleting a book that loans 1, 4 and 12 still refer to. Nothing is deleted, not even its `book_authors` row.
4. **Succeeds.** The `book_authors` rows for books 4, 5 and 10 are deleted because of `book_authors.author_id … ON DELETE CASCADE`. The books themselves stay.

| a | b | c | d | e | f | g | h |
|---|---|---|---|---|---|---|---|
| 2 | 7 | 4 | 12 | 6 | 11 | 8 | 6 |

**Improvement:** this is the 4th assessment where ON DELETE has cost marks (#03, #04, #06, #07). For every FK, say out loud what it does: CASCADE, SET NULL, or **no clause = blocked**.

### Q15 — Debug a schema script — Incorrect (0/1)
**What's right:** your corrected script runs, and I checked it against all 11 requirements. Keeping a surrogate `id` plus `UNIQUE(staff_code, skill)` is a valid alternative to a composite PK, and `ON DELETE RESTRICT` meets "a branch with staff can't be deleted".
**Mistake:** "Answer with" item 1, **the bug list with the error message and the line that causes it**, is missing entirely. Half the question wasn't submitted.
**Correct bug list:**
1. `id INT PRIMARY KEY` isn't generated by the database. Use `SERIAL`.
2. `employee_code` has no `NOT NULL`.
3. `employee_code` has no `UNIQUE`. This causes the script error: `there is no unique constraint matching given keys for referenced table "staff"` on the `staff_skills.staff_code REFERENCES staff(employee_code)` line. A FK must refer to a PK or UNIQUE column.
4. `branch_id SERIAL` makes the database generate values for a foreign key. It should be `INT NOT NULL`.
5. `manager_id … ON DELETE CASCADE` deletes the people a manager managed. It should be `SET NULL`.
6. `hourly_rate … DEFAULT 0` breaks its own `CHECK (> 0)`, so any insert that leaves it out fails. The default should be `250.00`.
7. `hourly_rate` has no `NOT NULL`, so NULL would pass the CHECK.
8. `staff_skills` allows the same (staff, skill) pair twice. It needs a composite PK or `UNIQUE`.
9. `staff_code` has no `NOT NULL`.
10. `staff_code` has no `ON DELETE CASCADE`.

**Improvement:** you fixed every bug in code, so you clearly found them. Writing them down was the missing step.

## D. Topic-Wise Performance

| Topic | Questions | Correct | Accuracy |
|---|---|---|---|
| SELECT, filtering, pagination, NULL | Q1, Q3, Q9 | 3 | 100% |
| JOINs and unmatched records | Q6, Q7, Q8 | 1 | 33% |
| Aggregates and GROUP BY | Q2, Q10, Q11 | 0 | 0% |
| Views | Q12 | 0 | 0% |
| DML (UPDATE / DELETE) | Q13 | 0 | 0% |
| DDL and constraints | Q4, Q5, Q15 | 0 | 0% |
| ON DELETE behaviour | Q14 | 0 | 0% (unanswered) |

**Progress:** #03 PostgreSQL scored 7/12 (58%); #07 scored 4/15 (27%). #07 covered much more (aggregates, views, DDL debugging, ON DELETE prediction), and 4 of its 11 lost marks came from the written parts alone.

## E. Learning Gap Analysis

**Strong:** `IS NULL` and AND/OR precedence (Q3); `LEFT JOIN … IS NULL`, including an extra condition in the `ON` clause (Q7b); NULL-safe filters (Q9); many-to-many joins with `DISTINCT` (Q8); stable pagination (Q1); constraint syntax (Q4 and Q15 code); UPDATE with a subquery (Q13a). You also know how `COUNT(column)` treats NULLs (Q11b).

**Weak:**
- **Requirement completeness, 5th assessment in a row.** This time it was mostly written parts: Q2 (none), Q4 (i), Q5 4b, Q8 count, Q12 part 4, Q15 bug list, and Q14 skipped.
- **Prediction questions:** Q2 had no predictions and Q14 was skipped. HTTP prediction was also 0 in #04 and #06. You haven't scored on a prediction question since tracking started.
- **ON DELETE:** a recurring weak area (#03, #04, #06, #07), and the default NO ACTION behaviour has never been tested correctly.
- **LEFT JOIN when you need an INNER JOIN** (Q12), and a mixed LEFT/INNER chain (Q10).
- **Boundary conditions:** `>` vs `>=` (Q5), DESC vs oldest first (Q6), `OR` vs `AND` (Q13b).
- **Missing filters that the data happened not to need** (Q10).
- **`COUNT(*)` vs `COUNT(column)` in practice** (Q11).

**Repeated mistakes:** skipped sub-requirements (#01, #04, #05, #06, #07), predictions left blank (#04, #06, #07), ON DELETE explanations (#03, #04, #06, #07).

## F. Recommended Practice (no solutions)

1. **Predict first, then run.** On the library database, write down the result of each statement before running it: `SELECT COUNT(phone), COUNT(DISTINCT home_branch_id) FROM members;`, `DELETE FROM authors WHERE name = 'Amitav Ghosh';` (and the `book_authors` count afterwards), and `DELETE FROM books WHERE title = 'Gun Island';`. Then run each one, and for every wrong prediction write one line on why.
2. **LEFT vs INNER.** Write two queries: (a) every author with the title of each of their books, where authors with no books still appear with a NULL title; (b) only authors with at least one book that has been loaned, one row per author. Before running, say which join each needs and how many rows you expect.
3. **Requirement checklist.** Redo Q4, Q8, Q12 and Q15 in full. Number every requirement and every "written" item, and tick each one only after it's answered in your file.

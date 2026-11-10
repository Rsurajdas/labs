# SQL Assessment 1: Evaluation Report

## A. Overall Results

| Metric            | Result |
| ----------------- | ------ |
| Total Questions   | 12     |
| Correct Answers   | 7      |
| Incorrect Answers | 5      |
| Unanswered        | 0      |
| Final Score       | 7 / 12 |
| Percentage        | 58.33% |

## B. Question-by-Question Results

| Question | Topic                        | Result                 | Marks |
| -------- | ---------------------------- | ---------------------- | ----- |
| Q1       | Constraints and FKs          | Incorrect              | 0     |
| Q2       | INSERT with subquery         | Correct                | 1     |
| Q3       | Filtering and sorting        | Correct                | 1     |
| Q4       | UPDATE with NULL handling    | Correct                | 1     |
| Q5       | Multi-table INNER JOIN       | Correct                | 1     |
| Q6       | LEFT JOIN output             | Correct                | 1     |
| Q7       | Unmatched records            | Incorrect              | 0     |
| Q8       | Debugging                    | Incorrect (incomplete) | 0     |
| Q9       | Many-to-many JOIN            | Correct                | 1     |
| Q10      | Top-N with LEFT JOIN         | Correct                | 1     |
| Q11      | Views and DISTINCT           | Incorrect              | 0     |
| Q12      | DELETE and cascading effects | Incorrect (incomplete) | 0     |

---

## C. Detailed Evaluation

### Q1: Constraints and Foreign Keys

**Question:** (a) Which constraint on `employees.email` allows it to be referenced, and why does PostgreSQL require it? (b) Why must `teams.building_id` and `employees.team_id` be nullable for their `ON DELETE` rules to work?

**My Answer:**

```
a) The UNIQUE constraint on `employees.email` ensures that each email address is unique. A foreign key constraint requires the referenced column in the parent table to have a UNIQUE or PRIMARY KEY constraint.
b) I am aware that this approach will allow team records to exist without a `building_id` and employee records to exist without a `team_id`. I would have opted for the RESTRICT constraint, which allows a building or team record to be deleted only after all its related records have been removed.
```

**Result:** Incorrect | **Marks:** 0/1

**Mistake:** Part (a) is correct. Part (b) gives a design opinion but doesn't answer the question. It never explains the link between `ON DELETE SET NULL` and the column being nullable.

**Correct Solution:**

- (a) `UNIQUE`. A foreign key must point to a column whose values are guaranteed unique, so every child row maps to exactly one parent row.
- (b) `ON DELETE SET NULL` works by writing `NULL` into the child's foreign key column when the parent row is deleted. If that column were `NOT NULL`, writing `NULL` would violate the constraint, and PostgreSQL would reject the `DELETE` with an error. Being nullable is what lets the rule run at all.

**Explanation:** Your RESTRICT suggestion is a valid design choice, and a good one in many systems. In an assessment, though, answer what the question asks before offering alternatives.

**Improvement:** For every `ON DELETE` rule, ask: "What value ends up in the child column, and does the column's constraint allow it?"

---

### Q2: INSERT with Subquery

**My Answer:**

```sql
INSERT INTO employees (first_name, last_name, brithdate, email, team_id)
VALUES ('Sneha', 'Kulkarni', '1997-03-18', 'sneha@co.com',
        (SELECT id FROM teams WHERE team_name = 'QA'));
```

**Result:** Correct | **Marks:** 1/1

**Explanation:** The scalar subquery returns the QA team's id (3), and the column list matches the values in order. `SERIAL` generates the `id` automatically.

---

### Q3: Filtering and Sorting

**My Answer:**

```sql
SELECT first_name, last_name, email
FROM employees
WHERE brithdate >= '1990-01-01'
ORDER BY brithdate ASC;
```

**Result:** Correct | **Marks:** 1/1

**Explanation:** `>=` correctly includes 1 January 1990, and `ASC` on a date puts the oldest employee first. You don't need to select a column to sort by it.

---

### Q4: UPDATE with NULL Handling

**My Answer:**

```sql
UPDATE employees
SET team_id = (SELECT id FROM teams WHERE team_name = 'DevOps')
WHERE team_id IS NULL;
```

**Result:** Correct | **Marks:** 1/1

**Explanation:** You correctly used `IS NULL` rather than `= NULL`, and the subquery avoids hardcoding the id. Only Priya is updated.

---

### Q5: Multi-Table INNER JOIN

**My Answer:**

```sql
SELECT e.first_name, e.last_name, t.team_name, b.building_name
FROM employees AS e
    INNER JOIN teams AS t ON e.team_id = t.id
    INNER JOIN buildings AS b ON t.building_id = b.id
ORDER BY b.building_name ASC, e.first_name ASC;
```

**Result:** Correct | **Marks:** 1/1

**Explanation:** The two `INNER JOIN`s together drop employees with no team (Priya) and teams with no building (DevOps → Arjun). This meets the "both a team and a building" requirement. The result is Asha, Neha, and Vikram (Alpha Tower), then Rohan (Beta Block).

---

### Q6: LEFT JOIN Output

**My Answer:** Frontend/Alpha Tower, Backend/Alpha Tower, QA/Beta Block, DevOps/null; "Gamma House will not appear in the results because it is not associated with any team."

**Result:** Correct | **Marks:** 1/1

**Explanation:** All four rows are correct, in the right order, with `NULL` for DevOps. Your reasoning is also right. To make it more precise: a `LEFT JOIN` keeps every row from the **left** table (`teams`). A building that no team points to has nothing to attach to, so it is dropped.

---

### Q7: Unmatched Records

**Question:** Using a `LEFT JOIN`, return the `title` and `deadline` of projects with no employees assigned.

**My Answer:**

```sql
SELECT p.title
FROM projects_employees AS pe
    LEFT JOIN projects AS p ON pe.project_id = p.id
WHERE pe.employee_id IS NULL;
```

**Result:** Incorrect | **Marks:** 0/1

**Mistake:** The JOIN is reversed, and the `deadline` column is missing.

- **JOIN error:** `projects_employees` is the left table, so the query starts only from projects that _are_ assigned. Audit Portal has no row in that table, so it can never appear.
- **Logic error:** Every row in `projects_employees` has an `employee_id`, so `pe.employee_id IS NULL` is never true. The query returns **0 rows**.

**Correct Solution:**

```sql
SELECT p.title, p.deadline
FROM projects AS p
    LEFT JOIN projects_employees AS pe ON p.id = pe.project_id
WHERE pe.id IS NULL;
```

Result: `Audit Portal | 2026-10-30`

**Explanation:** To find "A with no B", put **A** on the left and check a column from **B** for `NULL`. The `LEFT JOIN` keeps every project. Projects with no match get `NULL` in every `pe` column, and the `WHERE` keeps only those rows.

**Improvement:** Before writing the query, say the pattern out loud: "keep all _projects_, find those with no _assignment_". The table you want to keep all of goes in `FROM`.

---

### Q8: Debugging

**Question:** Identify every mistake, explain why each one gives the wrong result, and write the corrected query.

**My Answer:**

```
The `LEFT JOIN` should use `employees.email` instead of `employees.id`. Additionally, the filtering condition is incorrect; it should be `WHERE ia.email IS NULL`.
```

**Result:** Incorrect (incomplete) | **Marks:** 0/1

**Mistake:** You found both bugs correctly, which is the hardest part. However, two of the three requirements are missing: you didn't explain _why_ each bug causes the wrong result, and you didn't write the corrected query.

**Correct Solution:**

```sql
SELECT e.first_name, e.email
FROM employees e
    LEFT JOIN internet_accounts ia ON e.email = ia.email
WHERE ia.email IS NULL;
```

Result: Neha, Priya, Arjun.

**Explanation:**

- **Wrong JOIN condition:** `e.id = ia.id` compares two separate `SERIAL` counters that have nothing to do with each other. Employee 3 (Neha) gets matched to account 3, which belongs to Rohan. The real relationship is through `email`.
- **NULL comparison:** `= NULL` evaluates to unknown, never true, so the `WHERE` filters out every row. That is why the query returned nothing. Only `IS NULL` tests for missing values.

**Improvement:** For debugging questions, use a fixed checklist: _bug → effect → fixed code_.

---

### Q9: Many-to-Many JOIN

**My Answer:**

```sql
SELECT e.first_name, e.last_name, p.title, p.deadline
FROM projects_employees AS pe
    INNER JOIN employees AS e ON pe.employee_id = e.id
    INNER JOIN projects AS p ON pe.project_id = p.id
WHERE p.title = 'Payments Revamp';
```

**Result:** Correct | **Marks:** 1/1

**Explanation:** Starting from the junction table and joining out to both sides is the standard pattern. It returns Asha and Vikram.

---

### Q10: Top-N with LEFT JOIN

**My Answer:**

```sql
SELECT e.first_name, e.last_name, e.brithdate, t.team_name
FROM employees AS e
    LEFT JOIN teams AS t ON e.team_id = t.id
ORDER BY e.brithdate DESC
LIMIT 3;
```

**Result:** Correct | **Marks:** 1/1

**Explanation:** `DESC` on the birthdate puts the youngest first, and the `LEFT JOIN` keeps Priya, who has no team. The result is Priya (NULL), Neha (Backend), Rohan (QA). Notice that you put `employees` on the left here, which is exactly the direction Q7 needed.

---

### Q11: Views and DISTINCT

**Question:** (a) Create `employee_projects_view`. (b) Return the **distinct** emails of employees with a deadline before `2027-01-01`, sorted alphabetically.

**My Answer:**

```sql
CREATE VIEW employee_projects_view AS
SELECT e.first_name, e.last_name, e.email, p.title, p.deadline
FROM projects_employees AS pe
    INNER JOIN employees AS e ON pe.employee_id = e.id
    INNER JOIN projects AS p ON pe.project_id = p.id;

SELECT email
FROM employee_projects_view
WHERE deadline < '2027-01-01'
ORDER BY email ASC;
```

**Result:** Incorrect | **Marks:** 0/1

**Mistake:** Part (a) is correct. Part (b) is missing `DISTINCT`, which the question explicitly required.

**Correct Solution:**

```sql
SELECT DISTINCT email
FROM employee_projects_view
WHERE deadline < '2027-01-01'
ORDER BY email ASC;
```

**Explanation:** The view has one row per employee–project assignment. An employee on two qualifying projects would appear twice. In this sample data, your query happens to return the same four emails, because Asha's second project is due in 2027. Add one more assignment, such as Asha on Mobile App, and your query returns `asha@co.com` twice. A query has to be correct for every valid dataset, not only the sample.

**Improvement:** Whenever you query a view or JOIN that has one row per relationship, check whether the same entity can appear more than once.

---

### Q12: DELETE and Cascading Effects

**Question:** (a) Write both `DELETE` statements. (b) Describe exactly which rows in other tables are affected, and whether each is **updated or deleted**.

**My Answer:**

```sql
DELETE FROM buildings WHERE building_name = 'Alpha Tower';
DELETE FROM employees WHERE email = 'vikram@co.com';
```

```
In the `teams` table, the Frontend and Backend rows are affected. Additionally, the second row in both the `internet_accounts` and `projects_employees` tables is deleted due to the `ON DELETE CASCADE` constraint.
```

**Result:** Incorrect (incomplete) | **Marks:** 0/1

**Mistake:** Part (a) is correct, and the cascade analysis for Vikram is correct. For Alpha Tower, though, you said Frontend and Backend are "affected" without saying how, and the question specifically asked whether each row is updated or deleted. This is the same gap as Q1(b): the behaviour of `SET NULL`.

**Correct Solution:**

- **Delete Alpha Tower** → `teams` rows Frontend (id 1) and Backend (id 2) are **updated**, and their `building_id` becomes `NULL`. Both teams still exist. `employees` is not affected, because Asha, Vikram, and Neha still point to teams that exist.
- **Delete Vikram** → the `internet_accounts` row for `vikram@co.com` is **deleted** (CASCADE on email). The `projects_employees` row (employee 2, project 1) is **deleted** (CASCADE on employee_id). `projects` and `teams` are untouched.

**Explanation:** `SET NULL` **keeps** the child row and clears the reference. `CASCADE` **removes** the child row. The deletes only reach tables that hold a foreign key pointing _to_ the deleted row.

---

## D. Topic-Wise Performance

All questions were SQL. Here is the breakdown by sub-topic:

| Sub-topic                                | Correct | Total  | Accuracy   |
| ---------------------------------------- | ------- | ------ | ---------- |
| INSERT / UPDATE / DELETE statements      | 3       | 3      | 100%       |
| Filtering, sorting, Top-N                | 2       | 2      | 100%       |
| INNER JOIN / many-to-many                | 2       | 2      | 100%       |
| LEFT JOIN (output and unmatched records) | 1       | 2      | 50%        |
| NULL handling (debugging)                | 0       | 1      | 0%         |
| Views and DISTINCT                       | 0       | 1      | 0%         |
| Constraints and `ON DELETE` behaviour    | 0       | 2      | 0%         |
| **SQL total**                            | **7**   | **12** | **58.33%** |

Note: Q12 is counted under constraints, since part (b) is what lost the mark, even though its `DELETE` statements were correct.

---

## E. Improvement Recommendations

**Your strengths:** Your query writing is solid. All INSERT, UPDATE, DELETE, INNER JOIN, and Top-N queries were correct. You also used subqueries and `IS NULL` correctly whenever you wrote full SQL.

**Weak concepts:**

1. **`ON DELETE SET NULL` vs `CASCADE`.** You missed this twice (Q1b, Q12b). Learn exactly what each rule does to the child row, and why `SET NULL` needs a nullable column.
2. **LEFT JOIN direction for unmatched records (Q7).** You chose the right direction in Q10 but the wrong one in Q7. The rule: the table you want _all rows_ from goes in `FROM`.
3. **Duplicates in JOIN results (Q11).** Watch for duplicates whenever a one-to-many or many-to-many relationship is involved.

**A pattern to fix:** Three of your five lost marks (Q8, Q11, Q12) came from **not completing every stated requirement**, not from a lack of knowledge. Before submitting, re-read the Requirements list and tick off each item.

### Practice Exercises (no solutions)

**Exercise 1: ON DELETE behaviour.** Using the original sample data, suppose `employees.team_id` were changed to `INT NOT NULL REFERENCES teams(id) ON DELETE SET NULL`. Describe what happens when you run `DELETE FROM teams WHERE team_name = 'QA';`. Then rewrite the foreign key in two different ways so the delete succeeds, and state the effect each version has on Rohan.

**Exercise 2: Unmatched records, both directions.** Write two queries using `LEFT JOIN`: (a) buildings that have no teams; (b) employees who are not assigned to any project. For each, state which table goes in `FROM`, and which column you check for `NULL`.

**Exercise 3: Spotting duplicates.** Add the assignment `(1, 2)` (Asha on Mobile App). Write a query that lists the `team_name` of every team with at least one member working on a project due before `2027-01-01`. Each team name should appear only once. Run it with and without `DISTINCT`, and explain the difference.

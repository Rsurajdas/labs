# SQL Assessment 1: Company Projects Database

**Database:** PostgreSQL

**Note:** The `employees` table spells the column `brithdate`. Use the column name exactly as it appears in the schema.

### Sample Data (applies to all questions)

```sql
INSERT INTO buildings (building_name) VALUES
('Alpha Tower'), ('Beta Block'), ('Gamma House');
-- ids: 1, 2, 3

INSERT INTO teams (team_name, building_id) VALUES
('Frontend', 1), ('Backend', 1), ('QA', 2), ('DevOps', NULL);
-- ids: 1, 2, 3, 4

INSERT INTO employees (first_name, last_name, brithdate, email, team_id) VALUES
('Asha',   'Rao',    '1990-04-12', 'asha@co.com',   1),
('Vikram', 'Shah',   '1985-11-03', 'vikram@co.com', 2),
('Neha',   'Iyer',   '1995-07-21', 'neha@co.com',   2),
('Rohan',  'Mehta',  '1992-01-30', 'rohan@co.com',  3),
('Priya',  'Nair',   '1998-09-15', 'priya@co.com',  NULL),
('Arjun',  'Desai',  '1988-06-08', 'arjun@co.com',  4);
-- ids: 1–6

INSERT INTO projects (title, deadline) VALUES
('Payments Revamp', '2026-12-15'),
('Mobile App',      '2026-11-05'),
('Data Migration',  '2027-02-28'),
('Audit Portal',    '2026-10-30');
-- ids: 1–4

INSERT INTO internet_accounts (email, password) VALUES
('asha@co.com', 'pass_a1'), ('vikram@co.com', 'pass_v2'), ('rohan@co.com', 'pass_r3');

INSERT INTO projects_employees (employee_id, project_id) VALUES
(1, 1), (2, 1), (3, 2), (1, 3), (4, 2);
```

---

**Question 1: Constraints and Foreign Keys**

**Difficulty:** Easy
**Type:** Conceptual

**Question:** The `internet_accounts.email` column references `employees(email)` instead of `employees(id)`.

**Requirements:**

- (a) Name the constraint on `employees.email` that makes this foreign key reference allowed, and explain why PostgreSQL requires it.
- (b) Explain why `teams.building_id` and `employees.team_id` must be nullable for their `ON DELETE` rules to work.

**Marks:** 1

---

**Question 2: INSERT with Subquery**

**Difficulty:** Easy
**Type:** SQL

**Question:** A new employee joins the QA team. Her details are: Sneha Kulkarni, born 1997-03-18, email `sneha@co.com`.

**Requirements:**

- Insert the employee into `employees`.
- Do **not** hardcode the `team_id`. Look it up by team name using a subquery.

**Marks:** 1

---

**Question 3: Filtering and Sorting**

**Difficulty:** Easy
**Type:** SQL

**Question:** HR needs a list of employees born on or after 1 January 1990.

**Requirements:**

- Return `first_name`, `last_name`, and `email`.
- Sort the list from the oldest to the youngest employee.

**Marks:** 1

---

**Question 4: UPDATE with NULL Handling**

**Difficulty:** Medium
**Type:** SQL

**Question:** Every employee who has no team must be assigned to the DevOps team.

**Requirements:**

- Write a single `UPDATE` statement.
- Update only employees whose team is missing.
- Look up the DevOps `team_id` with a subquery instead of hardcoding it.

**Marks:** 1

---

**Question 5: Multi-Table INNER JOIN**

**Difficulty:** Medium
**Type:** SQL

**Question:** List each employee with the name of their team and the building that team is located in.

**Requirements:**

- Return `first_name`, `last_name`, `team_name`, and `building_name`.
- Include only employees who have **both** a team **and** a building.
- Sort the results by `building_name`, then by `first_name`.

**Marks:** 1

---

**Question 6: LEFT JOIN Output**

**Difficulty:** Medium
**Type:** Output Prediction

**Question:** Using the sample data, predict the exact result of this query.

```sql
SELECT t.team_name, b.building_name
FROM teams t
LEFT JOIN buildings b ON t.building_id = b.id
ORDER BY t.id;
```

**Requirements:**

- Write every row the query returns, in order, as a table.
- Show `NULL` wherever a value is missing.
- In one sentence, explain why `Gamma House` does or does not appear.

**Marks:** 1

---

**Question 7: Unmatched Records**

**Difficulty:** Medium
**Type:** SQL

**Question:** Management wants to know which projects have no employees assigned.

**Requirements:**

- Use a `LEFT JOIN`.
- Return `title` and `deadline` of the unassigned projects.

**Marks:** 1

---

**Question 8: Debugging**

**Difficulty:** Medium
**Type:** Debugging

**Question:** This query should list every employee who does **not** have an internet account. It returns no rows.

```sql
SELECT e.first_name, e.email
FROM employees e
LEFT JOIN internet_accounts ia ON e.id = ia.id
WHERE ia.email = NULL;
```

**Requirements:**

- Identify every mistake in the query.
- Explain why each mistake gives the wrong result.
- Write the corrected query.

**Marks:** 1

---

**Question 9: Many-to-Many JOIN**

**Difficulty:** Medium
**Type:** SQL

**Question:** List all employees working on the project titled `Payments Revamp`.

**Requirements:**

- Go through the `projects_employees` junction table to connect the two tables.
- Return `first_name`, `last_name`, `title`, and `deadline`.
- Filter by project title, not by project id.

**Marks:** 1

---

**Question 10: Top-N with LEFT JOIN**

**Difficulty:** Challenging
**Type:** SQL

**Question:** Find the 3 youngest employees and the team each one belongs to.

**Requirements:**

- Return `first_name`, `last_name`, `brithdate`, and `team_name`.
- Include employees who have no team. Their `team_name` should appear as `NULL`.
- Return exactly 3 rows, youngest first.
- Assume the query runs on the original sample data, before any changes from Questions 2 and 4.

**Marks:** 1

---

**Question 11: Views**

**Difficulty:** Challenging
**Type:** SQL

**Question:** The reporting team often needs to see which employee works on which project.

**Requirements:**

- (a) Create a view named `employee_projects_view`. It should show `first_name`, `last_name`, `email`, `title`, and `deadline` for every employee–project assignment.
- (b) Write a query on that view that returns the **distinct** emails of employees with at least one project deadline before `2027-01-01`. Sort the emails alphabetically.

**Marks:** 1

---

**Question 12: DELETE and Cascading Effects**

**Difficulty:** Challenging
**Type:** SQL + Conceptual

**Question:** Two changes happen on the original sample data:

1. The building `Alpha Tower` is removed from the system.
2. The employee `Vikram Shah` leaves the company and is removed from the system.

**Requirements:**

- (a) Write both `DELETE` statements. Identify the rows by name or email, not by id.
- (b) For each delete, describe exactly which rows in other tables are affected, and how. Name the specific rows from the sample data and say whether each one is updated or deleted.

**Marks:** 1

---

## Assessment Summary

| Item            | Detail                                                                                                                                                                                                  |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Total Questions | 12                                                                                                                                                                                                      |
| Total Marks     | 12                                                                                                                                                                                                      |
| Database        | PostgreSQL                                                                                                                                                                                              |
| Topics Covered  | Constraints and FKs, `ON DELETE` rules, INSERT, UPDATE, DELETE, WHERE, ORDER BY, LIMIT, DISTINCT, NULL handling, subqueries, views, INNER JOIN, LEFT JOIN, unmatched records, many-to-many JOINs, Top-N |

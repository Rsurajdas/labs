-- Q1 -> a -> The UNIQUE constraint on `employees.email` ensures that each email address is unique. A foreign key constraint requires the referenced column in the parent table to have a UNIQUE or PRIMARY KEY constraint.
-- Q1 -> b -> I am aware that this approach will allow team records to exist without a `building_id` and employee records to exist without a `team_id`. I would have opted for the RESTRICT constraint, which allows a building or team record to be deleted only after all its related records have been removed.
-- Q2
INSERT INTO employees (first_name, last_name, brithdate, email, team_id)
VALUES (
        'Sneha',
        'Kulkarni',
        '1997-03-18',
        'sneha@co.com',
        (
            SELECT id
            FROM teams
            WHERE team_name = 'QA'
        )
    );
-- Q3
SELECT first_name,
    last_name,
    email
FROM employees
WHERE brithdate >= '1990-01-01'
ORDER BY brithdate ASC;
-- Q4
UPDATE employees
SET team_id = (
        SELECT id
        FROM teams
        WHERE team_name = 'DevOps'
    )
WHERE team_id IS NULL;
-- Q5
SELECT e.first_name,
    e.last_name,
    t.team_name,
    b.building_name
FROM employees AS e
    INNER JOIN teams AS t ON e.team_id = t.id
    INNER JOIN buildings AS b ON t.building_id = b.id
ORDER BY b.building_name ASC,
    e.first_name ASC;
-- Q6 -> “Gamma House” will not appear in the results because it is not associated with any team.
SELECT t.team_name,
    b.building_name
FROM teams t
    LEFT JOIN buildings b ON t.building_id = b.id
ORDER BY t.id;
-- Q7
SELECT p.title
FROM projects_employees AS pe
    LEFT JOIN projects AS p ON pe.project_id = p.id
WHERE pe.employee_id IS NULL;
-- Q8
SELECT e.first_name,
    e.email
FROM employees e
    LEFT JOIN internet_accounts ia ON e.email = ia.email
WHERE ia.email IS NULL;
-- The `LEFT JOIN` should use `employees.email` instead of `employees.id`. Additionally, the filtering condition is incorrect; it should be `WHERE ia.email IS NULL`.
-- Q9
SELECT e.first_name,
    e.last_name,
    p.title,
    p.deadline
FROM projects_employees AS pe
    INNER JOIN employees AS e ON pe.employee_id = e.id
    INNER JOIN projects AS p ON pe.project_id = p.id
WHERE p.title = 'Payments Revamp';
-- Q10
SELECT e.first_name,
    e.last_name,
    e.brithdate,
    t.team_name
FROM employees AS e
    LEFT JOIN teams AS t ON e.team_id = t.id
ORDER BY e.brithdate DESC
LIMIT 3;
-- Q11
CREATE VIEW employee_projects_view AS
SELECT e.first_name,
    e.last_name,
    e.email,
    p.title,
    p.deadline
FROM projects_employees AS pe
    INNER JOIN employees AS e ON pe.employee_id = e.id
    INNER JOIN projects AS p ON pe.project_id = p.id;
SELECT email
FROM employee_projects_view
WHERE deadline < '2027-01-01'
ORDER BY email ASC;
-- Q12
DELETE FROM buildings
WHERE building_name = 'Alpha Tower';
DELETE FROM employees
WHERE email = 'vikram@co.com';
-- In the `teams` table, the Frontend and Backend rows are affected. Additionally, the second row in both the `internet_accounts` and `projects_employees` tables is deleted due to the `ON DELETE CASCADE` constraint.
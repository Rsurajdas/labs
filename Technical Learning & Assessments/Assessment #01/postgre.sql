-- Q1
SELECT name,
    salary
FROM employees
WHERE salary IS NOT NULL
ORDER BY salary DESC
LIMIT 3;
-- Q4
SELECT d.id,
    d.name
FROM departments AS d
    LEFT JOIN employees as e ON e.department_id = d.id
WHERE e.department_id IS NOT NULL
ORDER BY department_id ASC;
-- Q8
CREATE VIEW user_locations AS
SELECT u.id AS user_id,
    u.name AS user_name,
    a.street,
    c.name AS city_name
FROM users AS u
    LEFT JOIN addresses AS a ON u.address_id = a.id
    LEFT JOIN cities AS c ON a.city_id = c.id;
SELECT *
FROM user_locations
WHERE city_name = 'Mumbai'
    OR city_name IS NULL
ORDER BY user_name ASC;
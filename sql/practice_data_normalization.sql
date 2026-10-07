CREATE TABLE departments (
    -- id INT PRIMARY KEY AUTO_INCREMENT,
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);
CREATE TABLE employees (
    -- id INT PRIMARY KEY AUTO_INCREMENT,
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    department_id INT,
    salary DECIMAL(10, 2) NOT NULL,
    city VARCHAR(50) NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);
INSERT INTO departments (name)
VALUES ('Engineering'),
    ('Marketing'),
    ('Sales'),
    ('Finance');
INSERT INTO employees (full_name, department_id, salary, city)
VALUES ('Aarav Sharma', 1, 95000.00, 'Bengaluru'),
    ('Priya Nair', 2, 62000.00, 'Mumbai'),
    ('Rohan Mehta', 1, 78000.00, 'Pune'),
    ('Sneha Iyer', 3, 54000.00, 'Mumbai'),
    ('Karan Gupta', 1, 88000.00, 'Bengaluru'),
    ('Divya Rao', 2, 71000.00, 'Bengaluru'),
    ('Vikram Singh', NULL, 49000.00, 'Delhi'),
    ('Ananya Desai', 2, 58000.00, 'Denver');
SELECT full_name,
    d.name AS dept_name
FROM employees AS e
    INNER JOIN departments AS d ON e.department_id = d.id;
SELECT full_name,
    d.name AS dept_name
FROM employees AS e
    INNER JOIN departments AS d ON e.department_id = d.id
WHERE city = 'Bengaluru'
ORDER BY full_name;
SELECT full_name,
    d.name AS dept_name
FROM employees AS e
    LEFT JOIN departments AS d ON e.department_id = d.id;
SELECT d.name AS dept_name,
    full_name
FROM departments as d
    LEFT JOIN employees AS e ON e.department_id = d.id;
SELECT full_name,
    d.name AS dept_name,
    salary
FROM employees AS e
    INNER JOIN departments AS d ON e.department_id = d.id
WHERE d.name = 'Engineering'
ORDER BY salary DESC;
SELECT full_name,
    d.name AS dept_name
FROM employees AS e
    INNER JOIN departments AS d ON e.department_id = d.id
ORDER BY salary DESC
LIMIT 3;
SELECT full_name,
    city
FROM employees AS e
    LEFT JOIN departments AS d ON e.department_id = d.id
WHERE d.name IS NULL;
SELECT e.full_name,
    d.name
FROM employees AS e
    LEFT JOIN departments AS d ON e.department_id = d.id
ORDER BY d.name,
    e.full_name;
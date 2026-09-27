CREATE TABLE employees (
    -- id INT PRIMARY KEY AUTO_INCREMENT,
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(100),
    department VARCHAR(50),
    salary DECIMAL(8, 2),
    city VARCHAR(50),
    hire_date DATE
);
INSERT INTO employees (full_name, department, salary, city, hire_date)
VALUES (
        'Aarav Sharma',
        'Engineering',
        95000.00,
        'Bengaluru',
        '2021-03-15'
    ),
    (
        'Priya Nair',
        'Marketing',
        62000.00,
        'Mumbai',
        '2020-07-01'
    ),
    (
        'Rohan Mehta',
        'Engineering',
        78000.00,
        'Pune',
        '2022-01-10'
    ),
    (
        'Sneha Iyer',
        'Sales',
        54000.00,
        'Mumbai',
        '2019-11-25'
    ),
    (
        'Karan Gupta',
        'Engineering',
        88000.00,
        'Bengaluru',
        '2023-06-20'
    ),
    (
        'Divya Rao',
        'Marketing',
        71000.00,
        'Bengaluru',
        '2021-09-05'
    ),
    (
        'Vikram Singh',
        'Sales',
        49000.00,
        'Delhi',
        '2018-02-14'
    ),
    (
        'Ananya Desai',
        'HR',
        58000.00,
        'Pune',
        '2022-12-01'
    );
SELECT *
FROM employees;
SELECT full_name,
    salary
FROM employees;
SELECT *
FROM employees
WHERE department = 'Engineering';
SELECT *
FROM employees
WHERE salary >= 70000;
SELECT *
FROM employees
WHERE department = 'Marketing'
    AND city = 'Bengaluru';
SELECT *
FROM employees
WHERE department = 'Sales'
    OR salary < 55000;
SELECT *
FROM employees
ORDER BY salary ASC;
SELECT full_name,
    hire_date
FROM employees
ORDER BY hire_date ASC
LIMIT 3;
SELECT *
FROM employees
ORDER BY salary DESC
LIMIT 2 OFFSET 2;
UPDATE employees
SET city = 'Hyderabad'
WHERE department = 'HR';
DELETE FROM employees
WHERE hire_date < '2019-01-01';
SELECT full_name,
    salary
FROM employees
WHERE department = 'Engineering'
ORDER BY salary DESC
LIMIT 1;
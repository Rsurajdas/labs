CREATE TABLE projects(
    id SERIAL PRIMARY KEY,
    title VARCHAR(250) NOT NULL,
    deadline DATE NOT NULL
);
CREATE TABLE buildings (
    id SERIAL PRIMARY KEY,
    building_name VARCHAR(200) NOT NULL
);
CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    team_name VARCHAR(200) NOT NULL,
    building_id INT REFERENCES buildings (id) ON DELETE
    SET NULL
);
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    brithdate DATE NOT NULL,
    email VARCHAR(200) UNIQUE NOT NULL,
    team_id INT REFERENCES teams (id) ON DELETE
    SET NULL
);
CREATE TABLE internet_accounts (
    id SERIAL PRIMARY KEY,
    email VARCHAR(200) REFERENCES employees (email) ON DELETE CASCADE,
    password VARCHAR(100) NOT NULL
);
CREATE TABLE projects_employees (
    id SERIAL PRIMARY KEY,
    employee_id INT REFERENCES employees (id) ON DELETE CASCADE,
    project_id INT REFERENCES projects (id) ON DELETE CASCADE
);
-- ==========================================
-- 1. BUILDINGS (6 records)
-- ==========================================
INSERT INTO buildings (building_name)
VALUES ('North Tower'),
    ('South Tower'),
    ('Technology Park'),
    ('Innovation Hub'),
    ('Corporate Center'),
    ('Research Campus');
-- ==========================================
-- 2. TEAMS (12 records)
-- Approximately 20% NULL building_id
-- ==========================================
INSERT INTO teams (team_name, building_id)
SELECT 'Team ' || LPAD(n::TEXT, 2, '0') || ' - ' || (
        ARRAY [
        'Engineering',
        'Frontend',
        'Backend',
        'Quality Assurance',
        'DevOps',
        'Cybersecurity',
        'Data Science',
        'Design',
        'Human Resources',
        'Operations',
        'Product',
        'Infrastructure'
    ]
    ) [n],
    CASE
        WHEN RANDOM() < 0.20 THEN NULL
        ELSE b.ids [
            1 + FLOOR(RANDOM() * CARDINALITY(b.ids))::INT
        ]
    END
FROM GENERATE_SERIES(1, 12) AS gs(n)
    CROSS JOIN (
        SELECT ARRAY_AGG(id) AS ids
        FROM buildings
    ) AS b;
-- ==========================================
-- 3. PROJECTS (10 records)
-- Random future deadlines
-- ==========================================
INSERT INTO projects (title, deadline)
SELECT 'Project ' || LPAD(n::TEXT, 2, '0') || ' - ' || (
        ARRAY [
        'Employee Management System',
        'E-Commerce Platform',
        'Banking Application',
        'Customer Relationship Management',
        'Inventory Management',
        'Cybersecurity Dashboard',
        'AI Analytics Platform',
        'Payment Gateway',
        'Learning Management System',
        'Cloud Infrastructure'
    ]
    ) [n],
    CURRENT_DATE + (30 + FLOOR(RANDOM() * 335))::INT
FROM GENERATE_SERIES(1, 10) AS gs(n);
-- ==========================================
-- 4. EMPLOYEES (50 records)
-- Approximately 15% NULL team_id
-- Unique generated email addresses
-- ==========================================
INSERT INTO employees (
        first_name,
        last_name,
        brithdate,
        email,
        team_id
    )
SELECT emp.first_name,
    emp.last_name,
    DATE '1975-01-01' + FLOOR(RANDOM() * 10000)::INT,
    LOWER(
        emp.first_name || '.' || emp.last_name || '.' || emp.n || '.' || LEFT(MD5(RANDOM()::TEXT), 8) || '@example.com'
    ),
    CASE
        WHEN RANDOM() < 0.15 THEN NULL
        ELSE t.ids [
            1 + FLOOR(RANDOM() * CARDINALITY(t.ids))::INT
        ]
    END
FROM (
        SELECT n,
            (
                ARRAY [
            'Aarav', 'Vivaan', 'Aditya',
            'Isha', 'Ananya', 'Priya',
            'Rahul', 'Rohan', 'Neha',
            'Sneha', 'Arjun', 'Karan',
            'Meera', 'Sanjay', 'Pooja'
        ]
            ) [1 + FLOOR(RANDOM() * 15)::INT] AS first_name,
            (
                ARRAY [
            'Sharma', 'Verma', 'Patel',
            'Singh', 'Kumar', 'Gupta',
            'Mehta', 'Joshi', 'Reddy',
            'Nair', 'Das', 'Mishra'
        ]
            ) [1 + FLOOR(RANDOM() * 12)::INT] AS last_name
        FROM GENERATE_SERIES(1, 50) AS gs(n)
    ) AS emp
    CROSS JOIN (
        SELECT ARRAY_AGG(id) AS ids
        FROM teams
    ) AS t;
-- ==========================================
-- 5. INTERNET ACCOUNTS
-- Approximately 70% of employees
-- ==========================================
INSERT INTO internet_accounts (email, password)
SELECT email,
    'DUMMY_PASSWORD_' || id
FROM employees
WHERE RANDOM() < 0.70;
-- Include a NULL email record
INSERT INTO internet_accounts (email, password)
VALUES (NULL, 'DUMMY_PASSWORD_NO_EMPLOYEE');
-- ==========================================
-- 6. PROJECT-EMPLOYEE RELATIONSHIPS
-- 120 randomly selected unique pairs
-- ==========================================
INSERT INTO projects_employees (employee_id, project_id)
SELECT e.id,
    p.id
FROM employees AS e
    CROSS JOIN projects AS p
ORDER BY RANDOM()
LIMIT 120;
-- ==========================================
-- 7. OPTIONAL NULL RELATIONSHIPS
-- Both foreign keys are nullable
-- ==========================================
INSERT INTO projects_employees (employee_id, project_id)
VALUES (NULL, NULL),
    (
        NULL,
        (
            SELECT MIN(id)
            FROM projects
        )
    );
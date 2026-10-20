CREATE TABLE projects(
    id SERIAL PRIMARY KEY,
    title VARCHAR(250) NOT NULL,
    deadline DATE NOT NULL,
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
-- CREATE DATABASE talently;

-- CREATE TYPE employment_status AS ENUM ('employed', 'self-employed', 'unemployed');

CREATE TABLE users(
    full_name VARCHAR(100),
    yearly_salary INT,
    current_status employment_status
)
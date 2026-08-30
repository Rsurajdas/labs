-- CREATE DATABASE talently;

-- CREATE TYPE employment_status AS ENUM ('employed', 'self-employed', 'unemployed');

-- CREATE TABLE users(
--     full_name VARCHAR(100),
--     yearly_salary INT,
--     current_status employment_status
-- );

-- INSERT INTO users (current_status, full_name, yearly_salary) VALUES ('employed', 'Suraj Kumar', 12473412);
-- INSERT INTO users (current_status, full_name, yearly_salary) VALUES ('self-employed', 'Subhankar Kumar', 22473412);
-- INSERT INTO users (current_status, full_name, yearly_salary) VALUES ('unemployed', 'abc', 0);

-- DELETE FROM users WHERE full_name = 'Subhankar Kumar';
-- DELETE FROM users WHERE full_name = 'abc';

SELECT * FROM users;
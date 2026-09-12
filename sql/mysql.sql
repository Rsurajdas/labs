CREATE DATABASE IF NOT EXISTS talently;

CREATE TABLE users(
    full_name VARCHAR(100),
    yearly_salary INT,
    current_status ENUM("employed", "self-employed", "unemployed")
);

INSERT INTO users (current_status, full_name, yearly_salary) VALUES ('employed', 'Suraj Kumar', 12473412);
INSERT INTO users (current_status, full_name, yearly_salary) VALUES ('self-employed', 'Subhankar Kumar', 22473412);
INSERT INTO users (current_status, full_name, yearly_salary) VALUES ('unemployed', 'abc', 0);

SELECT * FROM users;

CREATE TABLE employers (
    company_name VARCHAR(200),
    company_address VARCHAR(350),
    yearly_revenue NUMERIC(10,2),
    is_hiring BOOLEAN
);

INSERT INTO employers VALUES ('Google', '1600 Amphitheatre Parkway, Mountain View, CA 94043, USA', 25763700.00, true),
('Microsoft', 'One Microsoft Way, Redmond, WA 98052-6399, USA', 16808800.00, true),
('Apple', '1 Apple Park Way, Cupertino, CA 95014, USA', 39432800.00, false),
('Amazon', '410 Terry Ave N, Seattle, WA 98109-5210, USA', 46982200.00, true),
('Facebook', '1 Hacker Way, Menlo Park, CA 94025, USA', 11792900.00, false);

DELETE FROM employers WHERE company_name = 'Facebook';
DELETE FROM employers WHERE company_name = 'Google';
DELETE FROM employers WHERE company_name = 'Apple';
DELETE FROM employers WHERE company_name = 'Amazon';
DELETE FROM employers WHERE company_name = 'Microsoft';

SELECT * FROM employers;

CREATE TABLE conversations (
    user_name VARCHAR(100),
    employer_name VARCHAR(200),
    message TEXT,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

INSERT INTO conversations VALUES ('Suraj Kumar', 'Google', 'Hello, I am interested in the job opening at Google. Can you provide more details?', '2023-10-01 10:15:00'),
('Subhankar Kumar', 'Microsoft', 'Hi, I would like to know more about the software engineer position at Microsoft.', '2023-10-02 14:30:00'),
('abc', 'Apple', 'Good day, I am looking for opportunities at Apple. Could you share any available positions?', '2023-10-03 09:45:00');

SELECT * FROM conversations;

ALTER TABLE employers
MODIFY COLUMN is_hiring BOOLEAN DEFAULT FALSE;

ALTER TABLE employers
MODIFY COLUMN yearly_revenue NUMERIC(20,2);

ALTER TABLE users
MODIFY COLUMN full_name VARCHAR(100) NOT NULL,
MODIFY COLUMN current_status ENUM("employed", "self-employed", "unemployed") NOT NULL;

UPDATE users
SET yearly_salary = NULL
WHERE full_name = 'abc';

ALTER TABLE users
ADD CONSTRAINT check_yearly_salary CHECK (yearly_salary > 0);

INSERT INTO users VALUES ('John Doe', 0, 'unemployed');

ALTER TABLE users
ADD COLUMN id INT PRIMARY KEY AUTO_INCREMENT;

ALTER TABLE employers
ADD COLUMN id INT PRIMARY KEY AUTO_INCREMENT;

ALTER TABLE conversations
ADD COLUMN id INT PRIMARY KEY AUTO_INCREMENT;

ALTER TABLE employers
MODIFY COLUMN yearly_revenue FLOAT CHECK (yearly_revenue > 0);

ALTER TABLE employers
MODIFY COLUMN company_name VARCHAR(200) NOT NULL;
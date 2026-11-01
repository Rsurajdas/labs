-- ===== Tables =====
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    username VARCHAR(50) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(200)
);
CREATE TABLE expenses (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    amount NUMERIC(10, 2) NOT NULL CHECK (amount > 0),
    spent_on DATE NOT NULL,
    category_id INT REFERENCES categories(id) ON DELETE
    SET NULL,
        user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE
);
-- ===== Seed data =====
-- These hashes are placeholders, so the seed users cannot log in.
-- Register new users through the API to test login.
INSERT INTO users (email, username, hashed_password, is_active)
VALUES (
        'asha@example.com',
        'asha',
        'seed-placeholder-hash',
        TRUE
    ),
    -- id 1
    (
        'ravi@example.com',
        'ravi',
        'seed-placeholder-hash',
        TRUE
    ),
    -- id 2
    (
        'old@example.com',
        'olduser',
        'seed-placeholder-hash',
        FALSE
    );
-- id 3
INSERT INTO categories (name, description)
VALUES ('Food', 'Meals and groceries'),
    -- id 1
    ('Travel', 'Commute and trips'),
    -- id 2
    ('Utilities', 'Bills'),
    -- id 3
    ('Entertainment', NULL);
-- id 4 (no expenses)
INSERT INTO expenses (title, amount, spent_on, category_id, user_id)
VALUES (
        'Lunch at office',
        250.00,
        '2026-10-01',
        1,
        1
    ),
    -- id 1
    (
        'Metro card recharge',
        500.00,
        '2026-10-03',
        2,
        1
    ),
    -- id 2
    (
        'Electricity bill',
        1840.50,
        '2026-10-05',
        3,
        2
    ),
    -- id 3
    (
        'Groceries',
        1320.00,
        '2026-10-07',
        1,
        2
    ),
    -- id 4
    (
        'Cab to airport',
        760.00,
        '2026-10-10',
        2,
        1
    ),
    -- id 5
    (
        'Misc cash',
        100.00,
        '2026-10-12',
        NULL,
        1
    );
-- id 6
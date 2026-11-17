-- Assessment 07 — PostgreSQL — library database setup
-- Run on an EMPTY database:  createdb library_07 && psql -d library_07 -f library_setup.sql
CREATE TABLE branches (
    id SERIAL PRIMARY KEY,
    name VARCHAR(60) NOT NULL UNIQUE,
    city VARCHAR(40) NOT NULL
);
CREATE TABLE members (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(80) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    phone VARCHAR(15),
    -- optional
    home_branch_id INT REFERENCES branches ON DELETE
    SET NULL,
        -- optional
        joined_on DATE NOT NULL DEFAULT CURRENT_DATE
);
CREATE TABLE authors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(80) NOT NULL UNIQUE
);
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    isbn CHAR(13) NOT NULL UNIQUE,
    title VARCHAR(120) NOT NULL,
    genre VARCHAR(30),
    -- optional
    published_year INT CHECK (
        published_year BETWEEN 1800 AND 2100
    ),
    price NUMERIC(6, 2) NOT NULL CHECK (price > 0)
);
-- many-to-many: a book can have several authors, an author several books
CREATE TABLE book_authors (
    book_id INT REFERENCES books ON DELETE CASCADE,
    author_id INT REFERENCES authors ON DELETE CASCADE,
    PRIMARY KEY (book_id, author_id)
);
CREATE TABLE loans (
    id SERIAL PRIMARY KEY,
    book_id INT NOT NULL REFERENCES books,
    -- no ON DELETE clause
    member_id INT NOT NULL REFERENCES members ON DELETE CASCADE,
    loaned_on DATE NOT NULL,
    returned_on DATE,
    -- NULL = still out
    fine NUMERIC(6, 2) -- NULL = no fine charged
);
INSERT INTO branches (name, city)
VALUES ('Indiranagar', 'Bengaluru'),
    ('Koramangala', 'Bengaluru'),
    ('Andheri', 'Mumbai');
INSERT INTO members (
        full_name,
        email,
        phone,
        home_branch_id,
        joined_on
    )
VALUES (
        'Asha Rao',
        'asha@mail.in',
        '9800000001',
        1,
        '2025-01-10'
    ),
    (
        'Vikram Shah',
        'vikram@mail.in',
        NULL,
        1,
        '2025-03-02'
    ),
    (
        'Neha Iyer',
        'neha@mail.in',
        '9800000003',
        2,
        '2025-06-15'
    ),
    (
        'Rahul Menon',
        'rahul@mail.in',
        NULL,
        2,
        '2025-08-20'
    ),
    (
        'Priya Das',
        'priya@mail.in',
        '9800000005',
        NULL,
        '2026-01-05'
    ),
    (
        'Arjun Nair',
        'arjun@mail.in',
        '9800000006',
        3,
        '2026-02-11'
    ),
    (
        'Kavya Pillai',
        'kavya@mail.in',
        NULL,
        3,
        '2026-04-01'
    ),
    (
        'Sameer Khan',
        'sameer@mail.in',
        '9800000008',
        NULL,
        '2026-09-30'
    );
INSERT INTO authors (name)
VALUES ('R. K. Narayan'),
    -- 1
    ('Ruskin Bond'),
    -- 2
    ('Amitav Ghosh'),
    -- 3
    ('Sudha Murty'),
    -- 4
    ('A. P. J. Abdul Kalam'),
    -- 5
    ('Arun Tiwari'),
    -- 6
    ('Jhumpa Lahiri');
-- 7
INSERT INTO books (isbn, title, genre, published_year, price)
VALUES (
        '9780000000001',
        'Malgudi Days',
        'Fiction',
        1943,
        299.00
    ),
    -- 1
    (
        '9780000000002',
        'The Guide',
        'Fiction',
        1958,
        350.00
    ),
    -- 2
    (
        '9780000000003',
        'Swami and Friends',
        'Fiction',
        1935,
        250.00
    ),
    -- 3
    (
        '9780000000004',
        'The Blue Umbrella',
        'Children',
        1980,
        150.00
    ),
    -- 4
    (
        '9780000000005',
        'Rusty Runs Away',
        'Children',
        2002,
        199.00
    ),
    -- 5
    (
        '9780000000006',
        'The Hungry Tide',
        'Fiction',
        2004,
        499.00
    ),
    -- 6
    (
        '9780000000007',
        'Wise and Otherwise',
        'Non-fiction',
        2002,
        250.00
    ),
    -- 7
    (
        '9780000000008',
        'Wings of Fire',
        'Non-fiction',
        1999,
        399.00
    ),
    -- 8
    (
        '9780000000009',
        'Gun Island',
        NULL,
        2019,
        599.00
    ),
    -- 9
    (
        '9780000000010',
        'The Room on the Roof',
        NULL,
        1956,
        299.00
    ),
    -- 10
    (
        '9780000000011',
        'Local History Pamphlet',
        'Non-fiction',
        2020,
        99.00
    );
-- 11
INSERT INTO book_authors (book_id, author_id)
VALUES (1, 1),
    (2, 1),
    (3, 1),
    (4, 2),
    (5, 2),
    (10, 2),
    (6, 3),
    (9, 3),
    (7, 4),
    (8, 5),
    (8, 6);
-- book 11 has no author listed; author 7 has no books
INSERT INTO loans (book_id, member_id, loaned_on, returned_on, fine)
VALUES (1, 1, '2026-09-01', '2026-09-14', NULL),
    -- 1
    (2, 1, '2026-10-02', '2026-10-20', 20.00),
    -- 2
    (6, 2, '2026-10-05', '2026-10-28', 45.00),
    -- 3
    (1, 3, '2026-10-10', '2026-10-18', NULL),
    -- 4
    (4, 3, '2026-10-15', NULL, NULL),
    -- 5
    (8, 4, '2026-10-21', '2026-11-02', 10.00),
    -- 6
    (2, 4, '2026-11-01', NULL, NULL),
    -- 7
    (9, 4, '2026-11-03', NULL, NULL),
    -- 8
    (7, 5, '2026-10-25', '2026-10-30', NULL),
    -- 9
    (3, 5, '2026-11-05', NULL, NULL),
    -- 10
    (6, 6, '2026-11-02', '2026-11-12', 0.00),
    -- 11
    (1, 7, '2026-11-08', NULL, NULL),
    -- 12
    (2, 2, '2026-09-10', '2026-09-25', 15.00),
    -- 13
    (8, 6, '2026-11-10', NULL, NULL);
-- 14
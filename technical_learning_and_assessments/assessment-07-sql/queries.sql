-- Q#01
SELECT title,
    price
FROM books
ORDER BY price DESC,
    title ASC OFFSET 4
LIMIT 4;
-- Q#02
SELECT COUNT(*) AS a,
    COUNT(returned_on) AS b,
    COUNT(fine) AS C,
    COUNT(DISTINCT member_id) AS d,
    SUM(fine) AS E,
    ROUND(AVG(fine), 2) AS F,
    MIN(fine) AS g
FROM loans;
-- Q#03
SELECT full_name,
    email
FROM members
WHERE (
        phone IS NULL
        OR home_branch_id IS NULL
    )
    AND joined_on >= '2026-01-01'
ORDER BY full_name;
-- Bug #1: The SQL query uses incorrect syntax to check for `NULL` values. Replace `phone = NULL OR home_branch_id = NULL` with `phone IS NULL OR home_branch_id IS NULL`. In SQL, `IS NULL` must be used to check for `NULL` values.
-- Bug #2: The SQL query does not group the conditions (phone IS NULL OR home_branch_id IS NULL) using parentheses. According to the question, we need to retrieve members who joined on or after 1 January 2026 and are missing contact details (either a phone number, a home branch, or both). The correct query should use parentheses to ensure the OR conditions are evaluated together with the AND condition.
-- Q#04
CREATE TABLE reviews(
    member_id INT NOT NULL REFERENCES members(id) ON DELETE CASCADE,
    book_id INT NOT NULL REFERENCES books(id) ON DELETE CASCADE,
    rating INT NOT NULL CHECK (
        rating > 0
        AND rating <= 5
    ),
    comment VARCHAR(500),
    reviewed_on DATE NOT NULL DEFAULT(CURRENT_DATE),
    PRIMARY KEY(member_id, book_id)
)
INSERT INTO reviews (member_id, book_id, rating)
VALUES (1, 2, 5);
INSERT INTO reviews (member_id, book_id, rating, comment)
VALUES (1, 2, 4, 'Changed my mind');
INSERT INTO reviews (member_id, book_id, rating)
VALUES (3, 4, 0);
INSERT INTO reviews (member_id, book_id, rating)
VALUES (2, 99, 3);
-- (ii) Fail: unique constraint "reviews_pkey"
-- (iii) Fail: check constraint "reviews_rating_check"
-- (iv) Fail: foreign key constraint "reviews_book_id_fkey"
-- Q#05
ALTER TABLE loans
ADD CONSTRAINT chk_returned_after_loaned CHECK (returned_on > loaned_on);
ALTER TABLE loans
ADD CONSTRAINT chk_fine_not_negative CHECK (fine >= 0);
ALTER TABLE loans
ADD COLUMN due_on DATE;
-- 5.4a: It won't violate the `chk_returned_after_loaned` constraint because it only checks whether returned_on is later than loaned_on.
-- 5.4b: This will throw a `chk_returned_after_loaned` check constraint violation error.
-- Q#06
SELECT l.id AS id,
    m.full_name AS full_name,
    b.title AS title,
    br.name AS branch_name,
    l.loaned_on AS loaned_on
FROM loans AS l
    INNER JOIN members AS m ON l.member_id = m.id
    INNER JOIN books AS b ON l.book_id = b.id
    LEFT JOIN branches AS br ON m.home_branch_id = br.id
WHERE l.returned_on IS NULL
ORDER BY l.loaned_on DESC,
    l.id ASC;
-- Q#07a
SELECT b.title AS title,
    b.isbn AS isbn
FROM books AS b
    LEFT JOIN loans AS l ON b.id = l.book_id
WHERE l.book_id IS NULL
ORDER BY title ASC;
-- Q#7b
SELECT m.full_name AS full_name
FROM members AS m
    LEFT JOIN loans AS l ON m.id = l.member_id
    AND l.returned_on IS NULL
WHERE l.member_id IS NULL
ORDER BY full_name ASC;
-- Q#8
SELECT DISTINCT m.full_name AS full_name,
    m.email AS email
FROM members AS m
    INNER JOIN loans AS l ON m.id = l.member_id
    INNER JOIN books AS b ON l.book_id = b.id
    INNER JOIN book_authors AS ba ON b.id = ba.book_id
WHERE ba.author_id = (
        SELECT id
        FROM authors
        WHERE name = 'R. K. Narayan'
    )
ORDER BY full_name ASC;
-- Without DISTINCT, qyery will reture one row per matching record
-- Q#9
SELECT title,
    genre,
    price
FROM books
WHERE price > (
        SELECT AVG(price)
        FROM books
    )
    AND (
        genre != 'Fiction'
        OR genre IS NULL
    )
ORDER BY price DESC;
-- Q#10
SELECT SUM(l.fine) AS total_fines,
    ROUND(AVG(l.fine), 2) AS avg_fine,
    COUNT(l.fine) AS fined_loans,
    MIN(l.loaned_on) AS first_loan,
    MAX(l.returned_on) AS last_return
FROM loans AS l
    LEFT JOIN members AS m ON l.member_id = m.id
    INNER JOIN branches AS b ON m.home_branch_id = b.id
WHERE b.name = 'Indiranagar';
-- Q#11
SELECT genre,
    COUNT(genre) AS book_count
FROM books
GROUP BY genre
ORDER BY genre ASC;
-- Q#11a: My SQL query returns 4 rows, one row for each `genre`, row with empty genre represent as `NULL`
-- Q#11b: The NULL row count is 0 because the `COUNT()` function only counts non-NULL values in the specified column.
-- Q#12
CREATE VIEW current_borrowers AS
SELECT DISTINCT full_name,
    phone
FROM members AS m
    LEFT JOIN loans AS l ON m.id = l.member_id
WHERE l.returned_on IS NULL;
SELECT full_name
FROM current_borrowers
ORDER BY full_name ASC;
-- Q#13
UPDATE loans
SET returned_on = '2026-11-16'
WHERE member_id IN (
        SELECT id
        FROM members
        WHERE email = 'rahul@mail.in'
    )
    AND returned_on is NULL;
-- query updates 2 rows
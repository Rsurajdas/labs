SELECT title,
    price
FROM books
ORDER BY price DESC,
    title ASC OFFSET 4
LIMIT 4;
SELECT COUNT(*) AS a,
    COUNT(returned_on) AS b,
    COUNT(fine) AS C,
    COUNT(DISTINCT member_id) AS d,
    SUM(fine) AS E,
    ROUND(AVG(fine), 2) AS F,
    MIN(fine) AS g
FROM loans;
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
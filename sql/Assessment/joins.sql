SELECT b.title,
    a.name AS author_name
FROM books AS b
    INNER JOIN authors AS a ON b.author_id = a.author_id;
SELECT a.name AS author_name,
    b.title
FROM authors AS a
    LEFT JOIN books AS b ON b.author_id = a.author_id;
SELECT b.title,
    a.name AS author_name
FROM books AS b
    LEFT JOIN authors AS a ON a.author_id = b.author_id
WHERE b.author_id IS NULL;
SELECT b.title,
    a.name AS author_name,
    b.price
FROM books AS b
    INNER JOIN authors AS a ON b.author_id = a.author_id
WHERE a.country = 'India'
ORDER BY price DESC;
SELECT title,
    price
FROM books
ORDER BY price DESC
LIMIT 3 OFFSET 1;
SELECT name,
    email
FROM authors
ORDER BY name ASC
LIMIT 2;
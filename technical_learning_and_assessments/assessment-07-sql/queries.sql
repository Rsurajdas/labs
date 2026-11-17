SELECT title,
    price
FROM books
ORDER BY price DESC,
    title ASC OFFSET 0
LIMIT 4;
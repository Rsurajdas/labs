SELECT title,
    price
FROM books
ORDER BY price DESC,
    title ASC OFFSET 4
LIMIT 4;
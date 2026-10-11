INSERT INTO authors (name, country, email)
VALUES ('George Orwell', 'UK', 'orwell@example.com');
INSERT INTO books (title, price, stock, genre_id, author_id)
VALUES ('Animal Farm', 320.00, 60, 1, 6);
UPDATE books
SET price = price + 50
WHERE genre_id = 1;
DELETE FROM books
WHERE stock = 0;
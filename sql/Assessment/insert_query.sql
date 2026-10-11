INSERT INTO genres (name)
VALUES ('Fiction'),
    ('Classic'),
    ('Mystery');
INSERT INTO authors (name, country, email)
VALUES ('R. K. Narayan', 'India', 'rk@example.com'),
    ('Jane Austen', 'UK', 'jane@example.com'),
    ('Haruki Murakami', 'Japan', 'haruki@example.com'),
    ('Chetan Bhagat', 'India', 'chetan@example.com'),
    ('Unknown Writer', 'Unknown', NULL);
INSERT INTO books (title, price, stock, genre_id, author_id)
VALUES ('Malgudi Days', 299.00, 40, 1, 1),
    ('Pride and Prejudice', 450.00, 15, 2, 2),
    ('Norwegian Wood', 599.00, 0, 1, 3),
    ('Five Point Someone', 250.00, 120, 1, 4),
    ('The Guide', 350.00, 25, 1, 1),
    ('Kafka on the Shore', 650.00, 8, 1, 3),
    ('Mystery Title', 200.00, 50, 3, NULL);
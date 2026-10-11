CREATE TABLE authors(
    author_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country VARCHAR(50) DEFAULT 'UNKNOWN',
    email VARCHAR(100) UNIQUE
);
CREATE TABLE books(
    book_id SERIAL PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    price DECIMAL(8, 2) CHECK (price > 0),
    stock INT DEFAULT 0 CHECK (stock >= 0),
    genre VARCHAR(50),
    author_id INT,
    FOREIGN KEY (author_id) REFERENCES authors(author_id)
);
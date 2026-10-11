ALTER TABLE books
ADD COLUMN published_year INT;
ALTER TABLE books
ADD CONSTRAINT check_published_year CHECK (published_year >= 1000);
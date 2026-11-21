SELECT COUNT(*)
FROM bookings;
SELECT COUNT(booking_date)
from bookings;
SELECT COUNT(DISTINCT booking_date)
from bookings;
SELECT COUNT(amount_tipped)
FROM bookings;
SELECT COUNT(*)
FROM payment_methods;
SELECT COUNT(*)
FROM tables;
SELECT MAX(num_seats)
FROM tables;
SELECT MAX(amount_billed),
    MIN(amount_tipped)
FROM bookings;
SELECT MIN(category),
    MAX(category)
from tables;
SELECT MIN(booking_date) AS start_date,
    MAX(booking_date) AS end_date
FROM bookings;
SELECT *
FROM bookings;
SELECT SUM(amount_billed),
    SUM(amount_tipped)
FROM bookings;
SELECT AVG(amount_billed),
    AVG(amount_tipped)
FROM bookings;
SELECT ROUND(AVG(amount_billed)),
    ROUND(AVG(amount_tipped))
FROM bookings;
SELECT ROUND(AVG(amount_billed), 2),
    ROUND(AVG(amount_tipped), 2)
FROM bookings;
SELECT ROUND(AVG(amount_tipped), 2) AS avg_tipped
FROM bookings
WHERE amount_billed >= 1800
    AND num_guests >= 4;
SELECT MAX(b.num_guests) AS max_guests,
    MAX(t.num_seats) AS max_seats
FROM bookings AS b
    INNER JOIN tables as t ON b.table_id = t.id
    INNER JOIN payment_methods AS p ON b.payment_id = p.id
WHERE t.num_seats <= 4
    AND p.name = 'UPI';
SELECT booking_date,
    SUM(num_guests) AS no_guests
FROM bookings
GROUP BY booking_date;
SELECT booking_date,
    COUNT(booking_date),
    SUM(amount_billed)
FROM bookings
GROUP BY booking_date
HAVING SUM(amount_billed) >= 2599;
SELECT MIN(daily_sum_amount)
FROM (
        SELECT booking_date,
            SUM(amount_billed) AS daily_sum_amount
        FROM bookings
        GROUP BY booking_date
    );
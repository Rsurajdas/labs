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
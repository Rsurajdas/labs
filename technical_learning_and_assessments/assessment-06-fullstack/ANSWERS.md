# Assessment 06 — Written answers

## Q1 — (code only: backend/config.py)

## Q2 — ON DELETE (written part)

(a) On deletes of room 2, all the related bookings will be deleted
(b) BookingOut schema expect Room object attach to it. it will throw an error.

## Q6 — Predict the responses

1.
2.
3.
4.
5.
6.
7.
8.
9.
10.
11.
12.

## Q7 — Does it compile? (written part)

(a) It will not compiles, `role` should be either "user" or "admin"
(b) data is missing
(c) it compiles with type NewBooking
(d) FetchState `error` type does not have data property

## Q12 — Bug list

1. useEffect, and useCallback dependency is missing
2. error is not reset on handleCancel and on useEffect (on Mount)
3. "0" renders, when bookings length is 0
4. Wrong event type on chnage event, it should be ChangeEvent.
5. on booking map function, index is used a <li> key
6. updating bookings state on cancel was not working.

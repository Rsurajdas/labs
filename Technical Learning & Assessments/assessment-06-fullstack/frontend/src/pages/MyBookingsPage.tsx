// Q12 — this component is broken on purpose. Find and fix every bug.
import { useCallback, useEffect, useMemo, useState, type FormEvent } from "react";
import { deleteBooking, getErrorMessage, getMyBookings } from "../api";

type MyBookingsPageProps = { token: string };

export function MyBookingsPage({ token }: MyBookingsPageProps) {
  const [bookings, setBookings] = useState([]);
  const [day, setDay] = useState("");
  const [error, setError] = useState<string | null>(null);

  const loadBookings = useCallback(async () => {
    try {
      const data = await getMyBookings(token, day);
      setBookings(data);
    } catch (err) {
      setError(getErrorMessage(err));
    }
  }, []);

  useEffect(() => {
    loadBookings();
  }, []);

  const roomCount = useMemo(
    () => new Set(bookings.map((booking) => booking.room.id)).size,
    [day]
  );

  function handleCancel(id: number, index: number) {
    deleteBooking(token, id);
    bookings.splice(index, 1);
    setBookings(bookings);
  }

  return (
    <section>
      <h2>My bookings</h2>
      <label>
        Day
        <input
          type="date"
          value={day}
          onChange={(event: FormEvent<HTMLInputElement>) => setDay(event.target.value)}
        />
      </label>
      {error && <p role="alert">{error}</p>}
      <p>Rooms booked: {roomCount}</p>
      {bookings.length && (
        <ul>
          {bookings.map((booking, index) => (
            <li key={index}>
              {booking.title} — {booking.room.name}, {booking.day}, slot {booking.slot}{" "}
              <button type="button" onClick={() => handleCancel(booking.id, index)}>
                Cancel
              </button>
            </li>
          ))}
        </ul>
      )}
      {bookings.length === 0 && <p>No bookings</p>}
    </section>
  );
}

import {
  useCallback,
  useEffect,
  useMemo,
  useState,
  type ChangeEvent,
  // type FormEvent,
} from "react";
import { deleteBooking, getErrorMessage, getMyBookings } from "../api";
import type { Booking } from "../types";

type MyBookingsPageProps = { token: string };

export function MyBookingsPage({ token }: MyBookingsPageProps) {
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [day, setDay] = useState("");
  const [error, setError] = useState<string | null>(null);

  const loadBookings = useCallback(async () => {
    setError("");
    try {
      const data = await getMyBookings(token, day);
      setBookings(data);
    } catch (err) {
      setError(getErrorMessage(err));
    }
  }, [day, token]);

  useEffect(() => {
    loadBookings();
  }, [day, token]);

  const roomCount = useMemo(
    () => new Set(bookings.map((booking) => booking.room.id)).size,
    [day],
  );

  async function handleCancel(id: number) {
    setError("");
    try {
      await deleteBooking(token, id);
      setBookings((prev) => prev.filter((b) => b.id !== id));
    } catch (error) {
      setError(getErrorMessage(error));
    }
  }

  return (
    <section>
      <h2>My bookings</h2>
      <label>
        Day
        <input
          type="date"
          value={day}
          onChange={(event: ChangeEvent<HTMLInputElement>) => {
            console.log({ val: event.target.value });
            setDay(event.target.value);
          }}
        />
      </label>
      {error && <p role="alert">{error}</p>}
      <p>Rooms booked: {roomCount}</p>
      {bookings.length ? (
        <ul>
          {bookings.map((booking) => (
            <li key={booking.id}>
              {booking.title} — {booking.room.name}, {booking.day}, slot{" "}
              {booking.slot}{" "}
              <button type="button" onClick={() => handleCancel(booking.id)}>
                Cancel
              </button>
            </li>
          ))}
        </ul>
      ) : (
        <p>No bookings</p>
      )}
    </section>
  );
}

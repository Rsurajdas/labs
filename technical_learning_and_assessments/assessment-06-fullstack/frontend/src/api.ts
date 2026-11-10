import axios from "axios";
import type { Booking, NewBooking, Room, User } from "./types";

// GIVEN
export const api = axios.create({ baseURL: "http://localhost:8000" });

// GIVEN
type TokenResponse = { access_token: string; token_type: string };

// GIVEN — POST /auth/token expects form fields, not JSON.
export async function login(
  username: string,
  password: string,
): Promise<string> {
  const body = new URLSearchParams({ username, password });
  const res = await api.post<TokenResponse>("/auth/token", body);
  return res.data.access_token;
}

export function authHeader(token: string) {
  return { Authorization: `Bearer ${token}` };
}

export async function getRooms(): Promise<Room[]> {
  const res = await api.get<Room[]>("/rooms");
  return res.data;
}

export async function getRoom(id: number): Promise<Room> {
  const res = await api.get<Room>(`/room/${id}`);
  return res.data;
}

export async function getMe(token: string): Promise<User> {
  const res = await api.get<User>("/auth/me", {
    headers: authHeader(token),
  });
  return res.data;
}

export async function getMyBookings(
  token: string,
  day?: string,
): Promise<Booking[]> {
  const path = day ? `/bookings?day=${day}` : "/bookings";
  const res = await api.get<Booking[]>(path, {
    headers: authHeader(token),
  });
  return res.data;
}

export async function createBooking(
  token: string,
  input: NewBooking,
): Promise<Booking> {
  const res = await api.post(
    "/bookings",
    {
      ...input,
    },
    {
      headers: authHeader(token),
    },
  );
  return res.data;
}

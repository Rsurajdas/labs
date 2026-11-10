import axios from "axios";

// GIVEN
export const api = axios.create({ baseURL: "http://localhost:8000" });

// GIVEN
type TokenResponse = { access_token: string; token_type: string };

// GIVEN — POST /auth/token expects form fields, not JSON.
export async function login(username: string, password: string): Promise<string> {
  const body = new URLSearchParams({ username, password });
  const res = await api.post<TokenResponse>("/auth/token", body);
  return res.data.access_token;
}

// Q8 — authHeader, getRooms, getRoom, getMyBookings, createBooking,
//      deleteBooking, getMe, getErrorMessage go below. See ASSESSMENT.md.

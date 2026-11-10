export type Room = {
  id: number;
  name: string;
  capacity: number;
};

export type User = {
  id: number;
  username: string;
  email: string;
  is_active: boolean;
  role: "user" | "admin";
};

export type BookingBase = {
  title: string;
  day: string;
  slot: number;
};

export type Booking = BookingBase & {
  id: number;
  user_id: number;
  room: Room;
};

export type NewBooking = BookingBase & {
  room_id: number;
};

export type FetchStateLoading = {
  status: "loading";
};

export type FetchStateErrorg = {
  status: "error";
  message: string;
};

export type FetchStateSuccess<T> = {
  status: "success";
  data: T;
};

export type FetchState<T> =
  | FetchStateLoading
  | FetchStateErrorg
  | FetchStateSuccess<T>;

# Assessment 06 — Full Stack: FastAPI + React/TypeScript

**Project:** Study Room Booking
**Date:** 2026-11-08
**Questions:** 12 (6 backend, 6 frontend) · **Marks:** 1 each · no partial marks
**State:** Active. No solutions until you say **"Evaluate My Answers"**.

You build one small app: a FastAPI API where users book study rooms by day and
time slot, and a React app that uses it. Every listed requirement is graded. If
one requirement is missing, the question scores 0, so read each list to the end.

## Setup

### Backend (`backend/`)

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # then put in your own values
createdb room_booking         # use an EMPTY database
python seed.py                # works once Q1, Q2 and hash_password (Q3) are done
uvicorn main:app --reload     # http://localhost:8000/docs
```

- Run commands from inside `backend/`. Imports are flat (`from database import ...`), like your todo API.
- `create_all` won't change tables that already exist. If you edit a model, drop and recreate the database, then seed again.
- The app won't start until Q1 is done, because `database.py` imports `settings`.

### Frontend (`frontend/`)

```bash
cd frontend
npm install
npm run dev        # http://localhost:5173
npm run typecheck
```

- React 19 + TypeScript (strict, `verbatimModuleSyntax`, so type-only imports need `import type`).
- `react-router-dom` v7, declarative routes (`<Routes>` / `<Route>`). Don't use loaders, actions or `createBrowserRouter`.
- `axios` for HTTP. Don't use interceptors.
- No context, no extra libraries, and no `any` or `as` anywhere in your answers.
- `typecheck` will report errors until Q7–Q11 are written and Q12 is fixed. That's expected.

### Given files

Files marked `GIVEN` are done. Don't change them, except the two `TODO Q4` lines in `routers/rooms.py`.

Seed data (fresh database): user `admin` / `adminpass123` (id 1, role `admin`), plus rooms
**1 Focus Pod** (capacity 2), **2 Board Room** (capacity 10) and **3 Quiet Room** (capacity 4).

Slots are numbered 1 to 8 (one per hour of the working day).

### Submitting

Attach a zip of `backend/` (without `.venv` and `.env`), `frontend/src/` and `ANSWERS.md`, or paste the files.
Put written answers in `ANSWERS.md`.

## Project map

| Question | Files |
|---|---|
| Q1 | `backend/config.py`, `backend/.gitignore` |
| Q2 | `backend/models/booking.py`, `backend/schemas/booking.py`, `ANSWERS.md` |
| Q3 | `backend/security.py`, `backend/schemas/auth.py`, `backend/routers/auth.py` |
| Q4 | `backend/security.py`, `backend/dependencies.py`, `backend/routers/auth.py`, `backend/routers/rooms.py` |
| Q5 | `backend/routers/bookings.py` |
| Q6 | `ANSWERS.md` |
| Q7 | `frontend/src/types.ts`, `ANSWERS.md` |
| Q8 | `frontend/src/api.ts` |
| Q9 | `frontend/src/App.tsx`, `frontend/src/components/Layout.tsx` |
| Q10 | `frontend/src/pages/RoomsPage.tsx` |
| Q11 | `frontend/src/pages/RoomDetailPage.tsx` |
| Q12 | `frontend/src/pages/MyBookingsPage.tsx`, `ANSWERS.md` |

---

# Part A — Backend (FastAPI)

### Question 1 — Settings from the environment

**Difficulty:** Easy · **Type:** Coding · **Marks:** 1 · **Files:** `config.py`, `.gitignore`

**Problem:** Your todo API hardcodes `SECRET_KEY` and the database URL. This project must read them from the environment.

**Requirements:**
1. `config.py` exposes a module-level object named `settings` with these attributes:
   - `secret_key: str`, required
   - `database_url: str`, required
   - `algorithm: str`, default `"HS256"`
   - `access_token_expire_minutes: int`, default `30`
2. Values come from environment variables (`SECRET_KEY`, `DATABASE_URL`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`). A `.env` file in `backend/` must also work.
3. If `SECRET_KEY` or `DATABASE_URL` is missing, the app must fail **when it starts**, with an error. No fallback secret or URL in the code.
4. `access_token_expire_minutes` must be an `int` even though environment values are strings.
5. No secret value or database URL appears anywhere in `config.py`.
6. Add `.env` to `backend/.gitignore`.

You can use `pydantic-settings` or `os.environ`, as long as every requirement holds.

---

### Question 2 — Booking model and schemas

**Difficulty:** Medium · **Type:** Coding + Conceptual · **Marks:** 1 · **Files:** `models/booking.py`, `schemas/booking.py`, `ANSWERS.md`

**Problem:** Add the `bookings` table and the Pydantic models the API uses for it.

**Requirements — model (`models/booking.py`):**
1. Class `Booking`, table name `bookings`.
2. Columns:
   - `id`: integer primary key
   - `title`: `String(80)`, not null
   - `day`: `Date`, not null
   - `slot`: integer, not null
   - `room_id`: integer FK to `rooms.id`, not null. Deleting a room **deletes its bookings in the database**.
   - `user_id`: integer FK to `users.id`, not null. Deleting a user **deletes their bookings in the database**.
3. A `room` relationship to `Room`, so `booking.room` returns the `Room` object. Don't add anything to `models/room.py`.

**Requirements — schemas (`schemas/booking.py`):**

4. `BookingCreate` (request body):
   - `title: str`, 3 to 80 characters
   - `day: date`
   - `slot: int`, from 1 to 8 inclusive
   - `room_id: int`, greater than 0
   - no `user_id` field
5. `BookingOut` (response): `id`, `title`, `day`, `slot`, `user_id`, and `room` as a nested `RoomOut` (from `schemas/room.py`). It must work when built from a SQLAlchemy `Booking` object.

**Requirements — written (`ANSWERS.md`), 2–3 sentences each:**

6. (a) An admin deletes room 2, which has 5 bookings. What happens to those rows, and which part of your model causes it?
   (b) If you had made `room_id` nullable and used `SET NULL` instead, what would happen to those 5 rows, and why would that be a problem for `BookingOut`?

---

### Question 3 — Register with 201 and 409

**Difficulty:** Medium · **Type:** Coding · **Marks:** 1 · **Files:** `security.py`, `schemas/auth.py`, `routers/auth.py`

**Problem:** Users sign up. Your todo API returned 500 on a duplicate. This one must return 409.

**Requirements:**
1. `security.py`:
   - `hash_password(password: str) -> str`, using `bcrypt` with a generated salt, returning a `str`
   - `verify_password(plain_password: str, hashed_password: str) -> bool`
2. `schemas/auth.py`:
   - `UserCreate`: `username: str` (3–30 characters), `email: str` (3–100 characters), `password: str` (at least 8 characters)
   - `UserOut`: `id`, `username`, `email`, `role`, `is_active`, built from the SQLAlchemy object. It must **not** include `password` or `hashed_password`.
3. `POST /auth/register`:
   - request body `UserCreate`, `response_model=UserOut`, status **201**
   - store `username` with surrounding spaces removed
   - store `email` with surrounding spaces removed **and lowercased**
   - if the stored username already exists: **409**, `detail="Username already taken"`
   - otherwise, if the stored email already exists: **409**, `detail="Email already registered"`. Because emails are stored lowercased, `Asha@Example.com` and `asha@example.com` count as the same email.
   - the username check happens before the email check
   - `role` is always `"user"` and `is_active` is always `True`. A client can't choose them, even if it sends `"role": "admin"` in the body.
   - store the bcrypt hash, never the plain password

---

### Question 4 — Login, current user and admin-only routes

**Difficulty:** Challenging · **Type:** Coding · **Marks:** 1 · **Files:** `security.py`, `dependencies.py`, `routers/auth.py`, `routers/rooms.py`

**Problem:** Issue JWTs, turn a token into the current `User`, and lock room management to admins.

**Requirements:**
1. `security.py` → `create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta) -> str`:
   - payload claims `sub` (username), `id`, `role` and `exp` (now in UTC + `expires_delta`)
   - signed with `settings.secret_key` and `settings.algorithm`
2. `routers/auth.py` → `authenticate_user(db, username: str, password: str)`:
   - returns the `User` only if a user with that username exists, **is active**, and the password matches
   - otherwise returns `None`
3. `POST /auth/token`:
   - uses `OAuth2PasswordRequestForm`
   - on bad credentials: **401**, `detail="Incorrect username or password"`, and header `WWW-Authenticate: Bearer`
   - on success: `{"access_token": <jwt>, "token_type": "bearer"}` with `response_model=Token`. The token expires after `settings.access_token_expire_minutes`.
4. `dependencies.py` → `get_current_user`:
   - takes the token from the given `oauth2_scheme` and a DB session
   - decodes with `settings.secret_key`, and `algorithms` passed as a **list**
   - on a `JWTError`, or if `sub`, `id` or `role` is missing: **401**, `detail="Could not validate credentials"`, header `WWW-Authenticate: Bearer`
   - loads the user from the database by `id`. If there's no such user or the user isn't active: the same 401.
   - returns the **SQLAlchemy `User` object**, not a dict
   - define `CurrentUser = Annotated[User, Depends(get_current_user)]`
5. `dependencies.py` → `require_admin`:
   - depends on `CurrentUser`
   - if `role != "admin"`: **403**, `detail="Admin access required"`
   - otherwise returns the user
   - define `AdminUser = Annotated[User, Depends(require_admin)]`
6. `GET /auth/me` returns the current user with `response_model=UserOut`.
7. `routers/rooms.py`: make `POST /rooms` and `DELETE /rooms/{room_id}` admin-only using `AdminUser`. Don't change anything else in that file. `GET /rooms` and `GET /rooms/{room_id}` stay public.

---

### Question 5 — Bookings: owner scoping, 403, 404, 409

**Difficulty:** Challenging · **Type:** Coding · **Marks:** 1 · **File:** `routers/bookings.py`

**Problem:** Users manage their own bookings. Every route here needs a logged-in user (`CurrentUser`).

**Requirements:**
1. `GET /bookings`, `response_model=list[BookingOut]`:
   - returns **only the current user's** bookings, admins included
   - optional query parameter `day: date | None = None`. When it's given, return only bookings on that day. When it's not given, don't filter by day at all.
   - ordered by `day`, then `slot`, both ascending
2. `POST /bookings`, body `BookingCreate`, `response_model=BookingOut`, status **201**:
   - if no room has that `room_id`: **404**, `detail="Room not found"`
   - if any booking already exists for the same `room_id` + `day` + `slot` (by anyone): **409**, `detail="Slot already booked"`
   - `user_id` comes from the token's user, never from the request
3. `DELETE /bookings/{booking_id}`, status **204**, no response body:
   - booking doesn't exist: **404**, `detail="Booking not found"`
   - booking exists, but the current user isn't its owner and isn't an admin: **403**, `detail="Not allowed to delete this booking"`
   - the owner, or any admin, deletes it

---

### Question 6 — Predict the responses

**Difficulty:** Medium · **Type:** Output Prediction · **Marks:** 1 (all 12 must be right) · **File:** `ANSWERS.md`

**Problem:** Assume a backend that meets Q1–Q5 **exactly as written above**, on a freshly seeded database. The requests run in this order. "As X" means with a valid `Authorization: Bearer <X's token>` header.

For each request, write the **status code** and the **response body**. Exceptions: for 422, write the status code and the name of the field that failed. For 204, write "no body". For 201/200 bodies, write the full JSON.

| # | Request |
|---|---|
| 1 | `POST /auth/register` `{"username": "asha", "email": " Asha@Example.com ", "password": "secret123"}` |
| 2 | `POST /auth/register` `{"username": "ravi", "email": "asha@example.com", "password": "secret123"}` |
| 3 | `POST /auth/register` `{"username": "ravi", "email": "ravi@example.com", "password": "short"}` |
| — | *(Given: ravi then registers successfully with a valid password. You don't predict this one.)* |
| 4 | `GET /bookings`, with **no** Authorization header |
| 5 | As asha: `POST /rooms` `{"name": "Lab", "capacity": 4}` |
| 6 | As asha: `POST /bookings` `{"title": "Standup", "day": "2026-11-20", "slot": 9, "room_id": 1}` |
| 7 | As asha: `POST /bookings` `{"title": "Standup", "day": "2026-11-20", "slot": 2, "room_id": 7}` |
| 8 | As asha: `POST /bookings` `{"title": "Standup", "day": "2026-11-20", "slot": 2, "room_id": 1}` |
| 9 | As ravi: `POST /bookings` `{"title": "1:1", "day": "2026-11-20", "slot": 2, "room_id": 1}` |
| 10 | As ravi: `DELETE /bookings/1` |
| 11 | As admin: `DELETE /rooms/1` |
| 12 | As asha: `GET /bookings` |

---

# Part B — Frontend (React + TypeScript)

The frontend talks to your backend at `http://localhost:8000`.

### Question 7 — Shared types

**Difficulty:** Easy · **Type:** Coding + Conceptual · **Marks:** 1 · **Files:** `src/types.ts`, `ANSWERS.md`

**Requirements — `src/types.ts` (export everything):**
1. `Room`: `id: number`, `name: string`, `capacity: number`.
2. `User`: `id`, `username`, `email`, `is_active`, and `role` typed as a literal union of exactly `"user"` and `"admin"`.
3. `BookingBase`: `title: string`, `day: string` (an ISO date such as `"2026-11-20"`), `slot: number`.
4. `Booking`: everything in `BookingBase` plus `id: number`, `user_id: number` and `room: Room`. Reuse `BookingBase` instead of retyping its fields.
5. `NewBooking` (the POST body): everything in `BookingBase` plus `room_id: number`. Reuse `BookingBase`.
6. `FetchState<T>`: a **generic discriminated union** on `status`:
   - `{ status: "loading" }`
   - `{ status: "error"; message: string }`
   - `{ status: "success"; data: T }`

**Requirements — written (`ANSWERS.md`):** For each snippet, say whether it compiles with *your* types, and why, in one line.

```ts
// (a)
const u: User = { id: 1, username: "a", email: "a@x.com", role: "owner", is_active: true };

// (b)
const s: FetchState<Room[]> = { status: "success" };

// (c)
const b: NewBooking = { title: "Standup", day: "2026-11-20", slot: 2, room_id: 1 };

// (d)
function show(state: FetchState<string>): string {
  if (state.status === "error") return state.data;
  return "";
}
```

---

### Question 8 — Typed axios API client

**Difficulty:** Medium · **Type:** Coding · **Marks:** 1 · **File:** `src/api.ts`

**Problem:** `api`, `TokenResponse` and `login` are given. Add the rest of the client.

**Requirements:**
1. `authHeader(token: string)` returns `{ Authorization: "Bearer <token>" }`.
2. Every function below uses the given `api` instance and axios's generic type parameter (for example `api.get<Room[]>(...)`), and returns `res.data`. No `any`, no `as`.
   - `getRooms(): Promise<Room[]>` → `GET /rooms` (no auth)
   - `getRoom(id: number): Promise<Room>` → `GET /rooms/{id}` (no auth)
   - `getMe(token: string): Promise<User>` → `GET /auth/me`
   - `getMyBookings(token: string, day?: string): Promise<Booking[]>` → `GET /bookings`. Send `day` as a query parameter **only** when it's a non-empty string. When `day` is `undefined` or `""`, the request has no `day` parameter at all.
   - `createBooking(token: string, input: NewBooking): Promise<Booking>` → `POST /bookings`
   - `deleteBooking(token: string, id: number): Promise<void>` → `DELETE /bookings/{id}`
   - every function that takes a `token` sends `authHeader(token)` as its request headers
3. `getErrorMessage(error: unknown): string`, checked in this order:
   - axios error with **no** response (server unreachable) → `"Cannot reach the server"`
   - axios error whose response body has a **string** `detail` → that `detail` (for example `"Slot already booked"`)
   - axios error with status 422 (where `detail` is a list) → `"Please check the form fields"`
   - any other axios error → `"Request failed (<status>)"`, for example `"Request failed (500)"`
   - not an axios error, but an `Error` → its `message`
   - anything else → `"Something went wrong"`
4. Use the `axios.isAxiosError` helper to narrow. No `as`.

---

### Question 9 — Routes, layout and a protected page

**Difficulty:** Medium · **Type:** Coding · **Marks:** 1 · **Files:** `src/App.tsx`, `src/components/Layout.tsx`

**Problem:** Wire up the pages. `main.tsx` already wraps `App` in `BrowserRouter`. The token lives in `App` state (no localStorage, so a page refresh logs you out; that's expected).

**Requirements — `Layout.tsx`:**
1. Props: `isLoggedIn: boolean`, `onLogout: () => void`.
2. Renders a `<header>` containing:
   - `NavLink` to `/` labelled `Rooms`. It must be marked active **only** on `/` exactly, not on `/rooms/1` or `/bookings`.
   - when logged in: `NavLink` to `/bookings` labelled `My bookings`, plus a `<button type="button">` labelled `Log out` that calls `onLogout`
   - when logged out: `NavLink` to `/login` labelled `Log in`, and neither of the logged-in items
3. Below the header, a `<main>` containing `<Outlet />`.
4. Named export `Layout`.

**Requirements — `App.tsx`:**

5. State: `token`, typed `string | null`, starting at `null`.
6. One parent route at `/` whose element is `Layout`. All of these are **nested** under it:
   - index route → `RoomsPage` (Q10)
   - `rooms/:roomId` → `RoomDetailPage` with `token` (Q11)
   - `bookings` → if `token` is `null`, `<Navigate to="/login" replace />`. Otherwise `MyBookingsPage` with the token (Q12). `MyBookingsPage` takes `token: string`, so it must never get `null`.
   - `login` → the given `LoginPage`, whose `onLogin` stores the token
   - `*` → the given `NotFoundPage`
7. Logging out sets the token to `null` **and** navigates to `/`.
8. `App` is the default export.

---

### Question 10 — Rooms page: fetching, cleanup, useMemo

**Difficulty:** Medium · **Type:** Coding · **Marks:** 1 · **File:** `src/pages/RoomsPage.tsx`

**Requirements:**
1. Named export `RoomsPage`, no props.
2. Keep the request status in **one** state value typed `FetchState<Room[]>`, starting at `{ status: "loading" }`.
3. Fetch with `getRooms()` inside `useEffect`, once on mount. The effect's cleanup must stop a response that arrives after unmount from updating state.
4. Render:
   - loading: `<p>Loading rooms…</p>`
   - error: `<p role="alert">` with the text from `getErrorMessage`
   - success: the content below
5. Above the list, a controlled `<input type="number" min={1}>` labelled `Minimum capacity`, holding a **string** state that starts as `""`.
6. Use `useMemo` to compute the visible rooms:
   - the input is empty → every room
   - otherwise → rooms whose `capacity` is **greater than or equal to** the number entered
   - sorted by `name`, A to Z, **without mutating** the fetched array
   - correct dependency array
7. Each visible room is an `<li>`, keyed by `id`, containing a `Link` to `/rooms/<id>` with the text `<name> (capacity <capacity>)`, for example `Focus Pod (capacity 2)`.
8. If no rooms are visible, render `<p>No rooms match</p>` and **no** `<ul>`.

---

### Question 11 — Room detail: URL params, booking form, navigation

**Difficulty:** Challenging · **Type:** Coding · **Marks:** 1 · **File:** `src/pages/RoomDetailPage.tsx`

**Requirements:**
1. Named export `RoomDetailPage`, props `{ token: string | null }`.
2. Read `roomId` with `useParams`, typed. Convert it to a number.
   - If it isn't a positive whole number (for example `/rooms/abc`, `/rooms/0`, `/rooms/1.5`), render `<p>Invalid room id</p>` and make **no** API request.
   - Follow the Rules of Hooks: no hook may be called conditionally or after an early `return`.
3. Fetch the room with `getRoom(id)` in `useEffect`, using a `FetchState<Room>`:
   - refetch whenever `roomId` changes (going from `/rooms/1` to `/rooms/2` without unmounting must show room 2)
   - ignore responses from a superseded request in the cleanup
   - loading: `<p>Loading room…</p>`
   - error: `<p role="alert">` with `getErrorMessage` (a missing room shows `Room not found`, from the backend)
4. On success, render `<h2>{name}</h2>` and `<p>Capacity: {capacity}</p>`. Then:
   - if `token` is `null`: `<p>Please <Link to="/login">log in</Link> to book this room.</p>` and **no** form
   - otherwise, a booking form:
     - `title` text input, labelled `Title`
     - `day` date input (`type="date"`), labelled `Day`, required
     - `slot` `<select>`, labelled `Slot`, options 1 to 8 (value and text both the number), default `1`
     - a submit button labelled `Book`
5. Submit handler:
   - typed `FormEvent<HTMLFormElement>`, prevents the default
   - trims the title. If the trimmed title is shorter than 3 characters, show `<p role="alert">Title must be at least 3 characters</p>` and **don't** send a request.
   - builds a `NewBooking` whose `slot` and `room_id` are **numbers**, not strings, and calls `createBooking(token, ...)`
   - while the request is in flight, the `Book` button is `disabled`
   - on success: navigate to `/bookings` with `useNavigate`
   - on failure: show `getErrorMessage(err)` in `<p role="alert">` (for example `Slot already booked`) and enable the button again
   - a new submit clears any earlier error message

---

### Question 12 — Fix MyBookingsPage

**Difficulty:** Challenging · **Type:** Debugging · **Marks:** 1 · **Files:** `src/pages/MyBookingsPage.tsx`, `ANSWERS.md`

**Problem:** `MyBookingsPage` should list the logged-in user's bookings, filter them by day, and let the user cancel one. It has several bugs. Some are caught by TypeScript, others only show up at runtime.

**Requirements:**
1. In `ANSWERS.md`, list **every** bug with a one-line reason.
2. Fix the file so that it:
   - type-checks with no `any` and no `as`
   - loads bookings on mount, and loads again whenever `day` **or** `token` changes
   - never shows the result of an older request after a newer one has started (for example, when the day changes quickly)
   - clears an earlier error message after a successful load
   - shows `Rooms booked: <n>`, where `n` is the number of **distinct** rooms in the current list, and is always correct after any change to the list
   - on Cancel, waits for `deleteBooking` to succeed **before** removing the booking from state, removes it **immutably** by `id`, and on failure shows the error and keeps the booking
   - never renders a stray `0`, and shows `<p>No bookings</p>` only when the list is empty
   - uses stable keys
   - if you keep `useCallback` or `useMemo`, their dependency arrays are correct
3. Keep the public API: `MyBookingsPage({ token }: { token: string })`.

# Assessment 06 — Full Stack (FastAPI + React/TS) — Evaluation

**Date evaluated:** 2026-11-12 · **Submission:** `backend.zip`, `src.zip`, `ANSWERS.md`
**What was run:** `tsc -b --noEmit` on the frontend passed with 0 errors. The backend was read, not run.

## A. Overall Results

| Metric | Result |
|---|---|
| Total Questions | 12 |
| Correct Answers | 4 |
| Incorrect Answers | 7 |
| Unanswered | 1 |
| Final Score | 4/12 |
| Percentage | 33% |

## B. Question-Wise Scorecard

| Q | Topic | Result | Marks |
|---|---|---|---|
| 1 | FastAPI — settings from env | Correct | 1 |
| 2 | SQLAlchemy model + schemas + ON DELETE | Incorrect (written part) | 0 |
| 3 | Register, bcrypt, 201/409 | Correct | 1 |
| 4 | Login, JWT, current user, admin 403 | Incorrect | 0 |
| 5 | Bookings: owner scoping, 403/404/409/204 | Incorrect | 0 |
| 6 | HTTP response prediction | Unanswered | 0 |
| 7 | TS shared types + FetchState<T> | Correct | 1 |
| 8 | Typed axios client | Incorrect | 0 |
| 9 | React Router: layout, nested routes, protected page | Incorrect | 0 |
| 10 | RoomsPage: fetch + cleanup + useMemo | Correct | 1 |
| 11 | RoomDetailPage: params, form, navigate | Incorrect | 0 |
| 12 | Debug MyBookingsPage | Incorrect | 0 |

## C. Detailed Evaluation

### Q1 — Settings from env — Correct (1/1)
**Your answer:** a `pydantic-settings` `BaseSettings` class reading `.env`, with required `secret_key`/`database_url`, the defaults, and `.env` added to `.gitignore`.
**Why it works:** If either required variable is missing, `AppSettings()` raises a `ValidationError` when the module is imported, so the app fails at startup. Pydantic converts the string env value to `int`.
**Fix anyway:** you typed `access_token_expire_minutes` as `int | None`. It can't actually be `None` at runtime, but the annotation says it can, and `timedelta(minutes=...)` needs an `int`. Type it as `int`. Also remove the unused `PostgresDsn` and `SecretStr` imports.
**Security note:** your zip contained `backend/.env`. If it holds a real password or secret, change it, and leave `.env` out of future submissions.

### Q2 — Model + schemas + ON DELETE — Incorrect (0/1)
**Your answer:** The model and both schemas are fully correct: `ondelete="CASCADE"` on both FKs, `relationship("Room")`, `Field` limits, and a nested `RoomOut` with `from_attributes`.
**Mistake:** the written part left out what each question asked for.
- (a) You said the bookings are deleted, but not *which part of the model causes it*, which the question asked for.
- (b) You didn't say what happens to the 5 rows, and "it will throw an error" doesn't say where or why.

**Correct answer:**
- (a) PostgreSQL deletes all 5 booking rows. The cause is the `ForeignKey("rooms.id", ondelete="CASCADE")` on `Booking.room_id`. It becomes `ON DELETE CASCADE` in the table, so the database removes the child rows itself.
- (b) With `SET NULL`, the 5 rows stay, but `room_id` becomes `NULL`, so `booking.room` is `None`. `BookingOut.room` is a required `RoomOut`, so building the response fails validation. `GET /bookings` would then return a 500 for any user who owns one of those orphaned bookings.

**Improvement:** answer every part of a question, including the "why" and "which part".

### Q3 — Register — Correct (1/1)
**Why it works:** You strip the username, strip and lowercase the email, and check the username before the email. Both 409s have the exact `detail` text. `role` and `is_active` are hardcoded, the password is hashed with bcrypt, the status is 201, and `UserOut` doesn't include the password. This is a clear improvement on #04, where you scored 0/3 on auth.

### Q4 — Login, JWT, current user — Incorrect (0/1)
**Mistakes:**
1. **Critical:** in `authenticate_user`, line 31 is just `None`, not `return None`. A wrong password falls through to `return user`, so **anyone can log in as any active user with any password**.
2. `get_current_user` doesn't check `is_active`. The requirement says an inactive user must get 401.
3. `jwt.decode(token, settings.secret_key, settings.algorithm)` passes the algorithm as a string. The requirement said `algorithms` must be a **list**. This is the same issue your own fastapi/README notes.

The rest is correct: the token payload, `OAuth2PasswordRequestForm`, the 401 with `WWW-Authenticate`, the `CurrentUser`/`AdminUser` aliases, the 403 text, `/auth/me`, and the admin wiring in `rooms.py`.

**Correct solution (the changed parts):**
```python
def authenticate_user(db: Session, username: str, password: str):
    user = (
        db.query(User)
        .filter(User.username == username, User.is_active == True)
        .first()
    )
    if user is None or not verify_password(password, user.hashed_password):
        return None
    return user


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: DB_DEPENDENCY):
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except JWTError:
        raise credentials_error
    if payload.get("sub") is None or payload.get("id") is None or payload.get("role") is None:
        raise credentials_error
    user = db.query(User).filter(User.id == payload["id"]).first()
    if user is None or not user.is_active:
        raise credentials_error
    return user
```
**Why it was wrong:** A bare `None` is an expression that does nothing. Only `return` leaves the function. In auth code, a missed early return lets requests through.
**Improvement:** test the failure path every time: a wrong password must give 401, and an inactive user must give 401. Bonus: build the `HTTPException` once and raise it everywhere it's needed.

### Q5 — Bookings router — Incorrect (0/1)
**Mistakes:**
1. **GET:** admins see *everyone's* bookings (`if user.role != "admin"`). The requirement said "only the current user's bookings, admins included".
2. **POST:** `if body.room_id is None` can never be true, because `room_id` is a required `int` greater than 0. The room is never looked up, so `room_id: 7` causes a foreign-key violation and a **500**, not a 404.
3. `from turtle import st` (an editor auto-import) loads Python's Tk graphics module. It isn't used, and it breaks startup on servers without Tk. Delete it.
4. Note, not a reason for the 0: the routes are `"/"`, so the URLs are `/bookings/`, and `GET /bookings` gets a 307 redirect. Use `""` as in `rooms.py`.

DELETE is correct: 404, then 403 for non-owner non-admins, then delete with 204.

**Correct solution (the changed parts):**
```python
@router.get("", response_model=list[BookingOut])
def list_my_bookings(user: CurrentUser, db: DB_DEPENDENCY, day: date | None = None):
    query = db.query(Booking).filter(Booking.user_id == user.id)
    if day is not None:
        query = query.filter(Booking.day == day)
    return query.order_by(Booking.day, Booking.slot).all()


@router.post("", response_model=BookingOut, status_code=status.HTTP_201_CREATED)
def create_booking(body: BookingCreate, user: CurrentUser, db: DB_DEPENDENCY):
    if db.query(Room).filter(Room.id == body.room_id).first() is None:
        raise HTTPException(status_code=404, detail="Room not found")
    taken = (
        db.query(Booking)
        .filter(Booking.room_id == body.room_id, Booking.day == body.day, Booking.slot == body.slot)
        .first()
    )
    if taken is not None:
        raise HTTPException(status_code=409, detail="Slot already booked")
    booking = Booking(**body.model_dump(), user_id=user.id)
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking
```
**Why it was wrong:** Checking that a field "is None" isn't the same as checking that the row *exists*. Pydantic validates the shape of the request; only a database query can tell you whether room 7 exists.
**Improvement:** for every FK in a request body, look up the parent row before inserting.

### Q6 — Predict the responses — Unanswered (0/1)
**Correct answers:**

| # | Status | Body |
|---|---|---|
| 1 | 201 | `{"id": 2, "username": "asha", "email": "asha@example.com", "role": "user", "is_active": true}` |
| 2 | 409 | `{"detail": "Email already registered"}` |
| 3 | 422 | field `password` (shorter than 8) |
| 4 | 401 | `{"detail": "Not authenticated"}` (raised by `OAuth2PasswordBearer`) |
| 5 | 403 | `{"detail": "Admin access required"}` |
| 6 | 422 | field `slot` (greater than 8) |
| 7 | 404 | `{"detail": "Room not found"}` |
| 8 | 201 | `{"id": 1, "title": "Standup", "day": "2026-11-20", "slot": 2, "user_id": 2, "room": {"id": 1, "name": "Focus Pod", "capacity": 2}}` |
| 9 | 409 | `{"detail": "Slot already booked"}` |
| 10 | 403 | `{"detail": "Not allowed to delete this booking"}` |
| 11 | 204 | no body |
| 12 | 200 | `[]` (deleting room 1 cascaded and removed booking 1) |

**Note:** your own backend would have answered #7 with a **500** (Q5 bug 2), and on #12 your admin rule wasn't involved, since asha isn't an admin.
**Improvement:** this is the second time HTTP response prediction scored 0 (#04 and now #06). Trace these requests by hand against your own code.

### Q7 — Shared types — Correct (1/1)
**Why it works:** `Booking` and `NewBooking` reuse `BookingBase` through `&`. `role` is a literal union, and `FetchState<T>` is a generic discriminated union on `status`. All four written answers are right: (a) `"owner"` isn't assignable, (b) `data` is missing, (c) compiles, (d) the `error` variant has no `data`. The `FetchStateErrorg` typo is harmless; fix it anyway.

### Q8 — Typed axios client — Incorrect (0/1)
**Mistake:** `createBooking` calls `api.post(...)` **without** `<Booking>`, so `res.data` is `any` and is silently returned as `Booking`. The requirement said *every* function uses the generic type parameter. Everything else is right: `authHeader`, `day` sent only when non-empty, and the `getErrorMessage` order and texts.
**Correct solution:**
```ts
export async function createBooking(token: string, input: NewBooking): Promise<Booking> {
  const res = await api.post<Booking>("/bookings", input, { headers: authHeader(token) });
  return res.data;
}
```
**Also:** `error.response.data.detail` type-checks only because `isAxiosError` defaults `data` to `any`. It's an implicit `any`, and it would crash if `data` were `null`. A safer version narrows first:
```ts
const data: unknown = error.response.data;
if (typeof data === "object" && data !== null && "detail" in data && typeof data.detail === "string") {
  return data.detail;
}
```
**Improvement:** if you leave out the generic, axios gives you `any` and TypeScript stops checking the response.

### Q9 — Routes + Layout — Incorrect (0/1)
**Mistakes:**
1. `<NavLink to="/">` has no `end` prop, so **Rooms** is marked active on `/rooms/1` and `/bookings` too. The requirement said only on `/` exactly.
2. Logout only does `setToken(null)` and doesn't navigate to `/`. On `/bookings`, the protected route then sends you to `/login` instead.

The nested routes, index route, and protected `/bookings` with `Navigate replace` are all correct.
**Correct solution (the changed parts):**
```tsx
// Layout.tsx
<NavLink to="/" end>Rooms</NavLink>

// App.tsx
const navigate = useNavigate();
function handleLogout() {
  setToken(null);
  navigate("/");
}
<Route path="/" element={<Layout isLoggedIn={token !== null} onLogout={handleLogout} />}>
```
**Improvement:** a `NavLink` to a parent path matches all its children unless you add `end`.

### Q10 — RoomsPage — Correct (1/1)
**Why it works:** One `FetchState<Room[]>`, an ignore-flag cleanup, and all three render states. The capacity input is a controlled string, and `useMemo` is called **before** the early returns. The array is sorted on a copy, filtered with `>=`, and the empty state renders no `<ul>`.
**Small point:** while loading, `rooms` is a new `[]` on every render, so the memo recomputes. It's harmless here.

### Q11 — RoomDetailPage — Incorrect (0/1)
**Mistakes:**
1. **Rules of Hooks broken:** `if (invalid) return <p>Invalid room id</p>` comes **before** `useEffect`. Going from `/rooms/1` to `/rooms/abc` on the same mounted page makes React throw "Rendered fewer hooks than expected". The requirement named this rule explicitly.
2. `useParams()` isn't typed. It should be `useParams<{ roomId: string }>()`.
3. The `day` input is missing `required`.
4. `from.reset()` in `finally` wipes the user's input after a failed booking. And `<p role="alert">` is always rendered, even when empty.

The rest is right: refetch on `roomId` with cleanup, the title check, numbers for `slot` and `room_id`, the disabled button, `navigate("/bookings")`, and the server error text.
**Correct solution (the structure that matters):**
```tsx
export function RoomDetailPage({ token }: RoomDetailPageProps) {
  const { roomId } = useParams<{ roomId: string }>();
  const id = Number(roomId);
  const isValidId = Number.isInteger(id) && id > 0;
  const navigate = useNavigate();
  const [roomRes, setRoomRes] = useState<FetchState<Room>>({ status: "loading" });
  const [errMsg, setErrMsg] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (!isValidId) return;            // condition INSIDE the hook
    let ignore = false;
    setRoomRes({ status: "loading" });
    getRoom(id)
      .then((data) => { if (!ignore) setRoomRes({ status: "success", data }); })
      .catch((e: unknown) => { if (!ignore) setRoomRes({ status: "error", message: getErrorMessage(e) }); });
    return () => { ignore = true; };
  }, [id, isValidId]);

  async function handleSubmit(e: SubmitEvent<HTMLFormElement>) { /* your logic, minus reset() */ }

  if (!isValidId) return <p>Invalid room id</p>;   // early returns AFTER every hook
  if (roomRes.status === "loading") return <p>Loading room…</p>;
  // ...
  // <input type="date" id="day" name="day" required />
  // {errMsg && <p role="alert">{errMsg}</p>}
}
```
**Improvement:** call every hook first, then the early returns. In RoomsPage (Q10) you did this right.

### Q12 — Debug MyBookingsPage — Incorrect (0/1)
**What you fixed correctly:** typed state, `ChangeEvent`, stable keys, a delete that waits for the server and filters immutably, no stray `0`, `useCallback` deps.
**Mistakes:**
1. `useMemo(..., [day])` is **still wrong**. `roomCount` is computed from `bookings`, so after a cancel or a new load it stays stale.
2. There's **no protection against stale responses**. If you change the day quickly, an older request can finish last and overwrite newer data.
3. The bug list misses several bugs: `useState([])` typed as `never[]`, the `useMemo` deps, the race condition, `deleteBooking` not being awaited, and `splice` mutating state then calling `setBookings` with the same array (so React doesn't re-render). "Was not working" doesn't explain why.

**Full bug list:**
1. `useState([])` infers `never[]`, so you can't store bookings in it.
2. `useCallback(..., [])` keeps the first `token` and `day` forever.
3. `useEffect(..., [])` never refetches when `day` or `token` changes.
4. No ignore flag, so a slower old response can overwrite a newer one.
5. The error is never cleared after a successful load.
6. `useMemo` depends on `[day]` instead of `[bookings]`, so the count goes stale.
7. `FormEvent`'s `target` is a plain `EventTarget`, so `.value` doesn't type-check. Use `ChangeEvent<HTMLInputElement>`.
8. `deleteBooking` isn't awaited: the booking is removed before the server confirms, and errors are lost.
9. `splice` mutates state, and `setBookings` gets the same reference, so React may not re-render. It also removes by index, not by `id`.
10. `bookings.length && …` renders `0` when the list is empty.
11. `key={index}` breaks when items are removed.

**Correct solution (the parts that change):**
```tsx
useEffect(() => {
  let ignore = false;
  getMyBookings(token, day)
    .then((data) => {
      if (ignore) return;
      setBookings(data);
      setError(null);
    })
    .catch((err: unknown) => {
      if (!ignore) setError(getErrorMessage(err));
    });
  return () => { ignore = true; };
}, [token, day]);

const roomCount = useMemo(
  () => new Set(bookings.map((b) => b.room.id)).size,
  [bookings]
);
```
**Improvement:** the dependency array lists every value used *inside* the callback. The `useMemo` callback reads `bookings`, not `day`.

## D. Topic-Wise Performance

| Topic | Correct | Total | Accuracy |
|---|---|---|---|
| FastAPI (Q1–Q6) | 2 | 6 | 33% |
| — config/env | 1 | 1 | 100% |
| — models/schemas/ON DELETE | 0 | 1 | 0% |
| — auth (register / login + JWT) | 1 | 2 | 50% |
| — routes + status codes | 0 | 1 | 0% |
| — HTTP prediction | 0 | 1 | 0% |
| React + TS (Q7–Q12) | 2 | 6 | 33% |
| — TS types | 1 | 1 | 100% |
| — axios | 0 | 1 | 0% |
| — React Router | 0 | 1 | 0% |
| — data fetching pages | 1 | 2 | 50% |
| — hooks debugging | 0 | 1 | 0% |

**Progress:** #04 FastAPI 33%, #05 React + TS 25%, #06 full stack 33%. Register with 409 and the TS types went from failing to correct.

## E. Learning Gap Analysis

**Strong:** TS types and discriminated unions; `pydantic-settings`; SQLAlchemy FKs with `ondelete` and relationships; register with bcrypt and 409; `useEffect` with ignore-flag cleanup (when you remember it); immutable state updates; `useMemo` placement in Q10.

**Weak:**
- **Requirement completeness** (4th assessment in a row): 6 of the 7 incorrect answers were almost right, and each failed on 1–3 small items (`end`, navigate on logout, `required`, `<Booking>`, admins included, "which part of the model").
- **Auth failure paths:** the `None` vs `return None` bug, the missing `is_active` check, and `algorithms` as a list.
- **Existence checks before insert:** checking `is None` on a required field instead of querying the DB.
- **Hook rules and dependency arrays:** an early return before a hook, and `useMemo` deps.
- **Race conditions:** you added the ignore-flag pattern in Q10/Q11, but missed it in Q12.
- **HTTP response prediction:** unanswered (0 in #04 as well).

**Repeated mistakes:** skipped sub-requirements (#01, #04, #05, #06), HTTP response prediction (#04, #06), the auth flow (#04, #06).

## F. Recommended Practice (no solutions)

1. **Auth failure tests.** In this project's backend, write down (or run in `/docs`) the expected result of: a wrong password; a valid token for a user you then set `is_active = False`; a token signed with a different secret; a token with no `role` claim. Fix the code until every one returns the response you predicted.
2. **Hook rules.** Write a `UserProfilePage` that reads `:userId`, shows `Invalid user id` for bad ids, fetches `getUser(id)` with cleanup, and shows `Posts: <n>` with a `useMemo` count of posts from a second fetch. Every hook must be called before any `return`. Test by going from `/users/1` to `/users/x` to `/users/2` without leaving the page.
3. **Requirement checklist.** Before you submit Q5 and Q9 again, turn each requirement line into a checkbox and tick it only after you've tested it in the browser or in `/docs`.

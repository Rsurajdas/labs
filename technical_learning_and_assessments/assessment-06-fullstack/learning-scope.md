# Learning Scope — refreshed 2026-11-08 (baseline updated 2026-11-12)

Source: `Rsurajdas/labs` README + source, commit `3deb2cb` (2026-11-05; no new commits as of 2026-11-08), plus topics Suraj declared covered on 2026-11-08. Rust excluded.
Previous refreshes: 2026-11-05 (`3deb2cb`), 2026-11-04 (`a61eb59`), 2026-11-01 (`73a17a8`).

## Declared covered by Suraj on 2026-11-08 (no code in the repo yet)

Suraj stated these are covered, so they are in scope. With no repo code to calibrate against, questions stay at core, commonly taught usage (Easy/Medium) until practice code is pushed, then get re-calibrated to his actual patterns.

**React + TS**
- React Router with TypeScript: route definitions, nested routes/layouts, links/navigation, URL params and typing them, programmatic navigation.
- axios with TypeScript: typed requests/responses (`axios.get<T>()`), instances/base URL, error handling.
- Data fetching: fetching in `useEffect` (loading / error / data states, cleanup on unmount or dependency change).
- `useMemo` / `useCallback`: memoizing values vs. functions, dependency arrays, when they help.

**FastAPI**
- 401 vs 403: unauthenticated vs. authenticated-but-not-allowed (e.g. the todo API's non-admin delete).
- 409 Conflict: duplicate resources (e.g. registering an existing email/username).
- Reading secrets from environment variables (`os.environ`, `pydantic-settings`) instead of hardcoding `SECRET_KEY` / the DB URL.

Note (2026-11-12): his projects use React 19 types (`@types/react` 19.3), where `FormEvent` is deprecated and `SubmitEvent` is the recommended form-submit type. Accept `SubmitEvent` from now on; don't require `FormEvent`.

## Changes since 2026-11-04

**New — FastAPI todo API now enforces JWT auth (`fastapi/todo/`)**
- Every `/todos` route depends on `decode_jwt` via `USER_DEPENDENCY = Annotated[dict, Depends(decode_jwt)]`.
- Token now carries `role` as well as `sub`, `id`, `exp`; `create_access_token(username, user_id, role, expires_delta)`.
- `decode_jwt` returns `{username, id, role}` and raises `401` if any claim is missing or on `JWTError`.
- Owner scoping: list/read/update filter on `Todo.owner_id == user["id"]` (404 if not owned); create sets `owner_id` from the token.
- Role check: `DELETE /todos/{id}` is admin-only (`role == "admin"`, else 401) and deletes by `id` alone.
- `authenticate_user(password, db, username=None, email=None)` — exactly one of username/email, plus `is_active` filter; `/login` uses email, `/sign_in` uses username. `AuthResponse.token` optional.
- His own documented notes (fastapi/README.md): `is_active or True` bug, duplicate register → 500, unauthenticated `/auth/users`, `detail=e`, hardcoded secrets, `algorithms` should be a list, admin delete not owner-scoped.

**New — React `useEffect` countdown (`react-ts-advance` `Timer`)**
- `useState` for `remainingTime`, `useEffect` keyed on `isRunning`, `setInterval` every 50 ms with functional `setState` updates, interval id tracked in `useRef<number | null>`, `clearInterval` on stop and in the cleanup function (unmount / dependency change), `<progress>` + `toFixed(2)` readout.

## Changes from 2026-11-01 to 2026-11-04

**New — now assessable (React + TS, `typescript/react-ts-advance/` ReactTimer app)**
- `createContext<T | null>(null)` + a provider component wrapping `children`.
- `useReducer` with a typed reducer `(state, action) => State` and an initial state object.
- Discriminated-union **action** types (`ADD_TIMER` with `payload`, `START_TIMERS`, `STOP_TIMERS`), `switch` on `action.type`, immutable updates with object/array spread, `default: return state`.
- Context value = state fields + dispatcher functions (`addTimer`, `startTimers`, `stopTimers`), typed as an intersection (`TimersState & {...}`).
- `useContext` inside a typed custom hook (`useTimersContext`) that throws when the context is `null`, so consumers get a non-null value.
- Button/anchor wrapper using a **type predicate** (`props is AnchorProps`), `"href" in props` narrowing, and `href?: never` to keep the two prop types apart.
- Conditional handler/label from state (`isRunning ? stopTimers : startTimers`), rendering lists from context, reusing `Form`/`Input`/`Button` + the form ref inside a context consumer.

**Completed assessment**
- #05 React + TS "Workshop Registration Desk" (2026-11-01): **3/12 (25%)**. Code in `typescript/assessment-05-react-ts/` now holds the post-grading fixes.

**Renamed paths**: `fastapi/expense_tracker/` → `fastapi/assessment-04-expense-tracker/`.

## Still out of scope (unimplemented / not yet studied)
- React: multiple contexts, context performance, React 19 ref-as-prop, router data APIs (loaders/actions) unless confirmed, axios interceptors unless confirmed.
- FastAPI: JWT protection in the **expense tracker** (still passes `user_id` in body/query); Alembic, async SQLAlchemy, refresh tokens.

## Full scope summary (beyond the project instructions list)
- React + TS: everything listed in the project instructions, plus `forwardRef`, `useRef`, `useImperativeHandle`, `FormData` + `Object.fromEntries`, and now Context + `useReducer` + custom context hook + type predicates, and `useEffect` with intervals and cleanup.
- FastAPI: books API, todo API (auth, JWT create/decode, protected routes, owner scoping, role-based delete), expense tracker (`schema.sql` tables, optional AND filters, `check_references`, 201/204/404/422, `is_active` filtering).

## Baseline

| # | Date | Topic | Score |
|---|---|---|---|
| 01 | 2026-10-17 | Mixed | 3/12 (25%) |
| 02 | 2026-10-17 | TypeScript | 9/12 (75%) |
| 03 | 2026-10-20 | PostgreSQL company DB | 7/12 (58%) |
| 04 | 2026-10-31 | FastAPI expense tracker | 4/12 (33%) |
| 05 | 2026-11-01 | React + TS registration app | 3/12 (25%) — Q1, Q2, Q4 correct; Q12 skipped |
| 06 | 2026-11-12 | Full stack room booking (FastAPI + React/TS) | 4/12 (33%) — Q1, Q3, Q7, Q10 correct; Q6 unanswered. Report: `claude/assessments/06-fullstack-result.md` |

## Priority weak areas for future assessments
1. **Requirement completeness** — #01, #04, #05, #06. In #06, 6 of 7 wrong answers failed on 1–3 small items: NavLink `end`, navigate on logout, `required`, a missing `api.post<Booking>`, "admins included", "which part of the model causes it".
2. **Auth failure paths (#04, #06):** `None` instead of `return None` in `authenticate_user` (wrong password logs in), no `is_active` check in `get_current_user`, `algorithms` passed as a string. Register + 409 is now solid.
3. **React hooks (#06):** early return before `useEffect` (Rules of Hooks), `useMemo` deps (`[day]` instead of `[bookings]`), stale-response race when a dependency changes (uses the ignore flag in some places but not others).
4. **HTTP response prediction (#04 0, #06 unanswered)** — 201/204/401/403/404/409/422 bodies, `OAuth2PasswordBearer`'s default 401.
5. **Existence checks before insert (#06):** `if body.room_id is None` instead of querying the parent row → FK violation 500.
6. **React + TS details (#05):** prop-spread order, `0 && <X/>`, attributes on the wrong element, `FormData` trimming, `&&` vs `||` validation, ID collisions from `length + 1`, exact output strings.
7. **Optional / NULL handling** — optional FKs, `None` query params, NULL in responses (#04); SET NULL consequences (#06 Q2b).
8. **ON DELETE behaviour** — model correct in #06, but the written explanation was incomplete (#03, #04, #06).
9. TypeScript: literal types in typed functions, generics + typed functions (#02). #06 Q7 types were correct.
10. SQL: constraints/FKs, unmatched records, views with DISTINCT (#03).

Untested so far: Context + `useReducer` + type predicates, `useCallback` beyond deps (when memoization helps), React + TS conceptual (Q12 in #05 skipped), JavaScript problem-solving (only #01), Python OOP/inheritance, SQL since #03. Tested in #06: React Router, axios, data fetching, `useMemo`, 401 vs 403, 409, env-var secrets, owner scoping, roles.

Habit to flag: leftover editor auto-imports (`from turtle import st` in #06), and submitting `.env` files in zips.

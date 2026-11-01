# Assessment 05 — React + TypeScript (Project-Based)

**Project:** Workshop Registration Desk
**Date:** 2026-11-01
**Questions:** 12 · **Marks:** 1 each · no partial marks
**State:** Active. No solutions until you say **"Evaluate My Answers"**.

You build one small app over the 12 questions. Later questions use earlier ones,
so work roughly in order. Every requirement listed is graded: a missing
requirement means 0 for that question.

## Setup

```bash
npm install
npm run dev        # http://localhost:5173
npm run typecheck  # tsc --noEmit
```

- React 18 + TypeScript (strict). Use `forwardRef` for refs, the way you did in `react-ts-advance`.
- Don't use `useEffect`, context, custom hooks, routing or extra libraries. None of them are needed.
- Write code answers in the files named below. Put written answers (Q6, Q7 explanation, Q12) in `ANSWERS.md`.
- `src/components/SearchBox.tsx` is broken on purpose (Q7), so `typecheck` will report errors there until you fix it.
- Submit by pasting files into the chat or attaching a zip of `src/` + `ANSWERS.md`.

## Project map

| File | Question |
|---|---|
| `src/types.ts` | Q1 |
| `src/components/Card.tsx` | Q2 |
| `src/components/Button.tsx` | Q3 |
| `src/components/Container.tsx` | Q4 |
| `src/components/TicketDetails.tsx` | Q5 |
| `src/components/Summary.tsx` (given) + `ANSWERS.md` | Q6 |
| `src/components/SearchBox.tsx` + `ANSWERS.md` | Q7 |
| `src/components/TextField.tsx` | Q8 |
| `src/components/RegistrationForm.tsx` | Q9 |
| `src/components/AttendeeList.tsx` | Q10 |
| `src/App.tsx` | Q11 |
| `ANSWERS.md` | Q12 |

---

### Question 1 — Shared types

**Difficulty:** Easy · **Type:** Coding · **Marks:** 1 · **File:** `src/types.ts`

**Problem:** Define the types the rest of the app shares.

**Requirements:**
1. `TicketType`: a literal union of exactly `"standard"`, `"student"` and `"vip"`.
2. `AttendeeFormValues`: `name: string`, `email: string`, `ticket: TicketType`.
3. `Attendee`: everything in `AttendeeFormValues` plus `id: number` and `checkedIn: boolean`. Reuse `AttendeeFormValues` instead of retyping `name`, `email` and `ticket`.
4. `FormHandleRef`: an **interface** with one method, `clear`, that takes no arguments and returns nothing.
5. Export all four.

---

### Question 2 — Card with children

**Difficulty:** Easy · **Type:** Coding · **Marks:** 1 · **File:** `src/components/Card.tsx`

**Problem:** Build a reusable `Card` wrapper.

**Requirements:**
1. Props: `title: string` and an optional `footer?: string`. Type `children` using `PropsWithChildren`.
2. Render a `<section className="card">` with the title in an `<h2>`, then `children`.
3. Render `<footer>{footer}</footer>` **only** when `footer` is provided. When it isn't, no `<footer>` element is rendered at all.
4. Named export `Card`.

---

### Question 3 — Button wrapper

**Difficulty:** Medium · **Type:** Coding · **Marks:** 1 · **File:** `src/components/Button.tsx`

**Problem:** Wrap the native `<button>` so it accepts every native button prop plus a `variant`.

**Requirements:**
1. Props type combines `ComponentPropsWithoutRef<"button">` with `variant?: "primary" | "danger"`. The default is `"primary"`.
2. Every other prop the caller passes (`onClick`, `disabled`, `aria-*`, `children`, …) reaches the native `<button>` through rest/spread.
3. `type` defaults to `"button"`, but a caller-supplied `type` (for example `type="submit"`) must win.
4. `className` is `btn btn-primary` or `btn btn-danger`. If the caller passes a `className`, append it with a space. The rendered class must never contain the text `undefined` or a trailing space.
5. Named export `Button`.

---

### Question 4 — Polymorphic Container

**Difficulty:** Medium · **Type:** Coding · **Marks:** 1 · **File:** `src/components/Container.tsx`

**Problem:** Build a layout component that renders as whatever element the caller chooses.

**Requirements:**
1. Props: `as?: ElementType` (default `"div"`), `className?: string`, plus `children`.
2. Render the chosen element with `className` and `children`.
3. `<Container as="main">…</Container>` must render a `<main>`. `<Container>…</Container>` must render a `<div>`.
4. Named export `Container`.

---

### Question 5 — Ticket details (discriminated union props)

**Difficulty:** Medium · **Type:** Coding · **Marks:** 1 · **File:** `src/components/TicketDetails.tsx`

**Problem:** Show different information depending on the ticket type. Each ticket type has its own required props.

**Requirements:**
1. The props type is a discriminated union on `ticket`:
   - `"standard"`: no extra props
   - `"student"`: `studentId: string`
   - `"vip"`: `seat: number` and `lounge: boolean`
2. Render one `<span>`:
   - standard: `Standard pass`
   - student: `Student pass — ID: <studentId>`
   - vip: `VIP — Seat <seat>`, followed by ` (Lounge access)` only when `lounge` is `true`
3. Narrow on `ticket`. Don't use type assertions (`as`) or optional properties to get around the union.
4. At the bottom of the file, add this line, commented out, with a comment saying whether it compiles and why:
   `// <TicketDetails ticket="student" />`
5. Named export `TicketDetails`.

---

### Question 6 — Predict the render

**Difficulty:** Easy · **Type:** Output Prediction · **Marks:** 1 · **File:** `ANSWERS.md` (code is in `src/components/Summary.tsx`)

**Problem:** Here is the given component:

```tsx
type SummaryProps = { total: number; checkedIn: number; label?: string };

export function Summary({ total, checkedIn, label = "Today" }: SummaryProps) {
  return (
    <div>
      <h3>{label}</h3>
      {total && <p>{checkedIn}/{total} checked in</p>}
      {checkedIn === total ? <p>All present</p> : null}
    </div>
  );
}
```

**Requirements:** For each call, write exactly what text appears on screen, element by element (for example `h3: …`, `p: …`, or `bare text: …`). Then explain each case in one line.

- (a) `<Summary total={0} checkedIn={0} />`
- (b) `<Summary total={4} checkedIn={2} label="Morning" />`
- (c) `<Summary total={3} checkedIn={3} label="" />`

---

### Question 7 — Fix the SearchBox

**Difficulty:** Medium · **Type:** Debugging · **Marks:** 1 · **Files:** `src/components/SearchBox.tsx` + `ANSWERS.md`

**Problem:** `SearchBox` should call `onSearch` with the trimmed search term when the form is submitted. It has several bugs, some caught by TypeScript and some only at runtime.

**Requirements:**
1. In `ANSWERS.md`, list **every** bug with a one-line reason.
2. Fix the file so it:
   - type-checks with no `any` and no `as`
   - keeps the input controlled
   - doesn't reload the page on submit
   - calls `onSearch(trimmedTerm)` only when the trimmed term isn't empty
3. Keep the public API: `SearchBox({ onSearch })`, where `onSearch: (term: string) => void`.

---

### Question 8 — TextField with forwardRef

**Difficulty:** Medium · **Type:** Coding · **Marks:** 1 · **File:** `src/components/TextField.tsx`

**Problem:** Build a labelled input that parents can attach a ref to.

**Requirements:**
1. Use `forwardRef<HTMLInputElement, TextFieldProps>`.
2. `TextFieldProps` = `ComponentPropsWithoutRef<"input">` plus `label: string`, `id: string` (required) and `error?: string`.
3. Render a `<div className="field">` containing:
   - `<label htmlFor={id}>{label}</label>`
   - `<input>` with `id`, the forwarded `ref`, and every remaining prop spread onto it
   - when `error` is provided: `<p role="alert">{error}</p>` after the input, and `aria-invalid={true}` on the input. When `error` isn't provided, render neither.
4. `error` and `label` must **not** end up on the `<input>` as attributes.
5. Named export `TextField`.

---

### Question 9 — RegistrationForm with an imperative handle

**Difficulty:** Challenging · **Type:** Coding · **Marks:** 1 · **File:** `src/components/RegistrationForm.tsx`

**Problem:** Build the form that collects a new attendee and lets its parent clear it.

**Requirements:**
1. Use `forwardRef<FormHandleRef, RegistrationFormProps>` with `FormHandleRef` from Q1.
2. `RegistrationFormProps` = `ComponentPropsWithoutRef<"form">` plus `onSave: (values: AttendeeFormValues) => void`.
3. Destructure `{ onSave, children, ...props }` and spread `props` onto the `<form>`.
4. Use `useRef<HTMLFormElement>(null)` on the `<form>` and `useImperativeHandle` to expose `clear()`, which resets the form.
5. Fields:
   - `TextField` (Q8), `name="name"`, label `Name`
   - `TextField`, `name="email"`, `type="email"`, label `Email`
   - a `<select name="ticket">` with three options whose values are exactly the `TicketType` values, default `"standard"`
6. Render `children` after the fields. The parent passes the submit button.
7. Submit handler:
   - typed `FormEvent<HTMLFormElement>`
   - prevent the default
   - read the values with `new FormData(...)` + `Object.fromEntries(...)`
   - build an `AttendeeFormValues` with `name` and `email` **trimmed**
   - call `onSave` only if both trimmed `name` and `email` are non-empty
8. The form must **not** clear itself after saving. Clearing is the parent's decision (Q11).
9. Named export `RegistrationForm`.

---

### Question 10 — AttendeeList

**Difficulty:** Medium · **Type:** Coding · **Marks:** 1 · **File:** `src/components/AttendeeList.tsx`

**Problem:** Render the attendees with actions.

**Requirements:**
1. Props: `attendees: Attendee[]`, `onToggleCheckIn: (id: number) => void`, `onRemove: (id: number) => void`.
2. If `attendees` is empty, render `<p>No attendees yet</p>` and **no** `<ul>`.
3. Otherwise render a `<ul>` with one `<li>` per attendee, keyed by `id`, containing:
   - the attendee's `name`
   - `<TicketDetails ticket="standard" />` for **every** attendee (the form doesn't collect student IDs or seats yet)
   - a `Button` (Q3), `variant="primary"`, labelled `Check in` when `checkedIn` is `false` and `Undo` when it's `true`, which calls `onToggleCheckIn(id)`
   - a `Button` with `variant="danger"`, labelled `Remove`, which calls `onRemove(id)`
4. Named export `AttendeeList`.

---

### Question 11 — App: lifted state and the ref handle

**Difficulty:** Challenging · **Type:** Coding · **Marks:** 1 · **File:** `src/App.tsx`

**Problem:** Wire everything together. `App` owns all state.

**Requirements:**
1. State: `useState<Attendee[]>([])` and an error message state (`string | null`, starting at `null`).
2. `formRef = useRef<FormHandleRef>(null)`, passed as `ref` to `RegistrationForm`.
3. `handleSave(values: AttendeeFormValues)`:
   - If an attendee with the same email already exists (**case-insensitive**), set the error to `Email already registered`, **don't** add the attendee and **don't** clear the form.
   - Otherwise add a new attendee with `checkedIn: false` and `id` = highest existing `id` + 1 (`1` when the list is empty), clear the error, then call `clear()` through the ref.
4. `handleToggleCheckIn(id)` flips `checkedIn` for that attendee only. `handleRemove(id)` removes it. Both update state immutably (no `push`, `splice` or direct mutation).
5. Layout:
   - Root is `<Container as="main">`.
   - A `Card` titled `Register` containing `RegistrationForm`, whose child is `<Button type="submit">Add attendee</Button>`. When there's an error, render `<p role="alert">` with it inside this card.
   - A `Card` titled `Attendees` containing `AttendeeList`, with `footer` set to `"<checked-in count> of <total> checked in"`.
6. `App` is the default export. `src/main.tsx` already imports it.

---

### Question 12 — Explain the design

**Difficulty:** Medium · **Type:** Conceptual · **Marks:** 1 (every part must be correct) · **File:** `ANSWERS.md`

Answer each in 2–4 sentences:

- (a) In `Button`, what does `ComponentPropsWithoutRef<"button">` + `{...rest}` give you compared to declaring `onClick`, `disabled` and `type` yourself? Name one concrete thing that would break or need extra work without it.
- (b) In React 18, why can't a plain function component receive a `ref` from its parent the way it receives normal props? What does `forwardRef` change, and what do its two type parameters mean in `forwardRef<HTMLInputElement, TextFieldProps>`?
- (c) In `App`, why is the ref typed `useRef<FormHandleRef>(null)` rather than `useRef<HTMLFormElement>(null)`, and why is it called as `formRef.current?.clear()` and not `formRef.current.clear()`?

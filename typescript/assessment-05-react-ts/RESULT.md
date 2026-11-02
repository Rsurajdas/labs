The submission has 2 type errors against the project's React 18 types. Next I'll render a few components to confirm the actual output rather than reason about it.

I've graded all 12 questions. Before writing the report, I'll add the score to your baseline in the Project so future assessments use it.

# Assessment 05 — React + TypeScript: Evaluation Report

I ran your `src/` through `tsc` with the assessment's React 18 setup, and rendered `Summary`, `Button`, `TicketDetails` and `TextField` to HTML to check what they actually produce. Rendered output quoted below comes from those runs.

## A. Overall Results

| Metric            | Result  |
| ----------------- | ------- |
| Total Questions   | 12      |
| Correct Answers   | 3       |
| Incorrect Answers | 8       |
| Unanswered        | 1 (Q12) |
| Final Score       | 3/12    |
| Percentage        | 25%     |

## B. Question-Wise Scorecard

| Q   | Topic                     | Result        | Marks |
| --- | ------------------------- | ------------- | ----- |
| 1   | Shared types              | ✅ Correct    | 1     |
| 2   | Card + PropsWithChildren  | ✅ Correct    | 1     |
| 3   | Button wrapper            | ❌ Incorrect  | 0     |
| 4   | Polymorphic Container     | ✅ Correct    | 1     |
| 5   | Discriminated union props | ❌ Incorrect  | 0     |
| 6   | Output prediction         | ❌ Incorrect  | 0     |
| 7   | Debug SearchBox           | ❌ Incorrect  | 0     |
| 8   | TextField + forwardRef    | ❌ Incorrect  | 0     |
| 9   | RegistrationForm          | ❌ Incorrect  | 0     |
| 10  | AttendeeList              | ❌ Incorrect  | 0     |
| 11  | App: lifted state + ref   | ❌ Incorrect  | 0     |
| 12  | Conceptual                | ⬜ Unanswered | 0     |

## C. Detailed Evaluation

### Q1 — Shared types: ✅ 1/1

**Your answer:** a literal union for `TicketType`; `Attendee = AttendeeFormValues & { id; checkedIn }`; `FormHandleRef` as an interface with `clear: () => void`; all four exported.

**Why it works:** the intersection reuses the form fields instead of retyping them, which is what the question asked. `interface Attendee extends AttendeeFormValues` would also have been correct.

### Q2 — Card: ✅ 1/1

**Your answer:** `PropsWithChildren<CardProps>`, a `<section className="card">` containing the `<h2>` and the children, and `{footer ? <footer>… : null}`.

**Why it works:** when `footer` isn't passed, no `<footer>` element is rendered at all.

### Q3 — Button wrapper: ❌ 0/1

**Your answer:** `{ variant = "primary", ...props }`. You set `type` and `className` first and then spread `{...props}` after them.

**Mistakes (confirmed by rendering):**

- `<Button>Go</Button>` renders `class="btn btn-primary "`, with a trailing space. Requirement 4 says no trailing space.
- `<Button variant="danger" className="wide">` renders just `class="wide"`. The caller's `className` comes through the spread, which runs after your computed `className` and replaces it, so `btn btn-danger` is lost.

**Correct solution:**

```tsx
export function Button({
  variant = "primary",
  type = "button",
  className,
  ...rest
}: ButtonProps) {
  const classes = className
    ? `btn btn-${variant} ${className}`
    : `btn btn-${variant}`;
  return <button type={type} className={classes} {...rest} />;
}
```

**Why it was wrong:** in JSX, a later attribute wins. If you compute a value from a prop, pull that prop out by destructuring so it isn't still inside `rest`. Then the spread can't overwrite your computed value. `children` travels inside `rest`, so you don't need `{props.children}`.

**Improvement:** when you compute an attribute, check the spread order and test it with and without the caller passing that prop.

### Q4 — Polymorphic Container: ✅ 1/1

**Why it works:** you renamed `as` to a capitalised `Component` with `"div"` as the default, so JSX treats it as a component variable. `as="main"` renders a `<main>`.

### Q5 — TicketDetails: ❌ 0/1

**Your answer:** a correct three-member union, narrowed on `ticket`.

**Mistakes:**

- The VIP text renders `VIP — Seat: 12, (Lounge access)`. The spec is `VIP — Seat 12 (Lounge access)`, with no colon and no comma.
- Requirement 4 is missing: the commented-out `<TicketDetails ticket="student" />` line with a note on whether it compiles.

**Correct solution:**

```tsx
: `VIP — Seat ${props.seat}${props.lounge ? " (Lounge access)" : ""}`
...
// <TicketDetails ticket="student" />
// Does NOT compile: ticket="student" selects the student member of the union,
// which requires studentId.
```

**Why it was wrong:** the type logic was right. You lost the mark on exact output and on a skipped requirement.

**Improvement:** before submitting, tick off each numbered requirement one by one.

### Q6 — Output prediction: ❌ 0/1

**Your answer:** (a) `p: 0`; (b) `p: 2/3 checked in`, `p: null`; (c) correct.

**Actual output (from rendering):**
| Case | Renders |
|---|---|
| (a) | h3: Today · **bare text: 0** · p: All present |
| (b) | h3: Morning · p: **2/4** checked in. Nothing else. |
| (c) | h3: (empty) · p: 3/3 checked in · p: All present |

**Mistakes:**

- (a) `0 && <p>…` evaluates to the number `0`, and React renders numbers. The `0` appears as a bare text node, not inside a `<p>`, because the `<p>` branch never runs.
- (b) You wrote `2/3`, but `total` is 4. You also listed `p: null`. `null` renders nothing, so there is no element there.
- (c) Your answer is right, but your explanation leaves out why: a default parameter applies only when the value is `undefined`, and `""` counts as a passed value.

**Improvement:** `&&` returns its left side when that side is falsy. With a number on the left, use `total > 0 && …` to avoid rendering `0`.

### Q7 — SearchBox: ❌ 0/1

**Your answer:** you found four bugs (untyped `useState`, wrong change-event type, wrong submit-event type plus missing `preventDefault`, props not destructured) and fixed all four.

**Mistakes:**

- Your fix still calls `onSearch("")` when the term is empty or only spaces. Requirement 2 says it should call `onSearch` only when the trimmed term isn't empty.
- `React.SubmitEvent` doesn't exist in the project's React 18 types; `tsc` reports _"Namespace 'React' has no exported member 'SubmitEvent'"_. Your own `ANSWERS.md` correctly names `FormEvent<HTMLFormElement>`, but the code doesn't use it.

**Correct solution:**

```tsx
function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
  event.preventDefault();
  const trimmed = term.trim();
  if (trimmed !== "") onSearch(trimmed);
}
```

**Improvement:** a debugging question is complete only when every listed requirement holds, not just when the type errors are gone.

### Q8 — TextField: ❌ 0/1

**Your answer:** `forwardRef<HTMLInputElement, TextFieldProps>`. You correctly pulled `label`, `id` and `error` out of the spread, and the ref is forwarded.

**Mistake:** `aria-invalid` is on the `<p>`, not on the `<input>`. The render shows `<input id="e"/><p role="alert" aria-invalid="true">`.

**Correct solution:**

```tsx
<input id={id} ref={ref} aria-invalid={error ? true : undefined} {...props} />;
{
  error ? <p role="alert">{error}</p> : null;
}
```

**Why it was wrong:** `aria-invalid` tells screen readers which field is invalid, so it belongs on the field itself. The `<p role="alert">` only carries the message.

### Q9 — RegistrationForm: ❌ 0/1

**Your answer:** the `forwardRef<FormHandleRef, …>`, `useRef`, `useImperativeHandle` → `reset()` and `{ onSave, children, ...props }` parts are all correct.

**Mistakes:**

1. You used `SubmitEvent`. It doesn't exist in React 18's types, which is a type error, and the spec required `FormEvent<HTMLFormElement>`.
2. The values aren't trimmed. You trim only inside the check, then call `onSave(data)` with the untrimmed values.
3. You used `||` where `&&` was needed, so the form saves when only one of the two fields is filled in.
4. The email `TextField` is missing `type="email"`.
5. `Object.fromEntries(...) as AttendeeFormValues` asserts the whole object's type. The values are really `FormDataEntryValue`, so TypeScript stops checking them.

**Correct solution:**

```tsx
function handleSubmit(event: FormEvent<HTMLFormElement>) {
  event.preventDefault();
  const data = Object.fromEntries(new FormData(event.currentTarget));
  const values: AttendeeFormValues = {
    name: String(data.name ?? "").trim(),
    email: String(data.email ?? "").trim(),
    ticket: data.ticket as TicketType,
  };
  if (values.name !== "" && values.email !== "") onSave(values);
}
// ...
<TextField label="Email" name="email" id="email" type="email" />;
```

**Improvement:** say each validation rule out loud: "only if both are non-empty" means `&&`.

### Q10 — AttendeeList: ❌ 0/1

**Your answer:** the empty state, keys, `TicketDetails`, callbacks and both buttons are correct.

**Mistake:** the button always says `Check in`. It never switches to `Undo` when `checkedIn` is `true`.

**Correct solution:** `{attendee.checkedIn ? "Undo" : "Check in"}`

**Improvement:** whenever a label depends on state, ask what it shows in each state.

### Q11 — App: ❌ 0/1

**Your answer:** the state types, `useRef<FormHandleRef>(null)`, immutable toggle and remove, clearing only on success, and the error placement are correct.

**Mistakes:**

1. The ID comes from `prev.length + 1`, which collides after a delete. Add A (id 1) and B (id 2), remove A, then add C: C gets `1 + 1 = 2`, the same as B. That gives duplicate React keys, and checking in C also toggles B.
2. The duplicate check is case-sensitive, so `A@x.com` and `a@x.com` are treated as different emails.
3. The footer renders literal quotes: `"0 of 0 checked in"`. You wrapped `"…"` inside the template string.
4. The card title is `Registration`; the spec says `Register`.

**Correct solution (changed lines):**

```tsx
const email = values.email.toLowerCase();
if (attendees.some((a) => a.email.toLowerCase() === email)) { ... }

const nextId = prev.reduce((max, a) => Math.max(max, a.id), 0) + 1;

<Card title="Register">
footer={`${attendees.filter((a) => a.checkedIn).length} of ${attendees.length} checked in`}
```

**Improvement:** walk through add → remove → add on paper whenever you generate IDs.

### Q12 — Conceptual: ⬜ 0/1 (skipped)

**Model answers:**

- **(a)** `ComponentPropsWithoutRef<"button">` + `{...rest}` gives the wrapper every native attribute and its exact type for free: `onClick`, `disabled`, `type`, `aria-*`, `form`, `name`, and so on. Without it, you'd have to declare and forward each one by hand. For example, `<Button aria-label="Close">` or `<Button form="reg">` would be type errors until you added them.
- **(b)** In React 18, `ref` is a reserved prop. React handles it itself and never passes it inside `props`, so a plain function component can't receive it. `forwardRef` gives the component a second argument, `ref`, which it can attach to an inner element. In `forwardRef<HTMLInputElement, TextFieldProps>`, the first type parameter is what the ref points to and the second is the component's props.
- **(c)** The parent never touches the `<form>` element directly. It receives only the handle that `useImperativeHandle` exposes, which has a `clear()` method, so the ref is typed as `FormHandleRef`. `current` is `null` until the component mounts, and again after it unmounts, so its type is `FormHandleRef | null` and `?.` is needed to call it safely.

## D. Topic-Wise Performance

| Topic                                                         | Correct | Total | Accuracy |
| ------------------------------------------------------------- | ------- | ----- | -------- |
| Typed props, children, shared types, ElementType (Q1, Q2, Q4) | 3       | 3     | 100%     |
| Wrapper components + prop forwarding (Q3, Q8)                 | 0       | 2     | 0%       |
| Discriminated union props (Q5)                                | 0       | 1     | 0%       |
| Conditional rendering prediction (Q6)                         | 0       | 1     | 0%       |
| Form events + FormData + forwardRef handle (Q7, Q9)           | 0       | 2     | 0%       |
| State lifting + list rendering (Q10, Q11)                     | 0       | 2     | 0%       |
| Conceptual (Q12)                                              | 0       | 1     | 0%       |

## E. Learning Gap Analysis

- **Strong:** typing props, `PropsWithChildren`, polymorphic `as`, union design and narrowing, the `forwardRef` + `useImperativeHandle` setup, and immutable `map`/`filter` updates. Your architecture was right almost everywhere.
- **Weak:**
  - the order of props and the `{...rest}` spread
  - how `&&` renders falsy numbers
  - which element an attribute belongs on
  - validating `FormData` values
  - which event types exist in React 18
- **Repeated mistake: requirement completeness.** This happened in #01 and #04, and here 7 of your 8 incorrect answers had correct structure but missed a stated detail: exact text, a label in one state, an empty guard, case-insensitivity, a skipped sub-requirement. This one habit cost more marks than any concept gap.
- **Progress:**
  - **Score:** 25%. That equals #01 and is below #04 (33%).
  - **First React assessment:** this was your first dedicated React + TS assessment. In #01 the React questions went unanswered, so this is your first scored React work.

## F. Recommended Practice

1. **Spread-order drill:** write a `Badge` wrapper over `<span>` with `tone?: "info" | "warn"`. It must merge the caller's `className` and `title`, and let a caller-supplied `role` win. Render it four ways and check the HTML for each.
2. **FormData validation:** build a `LoginForm` that reads `email`, `password` and `remember` (a checkbox) through `FormData`. Trim the text fields, convert the checkbox to a `boolean` without using `as` on the whole object, and call `onLogin` only when both text fields are non-empty.
3. **Requirement checklist habit:** redo Q10 and Q11 from the spec alone, without looking at your code. Before submitting, copy each numbered requirement into a comment and tick it off.

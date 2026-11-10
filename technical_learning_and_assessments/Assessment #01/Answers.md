# Assessment #1 — Evaluation Report

## A. Overall Results

| Metric            | Result |
| ----------------- | ------ |
| Total Questions   | 12     |
| Correct Answers   | 3      |
| Incorrect Answers | 7      |
| Unanswered        | 2      |
| Final Score       | 3 / 12 |
| Percentage        | 25%    |

This is your first assessment, so it's your baseline. Your fundamentals are better than 25% suggests: several answers failed on one requirement you didn't finish, or one edge case.

## B. Question-by-Question Results

| Question | Topic      | Result     | Marks |
| -------- | ---------- | ---------- | ----- |
| Q1       | SQL        | Correct    | 1     |
| Q2       | TypeScript | Incorrect  | 0     |
| Q3       | Python     | Incorrect  | 0     |
| Q4       | SQL        | Incorrect  | 0     |
| Q5       | JavaScript | Incorrect  | 0     |
| Q6       | TypeScript | Incorrect  | 0     |
| Q7       | React + TS | Unanswered | 0     |
| Q8       | SQL        | Correct    | 1     |
| Q9       | FastAPI    | Incorrect  | 0     |
| Q10      | Python     | Correct    | 1     |
| Q11      | FastAPI    | Unanswered | 0     |
| Q12      | React + TS | Incorrect  | 0     |

---

## C. Detailed Evaluation

### Q1 — SQL: Top 3 highest-paid employees, excluding NULL salaries

**My Answer:**

```sql
SELECT name, salary
FROM employees
WHERE salary IS NOT NULL
ORDER BY salary DESC
LIMIT 3;
```

**Result:** Correct. **Marks:** 1/1

**Explanation:** You used `IS NOT NULL` rather than `!= NULL`, which is the correct way to test for NULL. In PostgreSQL, `ORDER BY ... DESC` puts NULLs first by default, so removing them before `LIMIT` was essential. The query returns Kiran, Asha and Ravi.

---

### Q2 — TypeScript: Interface merging vs type alias

**My Answer:**

```
// 2.1 -> User type will have both name and age properties in a object structure.
// 2.2 -> TypeScript will show an error `Dublicate indentifier 'User'`. User type strcture will consisder only first intialization in this case 'name'.
// 2.3 ->
```

**Result:** Incorrect (incomplete). **Marks:** 0/1

**Mistake:**

- 2.1 is correct.
- 2.2 is half right. The "Duplicate identifier" error is correct, but TypeScript does not fall back to the first declaration. It is a compile error, and there is no defined "winning" shape.
- 2.3 was not answered.

**Correct Solution:**

- **2.1:** The two declarations merge into one interface, so a `User` must have both `name: string` and `age: number`.
- **2.2:** Type aliases cannot be re-declared. The second `type User` produces a "Duplicate identifier" compile error. Aliases never merge.
- **2.3:** Merging is useful when you need to add properties to an interface declared somewhere you can't edit. For example, you can add fields to a type that comes from a library, or to a global interface like `Window`, without touching the original declaration.

**Improvement:** Answer every sub-part. A blank sub-part makes the whole answer incomplete.

---

### Q3 — Python: Output prediction (Enemy / Zombie)

**My Answer:**

```
"Grrr..."
"Goblin says nothing."
"35"
"35, 30"
"Zombie"
```

**Result:** Incorrect. **Marks:** 0/1

**Mistake:** Your reasoning about the values was correct: method overriding, `super().__init__` setting the name, and `take_damage` returning 35. But the question asked for the exact output, and two things are wrong:

1. `print(z.health, e.health)` separates its arguments with a **space**, not a comma.
2. `print()` does not show quotes around strings.

You also left out the required explanation for the first and last lines.

**Correct Solution:**

```
Grrr...
Goblin says nothing.
35
35 30
Zombie
```

**Explanation:**

- **Line 1:** `Zombie` overrides `talk()`, so Python uses the child class's version.
- **Line 5:** `Zombie.__init__` passes `"Zombie"` to `Enemy.__init__` through `super()`, so `self.name` is set even though `Zombie()` was called with only a health value.

**Improvement:** In output questions, picture the actual terminal. `print(a, b)` gives `a b`.

---

### Q4 — SQL: Departments with no employees (LEFT JOIN)

**My Answer:**

```sql
SELECT d.id, d.name
FROM departments AS d
    LEFT JOIN employees as e ON e.department_id = d.id
WHERE e.department_id IS NOT NULL
ORDER BY department_id ASC;
```

**Result:** Incorrect. **Marks:** 0/1

**Mistake:** This has a wrong condition and a wrong sort.

1. `IS NOT NULL` keeps the matched rows, which is the opposite of what was asked. It returns departments that _do_ have employees, repeated once per employee: Engineering ×3, Sales ×2, HR ×1. Legal, the correct answer, is filtered out.
2. `ORDER BY department_id` sorts by the employee's column. The requirement was to sort by department name.

**Correct Solution:**

```sql
SELECT d.id, d.name
FROM departments AS d
LEFT JOIN employees AS e ON e.department_id = d.id
WHERE e.id IS NULL
ORDER BY d.name;
```

**Explanation:** A LEFT JOIN keeps every department. When a department has no matching employee, all the `e.*` columns are filled with NULL. Filtering for NULL on the right table's primary key (`e.id IS NULL`) leaves only the unmatched departments. Result: `4 | Legal`.

**Improvement:** Memorise the anti-join pattern: **LEFT JOIN + `WHERE right_table.id IS NULL`** means "rows with no match."

---

### Q5 — JavaScript: `summarizeScores`

**My Answer:**

```js
function summarizeScores(students) {
  const result = { passed: [], failed: [], topScorer: null };
  if (!students.length) return result;
  let topScore = 0;
  for (let i = 0; i < students.length; i++) {
    const student = students[i];
    if (student.score >= 40) {
      result.passed.push(student.name);
      topScore = Math.max(student.score, topScore);
    } else {
      result.failed.push(student.name);
    }
  }
  result.topScorer = students.find(
    (student) => student.score === topScore,
  ).name;
  return result;
}
```

**Result:** Incorrect. **Marks:** 0/1

**Mistake:** This is a logic error that causes a runtime error. `topScore` is only updated inside the `passed` branch, so failing students are never considered for top scorer. If every student fails, for example `[{ name: "Sara", score: 35 }]`:

- `topScore` stays `0`.
- `find()` returns `undefined`.
- `.name` throws `TypeError: Cannot read properties of undefined`.

The empty-array case, the passed/failed split and the tie-breaking (`find` returns the first match) are all correct.

**Correct Solution:**

```js
function summarizeScores(students) {
  const result = { passed: [], failed: [], topScorer: null };
  if (students.length === 0) return result;

  let topScore = students[0].score;
  result.topScorer = students[0].name;

  for (const student of students) {
    if (student.score >= 40) {
      result.passed.push(student.name);
    } else {
      result.failed.push(student.name);
    }
    if (student.score > topScore) {
      // strict > keeps the first on ties
      topScore = student.score;
      result.topScorer = student.name;
    }
  }
  return result;
}
```

**Explanation:** Tracking the maximum has to be independent of the pass/fail branch. Starting from the first student, rather than from `0`, also makes it correct for any score range.

**Improvement:** Before submitting, test against edge-case inputs: empty, all pass, all fail, and ties.

---

### Q6 — TypeScript: Literal union, interface, generics

**My Answer:**

```ts
type Priority = "low" | "medium" | "high";
interface Goal {
  id: number;
  title: string;
  priority: Priority;
}
// ...goals array...
function getGoalsByPriority(
  goals: Array<Goal>,
  priority: Priority,
): Array<Goal> {
  return goals.filter((goal) => goal.priority === priority);
}
function lastOrDefault<T>(arr: Array<T>, fallback: T) {
  if (!arr.length) return fallback;
  return arr.pop();
}
getGoalsByPriority(goals, "high");
lastOrDefault<Goal>(goals, { id: 1, title: "Job in Dubai", priority: "high" });
```

**Result:** Incorrect. **Marks:** 0/1

**Mistake:** Requirements 1–3 are correct. The problems are in requirements 4 and 5.

1. **Logic error:** `arr.pop()` _removes_ the last element from the caller's array. Calling `lastOrDefault(goals, ...)` permanently deletes goal 5 from `goals`. The function should read the last element, not change the array.
2. **Type issue:** `pop()` returns `T | undefined`, so the inferred return type becomes `T | undefined`, not `T`.
3. Requirement 5 is missing: the call TypeScript must reject, and why.

**Correct Solution:**

```ts
function lastOrDefault<T>(items: T[], fallback: T): T {
  if (items.length === 0) return fallback;
  return items[items.length - 1];
}

lastOrDefault([10, 20, 30], 0); // 30
lastOrDefault<string>([], "none"); // "none"

// Rejected by TypeScript:
getGoalsByPriority(goals, "urgent");
// Error: '"urgent"' is not assignable to type 'Priority'.
// Priority only allows the literals "low" | "medium" | "high".
```

**Explanation:** Reading by index (`items[items.length - 1]`) leaves the array unchanged. An explicit `: T` return annotation would also have made TypeScript flag the `undefined` problem for you.

**Improvement:** Know which array methods mutate: `pop`, `push`, `splice`, `sort` and `reverse` do; `filter`, `map` and `slice` don't. Add explicit return types to generic functions.

---

### Q7 — React + TS: Delete bugs

**My Answer:** Skipped.
**Result:** Unanswered. **Marks:** 0/1

**Correct Solution:**

```tsx
// CourseGoal.tsx
<button onClick={() => onDelete(id)}>Delete</button>
```

```tsx
// App.tsx
function handleDeleteGoal(id: number) {
  setGoals((prevGoals) => prevGoals.filter((goal) => goal.id !== id));
}
```

**Explanation:**

- **Bug 1 — `onClick={onDelete(id)}`:** This _calls_ `onDelete` while the component renders, so the delete logic runs for every goal as soon as it appears on screen. Its return value (`undefined`) becomes the click handler, so clicking does nothing. Wrapping it in an arrow function passes a function to run later, on click.
- **Bug 2 — `goals.splice(...)` then `setGoals(goals)`:** `splice` mutates the existing state array, and `setGoals` receives the _same reference_. React compares old and new state by reference, sees no change and skips the re-render, so the UI doesn't update. There is also a hidden third bug: if `findIndex` returns `-1`, `splice(-1, 1)` deletes the _last_ item. `filter` returns a new array and avoids all of this.

Your own `deleteGoalHandler` in Q12 is exactly the correct fix, so you know this pattern. Attempt questions like this next time.

---

### Q8 — SQL: `user_locations` view

**My Answer:**

```sql
CREATE VIEW user_locations AS
SELECT u.id AS user_id, u.name AS user_name, a.street, c.name AS city_name
FROM users AS u
    LEFT JOIN addresses AS a ON u.address_id = a.id
    LEFT JOIN cities AS c ON a.city_id = c.id;

SELECT * FROM user_locations
WHERE city_name = 'Mumbai' OR city_name IS NULL
ORDER BY user_name ASC;
```

**Result:** Correct. **Marks:** 1/1

**Explanation:** Both joins are LEFT JOINs. If the second one were an INNER JOIN, it would silently drop the address-less users that the first LEFT JOIN kept, so this was the key point of the question. The column aliases match the required names exactly, and the NULL check is written correctly. Result: Asha, Divya, Sneha, Vikram.

---

### Q9 — FastAPI: GET /books with optional filters

**My Answer:**

```python
@app.get("/books", response_model=list[BookResponse])
async def get_books_by_published_year_and_rating(
    db: DB_DEPENDENCY,
    published_after: int | None = Query(gt=0),
    min_rating: int | None = Query(gt=0, lt=6),
):
    books = (
        db.query(models.Books)
        .filter_by(
            Book.published_year > published_after,
            Book.rating >= min_rating,
        )
        .all
    )
    return books
```

**Result:** Incorrect. **Marks:** 0/1

**Mistake:** There are several issues, and each one alone would break the endpoint:

1. **Parameters aren't optional:** `Query(gt=0)` without a `default` makes the parameter _required_, even with `int | None`. A request to plain `/books` returns 422.
2. **Wrong type:** `min_rating` is `int`, so `?min_rating=4.5` is rejected with 422. It should be `float`.
3. **Wrong method:** `filter_by()` only accepts keyword arguments such as `filter_by(title="X")`. Comparison expressions need `filter()`. As written, this raises a `TypeError`.
4. **Filters always applied:** The requirement was to filter only when a value is provided. This needs `if` checks.
5. **`.all` not called:** Without the `()`, you return the method object itself, and response validation fails.
6. **Ordering missing:** There is no `order_by` newest first.
7. **Model name inconsistent:** You used `models.Books` in the query but `Book` in the filters. The starter model is `Book`.

**Correct Solution:**

```python
from fastapi import Query

@app.get("/books", response_model=list[BookResponse])
def get_books(
    published_after: int | None = Query(default=None),
    min_rating: float | None = Query(default=None, ge=0, le=5),
    db: Session = Depends(get_db),
):
    query = db.query(Book)
    if published_after is not None:
        query = query.filter(Book.published_year > published_after)
    if min_rating is not None:
        query = query.filter(Book.rating >= min_rating)
    return query.order_by(Book.published_year.desc()).all()
```

**Explanation:** A SQLAlchemy query can be built up in steps: each `.filter()` returns a new query, and nothing runs until `.all()`. Use `is not None` rather than a truthiness check, so a legitimate value like `min_rating=0` still applies the filter.

**Improvement:** Run your endpoint once with no parameters, once with one parameter and once with both, and check the `/docs` page. Most of these bugs show up straight away.

---

### Q10 — Python: Battle simulation

**My Answer:** `Wapon`, `Enemy`, `Ogre` classes, `arsenal` dictionary and while loop (as submitted).
**Result:** Correct. **Marks:** 1/1

**Explanation:** Inheritance with `super().__init__("Ogre", health)` is correct. The weapon is stored on the Ogre and used through `self.wapon.damage`. The `take_damage` floor at 0 works, and the `is_alive()` loop ends correctly: 30 → 10 → 0. The returned message matches the required format.

**Improvement:**

- The class was required to be named `Weapon`. Your spelling `Wapon` works because you used it consistently, but any code importing `Weapon` would break. Fix spellings in names.
- In `take_damage`, the `if` already clamps the value, so `return max(self.health, 0)` can simply be `return self.health`.

---

### Q11 — FastAPI: Delete endpoint bugs

**My Answer:** Skipped.
**Result:** Unanswered. **Marks:** 0/1

**Correct Solution:**

```python
from fastapi import HTTPException

@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted"}
```

**Explanation:**

1. **Missing `.first()`:** `book` is a _Query object_, not a `Book` instance. `db.delete()` needs a model instance, so it raises an error and the client gets a 500.
2. **No 404 handling:** A nonexistent ID should raise `HTTPException(404)`. Otherwise the client either gets a crash or a false "Book deleted."
3. **Missing `db.commit()`:** Without it, the delete is never saved. It is rolled back when the session closes, so the endpoint reports success but the row still exists.

---

### Q12 — React + TS: NewGoal form and App wiring

**My Answer:**

```tsx
interface NewGoalProps {
  onAddGoal: (goal: string, summary: string) => void;
}
export default function NewGoal({ onAddGoal }: NewGoalProps) {
  function submitHandler(event: SubmitEvent<HTMLFormElement>) {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const { title, description } = Object.fromEntries(formData.entries());
    if (!String(title).trim() || !String(description).trim()) return;
    onAddGoal(String(title), String(description));
    event.currentTarget.reset();
  }
  // ...form JSX
}
```

```tsx
function addGoalHandler(title: string, description: string) {
  setGoals((prevGoals) => [
    ...prevGoals,
    { id: prevGoals.length + 1, title: title, description: description },
  ]);
}
```

**Result:** Incorrect. **Marks:** 0/1

**Mistake:**

1. **Requirement not met:** The question required controlled inputs using typed `useState`. Your form is uncontrolled and reads values with `FormData`. That's a valid technique, but it isn't what was asked.
2. **Type error:** `SubmitEvent` isn't imported, so it refers to the browser's DOM `SubmitEvent`, which is not generic. `SubmitEvent<HTMLFormElement>` won't compile. The React type is `FormEvent<HTMLFormElement>`.
3. **Unique-ID logic error:** `prevGoals.length + 1` creates duplicate IDs after a deletion. Add goals 1, 2 and 3, delete goal 1, then add a new one: it gets ID 3, which is already taken. Deleting one of them would then delete both.
4. **Minor deviation:** You also block an empty summary. Only the title was required.

What's correct: the props interface, `preventDefault`, the non-mutating spread in `setGoals`, the functional state update, and lifting state up through `onAddGoal`.

**Correct Solution:**

```tsx
// NewGoal.tsx
import { useState, type FormEvent } from "react";

interface NewGoalProps {
  onAddGoal: (goal: string, summary: string) => void;
}

export default function NewGoal({ onAddGoal }: NewGoalProps) {
  const [goal, setGoal] = useState<string>("");
  const [summary, setSummary] = useState<string>("");

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (goal.trim() === "") return;
    onAddGoal(goal, summary);
    setGoal("");
    setSummary("");
  }

  return (
    <form onSubmit={handleSubmit}>
      <label htmlFor="goal">Goal</label>
      <input id="goal" value={goal} onChange={(e) => setGoal(e.target.value)} />
      <label htmlFor="summary">Summary</label>
      <input
        id="summary"
        value={summary}
        onChange={(e) => setSummary(e.target.value)}
      />
      <button type="submit">Add Goal</button>
    </form>
  );
}
```

```tsx
// App.tsx
function addGoalHandler(title: string, description: string) {
  setGoals((prevGoals) => [
    ...prevGoals,
    { id: Date.now(), title, description }, // or Math.random()
  ]);
}
```

**Explanation:** In a controlled input, React state is the single source of truth through `value` plus `onChange`, and clearing the form just means resetting state. An ID must never depend on the array length, because the length shrinks on delete and old numbers get reused.

**Improvement:** Re-read the requirements list before writing code. This answer did the job, but not in the way the question specified.

---

## D. Topic-Wise Performance

| Topic      | Correct | Total | Accuracy |
| ---------- | ------- | ----- | -------- |
| SQL        | 2       | 3     | 67%      |
| Python     | 1       | 2     | 50%      |
| TypeScript | 0       | 2     | 0%       |
| React + TS | 0       | 2     | 0%       |
| FastAPI    | 0       | 2     | 0%       |
| JavaScript | 0       | 1     | 0%       |

## E. Improvement Recommendations

**Recurring patterns:**

1. **Incomplete answers to multi-part questions (Q2, Q3, Q6, Q12).** In four questions you missed a sub-part or requirement you clearly could have answered. This is your biggest point loss. Treat the requirements list as a checklist and tick it off before submitting.
2. **Accidental mutation and unstable identity (Q6 `pop`, Q12 `length + 1`, Q7).** Know which operations change existing data, and never derive IDs from something that changes.
3. **Conditional and NULL logic (Q4, Q5, Q9).** These are inverted NULL filters, a max tracked inside the wrong branch, and filters applied unconditionally. Each time, the "nothing matches" or "value not provided" case was the one that broke.
4. **FastAPI and SQLAlchemy query building (Q9, Q11).** `filter()` vs `filter_by()`, `.first()` / `.all()`, `commit()`, `Query(default=None)` and 404 handling need focused revision. This is your weakest practical area.

**Revise:** the LEFT JOIN anti-join pattern, mutating vs non-mutating array methods, controlled inputs with `FormEvent`, and SQLAlchemy session operations (query → filter → first/all, add/delete → commit).

**Practice exercises (no solutions):**

1. **FastAPI:** Write `PUT /books/{book_id}` that updates a book's title and rating from a Pydantic `BookUpdate` schema, returns 404 if the book doesn't exist, saves the change, and returns the updated book with `response_model=BookResponse`. Then write `GET /books/search` with an optional `author` query parameter that filters only when provided.
2. **SQL (PostgreSQL), departments/employees schema:** (a) List employees who have no department. (b) List every department with its employees, including departments that have none, showing `'No employees'` text is _not_ required, just NULLs, ordered by department name then employee name. (c) Return the single lowest-paid employee among those with a recorded salary.
3. **JavaScript + TypeScript:** Write a typed function `removeById<T extends { id: number }>`… _(skip the constraint if it's unfamiliar)_. Instead, write `removeGoal(goals: Goal[], id: number): Goal[]` that returns a new array without the goal, leaves the original untouched, and returns an unchanged copy if the ID doesn't exist. Prove that the original array is unmodified with a `console.log` before and after.

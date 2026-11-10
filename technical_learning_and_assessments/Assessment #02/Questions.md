# TypeScript Assessment — #1

**Scope:** Basic types, type aliases, interfaces, interface merging, union types, literal types, generics, typed function parameters and return values.

---

**Question 1 — Type Aliases vs Interfaces**

**Difficulty:** Easy

**Type:** Conceptual

**Question:** Both `type` aliases and `interface` declarations can describe the shape of an object. In your own words, explain **two** differences between them, and describe one situation where you would choose one over the other.

**Requirements:**

- State two concrete differences.
- Give one practical scenario that justifies your choice.

**Marks:** 1

---

**Question 2 — Typed Functions**

**Difficulty:** Easy

**Type:** Coding

**Question:** Write a function `formatBookTitle` that takes a book title and a publication year and returns a formatted string.

**Requirements:**

- Parameter `title` must be a string, and `year` must be a number.
- The return type must be explicitly annotated.
- Input `("Clean Code", 2008)` should return `"Clean Code (2008)"`.

**Marks:** 1

---

**Question 3 — Basic Types**

**Difficulty:** Easy

**Type:** Output Prediction

**Question:** Identify **every** line that produces a TypeScript compile error. For each one, briefly explain why.

**Starter Code:**

```ts
let username: string = "suraj"; // Line 1
let age: number = "30"; // Line 2
let isActive: boolean = true; // Line 3
isActive = "false"; // Line 4
let scores: number[] = [90, 85, 77]; // Line 5
scores.push("100"); // Line 6
let tags: string[] = []; // Line 7
username = 42; // Line 8
```

**Requirements:** List the line numbers that fail and give a one-line reason for each.

**Marks:** 1

---

**Question 4 — Union Types**

**Difficulty:** Easy

**Type:** Coding

**Question:** A system identifies records using either a numeric ID or a string code (for example `101` or `"EMP-101"`).

**Requirements:**

- Create a type alias named `RecordId` that allows both forms.
- Write a function `printRecordId` that accepts a `RecordId` and returns the string `"Record: <id>"`.
- Explicitly annotate the parameter and return types.

**Marks:** 1

---

**Question 5 — Union Types**

**Difficulty:** Medium

**Type:** Conceptual

**Question:** A developer writes this code and gets a compile error:

```ts
function shout(value: string | number) {
  return value.toUpperCase();
}
```

Explain **why** TypeScript rejects this code, even though `toUpperCase()` works on strings.

**Requirements:** Explain the reason in terms of how union types work. You do not need to provide a fix.

**Marks:** 1

---

**Question 6 — Interface Merging**

**Difficulty:** Medium

**Type:** Output Prediction

**Question:** Analyse the following code.

```ts
interface Employee {
  id: number;
  name: string;
}

interface Employee {
  department: string;
}

const emp: Employee = {
  id: 1,
  name: "Karan",
};
```

**Requirements:**

- State whether this code compiles, and why.
- Describe the final shape of `Employee` as TypeScript sees it.
- State what would happen if both declarations were written using `type Employee = { ... }` instead.

**Marks:** 1

---

**Question 7 — Literal Types (Enum Alternative)**

**Difficulty:** Medium

**Type:** Coding

**Question:** A course goal can be in one of exactly three states: pending, in progress, or completed. Instead of using an `enum`, model this using literal types.

**Requirements:**

- Create a type named `GoalStatus` that allows only the values `"pending"`, `"in-progress"` and `"completed"`.
- Write a function `getStatusLabel` that accepts a `GoalStatus` and returns a readable label:
  - `"pending"` → `"Not Started"`
  - `"in-progress"` → `"Working On It"`
  - `"completed"` → `"Done"`
- Annotate the parameter and return types.

**Marks:** 1

---

**Question 8 — Literal Types**

**Difficulty:** Medium

**Type:** Debugging

**Question:** The code below contains **three** type errors. Identify each one and explain why TypeScript reports it.

**Starter Code:**

```ts
type Role = "admin" | "editor" | "viewer";

interface User {
  id: number;
  name: string;
  role: Role;
}

const users: User[] = [
  { id: 1, name: "Jatin", role: "admin" },
  { id: 2, name: "Khushi", role: "Editor" },
  { id: "3", name: "Karan", role: "viewer" },
];

function setRole(user: User, newRole: Role): User {
  return { ...user, role: newRole };
}

setRole(users[0], "owner");
```

**Requirements:** Point out all three errors with a brief explanation for each. Do not just rewrite the code.

**Marks:** 1

---

**Question 9 — Interfaces**

**Difficulty:** Medium

**Type:** Coding

**Question:** Model the data for a small library system using interfaces.

**Requirements:**

- Create an `Author` interface with `id` (number) and `name` (string).
- Create a `Book` interface with `id` (number), `title` (string), `publishedYear` (number), `rating` (number) and `author` (an `Author`).
- Declare a typed variable `books` that holds an array of **two** `Book` objects with sample data.
- Write a function `getBookTitles` that accepts an array of `Book` and returns an array of their titles, with explicit parameter and return types.

**Marks:** 1

---

**Question 10 — Generics**

**Difficulty:** Medium

**Type:** Output Prediction

**Question:** For each numbered call below, state whether it **compiles** or produces a **compile error**. If it errors, explain why.

**Starter Code:**

```ts
function makePair<K, V>(key: K, value: V): [K, V] {
  return [key, value];
}

makePair<string, number>("age", 30); // Call 1
makePair<string, number>(30, "age"); // Call 2
makePair<boolean, string>(true, "active"); // Call 3
makePair<number, number[]>(1, [2, 3]); // Call 4
makePair<string, string>("city", null); // Call 5
```

**Requirements:** Assume `strict` mode is enabled. Give a result and a short reason for each call.

**Marks:** 1

---

**Question 11 — Generics and Interfaces**

**Difficulty:** Challenging

**Type:** Coding

**Question:** Your Books API returns all responses in a consistent wrapper. Model this wrapper on the frontend using a generic interface.

**Requirements:**

- Create a generic interface `ApiResponse<T>` with these properties:
  - `success` (boolean)
  - `message` (string)
  - `data` (of type `T`)
- Write a generic function `wrapResponse` that accepts `data` and a `message`, and returns an `ApiResponse` with `success` set to `true`.
- Show **two** example calls: one wrapping a single `Book` object, and one wrapping an array of `Book` objects (you may reuse the `Book` interface from Question 9).
- The function must work with any data type without using `any`.

**Marks:** 1

---

**Question 12 — Generics, Interfaces and Typed Functions**

**Difficulty:** Challenging

**Type:** Coding

**Question:** Build a reusable, type-safe pagination helper that works for any list of items.

**Requirements:**

- Create a generic interface `Paginated<T>` with:
  - `items` — the items for the current page
  - `page` — current page number
  - `pageSize` — number of items per page
  - `totalItems` — total number of items in the full list
  - `totalPages` — total number of pages
- Write a generic function `paginate` that takes an array of items, a page number, and a page size, and returns a `Paginated` result.
- Page numbers start at **1**.
- `totalPages` must round **up** (for example, 7 items with a page size of 3 means 3 pages).
- Example: paginating `[10, 20, 30, 40, 50, 60, 70]` with page `3` and page size `3` should give `items` of `[70]`.
- Do not use `any`. Annotate the parameter and return types.

**Marks:** 1

---

## Assessment Summary

| Item                  | Detail                                                                                                                                      |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| Total Questions       | 12                                                                                                                                          |
| Total Available Marks | 12                                                                                                                                          |
| Topics Covered        | Basic types, type aliases, interfaces, interface merging, union types, literal types, generics, typed function parameters and return values |

## How to Submit

1. Answer each question, labelled clearly (e.g. **Q1**, **Q2** …).
2. You can submit everything in one message or one answer at a time — I'll collect them without evaluating.
3. For coding questions, paste your full TypeScript code in a code block.
4. Leave a question blank or write "skip" if you don't want to attempt it — it counts as unanswered.
5. When you're done, say **"Evaluate My Answers"** to get your full report.

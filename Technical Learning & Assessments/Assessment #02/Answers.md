# TypeScript Assessment #1 — Results

## A. Overall Results

| Metric            | Result |
| ----------------- | ------ |
| Total Questions   | 12     |
| Correct Answers   | 9      |
| Incorrect Answers | 2      |
| Unanswered        | 1      |
| Final Score       | 9 / 12 |
| Percentage        | 75%    |

## B. Question-by-Question Results

| Question | Topic                      | Result     | Marks |
| -------- | -------------------------- | ---------- | ----- |
| Q1       | Type Aliases vs Interfaces | Correct    | 1     |
| Q2       | Typed Functions            | Incorrect  | 0     |
| Q3       | Basic Types                | Correct    | 1     |
| Q4       | Union Types                | Correct    | 1     |
| Q5       | Union Types                | Correct    | 1     |
| Q6       | Interface Merging          | Correct    | 1     |
| Q7       | Literal Types              | Correct    | 1     |
| Q8       | Literal Types (Debugging)  | Incorrect  | 0     |
| Q9       | Interfaces                 | Correct    | 1     |
| Q10      | Generics                   | Correct    | 1     |
| Q11      | Generics + Interfaces      | Correct    | 1     |
| Q12      | Generics + Typed Functions | Unanswered | 0     |

## C. Detailed Evaluation

### Q1 — Type Aliases vs Interfaces ✅ 1/1

**Your answer:** `type` can describe any type (unions, string literals); `interface` describes object shapes. Interfaces can be re-declared and merge; types cannot. You'd use `type` for unions and `interface` for objects.

**Explanation:** Both differences are accurate and your scenario follows from them. One small precision point: the redeclaration rule applies to the same scope, not specifically the same file.

---

### Q2 — Typed Functions ❌ 0/1

**Question:** Write `formatBookTitle(title, year)` with typed parameters and an annotated return type. `("Clean Code", 2008)` must return `"Clean Code (2008)"`.

**Your answer:**

```ts
function formatBookTitle(title: string, year: number): string {
  return `${title} ${year}`;
}
```

**Mistake:** This is a logic error, not a type error. Your typing is perfect, but the function returns `"Clean Code 2008"`. The required output wraps the year in parentheses.

**Correct solution:**

```ts
function formatBookTitle(title: string, year: number): string {
  return `${title} (${year})`;
}
```

**Explanation:** TypeScript checks that a string is returned. It does not check that it is the right string. The type system cannot catch output-format mistakes; only comparing against the requirement can.

**Improvement:** Before submitting, run the given example input through your code mentally and compare it character by character with the expected output.

---

### Q3 — Basic Types ✅ 1/1

**Your answer:** Lines 2, 4, 6 and 8, each with the correct mismatch.

**Explanation:** You found all four errors. Line 7 (`string[] = []`) is valid because an empty array satisfies any array type. For Line 6, the compiler's exact wording is that the _argument_ of type `string` isn't assignable to the _parameter_ of type `number`, but your reasoning is the same.

---

### Q4 — Union Types ✅ 1/1

**Your answer:** `type RecordId = number | string;` with a correctly typed `printRecordId`.

**Explanation:** Correct alias, annotations and output. Template literals accept both members of the union, so no extra handling is needed.

---

### Q5 — Union Types ✅ 1/1

**Your answer:** `toUpperCase()` exists on `string` but not on `number`, and a union means the value could be either.

**Explanation:** This is exactly right. To state the rule generally: on a union type, TypeScript only allows properties and methods that exist on **every** member of the union.

---

### Q6 — Interface Merging ✅ 1/1

**Your answer:** It doesn't compile because `department` is missing. The merged shape is `{ id; name; department }`. Using `type` twice throws an error.

**Explanation:** All three parts are correct. The `type` version fails with a "Duplicate identifier 'Employee'" error.

---

### Q7 — Literal Types ✅ 1/1

**Your answer:** A literal union `GoalStatus` and a lookup object indexed by `goalStatus`.

**Explanation:** This is a clean, valid alternative to a `switch` statement. Because `status` has exactly the keys `pending`, `in-progress` and `completed`, indexing it with a `GoalStatus` is type-safe and returns a `string`.

---

### Q8 — Literal Types (Debugging) ❌ 0/1

**Question:** Identify the three type errors in the `Role` / `User` code.

**Your answer:**

```
1. "Editor" is not assignable, Literal types are case-sensitive
2. "string" is not assignable to type "number"
3. "Editor" is not assignable to type "Role", only "admin" | "editor" | "viewer" are allowed.
```

**Mistake:** Points 1 and 3 describe the **same** error (`role: "Editor"`). You missed the third error entirely: the function call at the bottom.

**Correct solution:** The three errors are:

1. `role: "Editor"` on Khushi's object. Literal types are case-sensitive, so `"Editor"` ≠ `"editor"`.
2. `id: "3"` on Karan's object. `string` is not assignable to `id: number`.
3. `setRole(users[0], "owner")`. `"owner"` is not one of the allowed `Role` values, so the argument isn't assignable to parameter `newRole: Role`.

**Explanation:** Literal unions are checked everywhere a value meets the type. That includes object literals, function parameters and return values, not just variable declarations. The `newRole: Role` parameter protects the function exactly the way the `role: Role` property protects the object.

**Improvement:** In debugging tasks, review every line top to bottom, including function calls at the end. When your list repeats an item, take that as a signal that you've missed something.

---

### Q9 — Interfaces ✅ 1/1

**Your answer:** `Author` and `Book` interfaces, a typed `books` array with two entries, and `getBookTitles` using `.map()`.

**Explanation:** Everything is correct. Nesting `author: Author` inside `Book` is the right way to model the relationship. `Array<Book>` and `Book[]` are equivalent.

---

### Q10 — Generics ✅ 1/1

**Your answer:** Call 2 and Call 5 error. The others compile.

**Explanation:** Both are correct. Call 2 actually has two mismatches (both arguments are swapped), and Call 5 fails because `strict` mode makes `null` a separate type that `string` doesn't include. The question asked for a result for each call, so next time explicitly write "compiles" for Calls 1, 3 and 4 rather than leaving it implied.

---

### Q11 — Generics + Interfaces ✅ 1/1

**Your answer:** A generic `ApiResponse<T>` interface, a generic `wrapResponse<T>` function, and calls with `Book` and `Book[]`.

**Explanation:** This is correct and avoids `any`. The explicit `<Book>` and `<Book[]>` type arguments are optional, because TypeScript infers `T` from the `data` argument. Both styles are valid.

---

### Q12 — Generics + Typed Functions ⚪ 0/1 (Unanswered)

**Question:** Build a generic `Paginated<T>` interface and a `paginate` function. Pages start at 1, `totalPages` rounds up, and paginating `[10…70]` on page 3 with size 3 should return `[70]`.

**Correct solution:**

```ts
interface Paginated<T> {
  items: T[];
  page: number;
  pageSize: number;
  totalItems: number;
  totalPages: number;
}

function paginate<T>(items: T[], page: number, pageSize: number): Paginated<T> {
  const start = (page - 1) * pageSize;
  const end = start + pageSize;

  return {
    items: items.slice(start, end),
    page,
    pageSize,
    totalItems: items.length,
    totalPages: Math.ceil(items.length / pageSize),
  };
}
```

**Explanation:**

- **Generics:** `T` links the input array type to the output's `items` type. Paginating `number[]` gives `Paginated<number>`, and paginating `Book[]` gives `Paginated<Book>`.
- **Page offset:** Pages start at 1, so page 3 starts at index `(3 − 1) × 3 = 6`. `slice(6, 9)` returns `[70]`. `slice` safely stops at the end of the array.
- **Rounding:** `Math.ceil(7 / 3)` gives `3`, which rounds up as required.

**Improvement:** This combined the same generic-interface pattern you used correctly in Q11 with basic array logic. Next time, attempt the type definitions first, even if the logic feels harder. You'd likely have got most of it.

## D. Topic-Wise Performance

| Topic                                  | Correct | Total | Accuracy |
| -------------------------------------- | ------- | ----- | -------- |
| Type Aliases & Interfaces (Q1, Q6, Q9) | 3       | 3     | 100%     |
| Union Types (Q4, Q5)                   | 2       | 2     | 100%     |
| Basic Types & Typed Functions (Q2, Q3) | 1       | 2     | 50%      |
| Literal Types (Q7, Q8)                 | 1       | 2     | 50%      |
| Generics (Q10, Q11, Q12)               | 2       | 3     | 67%      |

## E. Improvement Recommendations

**Overall:** Your conceptual understanding of TypeScript is solid. Nothing you got wrong came from misunderstanding how the type system works. Both incorrect answers came from **precision and thoroughness**:

- **Q2:** The output didn't match the exact specified format.
- **Q8:** You counted the same error twice and missed one.

**Weak areas:**

1. **Checking output against the specification.** Correct types don't guarantee correct values.
2. **Systematic debugging.** Check every line, especially function calls and arguments.
3. **Applying generics alongside real logic.** You can define generic types well; now practise writing generic functions that also do processing.

**Practice exercises:**

1. **Generic search helper.** Write a generic function `findById` that accepts an array of objects of type `T` and a numeric `id`, and returns the matching item. Define two interfaces (`Book` and `Employee`), each with an `id: number`, and call the function with both. Decide and annotate what should be returned when no match is found.

2. **Literal union debugging drill.** Write a `Priority` literal union (`"low" | "medium" | "high"`) and a `Task` interface using it. Then deliberately write five lines that misuse it: in an object literal, a variable assignment, a function argument, a function return value, and an array. Predict each compiler error before checking it in an editor.

3. **Exact-format functions.** Write `formatSalary(name: string, amount: number, currency: "INR" | "USD"): string` so that `("Jatin", 50000, "INR")` returns exactly `"Jatin earns INR 50000/month"`. Then write three more test inputs and their expected outputs before running them.

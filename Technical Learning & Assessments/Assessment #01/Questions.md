# Technical Assessment #1 — Mixed Topics

The 12 questions run from easy to challenging. Answer every question without running the code first if possible, then submit.

---

**Question 1 — SQL (PostgreSQL)**

**Difficulty:** Easy
**Type:** SQL

**Question:** Using the schema below, write a query that returns the **3 highest-paid employees**.

**Requirements:**

- Return `name` and `salary` only.
- Employees whose salary is not recorded must **not** appear in the results.
- Highest salary first.

**Starter Schema:**

```sql
CREATE TABLE departments (
  id   SERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL
);

CREATE TABLE employees (
  id            SERIAL PRIMARY KEY,
  name          VARCHAR(50) NOT NULL,
  salary        NUMERIC(10,2),
  department_id INT REFERENCES departments(id)   -- nullable
);

INSERT INTO departments (name) VALUES
('Engineering'), ('Sales'), ('HR'), ('Legal');

INSERT INTO employees (name, salary, department_id) VALUES
('Asha',  85000, 1),
('Ravi',  62000, 1),
('Meera', 48000, 2),
('Kiran', 91000, 1),
('Neha',  55000, NULL),
('Arjun', 40000, 2),
('Pooja', NULL,  3);
```

**Marks:** 1

---

**Question 2 — TypeScript**

**Difficulty:** Easy
**Type:** Conceptual

**Question:** Consider these two declarations in the same file:

```ts
interface User {
  name: string;
}

interface User {
  age: number;
}
```

**Requirements:**

1. Explain what TypeScript does with these two declarations, and what shape an object of type `User` must have.
2. Explain what happens if you write the equivalent using **two `type User = ...` aliases** with the same name.
3. Give one practical situation where interface merging is useful.

**Marks:** 1

---

**Question 3 — Python**

**Difficulty:** Easy
**Type:** Output Prediction

**Question:** Write the **exact output** of this program, line by line.

```python
class Enemy:
    def __init__(self, name, health):
        self.name = name
        self.health = health

    def talk(self):
        return f"{self.name} says nothing."

    def take_damage(self, amount):
        self.health -= amount
        return self.health


class Zombie(Enemy):
    def __init__(self, health):
        super().__init__("Zombie", health)

    def talk(self):
        return "Grrr..."


z = Zombie(50)
e = Enemy("Goblin", 30)

print(z.talk())
print(e.talk())
print(z.take_damage(15))
print(z.health, e.health)
print(z.name)
```

**Requirements:** Give the exact printed output. Then explain in one or two sentences why the first and the last lines print what they do.

**Marks:** 1

---

**Question 4 — SQL (PostgreSQL)**

**Difficulty:** Medium
**Type:** SQL

**Question:** Using the **same schema and data as Question 1**, find every department that has **no employees**.

**Requirements:**

- Use a `LEFT JOIN`.
- Return the department `id` and `name`.
- Order by department name.

**Marks:** 1

---

**Question 5 — JavaScript**

**Difficulty:** Medium
**Type:** Coding

**Question:** Write a function `summarizeScores(students)`.

**Requirements:**

- **Input:** an array of objects shaped `{ name: string, score: number }`.
- **Output:** an object with this shape:
  ```js
  {
    passed: [...],   // names of students with score >= 40, in input order
    failed: [...],   // names of students with score < 40, in input order
    topScorer: ...   // name of the student with the highest score
  }
  ```
- If two students tie for the highest score, `topScorer` is the one who appears **first**.
- If the input array is empty, return `{ passed: [], failed: [], topScorer: null }`.
- Do not use any external libraries.

**Example input:**

```js
summarizeScores([
  { name: "Amit", score: 72 },
  { name: "Sara", score: 35 },
  { name: "Leo", score: 88 },
  { name: "Ira", score: 40 },
]);
```

**Marks:** 1

---

**Question 6 — TypeScript**

**Difficulty:** Medium
**Type:** Coding

**Question:** Write typed code for a small goal-tracking module.

**Requirements:**

1. Define a **literal-union type** `Priority` that allows only `'low'`, `'medium'` or `'high'`.
2. Define an **interface** `Goal` with `id` (number), `title` (string) and `priority` (Priority).
3. Write a function `getGoalsByPriority` that takes an array of goals and a priority and returns only the goals with that priority. Annotate the parameter and return types explicitly.
4. Write a **generic** function `lastOrDefault` that takes an array of any type and a fallback value of the same type. It returns the last element, or the fallback if the array is empty.
5. Show one valid call of each function. Then write **one call that TypeScript must reject** and explain why it is rejected.

**Marks:** 1

---

**Question 7 — React with TypeScript**

**Difficulty:** Medium
**Type:** Debugging

**Question:** In this Course Goals code, clicking "Delete" does not work correctly. The code has **at least two bugs**.

```tsx
// types.ts
export interface Goal {
  id: number;
  title: string;
  description: string;
}
```

```tsx
// CourseGoal.tsx
import { type PropsWithChildren } from "react";

type CourseGoalProps = PropsWithChildren<{
  id: number;
  title: string;
  onDelete: (id: number) => void;
}>;

export default function CourseGoal({
  id,
  title,
  onDelete,
  children,
}: CourseGoalProps) {
  return (
    <article>
      <h2>{title}</h2>
      {children}
      <button onClick={onDelete(id)}>Delete</button>
    </article>
  );
}
```

```tsx
// App.tsx (relevant part)
const [goals, setGoals] = useState<Goal[]>([]);

function handleDeleteGoal(id: number) {
  const index = goals.findIndex((goal) => goal.id === id);
  goals.splice(index, 1);
  setGoals(goals);
}
```

**Requirements:**

1. Identify each bug.
2. Explain what actually happens at runtime because of each bug.
3. Provide corrected code for both `CourseGoal.tsx` and `handleDeleteGoal`.

**Marks:** 1

---

**Question 8 — SQL (PostgreSQL)**

**Difficulty:** Challenging
**Type:** SQL

**Question:** Using the schema below, create a **view** and then query it.

**Requirements:**

1. Create a view named `user_locations` with the columns `user_id`, `user_name`, `street` and `city_name`.
2. The view must include **every user**, including users with no address. For those users, `street` and `city_name` should be `NULL`.
3. Write a query against the view that returns users who **live in Mumbai OR have no address**, ordered by `user_name`.

**Starter Schema:**

```sql
CREATE TABLE cities (
  id   SERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL
);

CREATE TABLE addresses (
  id      SERIAL PRIMARY KEY,
  street  VARCHAR(100) NOT NULL,
  city_id INT NOT NULL REFERENCES cities(id)
);

CREATE TABLE users (
  id         SERIAL PRIMARY KEY,
  name       VARCHAR(50) NOT NULL,
  address_id INT REFERENCES addresses(id)   -- nullable
);

INSERT INTO cities (name) VALUES ('Mumbai'), ('Pune'), ('Delhi');

INSERT INTO addresses (street, city_id) VALUES
('MG Road', 1),
('FC Road', 2),
('Linking Road', 1);

INSERT INTO users (name, address_id) VALUES
('Asha', 1),
('Rahul', 2),
('Sneha', NULL),
('Vikram', 3),
('Divya', NULL);
```

**Marks:** 1

---

**Question 9 — FastAPI**

**Difficulty:** Medium
**Type:** Coding

**Question:** Write a `GET /books` endpoint for the Books API that supports optional filters.

**Requirements:**

- Accept two **optional query parameters**:
  - `published_after` (int): return only books with `published_year` **greater than** this value.
  - `min_rating` (float): return only books with `rating` **greater than or equal to** this value.
- Apply each filter **only if it is provided**. With no parameters, return all books.
- Order results by `published_year`, newest first.
- Use `response_model` so the response is a list of `BookResponse`.
- Use the database session through `Depends(get_db)`.

**Starter Code:**

```python
from fastapi import FastAPI, Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import Session
from database import Base, get_db

app = FastAPI()

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    published_year = Column(Integer, nullable=False)
    rating = Column(Float, nullable=True)

class BookResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    author: str
    published_year: int
    rating: float | None = None

# Write your endpoint below
```

**Marks:** 1

---

**Question 10 — Python**

**Difficulty:** Challenging
**Type:** Coding

**Question:** Build a small battle simulation using classes, inheritance and a dictionary.

**Requirements:**

1. `Weapon` class with `name` and `damage` attributes.
2. `Enemy` base class with `name` and `health`, plus:
   - `take_damage(amount)`: reduces health but **never below 0**, and returns the remaining health.
   - `is_alive()`: returns `True` if health is greater than 0, otherwise `False`.
3. `Ogre` class that **inherits from `Enemy`**:
   - Its constructor takes `health` and a `weapon` (a `Weapon` object). The name is always `"Ogre"`.
   - `attack(target)`: deals the weapon's damage to `target` (any `Enemy`) and returns the string
     `"Ogre hits <target name> with <weapon name> for <damage> damage"`.
4. In the main script:
   - Create a dictionary `arsenal` holding two `Weapon` objects, keyed by weapon name (for example `"club"` with damage 20 and `"axe"` with damage 35).
   - Create an `Ogre` armed with the `"club"` taken from the dictionary.
   - Create an `Enemy` named `"Goblin"` with 50 health.
   - Using a loop, make the Ogre attack the Goblin until the Goblin is no longer alive. Print each attack message and the Goblin's remaining health after each attack.

**Marks:** 1

---

**Question 11 — FastAPI**

**Difficulty:** Challenging
**Type:** Debugging

**Question:** This delete endpoint is supposed to delete a book by ID. It has **at least three problems**.

```python
@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id)
    db.delete(book)
    return {"message": "Book deleted"}
```

**Requirements:**

1. Identify each problem.
2. Explain what happens at runtime, or in the database, because of each problem.
3. Provide a corrected endpoint that:
   - Returns a **404** with the detail `"Book not found"` when the book does not exist.
   - Actually removes the row from the database.
   - Returns `{"message": "Book deleted"}` on success.

**Marks:** 1

---

**Question 12 — React with TypeScript**

**Difficulty:** Challenging
**Type:** Coding

**Question:** Build the `NewGoal` form component and connect it to `App` using lifting state up.

**Requirements:**

_`NewGoal.tsx`:_

- Accepts one prop: `onAddGoal`, typed as a function that takes `goal: string` and `summary: string` and returns nothing.
- Holds two **controlled inputs** (goal title and summary) using typed `useState`.
- Has a submit handler with a correctly typed **form event** that prevents the page from reloading.
- If the goal title is empty or only whitespace, it must **not** call `onAddGoal`.
- After a successful add, both inputs are **cleared**.

_`App.tsx` (relevant part):_

- Holds `goals` state typed with the `Goal` interface from Question 7.
- Has a handler that receives the title and summary from `NewGoal`, creates a new `Goal` with a unique `id`, and adds it to state **without mutating** the existing array.
- Renders `<NewGoal />` with the handler passed in.

**Marks:** 1

---

## Assessment Summary

| Item                  | Detail     |
| --------------------- | ---------- |
| Total questions       | 12         |
| Total available marks | 12         |
| SQL (PostgreSQL)      | Q1, Q4, Q8 |
| TypeScript            | Q2, Q6     |
| React with TypeScript | Q7, Q12    |
| Python                | Q3, Q10    |
| FastAPI               | Q9, Q11    |
| JavaScript            | Q5         |

## How to Submit

1. Label each answer clearly, for example **"Q1:"** followed by your query, code or explanation. Put code in code blocks.
2. You can submit all answers in one message or a few at a time. I'll collect them without grading or giving hints.
3. If you skip a question, write **"Q\_: skipped"**. It will score 0 but stay in your report.
4. If a question's requirements are unclear, ask. I'll clarify the requirements without giving away the answer.
5. When you're done, say **"Evaluate My Answers"** to get the full report.

# Assessment #04: FastAPI Expense Tracker API

**Status:** Active. Answer every question without running the code first, then send **"Evaluate My Answers"**.

**Project:** a new standalone app in `fastapi/expense_tracker/`, laid out like your todo API:

```
fastapi/expense_tracker/
├── main.py
├── database.py
├── security.py          # Q10
├── models/              # Q2
├── schemas/             # Q3 (given) + Q4
└── routers/
    ├── auth.py          # /auth        (Q8, Q9)
    ├── categories.py    # /categories  (Q5, Q12)
    └── expenses.py      # /expenses    (Q6, Q7)
```

**Ground rules for this project:**

- The tables are created by the SQL script below, not by `Base.metadata.create_all()`.
- Expense routes are **not** protected by JWT. `user_id` is sent in the request body or query. Don't add authentication to expense or category routes.
- Use `bcrypt` directly and `python-jose`, the same as in your todo API.

---

## SQL Schema (PostgreSQL)

Save this as `fastapi/expense_tracker/schema.sql`, then run:

```bash
createdb -U postgres expenses
psql -U postgres -d expenses -f fastapi/expense_tracker/schema.sql
```

```sql
-- ===== Tables =====
CREATE TABLE users (
    id              SERIAL PRIMARY KEY,
    email           VARCHAR(255) NOT NULL UNIQUE,
    username        VARCHAR(50)  NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    is_active       BOOLEAN      NOT NULL DEFAULT TRUE
);

CREATE TABLE categories (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(200)
);

CREATE TABLE expenses (
    id          SERIAL PRIMARY KEY,
    title       VARCHAR(100)   NOT NULL,
    amount      NUMERIC(10, 2) NOT NULL CHECK (amount > 0),
    spent_on    DATE           NOT NULL,
    category_id INT REFERENCES categories(id) ON DELETE SET NULL,
    user_id     INT NOT NULL REFERENCES users(id) ON DELETE CASCADE
);

-- ===== Seed data =====
-- These hashes are placeholders, so the seed users cannot log in.
-- Register new users through the API to test login.
INSERT INTO users (email, username, hashed_password, is_active) VALUES
('asha@example.com', 'asha',    'seed-placeholder-hash', TRUE),   -- id 1
('ravi@example.com', 'ravi',    'seed-placeholder-hash', TRUE),   -- id 2
('old@example.com',  'olduser', 'seed-placeholder-hash', FALSE);  -- id 3

INSERT INTO categories (name, description) VALUES
('Food',          'Meals and groceries'),   -- id 1
('Travel',        'Commute and trips'),     -- id 2
('Utilities',     'Bills'),                 -- id 3
('Entertainment', NULL);                    -- id 4 (no expenses)

INSERT INTO expenses (title, amount, spent_on, category_id, user_id) VALUES
('Lunch at office',     250.00,  '2026-10-01', 1,    1),  -- id 1
('Metro card recharge', 500.00,  '2026-10-03', 2,    1),  -- id 2
('Electricity bill',    1840.50, '2026-10-05', 3,    2),  -- id 3
('Groceries',           1320.00, '2026-10-07', 1,    2),  -- id 4
('Cab to airport',      760.00,  '2026-10-10', 2,    1),  -- id 5
('Misc cash',           100.00,  '2026-10-12', NULL, 1);  -- id 6
```

---

**Question 1 — FastAPI: Project Setup**

**Difficulty:** Easy
**Type:** Coding
**Marks:** 1

**Problem:** Write `database.py` and `main.py`.

**Requirements:**

- Connection URL: `postgresql+psycopg://postgres:postgres@localhost:5432/expenses`
- Create a session factory with `autocommit=False` and `autoflush=False`, plus a declarative `Base`.
- `get_db()` yields a session and always closes it, even if the request raises an error.
- Export `DB_DEPENDENCY = Annotated[Session, Depends(get_db)]`.
- `main.py` creates the app and includes the `auth`, `categories`, and `expenses` routers. It must not call `create_all`.

---

**Question 2 — SQLAlchemy: Models**

**Difficulty:** Easy
**Type:** Coding
**Marks:** 1

**Problem:** Write the SQLAlchemy models `User`, `Category`, and `Expense` so they map exactly onto the three tables above.

**Requirements:**

- Use the correct table names, column types, lengths, `nullable`, `unique`, and primary keys.
- `is_active` defaults to `True`.
- `category_id` and `user_id` are foreign keys, and their nullability must match the schema.
- `amount` must use a type suitable for `NUMERIC(10, 2)`, and `spent_on` must use a date type.
- `relationship()` is not required.

---

**Question 3 — Pydantic: Field Validation**

**Difficulty:** Easy
**Type:** Output Prediction
**Marks:** 1

**Problem:** This is the given `ExpenseCreate` schema (use it as-is in your project):

```python
from datetime import date
from pydantic import BaseModel, Field

class ExpenseCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    amount: float = Field(gt=0)
    spent_on: date
    category_id: int | None = Field(default=None, gt=0)
    user_id: int = Field(gt=0)
```

For each request body sent to `POST /expenses`, state whether validation **passes** or returns **422**. If it's 422, name the field that fails and the reason.

```json
// A
{"title": "Tea", "amount": 20, "spent_on": "2026-10-20", "user_id": 1}

// B
{"title": "Bus ticket", "amount": 0, "spent_on": "2026-10-20", "user_id": 1}

// C
{"title": "TV", "amount": 15000, "spent_on": "2026-10-21", "user_id": 2}

// D
{"title": "Movie", "amount": 350, "spent_on": "2026-10-21", "category_id": null, "user_id": 2}

// E
{"title": "Snacks", "amount": 45.5, "user_id": 1}
```

**Requirements:** Give one verdict per body (A to E), with a reason for each 422.

---

**Question 4 — Pydantic: Remaining Schemas**

**Difficulty:** Medium
**Type:** Coding
**Marks:** 1

**Problem:** Write the rest of the schemas.

**Requirements:**

- `UserCreate`: `email` (str), `username` (3–50 chars), `password` (minimum 8 chars).
- `UserResponse`: `id`, `email`, `username`, `is_active`. It must never expose the password or the hash.
- `CategoryCreate`: `name` (2–50 chars) and an optional `description` (max 200 chars).
- `CategoryResponse`: `id`, `name`, `description`.
- `ExpenseResponse`: every column of `expenses`. Its types must match what the database can actually return.
- `ExpenseListResponse`: a wrapper with `count: int` and `data: list[ExpenseResponse]`.
- `Token`: `access_token` and `token_type`.
- Every response schema must be buildable directly from a SQLAlchemy object.

---

**Question 5 — FastAPI: Categories Router**

**Difficulty:** Medium
**Type:** Coding
**Marks:** 1

**Problem:** Write `routers/categories.py`.

**Requirements:**

- `APIRouter` with prefix `/categories` and tag `categories`.
- `POST /categories`: creates a category and returns `201` with `CategoryResponse`.
- `GET /categories`: returns all categories ordered by `name` ascending.
- `GET /categories/{category_id}`: `category_id` must be greater than 0. If the category is missing, return `404` with detail `"Category not found"`.
- Use `DB_DEPENDENCY` in every route.

---

**Question 6 — FastAPI: Filtered Listing with a Response Wrapper**

**Difficulty:** Medium
**Type:** Coding
**Marks:** 1

**Problem:** Write `GET /expenses` in `routers/expenses.py`.

**Requirements:**

- Three optional query parameters, each validated as greater than 0 when supplied: `user_id`, `category_id`, `min_amount`.
- Filters combine with AND. For example, `?user_id=1&category_id=2` returns only user 1's Travel expenses.
- `min_amount` is inclusive (`amount >= min_amount`).
- Results are ordered by `spent_on` with the newest first.
- The response uses `ExpenseListResponse`, where `count` is the number of items in `data`.
- If nothing matches, return `200` with `count: 0` and an empty list, **not** a 404.

---

**Question 7 — FastAPI: Create, Update, Delete with Existence Checks**

**Difficulty:** Medium
**Type:** Coding
**Marks:** 1

**Problem:** Write `POST /expenses`, `PUT /expenses/{expense_id}`, and `DELETE /expenses/{expense_id}`.

**Requirements:**

- `POST` takes `ExpenseCreate` and returns `201` with `ExpenseResponse`.
- `PUT` takes `ExpenseCreate`, replaces every field of the expense, and returns `ExpenseResponse`.
- On both `POST` and `PUT`:
  - If `category_id` is supplied but doesn't exist, return `404` with `"Category not found"`.
  - If the user doesn't exist **or is inactive**, return `404` with `"User not found"`.
- `PUT` and `DELETE` on a missing expense return `404` with `"Expense not found"`.
- `DELETE` returns `204` with no body.
- `expense_id` must be greater than 0.

---

**Question 8 — bcrypt: Debug the Register Endpoint**

**Difficulty:** Medium
**Type:** Debugging
**Marks:** 1

**Problem:** This endpoint contains **at least four** bugs. List every bug, explain why it's wrong, and give the corrected endpoint.

```python
@router.post("/register", response_model=UserCreate)
def register(user: UserCreate, db: DB_DEPENDENCY):
    hashed = bcrypt.hashpw(user.password, bcrypt.gensalt())
    new_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed,
        is_active=False,
    )
    db.add(new_user)
    db.commit()
    return new_user
```

**Requirements:** The fixed endpoint returns `201` with `UserResponse`. The new user must be active, and the stored hash must be verifiable later with `bcrypt.checkpw`.

---

**Question 9 — Authentication: Debug `authenticate_user` and `sign_in`**

**Difficulty:** Challenging
**Type:** Debugging
**Marks:** 1

**Problem:** Find and fix every bug in this code.

```python
def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if bcrypt.checkpw(user.hashed_password.encode("utf-8"), password.encode("utf-8")):
        return user
    return user


@router.post("/sign_in", response_model=Token)
def sign_in(form_data: OAuth2PasswordRequestForm, db: DB_DEPENDENCY):
    user = authenticate_user(form_data.email, form_data.password, db)
    if not user:
        raise HTTPException(status_code=404, detail="Invalid credentials")
    token = create_access_token(user.username, user.id)
    return {"access_token": token, "token_type": "bearer"}
```

**Requirements:**

- An unknown username, a wrong password, and an inactive user must **all** return `401` with `"Invalid credentials"`, and none of them may crash the server.
- `sign_in` must accept form data, not a JSON body.
- `authenticate_user` returns the user on success and `None` (or `False`) otherwise.

---

**Question 10 — JWT: Create and Decode Tokens**

**Difficulty:** Challenging
**Type:** Coding
**Marks:** 1

**Problem:** Write `security.py`.

**Requirements:**

- Define `SECRET_KEY` and `ALGORITHM = "HS256"`.
- `create_access_token(username: str, user_id: int, expires_delta: timedelta = timedelta(minutes=30)) -> str` puts `sub`, `id`, and `exp` in the payload. `exp` must be timezone-aware UTC.
- Define `oauth2_scheme` as an `OAuth2PasswordBearer` whose `tokenUrl` points to the sign-in route from Q9.
- `decode_jwt(token: Annotated[str, Depends(oauth2_scheme)]) -> dict` returns `{"username": ..., "id": ...}`.
- `decode_jwt` raises `401` with `"Could not validate credentials"` when:
  - the token is invalid or expired, or
  - the token is valid but `sub` or `id` is missing.
- Don't attach `decode_jwt` to any route.

---

**Question 11 — FastAPI: Predict the Responses**

**Difficulty:** Challenging
**Type:** Output Prediction
**Marks:** 1

**Problem:** Use this code and a freshly seeded database:

```python
class ExpenseOut(BaseModel):
    id: int
    title: str
    amount: float
    category_id: int | None
    model_config = ConfigDict(from_attributes=True)


@router.get("/{expense_id}", response_model=ExpenseOut)
def get_expense(expense_id: Annotated[int, Path(gt=0)], db: DB_DEPENDENCY):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.delete("/{expense_id}", status_code=204)
def delete_expense(expense_id: Annotated[int, Path(gt=0)], db: DB_DEPENDENCY):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()
```

Predict each response. The requests run **in this order**:

1. `GET /expenses/3`
2. `GET /expenses/6`
3. `GET /expenses/0`
4. `DELETE /expenses/6`
5. `DELETE /expenses/6`
6. `GET /expenses/abc`

**Requirements:**

- For 200 and 404 responses, give the status code and the exact JSON body.
- For 204, give the status code and say what the body is.
- For 422, give the status code and the reason. You don't need the full error body.

---

**Question 12 — Scenario: Deleting Categories and Users**

**Difficulty:** Challenging
**Type:** Coding + Conceptual
**Marks:** 1

**Problem:** Write `DELETE /categories/{category_id}`: `204` on success, `404` with `"Category not found"`, and `Path(gt=0)`. Then answer these questions, starting from a **fresh seed** each time:

a) After `DELETE /categories/2`, what happens to expenses 2 and 5 in the database? Which part of the system causes it, FastAPI or PostgreSQL?

b) If `ExpenseResponse.category_id` were typed as plain `int` instead of `int | None`, what would happen when you call `GET /expenses?user_id=1` after step (a)? Give the status code and explain why.

c) If you run `DELETE FROM users WHERE id = 1;` directly in psql, how many rows are left in `expenses`, and which ones?

d) If `expenses.user_id` had been declared without any `ON DELETE` rule, what would happen in (c)?

**Requirements:** The endpoint code, plus an answer to each of a, b, c, and d.

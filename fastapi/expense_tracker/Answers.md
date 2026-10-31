# Assessment #04: FastAPI Expense Tracker API (Evaluation Report)

**Date:** 2026-10-31
**Topic:** FastAPI + SQLAlchemy + Pydantic + bcrypt + JWT
**Project:** `fastapi/expense_tracker/` (`users`, `categories`, `expenses` on PostgreSQL)
**Rules:** answered without running the code first; 1 mark per question; no partial marks.

---

## A. Overall Results

| Metric | Result |
|---|---|
| Total Questions | 12 |
| Correct Answers | 4 |
| Incorrect Answers | 7 |
| Unanswered | 1 |
| Final Score | 4/12 |
| Percentage | 33.3% |

## B. Question-Wise Scorecard

| # | Topic | Type | Result | Marks |
|---|---|---|---|---|
| 1 | Project setup (`database.py`, `main.py`) | Coding | Correct | 1 |
| 2 | SQLAlchemy models | Coding | Incorrect | 0 |
| 3 | Pydantic `Field` validation | Output Prediction | Correct | 1 |
| 4 | Remaining Pydantic schemas | Coding | Incorrect | 0 |
| 5 | Categories router | Coding | Correct | 1 |
| 6 | Filtered listing + response wrapper | Coding | Correct | 1 |
| 7 | Create / update / delete with existence checks | Coding | Incorrect | 0 |
| 8 | bcrypt register endpoint | Debugging | Incorrect | 0 |
| 9 | `authenticate_user` + `sign_in` | Debugging | Incorrect | 0 |
| 10 | JWT create / decode | Coding | Incorrect | 0 |
| 11 | Predict the responses | Output Prediction | Incorrect | 0 |
| 12 | Deleting categories and users (ON DELETE) | Coding + Conceptual | Unanswered | 0 |

Six of the seven incorrect answers were *almost* right. Each one missed a single stated requirement or edge case. This is the same pattern noted in Assessment #01.

---

## C. Detailed Evaluation

### Q1: Project Setup

**Question:** Write `database.py` (engine, session factory with `autocommit=False` and `autoflush=False`, `Base`, `get_db` that always closes the session, `DB_DEPENDENCY`) and `main.py` (include the three routers, no `create_all`).

**My Answer:** `sessionmaker(bind=engine, autoflush=False)`, with `autocommit` left out because it's deprecated. `get_db` uses `try`/`finally`. `DB_DEPENDENCY = Annotated[Session, Depends(get_db)]`. `main.py` includes the `auth`, `categories`, and `expenses` routers.

**Result:** Correct. **Score:** 1/1

**Why it works:**
- `get_db` closes the session in `finally`, so it closes even when the request raises an error.
- Leaving out `autocommit=False` is fine. In SQLAlchemy 2.0, `False` is the only allowed value and it's the default.
- The local database password differs from the spec, which is harmless.

---

### Q2: SQLAlchemy Models

**Question:** Write `User`, `Category`, and `Expense` so they map exactly onto the SQL tables: types, lengths, nullability, unique, primary keys, foreign keys, and `is_active` defaulting to `True`.

**My Answer:** All three models. `Category.description = Column(Text(200))`.

**Result:** Incorrect. **Score:** 0/1

**Mistake:** `Text(200)` where the schema says `VARCHAR(200)`.

**Correct Solution:**
```python
description = Column(String(200))
```

**Why It Was Wrong:**
- `Text` maps to PostgreSQL `TEXT`, which has no length limit. On PostgreSQL the `200` is ignored.
- The question required an exact mapping of types and lengths.
- It runs here only because the SQL script created the table. If anyone builds the tables from these models, they get the wrong column.

Everything else was correct: the foreign keys with matching `ondelete`, `Numeric(10, 2)`, `Date`, the nullability, and the `CheckConstraint`.

**Improvement:** Compare the model against the schema line by line. `VARCHAR(n)` maps to `String(n)`, and `TEXT` maps to `Text`.

---

### Q3: Pydantic Field Validation

**Question:** Using the given `ExpenseCreate`, predict whether bodies A to E pass or return 422.

**My Answer:**
- A passes.
- B returns 422 (`amount` must be > 0).
- C returns 422 (`title` is shorter than 3 characters).
- D passes.
- E returns 422 (`spent_on` is missing).

**Result:** Correct. **Score:** 1/1

**Why it works:**
- `null` is valid for an optional field (D).
- `gt=0` rejects `0` (B).
- `min_length=3` rejects `"TV"` (C).
- A required field with no default must be present (E).

---

### Q4: Remaining Schemas

**Question:** Write `UserCreate` (username 3–50), `UserResponse` (no password), `CategoryCreate` and `CategoryResponse`, `ExpenseResponse` (all columns, matching types), `ExpenseListResponse`, and `Token`. Every response schema must be buildable directly from a SQLAlchemy object.

**My Answer:**
- `username: str = Field(min_length=3, max_length=100)`.
- `CategoryResponse(CategoryCreate)` and `ExpenseResponse(ExpenseCreate)` inherit from the create models.
- Only `ExpenseOut` has `from_attributes=True`.

**Result:** Incorrect. **Score:** 0/1

**Mistakes:**
1. `max_length=100` breaks the 3–50 requirement, and the database column is `VARCHAR(50)`. A 60-character username passes Pydantic, then fails at the database, which returns a 500 instead of a clean 422.
2. `UserResponse`, `CategoryResponse`, and `ExpenseResponse` don't have `from_attributes=True`. FastAPI's own response handling copes, so the routes work, but `ExpenseResponse.model_validate(expense_obj)` raises an error. That was the stated requirement.

**Correct Solution (relevant parts):**
```python
class UserCreate(BaseModel):
    email: str
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8)


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    is_active: bool
    model_config = ConfigDict(from_attributes=True)


class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str | None
    model_config = ConfigDict(from_attributes=True)


class ExpenseResponse(BaseModel):
    id: int
    title: str
    amount: float
    spent_on: date
    category_id: int | None
    user_id: int
    model_config = ConfigDict(from_attributes=True)
```

**Why It Was Wrong:** Validation limits must match the database columns, and the ORM-compatibility requirement was not met.

**Improvement:** Don't inherit response models from create models. `ExpenseResponse(ExpenseCreate)` also inherits input rules like `min_length=3`. Any existing row that breaks an input rule (for example, a title inserted through SQL) then turns a read into a 500 error. A response should describe the data, not validate input.

---

### Q5: Categories Router

**Question:** `APIRouter` with prefix `/categories`. `POST` returns 201, `GET` lists ordered by name, and `GET /{category_id}` uses `Path(gt=0)` and returns 404 `"Category not found"`.

**My Answer:** All three routes, plus a `find_category` helper. The list route returns `{"data": [...]}`, and the 404 detail is `"Category not found!"`.

**Result:** Correct. **Score:** 1/1

**Why it works:**
- The prefix, tag, 201 status, `order_by(Category.name.asc())`, `Path(gt=0)`, and 404 handling are all correct.
- A `{"data": [...]}` wrapper is an acceptable design choice.

**Note:** the trailing `!` in the detail wasn't deducted, but clients sometimes match on these strings, so copy them exactly.

---

### Q6: Filtered Listing

**Question:** `GET /expenses` with optional `user_id`, `category_id`, and `min_amount` (all > 0, combined with AND, `min_amount` inclusive), newest first, wrapped in `ExpenseListResponse`, and 200 with an empty list when nothing matches.

**My Answer:** Chained `.filter()` calls guarded by `is not None`, `order_by(Expense.spent_on.desc())`, and `{"count": len(expenses), "data": expenses}`. `min_amount` is typed `int`.

**Result:** Correct. **Score:** 1/1

**Why it works:** The filters combine correctly, `>=` makes `min_amount` inclusive, the order is right, and an empty result is not treated as an error.

**Note:** `min_amount: int` rejects `?min_amount=99.50` with a 422, even though amounts are `NUMERIC(10, 2)`. The spec didn't fix the type, so no deduction, but `float` is the better match for a money column.

---

### Q7: Create, Update, Delete

**Question:**
- `POST` returns 201.
- `PUT` replaces every field.
- `DELETE` returns 204 with no body.
- A supplied but missing `category_id` returns 404 `"Category not found"`.
- A missing or inactive user returns 404 `"User not found"`.
- A missing expense returns 404 `"Expense not found"`.

**My Answer:** `find_category(db, body.category_id)` is called unconditionally in `POST` and `PUT`. `find_user` filters on `is_active == True`. `DELETE` has no `status_code`.

**Result:** Incorrect. **Score:** 0/1

**Mistakes:**
1. **The optional category is treated as required.** When `category_id` is `None`, the filter `id == NULL` never matches, so every expense without a category gets 404 `"Category not found"`. Body D from Q3, which you correctly said passes validation, is rejected here.
2. **`DELETE` returns 200, not 204.** FastAPI defaults to 200 unless the status code is set.

The inactive-user check through `find_user` is correct.

**Correct Solution:**
```python
def check_references(db, body: ExpenseCreate):
    if body.category_id is not None and find_category(db, body.category_id) is None:
        raise HTTPException(status_code=404, detail="Category not found")
    if find_user(db, body.user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")


@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
async def create_expense(db: DB_DEPENDENCY, body: ExpenseCreate):
    check_references(db, body)
    new_expense = Expense(**body.model_dump())
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense


@router.put("/{expense_id}", response_model=ExpenseResponse)
async def update_expense(
    db: DB_DEPENDENCY, body: ExpenseCreate, expense_id: Annotated[int, Path(gt=0)]
):
    expense = find_expense(db, expense_id)
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    check_references(db, body)
    for field, value in body.model_dump().items():
        setattr(expense, field, value)
    db.commit()
    db.refresh(expense)
    return expense


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(db: DB_DEPENDENCY, expense_id: Annotated[int, Path(gt=0)]):
    expense = find_expense(db, expense_id)
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()
```

**Why It Was Wrong:** An optional foreign key is validated only when it's supplied, and a status code that isn't set falls back to 200.

**Improvement:** For every optional field, ask: "What happens when this is `None`?"

---

### Q8: bcrypt Register Endpoint

**Question:** The register endpoint has at least four bugs. Fix it so it returns 201 with `UserResponse`, the user is active, and the hash can be verified with `bcrypt.checkpw`.

**My Answer:**
- Bugs listed: wrong `response_model`, missing `db.refresh`, missing encode/decode, `is_active=False`.
- The fixed code uses `response_model=UserResponse` and a `create_hashed_password` helper, and has no `status_code`.

**Result:** Incorrect. **Score:** 0/1

**Mistakes:**
1. **The 201 status code is missing**, so the fixed endpoint returns 200.
2. The missing `db.refresh` isn't actually a bug. With the default `expire_on_commit=True`, reading `new_user.id` after `commit()` reloads the row automatically. Adding `refresh` is harmless and explicit, but the original code didn't need it.

You correctly found the response-model leak, `str` → `bytes` for hashing, `bytes` → `str` for storage, and the inactive default. Relying on the model's `default=True` is fine.

**Correct Solution:** your code, plus the status code:
```python
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
```

**Why It Was Wrong:** Missing the status code was a requirement miss.

**Improvement:** Treat the status code as part of every endpoint's contract.

---

### Q9: Authentication Debugging

**Question:** Fix `authenticate_user` and `sign_in`. An unknown user, a wrong password, and an inactive user must all return 401 `"Invalid credentials"` without crashing, and `sign_in` must accept form data.

**My Answer:**
- A `None` check.
- `verify_hashed_password(plain, hashed)` with the correct `checkpw` order.
- `Annotated[OAuth2PasswordRequestForm, Depends()]` and `form_data.username`.
- 401 instead of 404.
- The user query filters only on `username`.

**Result:** Incorrect. **Score:** 0/1

**Mistake:** No `is_active` check. An inactive user with the correct password still gets a token. You filtered active users correctly in `find_user` (Q7), but not here.

**Correct Solution:**
```python
def authenticate_user(username: str, password: str, db):
    user = (
        db.query(User)
        .filter(User.username == username, User.is_active == True)
        .first()
    )
    if user is None or not verify_hashed_password(password, user.hashed_password):
        return None
    return user
```

**Why It Was Wrong:** Login must reject inactive accounts. That is the purpose of the `is_active` flag.

**Improvement:** Before finishing, check your code against each failure case in the requirements: an unknown user, a wrong password, and an inactive user.

---

### Q10: JWT Create and Decode

**Question:**
- `create_access_token(username, user_id, expires_delta=timedelta(minutes=30))` puts `sub`, `id`, and `exp` (aware UTC) in the token.
- `oauth2_scheme` points to the sign-in route.
- `decode_jwt` returns `{"username", "id"}`.
- `decode_jwt` raises 401 on an invalid or expired token, or on missing claims.

**My Answer:**
- `SECRET_KEY`, `ALGORITHM = "HS256"`, and `OAuth2PasswordBearer(tokenUrl="auth/sign_in")`.
- `create_access_token` has no default for `expires_delta`.
- `decode_jwt` returns `{"username": ..., "user_id": ...}`.

**Result:** Incorrect. **Score:** 0/1

**Mistakes:**
1. `expires_delta` has no default, so `create_access_token(name, id)` raises `TypeError`.
2. The return key is `user_id`, but the required key is `id`. Any code that reads `payload["id"]` breaks.

The correct parts were the constants, `tokenUrl`, the aware `exp`, the missing-claim checks, and catching `JWTError` (which covers expired tokens too).

**Correct Solution (changed lines):**
```python
def create_access_token(
    username: str, user_id: int, expires_delta: timedelta = timedelta(minutes=30)
) -> str:
    ...

return {"username": username, "id": user_id}
```

**Why It Was Wrong:** The function signature and return shape are part of the specification.

**Improvement:** The repo is public. Anyone who reads a hardcoded `SECRET_KEY` can forge valid tokens, so move it to an environment variable.

---

### Q11: Predict the Responses

**Question:** On a freshly seeded database, predict the status and body of six requests run in order against `GET`/`DELETE /expenses/{expense_id}` with `response_model=ExpenseOut`.

**My Answer:**
- 1: 200, correct body.
- 2: 200 with `"category_id": 3`.
- 3: 422 (`greater_than`).
- 4: 204 with body `null`.
- 5: 404.
- 6: 422 (`greater_than`).

**Result:** Incorrect. **Score:** 0/1

**Mistakes:**
- **Request 2:** expense 6 has `category_id = NULL` in the seed data, so the response shows `null`. A small detail: the float field also serializes as `100.0`.
- **Request 4:** a 204 response has an **empty body**, not JSON `null`.
- **Request 6:** `"abc"` fails **integer parsing** (`int_parsing`) before the `gt=0` constraint is ever checked. The request 3 error was copied.

**Correct Solution:**

| # | Status | Body |
|---|---|---|
| 1 | 200 | `{"id": 3, "title": "Electricity bill", "amount": 1840.5, "category_id": 3}` |
| 2 | 200 | `{"id": 6, "title": "Misc cash", "amount": 100.0, "category_id": null}` |
| 3 | 422 | `Path(gt=0)` rejects 0 before the handler runs |
| 4 | 204 | Empty body (no content) |
| 5 | 404 | `{"detail": "Expense not found"}` |
| 6 | 422 | Type check fails: `"abc"` is not a valid integer |

**Why It Was Wrong:** The seed data wasn't checked for request 2, 204 was confused with a null body, and the validation order was reversed for request 6.

**Improvement:**
- Read the seed row for every request.
- Validation runs in order: type first, then constraints.
- 204 means "no content".

---

### Q12: Deleting Categories and Users

**Question:** Write `DELETE /categories/{category_id}` (204, 404, `Path(gt=0)`), then answer a to d about `ON DELETE SET NULL` / `CASCADE`, a non-optional `category_id` in the response model, and the default behaviour when there is no `ON DELETE` rule.

**My Answer:** Skipped.

**Result:** Unanswered. **Score:** 0/1

**Correct Solution:**
```python
@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(db: DB_DEPENDENCY, category_id: Annotated[int, Path(gt=0)]):
    category = find_category(db, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
```

**a)** Expenses 2 and 5 stay in the table, and their `category_id` becomes `NULL`. **PostgreSQL** does this through `ON DELETE SET NULL`. FastAPI only sends the `DELETE`.

**b)** The response is **500 Internal Server Error** (a response validation error).
- User 1's rows have `category_id = NULL`, and a plain `int` field can't hold `None`.
- This fails even before step (a), because expense 6 is already `NULL` in the seed data.
- The request itself is valid, so this is a server-side error, not a 422.

**c)** **2 rows** remain: expenses 3 and 4, which belong to Ravi. `ON DELETE CASCADE` removes user 1's expenses 1, 2, 5, and 6.

**d)** With no rule, PostgreSQL uses the default `NO ACTION` behavior. The `DELETE` **fails with a foreign key violation**, and nothing is deleted.

**Improvement:** This is the same area lost in Assessment #03 (cascading deletes). Revisit it with practice exercise 3.

---

## D. Topic-Wise Performance

| Topic | Questions | Correct | Accuracy |
|---|---|---|---|
| Setup + SQLAlchemy models | Q1, Q2 | 1/2 | 50% |
| Pydantic | Q3, Q4 | 1/2 | 50% |
| Routers + CRUD | Q5, Q6, Q7 | 2/3 | 67% |
| Auth (bcrypt, login, JWT) | Q8, Q9, Q10 | 0/3 | 0% |
| HTTP behaviour prediction | Q11 | 0/1 | 0% |
| ON DELETE + response models | Q12 | 0/1 | 0% |

## E. Learning Gap Analysis

**Strong concepts:**
- Session and dependency setup
- `Field` validation rules
- `APIRouter` structure
- Query-parameter filtering
- 404 handling
- bcrypt encoding and decoding
- `OAuth2PasswordRequestForm` wiring
- JWT claims and error handling

**Weak concepts:**
- **Requirement completeness.** Status codes (Q7, Q8), signature and return shape (Q10), the length limit (Q4), and the active filter (Q9) all share one root cause.
- **Optional / `NULL` handling** (Q7, Q11, Q12).
- **ON DELETE behaviour** across the database and API layers (Q12, also in #03).

**Repeated mistake:** "missed one requirement or edge case", which appeared in #01 and now in six questions here. The knowledge is mostly there; the checking before submitting is what's losing marks.

**Habit to build:** before submitting each answer, copy the requirements list and tick off every item against the code.

## Progress

| # | Topic | Score |
|---|---|---|
| 01 | Mixed | 25% (FastAPI question unanswered) |
| 02 | TypeScript | 75% |
| 03 | PostgreSQL | 58% |
| 04 | FastAPI | 33% |

In #01 the FastAPI question was left blank. This time nearly the whole API was built, and the lost marks are spec misses rather than missing concepts.

## F. Recommended Practice

1. **Optional references and status codes.** Add a `notes` table (`id`, `body`, an optional `expense_id` FK with `ON DELETE CASCADE`). Write `POST /notes`, which validates `expense_id` only when it's supplied, and `DELETE /notes/{id}`, which returns 204. List 6 requests, including one without `expense_id` and one with a nonexistent ID, and write down the expected status code for each before running anything.
2. **Auth failure matrix.** Write a table with five cases: unknown user, wrong password, inactive user with the correct password, active user with the correct password, and an expired token passed to `decode_jwt`. Write the expected status and response for each case, then rewrite `authenticate_user`, `create_access_token`, and `decode_jwt` from scratch so they match the table exactly.
3. **ON DELETE prediction.** Using `sql/relations_company.sql` and the #03 seed data, write three `DELETE` statements, predict the row counts in every table after each one, and then run them to check your predictions.

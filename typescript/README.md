# TypeScript

TypeScript fundamentals in one scratch file, then the same ideas applied to props, state, and events in a small React app.

## What's here

| Path              | Covers                                                                                         |
| ----------------- | ---------------------------------------------------------------------------------------------- |
| `basic.ts`        | Type aliases, union types, function types, interfaces, interface merging, literal unions, generics |
| `basic.js`        | Compiled output of `basic.ts` (an older version of it, see the notes)                          |
| `rect-ts-basics/` | React + TypeScript (Vite) course-goals app: add and delete goals with typed props and handlers |

### Fundamentals (basic.ts)

- **Type aliases:** `UserId = string | number`, an object type `User`, and a function type `CalcFn = (a: number, b: number) => number`
- **Union types:** `userId` holds a string, then a number
- **Function types as parameters:** `calculate(a, b, calcFn)` takes any function matching `CalcFn`, called here with `add`
- **Interfaces:** `Credentials`, `Admin`, `AppUser`
- **Combining interfaces:** `interface AppAdmin extends Admin, AppUser {}` gets the fields of both
- **Literal unions as enums:** `RoleEnum = "admin" | "user" | "editor"`, so assigning any other string is a compile error
- **Generics:** `DataStorage<T>` with a typed `storage` array and `append(data: T)`, used as `DataStorage<User>`

### React + TypeScript (rect-ts-basics/)

A course-goals list: a header with an image, a form to add a goal, and a list where each goal can be deleted.

```text
src/
├── App.tsx                    # useState<Goal[]>, addGoalHandler, deleteGoalHandler
├── components/
│   ├── Header.tsx             # image prop (object type) + children: ReactNode
│   ├── AddNewGoal.tsx         # form with useRef<HTMLInputElement>, typed submit event
│   ├── CourseGoalList.tsx     # maps goals to CourseGoal, passes the delete handler down
│   └── CourseGoal.tsx         # one goal: title, children, delete button
└── types/goal.ts              # Goal interface and GoalDeleteHandler type
```

The TypeScript patterns it practises:

- Props typed with an `interface` per component, destructured in the signature
- `children` typed as `ReactNode` (with the `PropsWithChildren<...>` alternative left commented out in `CourseGoal.tsx`)
- `useState<Goal[]>([])` so the empty initial array still has a type
- `useRef<HTMLInputElement>(null)` for uncontrolled inputs, read with `ref.current!.value`
- Callback props typed as function types, e.g. `onAdd: (title: string, description: string) => void`
- Shared types in `types/goal.ts`, imported with `import { type Goal }` so they're erased at build time
- State lifted into `App`, with child components calling handlers to change it

## Running

The TypeScript compiler is installed at the repo root.

```bash
# From the repo root
npm install
npx tsc typescript/basic.ts      # writes typescript/basic.js next to it
node typescript/basic.js         # prints 12

# React app
cd typescript/rect-ts-basics
npm install
npm run dev                      # Vite dev server
npm run build                    # tsc -b, then vite build
npm run lint
```

## Other notes

- `basic.js` is out of date. It stops at `console.log(output)`, so `cred`, `adminUser`, `role` and `userObj` were added to `basic.ts` after the last compile. Re-run `npx tsc typescript/basic.ts` to refresh it. The type aliases and interfaces are missing from it on purpose: types are erased, only the values survive.
- In `App.tsx`, new goals get `id: prevGoals.length + 1`. That breaks after a delete: add three goals (ids 1, 2, 3), delete goal 1, add another and it also gets id 3. React then warns about duplicate keys, and deleting either goal 3 removes both, because the filter matches on `id`. `crypto.randomUUID()` (with `id: string`), `Date.now()`, or `Math.max(0, ...ids) + 1` avoid it.
- `CourseGoalList` passes `onDelete={() => onDeleteGoal(goal.id)}`, but `CourseGoal` already calls `onDelete(id)` with its own id. Either side alone is enough; `onDelete={onDeleteGoal}` would do.
- The `!` in `titleEl.current!.value` tells TypeScript the ref is never `null` at that point. True here because the form only submits once it's rendered, but it's an assertion, not a check.
- The form submits empty strings happily. There's no validation on title or description yet.
- `rect-ts-basics/README.md` is still the Vite template README.

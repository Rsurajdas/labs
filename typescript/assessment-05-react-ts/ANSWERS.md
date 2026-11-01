# Assessment 05 — Written Answers

## Question 6 — Predict the render

(a) `<Summary total={0} checkedIn={0} />`

- Rendered: h3: Today, p: 0, p: All present
- Why: When no label is provided, "Today" renders by default. Since `total` is `0`, the `&&` operator returns `0` for a falsy condition. "All Present" renders because `checkedIn === total`.

(b) `<Summary total={4} checkedIn={2} label="Morning" />`

- Rendered: h3: Morning, p: 2/3 checked in, p: null
- Why: The label displays "Morning". Since `total` is truthy, "2/3 checked in" renders. Since `checkedIn !== total`, the condition is `false`, so `null` renders.

(c) `<Summary total={3} checkedIn={3} label="" />`

- Rendered: h3: "", p: 3/3 checked in, p: All present
- Why: The label renders "". Since `total` is truthy, "3/3 checked in" renders. Since `checkedIn === total`, so All present renders.

## Question 7 — SearchBox bugs

1.
2.

(Put the fixed code in src/components/SearchBox.tsx.)

## Question 12 — Explain the design

(a)

(b)

(c)

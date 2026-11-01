// Question 6 — GIVEN CODE. Do not edit. Predict the output in ANSWERS.md.

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

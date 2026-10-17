// Assessment #01 Q12
import { type SubmitEvent } from "react";

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
  return (
    <form onSubmit={submitHandler}>
      <div>
        <label htmlFor="title">Title</label>
        <input type="text" id="title" name="title" />
      </div>
      <div>
        <label htmlFor="description">Description</label>
        <input type="text" id="description" name="description" />
      </div>
      <div>
        <button type="submit">Add Goal</button>
      </div>
    </form>
  );
}

import { type SubmitEvent } from "react";

export default function AddNewGoal() {
  function submitHandler(event: SubmitEvent<HTMLFormElement>) {
    event.preventDefault();
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

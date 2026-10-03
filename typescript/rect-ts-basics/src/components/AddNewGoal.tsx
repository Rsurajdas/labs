import { useRef, type SubmitEvent } from "react";

interface AddNewGoalProps {
  onAdd: (title: string, description: string) => void;
}

export default function AddNewGoal({ onAdd }: AddNewGoalProps) {
  const titleEl = useRef<HTMLInputElement>(null);
  const descriptionEl = useRef<HTMLInputElement>(null);
  function submitHandler(event: SubmitEvent<HTMLFormElement>) {
    event.preventDefault();
    const title = titleEl.current!.value;
    const description = descriptionEl.current!.value;
    onAdd(title, description);
    event.currentTarget.reset();
  }
  return (
    <form onSubmit={submitHandler}>
      <div>
        <label htmlFor="title">Title</label>
        <input type="text" id="title" name="title" ref={titleEl} />
      </div>
      <div>
        <label htmlFor="description">Description</label>
        <input
          type="text"
          id="description"
          name="description"
          ref={descriptionEl}
        />
      </div>
      <div>
        <button type="submit">Add Goal</button>
      </div>
    </form>
  );
}

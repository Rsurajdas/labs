// Question 7 — BUGGY CODE. Find every bug, list them in ANSWERS.md, then fix this file.
import { useState } from "react";

type SearchBoxProps = {
  onSearch: (term: string) => void;
};

export function SearchBox(onSearch: SearchBoxProps) {
  const [term, setTerm] = useState();

  function handleChange(event: React.FormEvent<HTMLInputElement>) {
    setTerm(event.target.value);
  }

  function handleSubmit(event: React.ChangeEvent<HTMLFormElement>) {
    onSearch(term.trim());
  }

  return (
    <form onSubmit={handleSubmit}>
      <input value={term} onChange={handleChange} placeholder="Search attendees" />
      <button>Search</button>
    </form>
  );
}

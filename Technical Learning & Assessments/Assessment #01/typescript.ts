// Q2
interface User {
  name: string;
}

interface User {
  age: number;
}

const userObj: User = { name: "sk", age: 32 };
/* 
2.1: The two declarations merge into one interface, so a User must have both name: string and age: number.
2.2: Type aliases cannot be re-declared. The second type User produces a “Duplicate identifier” compile error. Aliases never merge.
2.3: Merging is useful when you need to add properties to an interface declared somewhere you can’t edit. For example, you can add fields to a type that comes from a library, or to a global interface like Window, without touching the original declaration. 
*/

// Q6
type Priority = "low" | "medium" | "high";
interface Goal {
  id: number;
  title: string;
  priority: Priority;
}
const goals: Array<Goal> = [
  {
    id: 1,
    title: "Finish reading 'Clean Code'",
    priority: "medium",
  },
  {
    id: 2,
    title: "Launch MVP of the SaaS app",
    priority: "high",
  },
  {
    id: 3,
    title: "Go to the gym 4 times this week",
    priority: "high",
  },
  {
    id: 4,
    title: "Organize the desk workspace",
    priority: "low",
  },
  {
    id: 5,
    title: "Prepare notes for Monday's team presentation",
    priority: "medium",
  },
];
function getGoalsByPriority(
  goals: Array<Goal>,
  priority: Priority,
): Array<Goal> {
  return goals.filter((goal) => goal.priority === priority);
}
function lastOrDefault<T>(arr: Array<T>, fallback: T) {
  if (!arr.length) return fallback;
  return arr[arr.length - 1];
}

getGoalsByPriority(goals, "high");
lastOrDefault<Goal>(goals, { id: 1, title: "Job in Dubai", priority: "high" });
lastOrDefault([10, 20, 30], 0); // 30
lastOrDefault<string>([], "none"); // "none"
// Rejected by TypeScript:
getGoalsByPriority(goals, "urgent");
// Error: '"urgent"' is not assignable to type 'Priority'.
// Priority only allows the literals "low" | "medium" | "high".

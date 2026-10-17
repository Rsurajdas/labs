// Q2
interface User {
  name: string;
}

interface User {
  age: number;
}

const userObj: User = { name: "sk", age: 32 };
// 2.1 User type will have both name and age properties in a object structure.
// 2.2 TypeScript will show an error `Dublicate indentifier 'User'`. User type strcture will consisder only first intialization in this case 'name'.
// 2.3

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
  return arr.pop();
}

getGoalsByPriority(goals, "high");
lastOrDefault<Goal>(goals, { id: 1, title: "Job in Dubai", priority: "high" });

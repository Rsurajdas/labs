import CourseGoal from "./CourseGoal";
import { type Goal, type GoalDeleteHandler } from "../types/goal";

interface CourseGoalListProps {
  goals: Array<Goal>;
  onDeleteGoal: GoalDeleteHandler;
}

export default function CourseGoalList({
  goals,
  onDeleteGoal,
}: CourseGoalListProps) {
  return (
    <ul>
      {goals.map((goal) => (
        <li key={goal.id}>
          <CourseGoal
            id={goal.id}
            title={goal.title}
            onDelete={() => onDeleteGoal(goal.id)}
          >
            <p>{goal.description}</p>
          </CourseGoal>
        </li>
      ))}
    </ul>
  );
}

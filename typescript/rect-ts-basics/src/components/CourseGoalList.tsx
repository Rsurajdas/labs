import CourseGoal from "./CourseGoal";
import { type Goal, type GoalDeleteHandler } from "../types/goal";
import InfoBox from "./InfoBox";
import type { ReactNode } from "react";

interface CourseGoalListProps {
  goals: Array<Goal>;
  onDeleteGoal: GoalDeleteHandler;
}

export default function CourseGoalList({
  goals,
  onDeleteGoal,
}: CourseGoalListProps) {
  if (!goals.length) {
    return <InfoBox mode="hint">Start adding the goals!</InfoBox>;
  }
  let warningBox: ReactNode;
  if (goals.length >= 10) {
    warningBox = (
      <InfoBox mode="warning">You have so many goals in the pipeline!</InfoBox>
    );
  }
  return (
    <>
      {warningBox}
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
    </>
  );
}

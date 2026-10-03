import CourseGoal from "./components/CourseGoal";
import Header from "./components/Header";
import goalImage from "./assets/goals.jpg";
import { useState } from "react";

interface Goal {
  id: number;
  title: string;
  description: string;
}

function App() {
  const [goals, setGoals] = useState<Goal[]>([]);
  function addGoalHandler() {
    setGoals((prevGoals) => [
      ...prevGoals,
      {
        id: prevGoals.length + 1,
        title: "New Goal",
        description: "This is a new goal.",
      },
    ]);
  }
  return (
    <main>
      <Header image={{ src: goalImage, alt: "Course Goals" }}>
        <h1>Welcome to the Course</h1>
      </Header>
      <button onClick={addGoalHandler}>Add Goal</button>
      <ul>
        {goals.map((goal) => (
          <li key={goal.id}>
            <CourseGoal title={goal.title}>
              <p>{goal.description}</p>
            </CourseGoal>
          </li>
        ))}
      </ul>
    </main>
  );
}

export default App;

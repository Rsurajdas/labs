import Header from "./components/Header";
import goalImage from "./assets/goals.jpg";
import { useState } from "react";
import CourseGoalList from "./components/CourseGoalList";
import { type Goal } from "./types/goal";
import NewGoal from "./components/NewGoal";

function App() {
  const [goals, setGoals] = useState<Goal[]>([]);
  function addGoalHandler(title: string, description: string) {
    setGoals((prevGoals) => [
      ...prevGoals,
      {
        id: prevGoals.length + 1,
        title: title,
        description: description,
      },
    ]);
  }
  function deleteGoalHandler(id: number) {
    setGoals((prevGoals) => prevGoals.filter((goal) => goal.id !== id));
  }

  return (
    <main>
      <Header image={{ src: goalImage, alt: "Course Goals" }}>
        <h1>Welcome to the Course</h1>
      </Header>
      <NewGoal onAddGoal={addGoalHandler} />
      <CourseGoalList goals={goals} onDeleteGoal={deleteGoalHandler} />
    </main>
  );
}

export default App;

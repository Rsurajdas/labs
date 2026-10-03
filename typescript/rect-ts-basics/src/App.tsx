import Header from "./components/Header";
import goalImage from "./assets/goals.jpg";
import { useState } from "react";
import CourseGoalList from "./components/CourseGoalList";
import { type Goal } from "./types/goal";
import AddNewGoal from "./components/AddNewGoal";

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
  function deleteGoalHandler(id: number) {
    setGoals((prevGoals) => prevGoals.filter((goal) => goal.id !== id));
  }

  return (
    <main>
      <Header image={{ src: goalImage, alt: "Course Goals" }}>
        <h1>Welcome to the Course</h1>
      </Header>
      <AddNewGoal />
      <CourseGoalList goals={goals} onDeleteGoal={deleteGoalHandler} />
    </main>
  );
}

export default App;

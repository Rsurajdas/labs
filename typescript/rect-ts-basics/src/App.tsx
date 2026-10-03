import CourseGoal from "./components/CourseGoal";
import Header from "./components/Header";
import goalImage from "./assets/goals.jpg";

function App() {
  return (
    <main>
      <Header image={{ src: goalImage, alt: "Course Goals" }}>
        <h1>Welcome to the Course</h1>
      </Header>
      <CourseGoal title="Learn React + TypeScript">
        <p>Master the fundamentals of React development.</p>
      </CourseGoal>
    </main>
  );
}

export default App;

import Button from "./components/Button";
import Inputs from "./components/Inputs";

function App() {
  return (
    <main>
      <Inputs label="Full Name" id="full-name" type="text" />
      <Inputs label="email" id="email" type="email" />

      <Button text="Submit" tag="button" />
    </main>
  );
}

export default App;

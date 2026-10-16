import Button from "./components/Button";
import Inputs from "./components/Inputs";
import PolymorphicComponent from "./components/PolymorphicComponent";

function App() {
  return (
    <main>
      <PolymorphicComponent el="div">
        <Inputs label="Full Name" id="full-name" type="text" />
        <Inputs label="email" id="email" type="email" />

        <Button text="Submit" tag="button" />
      </PolymorphicComponent>
      <PolymorphicComponent el="input" />
    </main>
  );
}

export default App;

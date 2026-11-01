import { useRef } from "react";
import Button from "./components/Button";
import Inputs from "./components/Inputs";
import PolymorphicComponent from "./components/PolymorphicComponent";

function App() {
  const nameRef = useRef<HTMLInputElement>(null);
  const emailRef = useRef<HTMLInputElement>(null);
  return (
    <main>
      <PolymorphicComponent el="div">
        <Inputs label="Full Name" id="full-name" type="text" ref={nameRef} />
        <Inputs label="email" id="email" type="email" ref={emailRef} />

        <Button text="Submit" tag="button" />
      </PolymorphicComponent>
    </main>
  );
}

export default App;

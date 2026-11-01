import { useRef } from "react";
import Button from "./components/Button";
import Inputs from "./components/Inputs";
import Form from "./components/Form";

function App() {
  const nameRef = useRef<HTMLInputElement>(null);
  const emailRef = useRef<HTMLInputElement>(null);

  const handleSave = (data: unknown) => {
    const extractedData = data as { "full-name": string; email: string };
    console.log(extractedData);
  };
  return (
    <main>
      <Form onSave={handleSave}>
        <Inputs label="Full Name" id="full-name" type="text" ref={nameRef} />
        <Inputs label="email" id="email" type="email" ref={emailRef} />

        <Button text="Submit" tag="button" />
      </Form>
    </main>
  );
}

export default App;

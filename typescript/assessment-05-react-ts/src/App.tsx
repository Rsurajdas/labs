// Question 11 — see ASSESSMENT.md for the full requirements.
import { useState, useRef } from "react";
import type { Attendee, FormHandleRef, AttendeeFormValues } from "./types";
import { RegistrationForm } from "./components/RegistrationForm";
import { Container } from "./components/Container";
import { Card } from "./components/Card";
import { Button } from "./components/Button";
import { AttendeeList } from "./components/AttendeeList";

export default function App() {
  const [attendees, setAttendees] = useState<Attendee[]>([]);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const formRef = useRef<FormHandleRef>(null);

  function handleSave(values: AttendeeFormValues) {
    if (attendees.some((attendee) => attendee.email === values.email)) {
      setErrorMessage("Email already registered");
      return;
    }
    setAttendees((prev) => [
      ...prev,
      { ...values, checkedIn: false, id: prev.length + 1 },
    ]);
    setErrorMessage(null);
    formRef.current?.clear();
  }

  function handleToggleCheckIn(id: number) {
    setAttendees((prev) =>
      prev.map((attendee) =>
        attendee.id === id
          ? { ...attendee, checkedIn: !attendee.checkedIn }
          : attendee,
      ),
    );
  }

  function handleRemove(id: number) {
    setAttendees((prev) => prev.filter((attendee) => attendee.id !== id));
  }

  return (
    <>
      <Container as="main">
        <Card title="Registration">
          <RegistrationForm ref={formRef} onSave={handleSave}>
            <Button type="submit">Add attendee</Button>
          </RegistrationForm>
          {errorMessage ? <p role="alert">{errorMessage}</p> : null}
        </Card>
        <Card
          title="Attendees"
          footer={`"${attendees.filter((a) => a.checkedIn).length} of ${attendees.length} checked in"`}
        >
          <AttendeeList
            attendees={attendees}
            onToggleCheckIn={handleToggleCheckIn}
            onRemove={handleRemove}
          />
        </Card>
      </Container>
    </>
  );
}

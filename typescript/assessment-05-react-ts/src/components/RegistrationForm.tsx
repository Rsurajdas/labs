// Question 9 — see ASSESSMENT.md for the full requirements.
import {
  type ComponentPropsWithoutRef,
  forwardRef,
  type SubmitEvent,
  useRef,
  useImperativeHandle,
} from "react";
import {
  type AttendeeFormValues,
  type FormHandleRef,
  type TicketType,
} from "../types";
import { TextField } from "./TextField";

type RegistrationFormProps = ComponentPropsWithoutRef<"form"> & {
  onSave: (value: AttendeeFormValues) => void;
};

export const RegistrationForm = forwardRef<
  FormHandleRef,
  RegistrationFormProps
>(function ({ onSave, children, ...props }, ref) {
  const formRef = useRef<HTMLFormElement>(null);

  useImperativeHandle(ref, () => ({
    clear: () => {
      formRef.current?.reset();
    },
  }));

  function handleSubmit(e: SubmitEvent<HTMLFormElement>) {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(e.currentTarget));
    const values: AttendeeFormValues = {
      name: String(data.name ?? "").trim(),
      email: String(data.email ?? "").trim(),
      ticket: data.ticket as TicketType,
    };
    if (values.name && values.email) onSave(values);
  }

  return (
    <form {...props} ref={formRef} onSubmit={handleSubmit}>
      <TextField label="Name" name="name" id="name" />
      <TextField label="Email" name="email" id="email" type="email" />
      <select name="ticket">
        <option value="standard">standard</option>
        <option value="student">student</option>
        <option value="vip">vip</option>
      </select>
      {children}
    </form>
  );
});

// Question 8 — see ASSESSMENT.md for the full requirements.
import { type ComponentPropsWithoutRef, forwardRef } from "react";

type TextFieldProps = ComponentPropsWithoutRef<"input"> & {
  label: string;
  id: string;
  error?: string;
};

const TextField = forwardRef<HTMLInputElement, TextFieldProps>(function (
  { label, id, error, ...props },
  ref,
) {
  return (
    <div className="field">
      <label htmlFor={id}>{label}</label>
      <input id={id} {...props} ref={ref} />
      {error ? (
        <p role="alert" aria-invalid={true}>
          {error}
        </p>
      ) : null}
    </div>
  );
});

export default TextField;

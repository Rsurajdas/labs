// Question 8 — see ASSESSMENT.md for the full requirements.
import { type ComponentPropsWithoutRef, forwardRef } from "react";

type TextFieldProps = ComponentPropsWithoutRef<"input"> & {
  label: string;
  id: string;
  error?: string;
};

export const TextField = forwardRef<HTMLInputElement, TextFieldProps>(function (
  { label, id, error, ...props },
  ref,
) {
  return (
    <div className="field">
      <label htmlFor={id}>{label}</label>
      <input
        id={id}
        ref={ref}
        aria-invalid={error ? true : undefined}
        {...props}
      />
      {error ? <p role="alert">{error}</p> : null}
    </div>
  );
});

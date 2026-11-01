import { forwardRef, type ComponentPropsWithoutRef } from "react";

interface InputProps extends ComponentPropsWithoutRef<"input"> {
  label: string;
  id: string;
}

// type method
// type InputProps = {
//   label: string;
//   id: string;
// } & ComponentPropsWithoutRef<"input">;

const Inputs = forwardRef<HTMLInputElement, InputProps>(function (
  { label, id, ...props },
  ref,
) {
  return (
    <div>
      <label htmlFor={id}>{label}</label>
      <input name={id} {...props} ref={ref} />
    </div>
  );
});

export default Inputs;

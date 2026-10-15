import type { ComponentPropsWithoutRef } from "react";

interface InputsProps extends ComponentPropsWithoutRef<"input"> {
  label: string;
  id: string;
}

// type method
// type InputsProps = {
//   label: string;
//   id: string;
// } & ComponentPropsWithoutRef<"input">;

export default function Inputs({ label, id, ...props }: InputsProps) {
  return (
    <div>
      <label htmlFor={id}>{label}</label>
      <input name={id} {...props} />
    </div>
  );
}

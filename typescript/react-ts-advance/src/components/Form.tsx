import {
  type ComponentPropsWithoutRef,
  type ReactNode,
  type SubmitEvent,
} from "react";

interface FormProps extends ComponentPropsWithoutRef<"form"> {
  onSave: (data: unknown) => void;
  children: ReactNode;
}

export default function Form({ onSave, children, ...props }: FormProps) {
  const handleSubmit = (e: SubmitEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const data = Object.fromEntries(formData.entries());
    onSave(data);
  };
  return (
    <form onSubmit={handleSubmit} {...props}>
      {children}
    </form>
  );
}

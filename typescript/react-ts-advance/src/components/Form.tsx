import { type ComponentPropsWithoutRef, type ReactNode } from "react";

interface FormProps extends ComponentPropsWithoutRef<"form"> {
  children: ReactNode;
}

export default function Form({ children, ...props }: FormProps) {
  return <form {...props}>{children}</form>;
}

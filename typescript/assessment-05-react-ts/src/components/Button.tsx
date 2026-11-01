// Question 3 — see ASSESSMENT.md for the full requirements.
import { type ComponentPropsWithoutRef } from "react";

type ButtonProps = {
  variant?: "primary" | "danger";
} & ComponentPropsWithoutRef<"button">;

export function Button({ variant = "primary", ...props }: ButtonProps) {
  return (
    <button
      type={props.type ?? "button"}
      className={`btn ${variant === "primary" ? "btn-primary" : "btn-danger"} ${props.className ?? ""}`}
      {...props}
    >
      {props.children}
    </button>
  );
}

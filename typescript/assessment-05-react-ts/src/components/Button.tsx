// Question 3 — see ASSESSMENT.md for the full requirements.
import { type ComponentPropsWithoutRef } from "react";

type ButtonProps = {
  variant?: "primary" | "danger";
} & ComponentPropsWithoutRef<"button">;

export function Button({
  variant = "primary",
  type = "button",
  className,
  ...props
}: ButtonProps) {
  const classes = className
    ? `btn btn-${variant} ${className}`
    : `btn btn-${variant}`;
  return <button type={type} className={classes} {...props} />;
}

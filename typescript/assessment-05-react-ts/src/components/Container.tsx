// Question 4 — see ASSESSMENT.md for the full requirements.
import { type ElementType, type ReactNode } from "react";

type ContainerProps = {
  as?: ElementType;
  className?: string;
  children: ReactNode;
};

export function Container({
  as: Component = "div",
  className,
  children,
}: ContainerProps) {
  return <Component className={className}>{children}</Component>;
}

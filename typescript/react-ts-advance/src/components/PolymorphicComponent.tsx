import type { ElementType, ReactNode } from "react";

interface PolymorphicProps {
  el: ElementType;
  children?: ReactNode;
}

export default function PolymorphicComponent({
  el: Component, // alias name
  children,
}: PolymorphicProps) {
  return <Component>{children}</Component>;
}

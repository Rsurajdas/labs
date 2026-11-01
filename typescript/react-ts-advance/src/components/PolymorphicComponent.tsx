import type { ElementType, ReactNode, ComponentPropsWithoutRef } from "react";

type PolymorphicProps<T extends ElementType> = {
  el?: T;
  children: ReactNode;
} & ComponentPropsWithoutRef<T>;

export default function PolymorphicComponent<T extends ElementType>({
  el,
  children,
  ...props
}: PolymorphicProps<T>) {
  const Component = el || "div";
  return <Component {...props}>{children}</Component>;
}

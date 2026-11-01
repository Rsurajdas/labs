// Question 2 — see ASSESSMENT.md for the full requirements.

import type { PropsWithChildren } from "react";

type CardProps = {
  title: string;
  footer?: string;
};

type CardComponentProps = PropsWithChildren<CardProps>;

export function Card({ title, footer, children }: CardComponentProps) {
  return (
    <section className="card">
      <h2>{title}</h2>
      {children}
      {footer ? <footer>{footer}</footer> : null}
    </section>
  );
}

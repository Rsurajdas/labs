import { type ReactNode } from "react";

interface InfoBoxHintProps {
  mode: "hint";
  children: ReactNode;
}
interface InfoBoxWarningProps {
  mode: "warning";
  severity: "low" | "medium" | "high";
  children: ReactNode;
}

type InfoBoxProps = InfoBoxHintProps | InfoBoxWarningProps;

export default function InfoBox(props: InfoBoxProps) {
  if (props.mode === "hint") {
    return (
      <aside className="infobox infobox-hint">
        <p>{props.children}</p>
      </aside>
    );
  }
  return (
    <aside className={`infobox infobox-warning warning--${props.severity}`}>
      <h2>Warning</h2>
      <p>{props.children}</p>
    </aside>
  );
}

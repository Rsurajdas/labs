import { type ComponentPropsWithoutRef } from "react";

// Discriminated union
interface ButtonProps extends ComponentPropsWithoutRef<"button"> {
  tag: "button";
  text: string;
}

interface AnchorProps extends ComponentPropsWithoutRef<"a"> {
  tag: "anchor";
  text: string;
}

export default function Button(props: ButtonProps | AnchorProps) {
  if (props.tag === "anchor") {
    return (
      <a className="button" {...props}>
        {props.text}
      </a>
    );
  }
  return (
    <button className="button" {...props}>
      {props.text}
    </button>
  );
}

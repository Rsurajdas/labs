import PolymorphicComponent from "./UI/PolymorphicComponent";

import { type Timer as TimerProps } from "../store/timers-context";

export default function Timer({ name, duration }: TimerProps) {
  return (
    <>
      <PolymorphicComponent el="article">
        <h2>{name}</h2>
        <p>{duration}</p>
      </PolymorphicComponent>
    </>
  );
}

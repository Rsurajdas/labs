import PolymorphicComponent from "./UI/PolymorphicComponent";

import { type Timer as TimerProps } from "../store/timers-context";
import { useEffect, useState } from "react";

export default function Timer({ name, duration }: TimerProps) {
  const [remainingTime, setRemainingTime] = useState(duration * 1000);

  useEffect(() => {
    const timer = setInterval(() => {
      setRemainingTime((prevState) => {
        if (prevState <= 0) {
          clearInterval(timer);
          return prevState;
        }
        return prevState - 50;
      });
    }, 50);

    return () => clearInterval(timer);
  }, []);

  const formatedRemainingTime = (remainingTime / 1000).toFixed(2);
  return (
    <>
      <PolymorphicComponent el="article">
        <h2>{name}</h2>
        <div>
          <progress max={duration * 1000} value={remainingTime} />
        </div>
        <p>{formatedRemainingTime}</p>
      </PolymorphicComponent>
    </>
  );
}

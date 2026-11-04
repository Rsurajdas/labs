import PolymorphicComponent from "./UI/PolymorphicComponent";

import {
  useTimersContext,
  type Timer as TimerProps,
} from "../store/timers-context";
import { useEffect, useRef, useState } from "react";

export default function Timer({ name, duration }: TimerProps) {
  const [remainingTime, setRemainingTime] = useState(duration * 1000);
  const { isRunning } = useTimersContext();
  const timerRef = useRef<number | null>(null);

  useEffect(() => {
    let timer: number;
    if (isRunning) {
      timer = setInterval(() => {
        setRemainingTime((prevState) => {
          if (prevState <= 0) {
            clearInterval(timer);
            return prevState;
          }
          return prevState - 50;
        });
        timerRef.current = timer;
      }, 50);
    }
    if (!isRunning && timerRef.current) {
      clearInterval(timerRef.current);
    }

    return () => clearInterval(timer);
  }, [isRunning]);

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

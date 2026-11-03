import { createContext, useContext, type ReactNode } from "react";

type Timer = {
  name: string;
  duration: number;
};

type TimersState = {
  isRunning: boolean;
  timers: Timer[];
};

type TimersContextValue = TimersState & {
  addTimer: (timer: Timer) => void;
  startTimers: () => void;
  stopTimers: () => void;
};

type TimersContextProviderProps = {
  children: ReactNode;
};

const TimesContext = createContext<TimersContextValue | null>(null);

export function useTimersContext() {
  const timersCtx = useContext(TimesContext);

  if (timersCtx === null) {
    throw new Error("Timers context is null!");
  }

  return timersCtx;
}

export default function TimersContextProvider({
  children,
}: TimersContextProviderProps) {
  const ctx: TimersContextValue = {
    timers: [],
    isRunning: false,
    addTimer(timer) {
      console.log(timer);
    },
    startTimers() {},
    stopTimers() {},
  };

  return <TimesContext.Provider value={ctx}>{children}</TimesContext.Provider>;
}

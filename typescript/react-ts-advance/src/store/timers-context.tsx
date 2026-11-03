import { createContext, type ReactNode } from "react";

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

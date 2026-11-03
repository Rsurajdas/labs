import { createContext, useContext, useReducer, type ReactNode } from "react";

export type Timer = {
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

const initialState: TimersState = {
  isRunning: false,
  timers: [],
};

type StartTimersAction = {
  type: "START_TIMERS";
};

type StopTimersAction = {
  type: "STOP_TIMERS";
};

type AddTimerAction = {
  type: "ADD_TIMER";
  payload: Timer;
};

type Action = StartTimersAction | StopTimersAction | AddTimerAction;

function timersReducer(state: TimersState, action: Action): TimersState {
  switch (action.type) {
    case "ADD_TIMER":
      return {
        ...state,
        timers: [
          ...state.timers,
          {
            name: action.payload.name,
            duration: action.payload.duration,
          },
        ],
      };
    case "START_TIMERS":
      return {
        ...state,
        isRunning: true,
      };
    case "STOP_TIMERS":
      return {
        ...state,
        isRunning: false,
      };
    default:
      return state;
  }
}

// eslint-disable-next-line react-refresh/only-export-components
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
  const [timerState, dispatch] = useReducer(timersReducer, initialState);
  const ctx: TimersContextValue = {
    timers: timerState.timers,
    isRunning: timerState.isRunning,
    addTimer(timer) {
      dispatch({ payload: timer, type: "ADD_TIMER" });
    },
    startTimers() {
      dispatch({ type: "START_TIMERS" });
    },
    stopTimers() {
      dispatch({ type: "STOP_TIMERS" });
    },
  };

  return <TimesContext.Provider value={ctx}>{children}</TimesContext.Provider>;
}

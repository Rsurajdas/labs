import { useTimersContext } from "../store/timers-context";
import Timer from "./Timer";

export default function Timers() {
  const timersCtx = useTimersContext();
  return (
    <ul>
      {timersCtx.timers.map((timer, idx) => (
        <li key={idx}>
          <Timer {...timer} />
        </li>
      ))}
    </ul>
  );
}

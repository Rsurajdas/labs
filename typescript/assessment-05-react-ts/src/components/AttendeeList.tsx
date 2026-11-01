// Question 10 — see ASSESSMENT.md for the full requirements.
import { type Attendee } from "../types";
import { Button } from "./Button";
import { TicketDetails } from "./TicketDetails";

type AttendeeListProps = {
  attendees: Attendee[];
  onToggleCheckIn: (id: number) => void;
  onRemove: (id: number) => void;
};

export function AttendeeList({
  attendees,
  onToggleCheckIn,
  onRemove,
}: AttendeeListProps) {
  if (!attendees.length) {
    return <p>No attendees yet</p>;
  }
  return (
    <ul>
      {attendees.map((attendee) => (
        <li key={attendee.id}>
          <TicketDetails ticket="standard" />
          <Button
            variant="primary"
            onClick={() => onToggleCheckIn(attendee.id)}
          >
            Check in
          </Button>
          <Button variant="danger" onClick={() => onRemove(attendee.id)}>
            Remove
          </Button>
        </li>
      ))}
    </ul>
  );
}

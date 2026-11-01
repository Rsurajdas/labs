// Question 5 — see ASSESSMENT.md for the full requirements.

type TicketDetailsBase = {
  ticket: "standard";
};

type TicketDetailsStudent = {
  ticket: "student";
  studentId: string;
};

type TicketDetailsVip = {
  ticket: "vip";
  seat: number;
  lounge: boolean;
};

type TicketDetailsProps =
  | TicketDetailsBase
  | TicketDetailsStudent
  | TicketDetailsVip;

export function TicketDetails(props: TicketDetailsProps) {
  const { ticket } = props;
  return (
    <span>
      {ticket === "standard"
        ? "Standard pass"
        : ticket === "student"
          ? `Student pass — ID: ${props.studentId}`
          : `VIP — Seat: ${props.seat}${props.lounge ? ", (Lounge access)" : ""}`}
    </span>
  );
}

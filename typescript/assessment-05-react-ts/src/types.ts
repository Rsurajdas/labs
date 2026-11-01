// Question 1 — see ASSESSMENT.md for the full requirements.
type TicketType = "standard" | "student" | "vip";

type AttendeeFormValues = {
  name: string;
  email: string;
  ticket: TicketType;
};

type Attendee = AttendeeFormValues & {
  id: number;
  checkedIn: boolean;
};

interface FormHandleRef {
  clear: () => void;
}

export type { TicketType, AttendeeFormValues, Attendee, FormHandleRef };

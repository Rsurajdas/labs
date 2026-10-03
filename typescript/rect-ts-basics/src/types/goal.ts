export interface Goal {
  id: number;
  title: string;
  description: string;
}

export type GoalDeleteHandler = (id: number) => void;

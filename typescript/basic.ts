type UserId = string | number;
type CalcFn = (a: number, b: number) => number;

let userId: UserId = "abc1"; // union type
userId = 123;

let user: {
  id: UserId;
  name: string;
  age: number;
  isValid: boolean;
};

user = {
  id: "abc",
  name: "john doe",
  age: 26,
  isValid: true,
};

let hobbies: Array<string> = [
  "cooking",
  "music",
  "anime",
  "coding",
  "learning",
];

function add(a: number, b: number): number {
  return a + b;
}

function calculate(a: number, b: number, calcFn: CalcFn): number {
  return calcFn(a, b);
}

let output = calculate(5, 7, add);
console.log(output);

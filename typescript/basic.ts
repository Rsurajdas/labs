type UserId = string | number;
type CalcFn = (a: number, b: number) => number;
type User = {
  id: UserId;
  name: string;
  age: number;
  isValid: boolean;
};
interface Credentials {
  email: string;
  password: string;
}
interface Admin {
  permissions: Array<string>;
}
interface AppUser {
  name: string;
}
interface AppAdmin extends Admin, AppUser {} // Merge types
type RoleEnum = "admin" | "user" | "editor";
type DataStorage<T> = {
  storage: Array<T>;
  append: (data: T) => void;
};

// ---------------------------------------------

let userId: UserId = "abc1"; // union type
userId = 123;

let user: User;

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

let cred: Credentials = {
  email: "suraj@gmail.com",
  password: "123456",
};

let adminUser: AppAdmin = {
  name: "suraj",
  permissions: ["all"],
};

let role: RoleEnum;
role = "admin";
role = "editor";
role = "user";

const userObj: DataStorage<User> = {
  storage: [{ id: 1, name: "suraj", age: 32, isValid: true }],
  append(data) {
    this.storage.push(data);
  },
};

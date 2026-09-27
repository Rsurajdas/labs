let userId: string | number = "abc1"; // union type
userId = 123;

let user: {
  id: string | number;
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

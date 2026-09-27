"use strict";
let userId = "abc1"; // union type
userId = 123;
let user;
user = {
    id: "abc",
    name: "john doe",
    age: 26,
    isValid: true,
};
let hobbies = [
    "cooking",
    "music",
    "anime",
    "coding",
    "learning",
];
function add(a, b) {
    return a + b;
}
function calculate(a, b, calcFn) {
    return calcFn(a, b);
}
let output = calculate(5, 7, add);
console.log(output);

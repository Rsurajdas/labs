//  Q1
/**
 * 1.1) Using 'type' keyword we can able to create any custom type, like union type, custom string type etc. 'interface' is used specially to create obj type.
 * 1.2) 'type' can not be re-declare in the same file, it will throe compile error. 'interface' can be re-declare, it will merge both types into one.
 * 2) i will use 'type' when i want to create custom types like union, i will use 'interface' when i want to create obj type, because it more compatible with it.
 */
// Q2
function formatBookTitle(title: string, year: number): string {
  return `${title} (${year})`;
}
// Q3
let username: string = "suraj"; // Line 1
let age: number = "30"; // Line 2
let isActive: boolean = true; // Line 3
isActive = "false"; // Line 4
let scores: number[] = [90, 85, 77]; // Line 5
scores.push("100"); // Line 6
let tags: string[] = []; // Line 7
username = 42; // Line 8
/**
 * Line 2 -> type 'string' can not be assign to type 'number'
 * Line 4 -> type 'string' can not be assign to type 'boolean'
 * Line 6 -> type 'string' can not be assign to type 'number'
 * Line 8 -> type 'number' can not be assign to type 'string'
 */
// Q4
type RecordId = number | string;
function printRecordId(id: RecordId): string {
  return `Record: ${id}`;
}
// Q5
function shout(value: string | number) {
  return value.toUpperCase();
}
/**
 * toUpperCase() is a vaild method available on type 'string', but not type 'number'. Union type means 'value' will either be number or string.
 */
// Q6
interface Employee {
  id: number;
  name: string;
}
interface Employee {
  department: string;
}
const emp: Employee = {
  id: 1,
  name: "Karan",
};
/**
 * 1. It will not compile, because 'department' is missing from 'emp' object
 * 2. Employee {id: number; name: string; department: string}
 * 3. It will throw compile error, as 'type' can not be re-declare.
 */
// Q7
type GoalStatus = "pending" | "in-progress" | "completed";
function getStatusLabel(goalStatus: GoalStatus): string {
  const status = {
    pending: "Not Started",
    "in-progress": "Working On It",
    completed: "Done",
  };
  return status[goalStatus];
}
// Q8
type Role = "admin" | "editor" | "viewer";
interface User {
  id: number;
  name: string;
  role: Role;
}
const users: User[] = [
  { id: 1, name: "Jatin", role: "admin" },
  { id: 2, name: "Khushi", role: "Editor" },
  { id: "3", name: "Karan", role: "viewer" },
];
function setRole(user: User, newRole: Role): User {
  return { ...user, role: newRole };
}
setRole(users[0], "owner");
/**
 * 1. "Editor" is not assignable, Literal types are case-sensitive
 * 2. "string" is not assignable to type "number"
 * 3. "owner" is not assignable to type "Role", only "admin" | "editor" | "viewer" are allowed.
 */
// Q9 -> Interfaces
interface Author {
  id: number;
  name: string;
}
interface Book {
  id: number;
  title: string;
  publishedYear: number;
  rating: number;
  author: Author;
}
const books: Array<Book> = [
  {
    id: 1,
    title: "My success story!",
    publishedYear: 2028,
    rating: 5,
    author: { id: 1, name: "Suraj Kumar" },
  },
  {
    id: 2,
    title: "Suraj's personal biography!",
    publishedYear: 2030,
    rating: 5,
    author: { id: 2, name: "Manisha Das" },
  },
];
function getBookTitles(books: Array<Book>): Array<string> {
  return books.map((book) => book.title);
}
// Q10 -> Generics
function makePair<K, V>(key: K, value: V): [K, V] {
  return [key, value];
}
makePair<string, number>("age", 30); // Call 1
makePair<string, number>(30, "age"); // Call 2
makePair<boolean, string>(true, "active"); // Call 3
makePair<number, number[]>(1, [2, 3]); // Call 4
makePair<string, string>("city", null); // Call 5
/**
 * Call 2 -> type 'number' is not assinable to 'string'
 * Call 5 -> type 'null' is not assinable to 'string'
 */
// Q11 -> Generics and Interfaces
interface ApiResponse<T> {
  success: boolean;
  message: string;
  data: T;
}
const book: Book = {
  id: 1,
  title: "My success story!",
  publishedYear: 2028,
  rating: 5,
  author: { id: 1, name: "Suraj Kumar" },
};
function wrapResponse<T>(data: T, message: string): ApiResponse<T> {
  return {
    success: true,
    message,
    data,
  };
}
wrapResponse<Book>(book, "Finished successfully!");
wrapResponse<Book[]>(books, "Finished successfully!");
// Q12 -> Generics, Interfaces and Typed Functions
interface Paginated<T> {
  items: T[];
  page: number;
  pageSize: number;
  totalItems: number;
  totalPages: number;
}
function paginate<T>(
  items: Array<T>,
  page: number,
  pageSize: number,
): Paginated<T> {
  const start = (page - 1) * pageSize;
  const end = start + pageSize;
  return {
    items: items.slice(start, end),
    page,
    pageSize,
    totalItems: items.length,
    totalPages: Math.ceil(items.length / pageSize),
  };
}

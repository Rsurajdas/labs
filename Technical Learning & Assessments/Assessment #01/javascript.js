// Q5
const students = [
  { name: "Amit", score: 72 },
  { name: "Sara", score: 35 },
  { name: "Leo", score: 88 },
  { name: "Ira", score: 40 },
  { name: "Suraj", score: 88 },
];
function summarizeScores(students) {
  const result = {
    passed: [],
    failed: [],
    topScorer: null,
  };
  if (!students.length) return result;
  let topScore = 0;
  for (let i = 0; i < students.length; i++) {
    const student = students[i];
    if (student.score >= 40) {
      result.passed.push(student.name);
      topScore = Math.max(student.score, topScore);
    } else {
      result.failed.push(student.name);
    }
  }
  result.topScorer = students.find(
    (student) => student.score === topScore,
  ).name;
  return result;
}

summarizeScores(students);

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
  let topScore = students[0].score;
  for (const student of students) {
    if (student.score >= 40) {
      result.passed.push(student.name);
    } else {
      result.failed.push(student.name);
    }
    if (student.score > topScore) {
      topScore = student.score;
      result.topScorer = student.name;
    }
  }
  return result;
}

console.log(summarizeScores(students));

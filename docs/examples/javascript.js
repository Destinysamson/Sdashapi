// SdashAPI — JavaScript Example (fetch)
// =======================================
// Install: No dependencies needed (uses native fetch)
// Works in: Browser, Node.js 18+, Deno

const BASE_URL = 'https://sdashapi.com/api/v1';
const TOKEN = 'sdash_your_token_here'; // Replace with your AccessToken

const headers = { 'AccessToken': TOKEN };

// ----------------------------------------------------------
// 1. Get a single random question
// ----------------------------------------------------------
async function getRandomQuestion() {
  const res = await fetch(`${BASE_URL}/q`, { headers });
  const { data } = await res.json();
  console.log('Random question:', data);
}

// ----------------------------------------------------------
// 2. Get questions by subject, exam type, and year
// ----------------------------------------------------------
async function getFilteredQuestions() {
  const params = new URLSearchParams({
    subject: 'biology',
    type: 'utme',
    year: '2021',
    limit: '5'
  });

  const res = await fetch(`${BASE_URL}/q?${params}`, { headers });
  const { data } = await res.json();

  data.forEach((q, i) => {
    console.log(`\nQ${i + 1}: ${q.question}`);
    Object.entries(q.option).forEach(([key, val]) => {
      const marker = key === q.answer ? '✅' : '  ';
      console.log(`  ${marker} ${key.toUpperCase()}) ${val}`);
    });
    if (q.solution) console.log(`  💡 ${q.solution}`);
  });
}

// ----------------------------------------------------------
// 3. List all subjects
// ----------------------------------------------------------
async function listSubjects() {
  const res = await fetch(`${BASE_URL}/subjects`, { headers });
  const { data } = await res.json();
  console.log('Subjects:', data.map(s => `${s.name} (${s.slug})`));
}

// ----------------------------------------------------------
// 4. List all exam types
// ----------------------------------------------------------
async function listExams() {
  const res = await fetch(`${BASE_URL}/exams`, { headers });
  const { data } = await res.json();
  console.log('Exam types:', data);
}

// ----------------------------------------------------------
// 5. List available years
// ----------------------------------------------------------
async function listYears() {
  const res = await fetch(`${BASE_URL}/years`, { headers });
  const { data } = await res.json();
  console.log('Available years:', data);
}

// ----------------------------------------------------------
// 6. Report a question
// ----------------------------------------------------------
async function reportQuestion(questionId, message) {
  const res = await fetch(`${BASE_URL}/report`, {
    method: 'POST',
    headers: { ...headers, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      question_id: questionId,
      report_type: 'wrong_answer',
      message
    })
  });
  const result = await res.json();
  console.log('Report result:', result.message);
}

// Run examples
(async () => {
  await getRandomQuestion();
  await listSubjects();
  await listYears();
  await getFilteredQuestions();
})();

# SdashAPI — Python Example
# ===========================
# Install: pip install requests

import requests

BASE_URL = "https://sdashapi.com/api/v1"
TOKEN = "sdash_your_token_here"  # Replace with your AccessToken

headers = {"AccessToken": TOKEN}


def get_random_question():
    """Fetch a single random question."""
    r = requests.get(f"{BASE_URL}/q", headers=headers)
    r.raise_for_status()
    data = r.json()["data"]
    print("Question:", data["question"])
    for key, val in data["option"].items():
        marker = "✅" if key == data["answer"] else "  "
        print(f"  {marker} {key.upper()}) {val}")
    if data.get("solution"):
        print("  💡", data["solution"])


def get_filtered_questions(subject, exam_type, year=None, limit=5):
    """Fetch multiple questions with filters."""
    params = {"subject": subject, "type": exam_type, "limit": limit}
    if year:
        params["year"] = year

    r = requests.get(f"{BASE_URL}/q", headers=headers, params=params)
    r.raise_for_status()
    questions = r.json()["data"]

    for i, q in enumerate(questions, 1):
        print(f"\nQ{i}: {q['question']}")
        print(f"  Exam: {q['examtype']} {q['examyear']}")
        for key, val in q["option"].items():
            marker = "✅" if key == q["answer"] else "  "
            print(f"  {marker} {key.upper()}) {val}")


def list_subjects():
    """List all available subjects."""
    r = requests.get(f"{BASE_URL}/subjects", headers=headers)
    r.raise_for_status()
    subjects = r.json()["data"]
    print("\nAvailable subjects:")
    for s in subjects:
        print(f"  {s['name']:30s} slug: {s['slug']}")
    return subjects


def list_exams():
    """List all exam types."""
    r = requests.get(f"{BASE_URL}/exams", headers=headers)
    r.raise_for_status()
    exams = r.json()["data"]
    print("\nExam types:")
    for e in exams:
        print(f"  {e['name']:20s} slug: {e['slug']}")
    return exams


def list_years():
    """List all available years."""
    r = requests.get(f"{BASE_URL}/years", headers=headers)
    r.raise_for_status()
    years = r.json()["data"]
    print(f"\nAvailable years: {years}")
    return years


def report_question(question_id, report_type="wrong_answer", message=""):
    """Report a question issue."""
    payload = {
        "question_id": question_id,
        "report_type": report_type,
        "message": message,
    }
    r = requests.post(f"{BASE_URL}/report", headers=headers, json=payload)
    r.raise_for_status()
    print(r.json()["message"])


if __name__ == "__main__":
    print("=== SdashAPI Python Example ===\n")
    list_subjects()
    list_exams()
    list_years()

    print("\n--- Random question ---")
    get_random_question()

    print("\n--- UTME Biology 2021 (5 questions) ---")
    get_filtered_questions("biology", "utme", year=2021, limit=5)

import os
import json
import time
import requests

from pathlib import Path
from datetime import datetime, timezone

# ==========================================
# STALWART PREP - SDASHAPI BIOLOGY EXTRACTOR
# ==========================================

BASE_URL = "https://sdashapi.com/api/v1/q"

SUBJECT = "biology"
EXAM_TYPE = "utme"

START_YEAR = 2015
END_YEAR = 2026

LIMIT = 50

TOKEN = os.getenv("SDASH_API_TOKEN")

OUTPUT_DIR = Path("data/sdash")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "sdash_biology_2015_2026.json"
REPORT_FILE = OUTPUT_DIR / "sdash_biology_extraction_report.json"

if not TOKEN:
    raise SystemExit(
        "ERROR: SDASH_API_TOKEN secret is missing."
    )

session = requests.Session()

session.headers.update({
    "AccessToken": TOKEN,
    "Accept": "application/json",
    "User-Agent": "StalwartPrep/1.0"
})

all_questions = []
seen_ids = set()
year_report = []


# ==========================================
# SAVE CHECKPOINT
# ==========================================

def save_checkpoint():

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            all_questions,
            file,
            indent=2,
            ensure_ascii=False
        )

    with open(
        REPORT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            year_report,
            file,
            indent=2,
            ensure_ascii=False
        )

    print("\nCHECKPOINT SAVED")
    print("Questions recovered:", len(all_questions))


# ==========================================
# EXTRACTION HEADER
# ==========================================

print("=" * 55)
print("STALWART PREP - SDASHAPI EXTRACTION")
print("SUBJECT: BIOLOGY")
print("EXAM: JAMB / UTME")
print(f"YEAR RANGE: {START_YEAR}-{END_YEAR}")
print("=" * 55)


# ==========================================
# EXTRACT ONE YEAR
# ==========================================

def extract_year(year):

    params = {
        "subject": SUBJECT,
        "type": EXAM_TYPE,
        "year": year,
        "limit": LIMIT
    }

    print(f"\nExtracting Biology {year}...")

    response = session.get(
        BASE_URL,
        params=params,
        timeout=45
    )

    print("REQUEST URL:", response.url)
    print("HTTP STATUS:", response.status_code)

    # --------------------------------------
    # ERROR HANDLING
    # --------------------------------------

    if response.status_code == 401:

        print("SERVER RESPONSE:", response.text[:3000])

        raise RuntimeError(
            "API authentication failed. "
            "Check SDASH_API_TOKEN."
        )

    if response.status_code == 403:

        print("\nSDASHAPI RETURNED HTTP 403")
        print("SERVER RESPONSE:")
        print(response.text[:3000])

        raise RuntimeError(
            "SdashAPI access denied. "
            "Check account restrictions."
        )

    if response.status_code == 429:

        print("SERVER RESPONSE:", response.text[:3000])

        raise RuntimeError(
            "API rate limit or quota reached."
        )

    if response.status_code == 404:

        print(f"No matching questions found for {year}.")
        return []

    response.raise_for_status()

    # --------------------------------------
    # READ JSON
    # --------------------------------------

    try:
        payload = response.json()

    except ValueError:

        print("INVALID JSON RESPONSE:")
        print(response.text[:3000])

        raise RuntimeError(
            f"Invalid JSON returned for {year}."
        )

    if payload.get("status") != 200:

        print("API RESPONSE:", json.dumps(
            payload,
            indent=2
        ))

        raise RuntimeError(
            f"API reported an error for {year}."
        )

    records = payload.get("data", [])

    if isinstance(records, dict):
        records = [records]

    if not isinstance(records, list):

        raise RuntimeError(
            f"Unexpected question format for {year}."
        )

    valid = []

    # --------------------------------------
    # NORMALIZE QUESTIONS
    # --------------------------------------

    for item in records:

        if not isinstance(item, dict):
            continue

        question = item.get("question")
        options = item.get("option")
        answer = item.get("answer")
        question_id = item.get("id")

        if not question_id or not question:
            continue

        if not isinstance(options, dict):
            continue

        if not answer:
            continue

        normalized_options = {
            str(key).upper(): value
            for key, value in options.items()
        }

        normalized_answer = str(answer).strip().upper()

        if normalized_answer not in normalized_options:
            continue

        question_id = str(question_id)

        if question_id in seen_ids:
            continue

        seen_ids.add(question_id)

        normalized = {
            "id": question_id,
            "subject": "Biology",
            "year": str(
                item.get("examyear") or year
            ),
            "exam": item.get("examtype", "UTME"),
            "question": question,
            "section": item.get("section"),
            "options": normalized_options,
            "answer": normalized_answer,
            "solution": item.get("solution"),
            "image": item.get("image"),
            "source": "SdashAPI",
            "verification_status": "pending",
            "extracted_at": datetime.now(
                timezone.utc
            ).isoformat()
        }

        valid.append(normalized)

    return valid


# ==========================================
# MAIN EXTRACTION
# ==========================================

for year in range(START_YEAR, END_YEAR + 1):

    try:

        records = extract_year(year)

        all_questions.extend(records)

        capped = len(records) >= LIMIT

        year_report.append({
            "year": year,
            "questions_recovered": len(records),
            "limit": LIMIT,
            "possible_cap": capped,
            "status": (
                "REVIEW_REQUIRED"
                if capped
                else "FETCH_COMPLETED"
            )
        })

        print(
            f"Biology {year}: "
            f"{len(records)} valid questions"
        )

        if capped:

            print(
                "WARNING: 50-question limit reached. "
                "Completeness is not confirmed."
            )

        # SAVE AFTER EVERY SUCCESSFUL YEAR
        save_checkpoint()

        time.sleep(1)

    except Exception as error:

        print("\nEXTRACTION ERROR")
        print("YEAR:", year)
        print("DETAILS:", str(error))

        year_report.append({
            "year": year,
            "questions_recovered": 0,
            "status": "FAILED",
            "error": str(error)
        })

        # PRESERVE PREVIOUSLY RECOVERED QUESTIONS
        save_checkpoint()

        raise


# ==========================================
# FINAL SUMMARY
# ==========================================

print("\n" + "=" * 55)
print("BIOLOGY EXTRACTION SUMMARY")
print("=" * 55)

print("YEAR RANGE:", START_YEAR, "-", END_YEAR)
print("TOTAL VALID QUESTIONS:", len(all_questions))
print("UNIQUE QUESTION IDS:", len(seen_ids))

for result in year_report:

    print(
        result["year"],
        "|",
        result["questions_recovered"],
        "|",
        result["status"]
    )

print("\nQUESTIONS FILE:", OUTPUT_FILE)
print("REPORT FILE:", REPORT_FILE)

print("\nEXTRACTION FINISHED SUCCESSFULLY.")

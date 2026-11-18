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

print("=" * 55)
print("STALWART PREP - SDASHAPI EXTRACTION")
print("SUBJECT: BIOLOGY")
print("EXAM: JAMB / UTME")
print(f"YEAR RANGE: {START_YEAR}-{END_YEAR}")
print("=" * 55)


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

    print("HTTP STATUS:", response.status_code)

    if response.status_code == 401:
        raise RuntimeError(
            "Invalid or missing SdashAPI Access Token."
        )

    if response.status_code == 403:
        raise RuntimeError(
            "SdashAPI access denied. Check your account."
        )

    if response.status_code == 429:
        raise RuntimeError(
            "API quota/rate limit reached. Stop extraction."
        )

    if response.status_code == 404:
        print(f"No matching records for {year}.")
        return []

    response.raise_for_status()

    payload = response.json()

    if payload.get("status") != 200:
        raise RuntimeError(
            f"API error for {year}: {payload}"
        )

    records = payload.get("data", [])

    if isinstance(records, dict):
        records = [records]

    if not isinstance(records, list):
        raise RuntimeError(
            f"Unexpected response format for {year}"
        )

    valid = []

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

        answer = str(answer).lower().strip()

        if answer not in options:
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
            "options": {
                str(k).upper(): v
                for k, v in options.items()
            },
            "answer": answer.upper(),
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
                "Completeness is not established."
            )

        time.sleep(1)

    except Exception as error:

        print(f"ERROR in {year}: {error}")

        year_report.append({
            "year": year,
            "questions_recovered": 0,
            "status": "FAILED",
            "error": str(error)
        })

        raise


# ==========================================
# SAVE RESULTS
# ==========================================

output_file = (
    OUTPUT_DIR /
    "sdash_biology_2015_2026.json"
)

with open(
    output_file,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        all_questions,
        file,
        indent=2,
        ensure_ascii=False
    )


report_file = (
    OUTPUT_DIR /
    "sdash_biology_extraction_report.json"
)

with open(
    report_file,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        year_report,
        file,
        indent=2
    )


print("\n" + "=" * 55)
print("EXTRACTION SUMMARY")
print("=" * 55)

print("SUBJECT: BIOLOGY")
print("YEARS:", START_YEAR, "-", END_YEAR)
print("TOTAL VALID QUESTIONS:", len(all_questions))
print("UNIQUE QUESTION IDs:", len(seen_ids))

for result in year_report:

    print(
        result["year"],
        result["questions_recovered"],
        result["status"]
    )

print("\nOUTPUT:", output_file)
print("REPORT:", report_file)

print("\nEXTRACTION FINISHED.")

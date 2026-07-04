# API Endpoint Reference — SdashAPI

**Base URL:** `https://sdashapi.com/api/v1`

All endpoints require the `AccessToken` header:
```
AccessToken: sdash_your_token_here
```

---

## Authentication

```bash
# Header (recommended for production)
curl https://sdashapi.com/api/v1/q \
  -H "AccessToken: sdash_your_token_here"

# Query parameter (quick testing only)
curl "https://sdashapi.com/api/v1/q?token=sdash_your_token_here"
```

---

## GET /api/v1/q

Fetch one or more past exam questions from the full question bank (2001–present).

**Default behaviour:** Returns 1 random question.

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `subject` | string | No | Subject slug (e.g. `chemistry`, `biology`). Get slugs from `/v1/subjects` |
| `type` | string | No | Exam type slug: `utme`, `wassce`, `neco`, `post-utme`, `university` |
| `year` | integer | No | 4-digit year e.g. `2022`. Get valid years from `/v1/years` |
| `id` | integer | No | Fetch a specific question by its ID |
| `limit` | integer | No | Number of questions to return (`1–50`). Default: `1` |

### Limit Behaviour

> **Important:** When `limit=1`, the `data` field is a **JSON object**.  
> When `limit > 1`, the `data` field is a **JSON array**.

### Example — Single question

**Request:**
```
GET /api/v1/q?subject=chemistry&type=utme&year=2022
AccessToken: sdash_xxxxxxxxxxxx
```

**Response:**
```json
{
  "status": 200,
  "data": {
    "id": 4821,
    "question": "Which of the following is the chemical formula for table salt?",
    "section": null,
    "option": {
      "a": "NaCl",
      "b": "KCl",
      "c": "CaCO3",
      "d": "NaOH"
    },
    "answer": "a",
    "solution": "NaCl is sodium chloride, with the chemical formula NaCl — one sodium atom bonded to one chlorine atom.",
    "image": null,
    "examtype": "UTME",
    "examyear": "2022"
  }
}
```

### Example — Multiple questions

**Request:**
```
GET /api/v1/q?limit=10
```

**Response:**
```json
{
  "status": 200,
  "data": [
    { "id": 101, "question": "...", ... },
    { "id": 204, "question": "...", ... },
    ...
  ]
}
```

---

## GET /api/v1/subjects

Returns all available subjects and their slugs.

**Request:**
```
GET /api/v1/subjects
AccessToken: sdash_xxxxxxxxxxxx
```

**Response:**
```json
{
  "status": 200,
  "data": [
    { "id": 1, "name": "Biology", "slug": "biology" },
    { "id": 2, "name": "Chemistry", "slug": "chemistry" },
    { "id": 3, "name": "Physics", "slug": "physics" },
    { "id": 4, "name": "Mathematics", "slug": "mathematics" },
    { "id": 5, "name": "English Language", "slug": "english" }
  ]
}
```

Use the `slug` as the `subject` parameter in `/v1/q`.

---

## GET /api/v1/exams

Returns all available exam types and their slugs.

**Request:**
```
GET /api/v1/exams
AccessToken: sdash_xxxxxxxxxxxx
```

**Response:**
```json
{
  "status": 200,
  "data": [
    { "id": 1, "name": "UTME",       "slug": "utme" },
    { "id": 2, "name": "WASSCE",     "slug": "wassce" },
    { "id": 3, "name": "POST-UTME",  "slug": "post-utme" },
    { "id": 4, "name": "NECO",       "slug": "neco" },
    { "id": 5, "name": "University", "slug": "university" }
  ]
}
```

Use the `slug` as the `type` parameter in `/v1/q`.

---

## GET /api/v1/years

Returns a list of all available years as integers, newest first.

**Request:**
```
GET /api/v1/years
AccessToken: sdash_xxxxxxxxxxxx
```

**Response:**
```json
{
  "status": 200,
  "data": [2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010]
}
```

---

## POST /api/v1/report

Report a question that has a wrong answer, typo, or other issue.

**Request:**
```
POST /api/v1/report
AccessToken: sdash_xxxxxxxxxxxx
Content-Type: application/json
```

**Body:**
```json
{
  "question_id": 4821,
  "report_type": "wrong_answer",
  "message": "Option B should be the correct answer because..."
}
```

### Body Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `question_id` | integer | **Yes** | The `id` from the question object |
| `report_type` | string | No | One of: `wrong_answer`, `typo`, `unclear`, `other`. Default: `wrong_answer` |
| `message` | string | No | Extra detail or explanation |

**Response:**
```json
{
  "status": 200,
  "message": "Report submitted. Thank you!"
}
```

---

## Error Responses

All error responses follow this format:

```json
{
  "status": 401,
  "message": "Invalid AccessToken."
}
```

| Status Code | Meaning |
|-------------|---------|
| `200` | Success |
| `400` | Bad request — missing or invalid parameters |
| `401` | Missing or invalid `AccessToken` |
| `403` | Account suspended, banned, or plan expired |
| `404` | No questions matched your filters / unknown endpoint |
| `405` | Wrong HTTP method used |
| `429` | Monthly quota exceeded |

---

## Rate Limits & Quotas

API calls are metered per plan. Check your usage on the [dashboard](https://sdashapi.com/dashboard).

---

[← Back to README](../README.md) · [Quick Start →](quickstart.md) · [Examples →](examples/)

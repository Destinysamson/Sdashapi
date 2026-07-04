# Quick Start Guide — SdashAPI

Get up and running with the SdashAPI in under 5 minutes.

---

## Step 1: Create your account

Go to **[sdashapi.com](https://sdashapi.com)** and sign up for a free account.

## Step 2: Get your AccessToken

After signing up, log in and go to your **Dashboard**. You'll see your `AccessToken` displayed — it looks like:

```
sdash_a1b2c3d4e5f6...
```

Copy it. This is your API key — treat it like a password.

## Step 3: Make your first API call

### Using curl

```bash
curl "https://sdashapi.com/api/v1/q?subject=biology&type=utme" \
  -H "AccessToken: sdash_your_token_here"
```

### Using JavaScript

```javascript
const res = await fetch('https://sdashapi.com/api/v1/q?subject=biology&type=utme', {
  headers: { 'AccessToken': 'sdash_your_token_here' }
});
const data = await res.json();
console.log(data.data); // your question object
```

### Using Python

```python
import requests

r = requests.get(
    'https://sdashapi.com/api/v1/q',
    params={'subject': 'biology', 'type': 'utme'},
    headers={'AccessToken': 'sdash_your_token_here'}
)
print(r.json())
```

## Step 4: Explore the response

A successful response looks like:

```json
{
  "status": 200,
  "data": {
    "id": 1042,
    "question": "Which organelle is responsible for ATP production?",
    "section": null,
    "option": {
      "a": "Nucleus",
      "b": "Mitochondria",
      "c": "Ribosome",
      "d": "Golgi apparatus"
    },
    "answer": "b",
    "solution": "The mitochondria is the powerhouse of the cell, responsible for producing ATP through cellular respiration.",
    "image": null,
    "examtype": "UTME",
    "examyear": "2021"
  }
}
```

## Step 5: Filter and explore

```bash
# Get 10 random questions
curl "https://sdashapi.com/api/v1/q?limit=10" -H "AccessToken: YOUR_TOKEN"

# Filter by subject + exam + year
curl "https://sdashapi.com/api/v1/q?subject=chemistry&type=wassce&year=2020" \
  -H "AccessToken: YOUR_TOKEN"

# List all subjects
curl "https://sdashapi.com/api/v1/subjects" -H "AccessToken: YOUR_TOKEN"

# List all exam types
curl "https://sdashapi.com/api/v1/exams" -H "AccessToken: YOUR_TOKEN"

# List all available years
curl "https://sdashapi.com/api/v1/years" -H "AccessToken: YOUR_TOKEN"
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Getting `401` | Check that you're sending `AccessToken` as a **header**, not in the URL |
| Getting `404` | The subject slug or exam type slug might be wrong — fetch `/v1/subjects` and `/v1/exams` to get the correct slugs |
| `data` is an object instead of array | When `limit=1` (default), `data` is an object. Use `limit=2` or more to get an array |
| Empty `section` field | `section` is `null` for most questions — only populated for comprehension/reading passages |

---

## Next steps

- [Full Endpoint Reference →](endpoints.md)
- [Code Examples in 5 Languages →](examples/)
- [Report a Bad Question →](https://sdashapi.com/docs#report)

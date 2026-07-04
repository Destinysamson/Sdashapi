<div align="center">

<img src="https://sdashapi.com/assets/img/logo.png" alt="SdashAPI Logo" width="120" />

# SdashAPI

### The #1 Nigerian Past Questions API

**Access 500,000+ past exam questions from JAMB/UTME, WAEC/WASSCE, NECO, and Post-UTME — via a single, blazing-fast REST API.**

[![API Status](https://img.shields.io/badge/API-Live-brightgreen?style=for-the-badge)](https://sdashapi.com)
[![Version](https://img.shields.io/badge/Version-v1.0-blue?style=for-the-badge)](https://sdashapi.com/docs)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![Docs](https://img.shields.io/badge/Docs-Read%20Now-orange?style=for-the-badge)](https://sdashapi.com/docs)

[🚀 Get Started](https://sdashapi.com) · [📖 Documentation](https://sdashapi.com/docs) · [💬 Community](https://sdashapi.com/community) · [🐛 Report a Bug](https://sdashapi.com/community)

</div>

---

## 🇳🇬 What is SdashAPI?

**SdashAPI** is the most comprehensive and developer-friendly **Nigerian past questions API** available. Whether you're building an EdTech app, a student revision platform, a quiz engine, or a learning management system — SdashAPI gives you instant, structured access to a growing bank of past exam questions, answers, and full worked solutions.

- ✅ **JAMB / UTME** past questions (2001–present)
- ✅ **WAEC / WASSCE** past questions
- ✅ **NECO** past questions
- ✅ **Post-UTME** past questions
- ✅ **University** exam questions
- ✅ Clean JSON responses — no scraping, no HTML parsing
- ✅ CORS-enabled — works from browser, mobile, or server
- ✅ Real-time answers + full worked solutions

---

## ⚡ Quick Start

### 1. Get your API key

Create a free account at **[sdashapi.com](https://sdashapi.com)** and copy your `AccessToken` from the dashboard.

### 2. Make your first request

```bash
curl "https://sdashapi.com/api/v1/q?subject=chemistry&type=utme" \
  -H "AccessToken: sdash_your_token_here"
```

### 3. Get back clean JSON

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
    "solution": "NaCl is sodium chloride — one sodium atom bonded to one chlorine atom.",
    "image": null,
    "examtype": "UTME",
    "examyear": "2022"
  }
}
```

That's it. No complex setup. No SDK required.

---

## 📚 Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/q` | Fetch one or more past exam questions |
| `GET` | `/api/v1/subjects` | List all available subjects |
| `GET` | `/api/v1/exams` | List all exam types |
| `GET` | `/api/v1/years` | List all available years |
| `POST` | `/api/v1/report` | Report an incorrect or unclear question |

Full reference → **[sdashapi.com/docs](https://sdashapi.com/docs)**

---

## 🔍 Filter Questions Precisely

```bash
# Random chemistry question
GET /api/v1/q?subject=chemistry

# JAMB Biology 2019
GET /api/v1/q?subject=biology&type=utme&year=2019

# 10 random mixed questions
GET /api/v1/q?limit=10

# Specific question by ID
GET /api/v1/q?id=4821

# WAEC Mathematics questions
GET /api/v1/q?subject=mathematics&type=wassce
```

All requests require the `AccessToken` header:

```
AccessToken: sdash_your_token_here
```

---

## 💻 Code Examples

### JavaScript / Fetch

```javascript
const response = await fetch(
  'https://sdashapi.com/api/v1/q?subject=biology&type=utme&limit=5',
  { headers: { 'AccessToken': 'sdash_your_token_here' } }
);
const data = await response.json();
console.log(data);
```

### Python

```python
import requests

resp = requests.get(
    'https://sdashapi.com/api/v1/q',
    params={'subject': 'biology', 'type': 'utme', 'limit': 5},
    headers={'AccessToken': 'sdash_your_token_here'}
)
print(resp.json())
```

### PHP

```php
$ch = curl_init('https://sdashapi.com/api/v1/q?subject=biology&type=utme&limit=5');
curl_setopt($ch, CURLOPT_HTTPHEADER, ['AccessToken: sdash_your_token_here']);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
$data = json_decode(curl_exec($ch), true);
print_r($data);
```

### Node.js (axios)

```javascript
const axios = require('axios');

const { data } = await axios.get('https://sdashapi.com/api/v1/q', {
  params: { subject: 'chemistry', type: 'utme', year: 2022 },
  headers: { AccessToken: 'sdash_your_token_here' }
});
console.log(data);
```

### Dart / Flutter

```dart
final response = await http.get(
  Uri.parse('https://sdashapi.com/api/v1/q?subject=mathematics&type=utme&limit=10'),
  headers: {'AccessToken': 'sdash_your_token_here'},
);
final data = jsonDecode(response.body);
```

More examples → [`docs/examples/`](docs/examples/)

---

## 📦 Response Schema

Every question object follows this structure:

| Field | Type | Description |
|-------|------|-------------|
| `id` | `integer` | Unique question ID |
| `question` | `string` | The question text |
| `section` | `string\|null` | Shared passage/instruction (for comprehension sets) |
| `option` | `object` | Options `a`, `b`, `c`, `d` (and optionally `e`) |
| `answer` | `string` | Correct option key e.g. `"a"` |
| `solution` | `string\|null` | Full worked solution/explanation |
| `image` | `string\|null` | URL to associated image, if any |
| `examtype` | `string` | Exam name e.g. `"UTME"`, `"WASSCE"`, `"NECO"` |
| `examyear` | `string` | 4-digit year as a string e.g. `"2022"` |

> **Note:** When `limit=1` (default), `data` is an **object**. When `limit > 1`, `data` is an **array**.

---

## 🎯 Supported Subjects

| Subject | Slug |
|---------|------|
| Biology | `biology` |
| Chemistry | `chemistry` |
| Physics | `physics` |
| Mathematics | `mathematics` |
| English Language | `english` |
| Economics | `economics` |
| Government | `government` |
| Geography | `geography` |
| Commerce | `commerce` |
| Accounting | `accounting` |
| Literature in English | `englishlit` |
| CRK | `crk` |
| IRK | `irk` |
| Civic Education | `civiledu` |
| History | `history` |
| Current Affairs | `currentaffairs` |

Get the full live list via `GET /api/v1/subjects`.

---

## 🏆 Why SdashAPI?

| Feature | SdashAPI | Others |
|---------|----------|--------|
| Nigerian exam coverage (JAMB, WAEC, NECO) | ✅ Full | ⚠️ Partial |
| Worked solutions / explanations | ✅ Yes | ❌ Rarely |
| Clean, consistent JSON | ✅ Yes | ⚠️ Varies |
| CORS enabled (browser-safe) | ✅ Yes | ❌ Often not |
| Section/comprehension support | ✅ Yes | ❌ No |
| Option E support (5-option questions) | ✅ Yes | ❌ No |
| Active maintenance & updates | ✅ Yes | ❌ Abandoned |
| Community support forum | ✅ Yes | ❌ No |

---

## 🛡️ Authentication

Every request must include your `AccessToken` as an HTTP header:

```bash
-H "AccessToken: sdash_xxxxxxxxxxxxxxxxxxxx"
```

For quick browser testing only, you can use a query parameter:

```
?token=sdash_xxxxxxxxxxxxxxxxxxxx
```

Get your token by creating a free account at [sdashapi.com](https://sdashapi.com).

---

## ❌ Error Codes

| Status | Meaning |
|--------|---------|
| `200` | ✅ Success |
| `400` | Bad request — check your parameters |
| `401` | Missing or invalid `AccessToken` |
| `403` | Account suspended or plan expired |
| `404` | No questions matched your filters, or unknown endpoint |
| `405` | Wrong HTTP method |
| `429` | Rate limit exceeded — upgrade your plan |

---

## 🗺️ Roadmap

- [x] UTME / JAMB questions (2001–present)
- [x] WAEC / WASSCE questions
- [x] NECO questions
- [x] Post-UTME questions
- [x] University exam questions
- [x] Full worked solutions
- [x] Image support for diagram questions
- [x] Community forum
- [ ] Webhook notifications for new questions
- [ ] SDKs for JavaScript, Python, PHP, Dart
- [ ] GraphQL endpoint
- [ ] Question difficulty ratings

---

## 🤝 Contributing

We welcome contributions to improve the community, docs, and SDKs!

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📜 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

The **question content** (past exam questions) is the intellectual property of their respective examination bodies (JAMB, WAEC, NECO) and is provided here for educational purposes.

---

## 📞 Support

- 📖 **Documentation:** [sdashapi.com/docs](https://sdashapi.com/docs)
- 💬 **Community Forum:** [sdashapi.com/community](https://sdashapi.com/community)
- 📧 **Email:** support@sdashapi.com

---

<div align="center">

**Built with ❤️ for Nigerian students and developers**

⭐ Star this repo if SdashAPI powers your project!

[sdashapi.com](https://sdashapi.com)

</div>

# Contributing to SdashAPI

Thank you for your interest in contributing! Here's how you can help.

---

## 🐛 Reporting Issues

Found a question with a wrong answer, typo, or unclear wording?

**Option 1 — Via the API (for developers):**
```bash
curl -X POST https://sdashapi.com/api/v1/report \
  -H "AccessToken: YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"question_id": 1234, "report_type": "wrong_answer", "message": "Option B is correct, not A."}'
```

**Option 2 — Via the Community Forum:**  
Post in [sdashapi.com/community](https://sdashapi.com/community)

---

## 📝 Improving Documentation

To improve these docs:

1. Fork this repository
2. Create a branch: `git checkout -b docs/improve-quickstart`
3. Make your changes in `docs/`
4. Submit a Pull Request with a clear description

---

## 💡 Suggesting Features

Open a GitHub Issue with the label `enhancement` describing:
- What you'd like to see
- Your use case
- Any relevant examples

---

## 🤝 Code of Conduct

- Be respectful and constructive
- Keep discussions focused on the project
- Help each other — we're all learning

---

## 📞 Contact

- Email: support@sdashapi.com
- Community: [sdashapi.com/community](https://sdashapi.com/community)

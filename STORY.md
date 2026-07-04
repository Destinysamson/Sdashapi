# The Story Behind SdashAPI

<div align="center">
<img src="../assets/logo.png" alt="SdashAPI" width="80" />

*By **Ogbu Chukwuemeka (Emmy)**, Founder of SdashAPI & StudentsDash*

📖 [Read more about the founder →](https://studentsdash.com/emmy-biography/)
</div>

---

## 🇳🇬 Building for Nigerian Students

Building a startup in Nigeria is not for the faint-hearted.

I have spent years in the trenches of Nigerian EdTech — building, failing, learning, and rebuilding. My journey started with a singular obsession: **how do we make Nigerian students actually enjoy preparing for exams?**

That obsession led me to build **[StudentsDash](https://studentsdash.com)** — a platform designed to help Nigerian students prepare for JAMB, WAEC, NECO, Post-UTME, and university exams in a smarter, more structured way. We weren't just another past questions site. We were building a full ecosystem — tools, analytics, and resources — to give every Nigerian student a fair shot at academic success.

It took enormous effort, sacrifice, and resources. But we built something real.

---

## 💾 The Database That Wouldn't Sleep

Along the way, we quietly assembled what is arguably **Nigeria's most comprehensive past questions database**.

Thousands of verified past exam questions. JAMB going back to **1990**. WAEC. NECO. Post-UTME from over a dozen universities. Worked solutions written and reviewed by subject experts. Questions with images, comprehension passages, and five-option variants.

This database didn't happen overnight. It was collected question by question, verified answer by answer, solution by solution. **Real work. Real cost. Real time.**

And then one day I asked myself a question that changed everything:

> *"These questions are just sitting here. What if every developer building an EdTech app in Nigeria could access them instantly?"*

---

## ⚡ The API Was Born

That thought became **SdashAPI**.

We opened up our entire question bank as a clean, well-documented REST API. Any developer — whether you're a student in a university hostel writing your first app, a startup founder building the next big EdTech platform, or an agency working with a school — can now access **decades of Nigerian past exam questions in seconds**.

No scraping. No PDFs. No WhatsApp groups. Just clean JSON.

```json
{
  "status": 200,
  "data": {
    "id": 4821,
    "question": "Which of the following is the chemical formula for table salt?",
    "option": { "a": "NaCl", "b": "KCl", "c": "CaCO3", "d": "NaOH" },
    "answer": "a",
    "solution": "NaCl is sodium chloride — one sodium atom bonded to one chlorine atom.",
    "examtype": "UTME",
    "examyear": "2022"
  }
}
```

---

## 🏆 Why SdashAPI Is Different

The ALOC.ng API — built by Ope Mesonrale, whom I respect for pioneering this idea — showed that the concept worked. But it had limits:

- **Years capped at 2001–2013**
- **Only ~6,000 questions**
- **No worked solutions**
- **No question reporting tool**
- **No CORS support for browsers**
- **No API usage dashboard**

We took everything that worked and went further:

| | ALOC.ng | **SdashAPI** |
|--|---------|-------------|
| Questions | ~6,000 | **100,000+** |
| Years covered | 2001–2013 | **1990–present** |
| Worked solutions | ❌ | ✅ |
| Question reporting | ❌ | ✅ Built-in |
| CORS support | ❌ | ✅ |
| Usage dashboard | ❌ | ✅ |
| API logs | ❌ | ✅ |
| Subjects covered | 17 | **17+ and growing** |
| University GST/GNS | ❌ | ✅ |
| Active maintenance | ❌ Abandoned | ✅ Live |

We didn't build a competitor. We built the **successor**.

---

## 🎯 The Mission

Every year, over **1.7 million candidates** sit for JAMB/UTME in Nigeria. Millions more write WAEC, NECO, and Post-UTME. Most of them don't have access to good preparation tools.

**SdashAPI exists to change that** — by making it radically easy for developers to build the tools these students need.

If you're building a quiz app, a CBT platform, an AI tutor, a Telegram bot for students, or anything that helps Nigerian students learn — **SdashAPI is for you**.

---

## 👤 About the Founder

**Ogbu Chukwuemeka** (Emmy) is a Nigerian software developer, EdTech entrepreneur, and the founder of SdashAPI and StudentsDash. He has spent years building technology that closes the gap between Nigerian students and academic success.

📖 [Read Emmy's full biography →](https://studentsdash.com/emmy-biography/)

🌐 [StudentsDash →](https://studentsdash.com)

🔗 [SdashAPI →](https://sdashapi.com)

---

## 🤝 Join the Mission

- ⭐ **Star this repo** to show support
- 🐛 **Report wrong questions** via [/api/v1/report](https://sdashapi.com/docs#report) or the [community forum](https://sdashapi.com/community)
- 📣 **Share SdashAPI** with any developer building for Nigerian students
- 💬 **Join the conversation** at [sdashapi.com/community](https://sdashapi.com/community)

---

<div align="center">

*"The questions were already there. We just opened the door."*

**— Ogbu Chukwuemeka, Founder, SdashAPI**

</div>

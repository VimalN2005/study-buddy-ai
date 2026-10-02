---
title: Building StudyBuddy AI for My College Friend: Turning Dense Notes into Interactive Quizzes with Open-Source AI
published: true
tags: hacktoberfest, ai, opensource, python
cover_image: https://raw.githubusercontent.com/open-telemetry/opentelemetry.io/main/icon.png
---

*This is a submission for the [Hacktoberfest 2026 Open-Source AI Weekend Challenge: Build for a Friend](https://dev.to/challenges).*

---

### 💡 Who I Built This For ("Build for a Friend")

During exam weeks at my college (IIIT Bhopal), my friends and roommates often get overwhelmed by hundreds of slides of dense lecture notes—whether it is Operating Systems, Distributed Systems, or Machine Learning. 

Reading passively through 50-page PDFs the night before an exam causes fatigue and poor retention. My friend Aman specifically told me: *"I just wish there was a fast way to test myself on these key concepts without spending hours manually making flashcards."*

That inspired me to build **StudyBuddy AI**.

---

### 🎓 What I Built

**StudyBuddy AI** is an open-source, interactive study companion built in Python. You simply paste your lecture notes or technical topic, and it immediately generates:

1. **⚡ Executive Summary:** 4–5 high-yield bullet takeaways.
2. **🧠 Interactive Active-Recall Quiz:** Custom multiple-choice questions with instant scoring, feedback, and in-depth explanations.
3. **📌 Flash Cheat-Sheet:** A clean glossary of core terms and definitions for quick revision right before the test.

---

### 🤖 Open-Source AI at the Core

To adhere to the core ethos of open-source and open-weight models, StudyBuddy AI is powered by **Meta's Llama 3.1** (via fast inference APIs like Groq or Hugging Face):

- It prompts the open-weight model to return strict, deterministic JSON schemas for summaries, quiz questions, and flash definitions.
- Includes a zero-setup **Demo / Offline Mode** so anyone can test the full active-recall workflow locally without even requiring an API key.

---

### 💻 Tech Stack

- **Frontend & App:** Python & [Streamlit](https://streamlit.io/)
- **AI Core:** Open-weight LLMs (Meta Llama 3.1 8B Instruct)
- **Data Schemas:** JSON-driven active recall structures

---

### 🔗 Code Repository

The code is 100% open-source and available on GitHub:

👉 **GitHub Repository:** [https://github.com/VimalN2005/study-buddy-ai](https://github.com/VimalN2005/study-buddy-ai)

---

### 🚀 What My Friend Thought

When I shared the prototype with Aman, he pasted his distributed systems notes and immediately took the 5-question generated quiz. The instant feedback on why an option was incorrect helped him grasp the CAP theorem and consensus protocols in minutes instead of hours. 

Happy Hacktoberfest 2026! 🎉

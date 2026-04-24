<div align="center">
  <img src="https://via.placeholder.com/120x120?text=🤖" alt="AI Study Coach Logo" width="100"/>
  <h1>AI Study Coach</h1>
  <p><strong>Your Personalized, AI-Powered Pedagogical Assistant & Study Planner</strong></p>
  
  [![Django](https://img.shields.io/badge/Django-5.0+-092E20?style=for-the-badge&logo=django)](https://www.djangoproject.com/)
  [![Gemini](https://img.shields.io/badge/Gemini_API-Google-4285F4?style=for-the-badge&logo=google)](https://aistudio.google.com/)
  [![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
</div>

<br>

## 📖 Overview

**AI Study Coach** is a production-ready, full-stack web application designed to help students optimize their learning journey. Powered by Django and Google's advanced **Gemini AI**, it serves two primary functions:
1. **Intelligent Schedule Engine**: Automatically generates a biologically-optimized, 7-day study curriculum tailored precisely to the user's available time, target exams, and pedagogical best practices.
2. **Empathetic AI Companion**: A conversational coach interface that provides motivational guidance, study strategies, and structured advice for academic hurdles.

Designed with clean architecture and a robust, modern, responsive UI.

---

## ✨ Features

- **🧠 Algorithmic Study Generation**
  - Converts user inputs (target exam, daily hours, subjects) into strict JSON schema using Gemini prompts.
  - Automatically handles cognitive load balancing (e.g., hard subjects in the morning, memory-retention subjects in the afternoon).
  - Enforces strict constraints like maximum block durations and mandatory screen-breaks (`Mola`).
- **💬 Empathetic AI Mentorship**
  - Integrated chat interface with a meticulously engineered persona prompt.
  - Responses are guaranteed to be actionable, empathetic, and structured exclusively via bullet points and clear takeaways.
- **🎨 Modern & Responsive UI/UX**
  - Beautiful, card-based interface with subtle glassmorphism and modern gradient design tokens.
  - **Swipe-to-Scroll Mobile Calendar**: The generated 7-day schedule features frictionless horizontal touch scrolling on mobile devices without breaking DOM structure.
- **🛡️ Enterprise-Grade Backend Safety**
  - Deep architectural decoupling: AI SDK logic exists purely in the `ai_service` layer, keeping views extremely lean.
  - Robust exception boundaries gracefully catching API quotas (429), timeouts, and validation errors seamlessly.

---

## 🛠️ Tech Stack

### Core & Backend
- **Python 3.10+**
- **Django 5.x** — Core framework, ORM, Auth, and templating.
- **Google GenAI SDK** — Direct integration with the Gemini family of models.
- **SQLite** — Lightweight local DB (easily swappable to PostgreSQL for production).

### Frontend
- **Vanilla CSS (Variables & Flexbox/Grid)** — No tailwind/bootstrap dependencies. Pure, lightweight performance.
- **HTML5 Django Templates**

---

## 📸 Screenshots

> **Note:** *(Replace placeholders with actual project screenshots)*

| Dashboard & Weekly Calendar | AI Chat Interface |
| :---: | :---: |
| <img src="https://via.placeholder.com/400x250?text=Dashboard+Screenshot" alt="Dashboard View"> | <img src="https://via.placeholder.com/400x250?text=AI+Coach+Screenshot" alt="AI Coach Interface"> |
| *Dynamic color-coded 7-day schedule with topic-level tooltips.* | *Conversational interface receiving structured pedagogical advice.* |

---

## 🚀 Easy Installation

Follow these steps to get a development environment running locally.

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/AI_Study_Coach.git
cd AI_Study_Coach
```

### 2. Set up the Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
*(Ensure `google-genai` and `django` are explicitly installed).*

### 4. Provide your API Key
The application expects a Google Gemini API key. Set it in your environment:
```bash
# Windows (PowerShell)
$env:GOOGLE_API_KEY="your_api_key_here"

# macOS/Linux
export GOOGLE_API_KEY="your_api_key_here"
```
*(Alternatively, insert it into your `.env` or Django `settings.py` if configured).*

### 5. Run Migrations & Start Server
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Navigate to `http://localhost:8000` to access the application.

---

## 🏗️ Architecture Highlight: `ai_service.py`

To ensure robust exception handling and template modularity, the Gemini calls are thoroughly abstracted:
- **`ask_ai_coach(query)`**: Validates formatting constraints.
- **`generate_study_program(hours, exam)`**: Forces the AI into a strict JSON output matching our frontend's custom Grid parser (`baslangic`, `bitis`, `ders`, `konu`, `tavsiye`).
- Catch blocks map directly to user-friendly UI toasts rather than throwing server 500s.

---

## 📄 License & Contribution

This project is licensed under the MIT License. Feel free to fork it, create a feature branch, and submit a PR!
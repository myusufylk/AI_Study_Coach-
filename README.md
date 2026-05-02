<div align="center">
  <img src="https://via.placeholder.com/120x120?text=🤖" alt="AI Study Coach Logo" width="100"/>
  <h1>AI Study Coach</h1>
  <p><strong>Your Personalized, AI-Powered Pedagogical Assistant & Study Planner</strong></p>
  
  [![Django](https://img.shields.io/badge/Django-5.0+-092E20?style=for-the-badge&logo=django)](https://www.djangoproject.com/)
  [![Grok](https://img.shields.io/badge/xAI_Grok-API-000000?style=for-the-badge&logo=x)](https://console.x.ai/)
  [![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
</div>

<br>

## 📖 Overview

**AI Study Coach** is a production-ready, full-stack web application designed to help students optimize their learning journey. Powered by Django and xAI's advanced **Grok AI**, it serves two primary functions:
1. **Intelligent Schedule Engine**: Automatically generates a biologically-optimized, 7-day study curriculum tailored precisely to the user's available time, target exams, and pedagogical best practices.
2. **Empathetic AI Companion**: A conversational coach interface that provides motivational guidance, study strategies, and structured advice for academic hurdles.

Designed with clean architecture and a robust, modern, responsive UI.

---

## ✨ Features

- **🧠 Algorithmic Study Generation**
  - Converts user inputs (target exam, daily hours, subjects) into strict JSON schema using Grok prompts.
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
- **OpenAI SDK** — Direct integration with the xAI Grok family of models.
- **Microsoft SQL Server** — A powerful database used in large-scale, real-world projects (can be replaced with simpler systems if needed).

### Frontend
- **Vanilla CSS (Variables & Flexbox/Grid)** — No tailwind/bootstrap dependencies. Pure, lightweight performance.
- **HTML5 Django Templates**

---

## 📸 Screenshots

### Dashboard
![Dashboard](screenshots/dashboard.png)
<img width="1850" height="925" alt="image" src="https://github.com/user-attachments/assets/5ca1beb7-9f85-43a0-bc99-712579245dd5" />


### AI Coach Chat
![AI Coach](screenshots/ai-coach.png)
<img width="1851" height="927" alt="image" src="https://github.com/user-attachments/assets/c75fbc54-3cf2-47c4-9fb7-1efa342adc40" />


### Subject Selection
![Subject Selection](screenshots/subjects.png)
<img width="1832" height="925" alt="image" src="https://github.com/user-attachments/assets/49f58355-4252-44a3-b843-abf184dde593" />


### Weekly Goal Form
![Weekly Goal](screenshots/weekly-goal.png)
<img width="1831" height="919" alt="image" src="https://github.com/user-attachments/assets/d3dc4fd7-6e5a-40d0-9aa5-32d850a73444" />


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
*(Ensure `openai` and `django` are explicitly installed).*

### 4. Provide your API Key
The application expects an xAI API key. Set it in your environment:
```bash
# Windows (PowerShell)
$env:XAI_API_KEY="your_api_key_here"

# macOS/Linux
export XAI_API_KEY="your_api_key_here"
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

In this project, I separated the AI-related code into `ai_service.py`.  
I did this because I did not want the Django views to become too crowded.

This file mainly handles the communication with xAI Grok.

- `ask_ai_coach(user_query)` is used for the AI coach chat.
- `generate_study_program(target_exam, daily_hours)` creates a weekly study plan for the student.
- The weekly plan is returned in JSON format so it can be used easily in the dashboard.
- If the API key is missing, the quota is exceeded, or xAI Grok returns an empty response, the error is handled here.
- Instead of showing technical errors to the user, the app shows simpler messages.

Thanks to this structure, the project is easier to read, debug, and improve later.

---

## 📄 License & Contribution

This project is licensed under the MIT License. Feel free to fork it, create a feature branch, and submit a PR!

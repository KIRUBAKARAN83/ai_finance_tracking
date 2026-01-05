# ai_finance_tracker



# 🤖 AI Finance Tracker

An **AI-powered personal finance & budget tracking web application** built with **Django**, featuring smart insights, budget monitoring, charts, and an AI assistant chatbot.

---

## 🚀 Features

### 💰 Finance Management
- Add **Income & Expense** transactions
- Categorize expenses automatically
- Monthly summary with **Income, Expense & Savings**
- Download monthly reports as **PDF**

### 📊 Visual Analytics
- Interactive **Bar & Pie Charts**
- Animated counters & progress bars
- Scroll-triggered UI animations
- Mobile-friendly responsive dashboard

### 📉 Budget Tracking
- Create category-wise budgets
- Live budget usage progress
- Alerts when budget crosses 80% / 100%
- Smart budget suggestions (based on history)

### 🤖 AI Assistant (Chatbot)
- Ask natural language questions like:
  - *“What is my budget status?”*
  - *“How much did I spend this month?”*
- Uses **local LLM (Ollama)** or cloud AI
- Secure user-specific financial context
- No data shared publicly

### 🔐 Authentication & Admin
- User login & registration
- Admin dashboard
- User management (ban / unban)
- Staff-only admin views

### 📱 PWA Support
- Installable as a mobile app
- Offline fallback page
- Custom app icons
- Dark / Light mode toggle

---

## 🛠 Tech Stack

| Layer | Technology |
|-----|-----------|
| Backend | Django (Python) |
| Frontend | HTML, Bootstrap 5, JS |
| Database | PostgreSQL (Supabase) |
| Charts | Chart.js |
| AI | Ollama (Local LLM) / OpenAI |
| Auth | Django Auth |
| Hosting | Render |
| PWA | Service Worker + Manifest |

---


## 📂 Project Structure

**ai_finance_tracker/
  │
  ├── accounts/
  ├── transactions/
  ├── insights/
  │ ├── budget_alerts.py
  │ ├── budget_progress.py
  │ ├── chat_engine.py
  │
  ├── templates/
  │ ├── base.html
  │ ├── dashboard.html
  │ ├── admin_dashboard.html
  │
  ├── static/
  │ ├── service-worker.js
  │ ├── manifest.json
  │
  ├── manage.py
  ├── requirements.txt
  └── README.md
  **

---

## ⚙️ Local Setup

### 1️⃣ Clone the repo
```bash
git clone https://github.com/KIRUBAKARAN83/ai_finance_tracker.git
cd ai_finance_tracker

2️⃣ Create virtual environment
python -m venv venv
venv\Scripts\activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Configure environment variables

Create a .env file or set variables:

DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://...

🧠 AI Chatbot Setup (Ollama)
Install Ollama

👉 https://ollama.com/download

Pull a model (recommended)
ollama pull llama3.1:8b

Run Ollama
ollama serve


Chatbot uses Ollama HTTP API for fast responses.

🚀 Deployment (Render + Supabase)
Backend (Render)

Create Web Service

Connect GitHub repo

Build command:

pip install -r requirements.txt


Start command:

gunicorn ai_finance_tracker.wsgi

Database (Supabase)

Create PostgreSQL project

Copy connection string

Set DATABASE_URL in Render env vars

⚠️ Important Notes

Ollama will NOT run on Render Free tier

Use:

OpenAI API (paid) OR

External VPS with Ollama OR

Local-only AI mode

🧪 Test Login

Create superuser:

python manage.py createsuperuser

🧑‍💻 Author

Kirubakaran D
BCA Graduate | Full Stack Developer
Python • Django • AI • PostgreSQL

⭐ Support

If you like this project:

⭐ Star the repo

🐛 Open issues

🤝 Fork & contribute

# 🩺 HealthBridge AI

HealthBridge AI is a Flask-based web application that uses **RAG (Retrieval-Augmented Generation)** and AI models to provide intelligent health insights, symptom analysis, and personalized recommendations.

---

## 🚀 Features
- 🔐 User authentication (Register / Login / Logout)
- 👤 Patient dashboard with health details
- 🤖 AI-powered symptom analysis (LangChain + Groq)
- 🏥 Doctor and hospital overview
- 📊 Health metrics visualization
- 🗄️ Vector search with Qdrant
- 📄 CSV ingestion for medical knowledge

---

## 🛠️ Tech Stack
- **Backend:** Flask, Flask-SQLAlchemy, Flask-Migrate
- **AI & RAG:** LangChain, Groq API, sentence-transformers
- **Database:** SQLite (dev) / Qdrant for vectors
- **Frontend:** Bootstrap + custom CSS
- **Other:** Python-dotenv for environment management

---

## ⚙️ Setup & Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR-USERNAME/healthbridge-ai.git
   cd healthbridge-ai

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   # mac/linux
   venv\Scripts\activate      # windows

3. Install dependencies
   ```bash
   pip install -r requirements.txt

4. Set environment variables
  Create a .env file in the project root:
   ```bash
   FLASK_APP=app.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key
   DATABASE_URL=sqlite:///healthbridge.db

6. Run database migrations
   ```bash
   flask db upgrade
   
7. Start the app
   ```bash
   python app.pu
     OR
   flask run

App will run on: http://127.0.0.1:5000




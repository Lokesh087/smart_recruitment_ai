# Smart Recruitment AI

A Flask-based recruitment assistant that parses resumes, matches them against job descriptions, and provides a chatbot-style UI for recruiters.

## Features

- Resume upload and parsing from PDF, DOC, and DOCX files
- Raw resume text analysis
- Resume-to-job matching with SentenceTransformers
- Structured skill taxonomy for categorized skill extraction
- Role templates and custom job description support
- Simple web-based frontend for parsing, matching, and taxonomy viewing
- Health check endpoint

## 1. Backend setup

Open a terminal in the project folder and run:

```bash
cd /workspaces/smart_recruitment_ai
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## 2. Run the backend

From the project folder:

```bash
cd /workspaces/smart_recruitment_ai
source .venv/bin/activate
python app.py
```

The backend will run at:

```text
http://127.0.0.1:5000
```

You can also test health with:

```bash
curl http://127.0.0.1:5000/health
```

## 3. Open the frontend

Once the backend is running, open your browser at:

```text
http://127.0.0.1:5000/
```

The frontend is served directly by Flask from the templates and static files, so you do not need a separate frontend server.

## 4. How to use the app

1. Open the app in the browser.
2. Upload a resume file or paste resume text into the analyzer.
3. Choose a job role template or enter a custom job description.
4. Click "Parse Text" to extract structured resume details.
5. Click "Match Resume" to get a match score.
6. Use "View Skill Taxonomy" to inspect the skill categories.

## 5. API endpoints

- GET / - Main web page
- GET /health - Health check
- POST /api/resume - Upload a resume and analyze it
- POST /api/parse-text - Parse resume text directly
- POST /api/match-text - Match text against a job description
- GET /api/skill-taxonomy - Get skill categories
- POST /api/chat - Chatbot message endpoint

## 6. Example API commands

Parse text:

```bash
curl -X POST http://127.0.0.1:5000/api/parse-text \
  -H "Content-Type: application/json" \
  -d '{"text": "Experienced software engineer with Python, Flask, and Docker."}'
```

Match text:

```bash
curl -X POST http://127.0.0.1:5000/api/match-text \
  -H "Content-Type: application/json" \
  -d '{"resume_text": "Experienced software engineer with Python, Flask, and Docker.", "job_description": "Backend developer with Python, Flask, and Docker experience."}'
```

View taxonomy:

```bash
curl http://127.0.0.1:5000/api/skill-taxonomy
```

Upload a resume:

```bash
curl -X POST http://127.0.0.1:5000/api/resume \
  -F "resume=@/path/to/resume.pdf" \
  -F "job_description=Backend Developer role with Python and Docker"
```

## 7. Project files

- app.py - Flask application and routes
- resume_parser.py - Resume parsing, entity extraction, and taxonomy logic
- matcher.py - Resume-to-job matching logic
- templates/index.html - Main webpage
- static/script.js - Frontend behavior and API calls
- static/style.css - UI styling

## 8. Troubleshooting

- If the browser shows a connection error, ensure the Flask server is still running and that you opened the correct URL.
- If you are using a remote environment, use the forwarded port URL shown by the dev container instead of localhost.
- For lighter deployments such as Vercel or Streamlit, the app now uses fallback parsing and keyword matching so it does not depend on the large spaCy and sentence-transformer model downloads.

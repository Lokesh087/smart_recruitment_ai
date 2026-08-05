# Smart Recruitment AI

A Flask-based recruitment assistant that parses resumes, matches resumes against job descriptions, and provides a chatbot interface.

## Features

- Resume upload and parsing from PDF/DOC/DOCX files
- Raw resume text analysis
- Semantic resume-job matching using SentenceTransformers
- Structured skill taxonomy for categorized skill extraction
- Role template selection with auto-filled job descriptions
- Custom role option for free-form job descriptions
- Live UI for parsing, matching, and browsing the skill taxonomy
- Health endpoint for readiness checks

## Installation

1. Create a Python environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install spaCy model if not already installed:
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Running

```bash
export FLASK_APP=app.py
flask run --host=0.0.0.0 --port=5000
```

Then open the browser at `http://localhost:5000`.

## API Endpoints

- `GET /` - Load the UI
- `GET /health` - Service health check
- `POST /api/resume` - Upload resume and match against job description
- `POST /api/parse-text` - Parse resume text directly
- `POST /api/match-text` - Match resume text against a job description
- `GET /api/skill-taxonomy` - Return categorized skill taxonomy
- `POST /api/chat` - Chatbot messaging endpoint

## UI Usage

1. Upload a resume file to parse the content and populate the analyzer.
2. Paste or edit resume text in the analyzer.
3. Choose a role template or select `Custom` to enter a custom job description.
4. Click `Match Resume` to generate a match score.
5. Click `View Skill Taxonomy` to inspect the categorized skill list.

## Example API Commands

```bash
curl -X POST http://localhost:5000/api/parse-text \
  -H "Content-Type: application/json" \
  -d '{"text": "Experienced software engineer with Python, Flask, and Docker."}'
```

```bash
curl -X POST http://localhost:5000/api/match-text \
  -H "Content-Type: application/json" \
  -d '{"resume_text": "Experienced software engineer with Python, Flask, and Docker.", "job_description": "Looking for a backend developer with Python, Flask, and Docker experience."}'
```

```bash
curl http://localhost:5000/api/skill-taxonomy
```

```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What jobs do you have?"}'
```

```bash
curl -X POST http://localhost:5000/api/resume \
  -F "resume=@/path/to/resume.pdf" \
  -F "job_description=Backend Developer role with Python and Docker"
```

## Project Files

- `app.py` - Flask application and routes
- `resume_parser.py` - Resume parsing, entity extraction, and skill taxonomy
- `matcher.py` - Resume-job semantic matching with SentenceTransformers
- `templates/index.html` - Front-end UI page
- `static/script.js` - UI interactivity and API integration
- `static/style.css` - UI styling

## Notes

- The app uses lazy-loading for large models to reduce startup overhead.
- If the spaCy model is unavailable, it falls back to a blank English pipeline.

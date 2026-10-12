# AI Resume Analyzer

A small web app that analyzes pasted resume text and suggests matching jobs.

- **Backend** (`app.py`): FastAPI service using spaCy (`en_core_web_sm`).
- **Frontend** (`frontend/`): React app with Material UI.

## How it works

`POST /analyze` takes `{"resume": "<text>"}` and returns:

- `skills`: skills found by keyword matching against a built-in skills list plus the skills in `jobs.json`
- `education`: degree names (e.g. "Bachelor", "MS"), fields of study, and organizations detected by spaCy whose names contain "University", "College", "Institute" or "School"
- `experience`: phrases such as "3 years" or "5+ years"

`POST /recommend` takes `{"analysis": <result of /analyze>}` and returns the jobs from `jobs.json` that share at least one skill with the resume, ranked by the number of matching skills, with a bonus for a matching field of study and for meeting the job's years of experience. Each job includes `matched_skills` and `score`.

The job list in `jobs.json` is a small sample and can be edited.

## Running locally

### Backend

Requires Python 3.

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python app.py
```

The API listens on `http://127.0.0.1:8000` by default. Set `PORT` to use a different port (port 5000 is avoided because macOS uses it for AirPlay Receiver):

```bash
PORT=8080 python app.py
```

CORS is enabled for `http://localhost:3000`.

### Frontend

```bash
cd frontend
npm install
npm start
```

Open http://localhost:3000. If the backend is not on port 8000, start the frontend with `REACT_APP_API_URL`, for example `REACT_APP_API_URL=http://127.0.0.1:8080 npm start`.

## Project structure

```
├── app.py             # FastAPI backend (/analyze, /recommend)
├── jobs.json          # Sample job postings used for recommendations
├── requirements.txt   # Python dependencies
└── frontend/          # React frontend
```

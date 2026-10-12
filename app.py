import json
import os
import re
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import spacy

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Job postings used by /recommend
JOBS_PATH = Path(__file__).parent / "jobs.json"
with open(JOBS_PATH, encoding="utf-8") as jobs_file:
    JOBS = json.load(jobs_file)

# en_core_web_sm has no SKILL/EDUCATION/EXPERIENCE labels, so skills and
# fields of study are found by keyword matching. The skills from jobs.json are
# always included so that every job can be matched.
BASE_SKILLS = [
    "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "SQL",
    "React", "Node.js", "HTML", "CSS", "Django", "Flask", "FastAPI",
    "Machine Learning", "Deep Learning", "Pandas", "NumPy", "TensorFlow",
    "PyTorch", "scikit-learn", "Docker", "Kubernetes", "AWS", "Git",
]
SKILLS = sorted(
    {*BASE_SKILLS, *(skill for job in JOBS for skill in job.get("skills", []))},
    key=str.lower,
)

FIELDS_OF_STUDY = sorted(
    {
        "Computer Science", "Data Science", "Software Engineering",
        "Information Technology", "Mathematics", "Statistics",
        *(field for job in JOBS for field in job.get("education", [])),
    },
    key=str.lower,
)
DEGREE_PATTERN = re.compile(
    r"\b(?:Bachelor(?:'s)?|Master(?:'s)?|Ph\.?D\.?|Doctorate|Associate(?:'s)?|"
    r"B\.?S\.?c?|M\.?S\.?c?|B\.?A\.?|M\.?A\.?|B\.?Tech|M\.?Tech|MBA)\b"
)
INSTITUTION_WORDS = ("university", "college", "institute", "school")
YEARS_PATTERN = re.compile(r"\b(\d+)\s*\+?\s*(?:years?|yrs?)\b", re.IGNORECASE)


def find_keywords(text, keywords):
    """Return the keywords that appear in text (case-insensitive, whole words)."""
    found = []
    for keyword in keywords:
        pattern = r"(?<![\w+#.])" + re.escape(keyword) + r"(?![\w+#])"
        if re.search(pattern, text, re.IGNORECASE):
            found.append(keyword)
    return found


def unique(items):
    """Remove duplicates while keeping the original order."""
    return list(dict.fromkeys(items))


@app.post("/analyze")
def analyze_resume(resume: dict):
    resume_text = resume.get("resume") or ""
    doc = nlp(resume_text)

    skills = find_keywords(resume_text, SKILLS)

    # Education: degree names, fields of study and institutions (ORG entities)
    education = [match.group(0) for match in DEGREE_PATTERN.finditer(resume_text)]
    education += find_keywords(resume_text, FIELDS_OF_STUDY)
    education += [
        ent.text
        for ent in doc.ents
        if ent.label_ == "ORG" and any(word in ent.text.lower() for word in INSTITUTION_WORDS)
    ]

    # Experience: phrases such as "3 years" or "5+ years"
    experience = [match.group(0) for match in YEARS_PATTERN.finditer(resume_text)]

    return {
        "skills": unique(skills),
        "education": unique(education),
        "experience": unique(experience),
    }


def years_from(phrases):
    """Return the largest number of years mentioned in a list of phrases."""
    years = [int(match.group(1)) for phrase in phrases for match in YEARS_PATTERN.finditer(phrase)]
    return max(years, default=0)


@app.post("/recommend")
def recommend_jobs(payload: dict):
    analysis = payload.get("analysis") or {}
    candidate_skills = {skill.lower() for skill in analysis.get("skills", [])}
    candidate_education = " ".join(analysis.get("education", [])).lower()
    candidate_years = years_from(analysis.get("experience", []))

    recommendations = []
    for job in JOBS:
        matched_skills = [skill for skill in job.get("skills", []) if skill.lower() in candidate_skills]
        if not matched_skills:
            continue
        score = len(matched_skills)
        if any(field.lower() in candidate_education for field in job.get("education", [])):
            score += 1
        if candidate_years and candidate_years >= years_from(job.get("experience", [])):
            score += 1
        recommendations.append({**job, "matched_skills": matched_skills, "score": score})

    recommendations.sort(key=lambda job: job["score"], reverse=True)
    return recommendations


if __name__ == "__main__":
    import uvicorn

    # Port 5000 is used by AirPlay Receiver on macOS, so default to 8000.
    uvicorn.run(app, host="127.0.0.1", port=int(os.getenv("PORT", "8000")))

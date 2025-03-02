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

@app.post("/analyze")
def analyze_resume(resume: dict):
    resume_text = resume.get("resume")
    doc = nlp(resume_text)

    # Extract entities (e.g., skills, education, experience)
    skills = [ent.text for ent in doc.ents if ent.label_ == "SKILL"]
    education = [ent.text for ent in doc.ents if ent.label_ == "EDUCATION"]
    experience = [ent.text for ent in doc.ents if ent.label_ == "EXPERIENCE"]

    return {
        "skills": skills,
        "education": education,
        "experience": experience
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
import os
import re
import logging

import fitz
from docx import Document


from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sentence_transformers import SentenceTransformer, util

from sqlalchemy import text
from backend.database import engine, SessionLocal


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


app = FastAPI(
    title="AI Resume Screening & Candidate Ranking System",
    version="1.0.0",
    description="AI-based resume screening system using NLP and semantic similarity."
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


logger.info("Loading sentence transformer model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
logger.info("Model loaded successfully.")


SKILLS = [
    "python",
    "java",
    "c++",
    "c#",
    "javascript",
    "typescript",
    "html",
    "css",
    "react",
    "angular",
    "node.js",
    "nodejs",
    "django",
    "flask",
    "fastapi",
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "nlp",
    "natural language processing",
    "tensorflow",
    "pytorch",
    "keras",
    "scikit-learn",
    "pandas",
    "numpy",
    "opencv",
    "docker",
    "kubernetes",
    "git",
    "github",
    "aws",
    "azure",
    "power bi",
    "excel",
    "data analysis",
    "data science"
]


EDUCATION_KEYWORDS = [
    "b.tech",
    "btech",
    "b.e",
    "be",
    "m.tech",
    "mtech",
    "m.e",
    "me",
    "bca",
    "mca",
    "b.sc",
    "bsc",
    "m.sc",
    "msc",
    "mba",
    "phd",
    "bachelor",
    "master",
    "computer science",
    "information technology",
    "information technology"
]


CERTIFICATION_KEYWORDS = [
    "certified",
    "certification",
    "certificate",
    "aws certified",
    "azure certified",
    "google certified",
    "python certification",
    "machine learning certification",
    "data science certification"
]


def extract_pdf(file_path):
    text_content = ""

    try:
        document = fitz.open(file_path)

        for page in document:
            text_content += page.get_text()

        document.close()

    except Exception as e:
        logger.error(f"PDF extraction error: {e}")
        raise

    return text_content


def extract_docx(file_path):
    text_content = ""

    try:
        document = Document(file_path)

        for paragraph in document.paragraphs:
            text_content += paragraph.text + "\n"

        for table in document.tables:
            for row in table.rows:
                for cell in row.cells:
                    text_content += cell.text + " "

    except Exception as e:
        logger.error(f"DOCX extraction error: {e}")
        raise

    return text_content


def extract_text(file_path):
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return extract_pdf(file_path)

    if extension == ".docx":
        return extract_docx(file_path)

    raise ValueError("Only PDF and DOCX files are supported.")


def extract_email(text_content):
    match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text_content
    )

    if match:
        return match.group(0)

    return ""


def extract_name(text_content):
    lines = [
        line.strip()
        for line in text_content.splitlines()
        if line.strip()
    ]

    for line in lines[:10]:

        if "@" in line:
            continue

        if any(char.isdigit() for char in line):
            continue

        if len(line.split()) > 5:
            continue

        cleaned = re.sub(
            r"[^A-Za-z\s]",
            "",
            line
        ).strip()

        if 2 <= len(cleaned.split()) <= 4:
            return cleaned

    return "Unknown"


def extract_skills(text_content):
    lower_text = text_content.lower()

    found_skills = []

    for skill in SKILLS:

        if skill.lower() in lower_text:
            found_skills.append(skill)

    return sorted(list(set(found_skills)))


def extract_education(text_content):
    lower_text = text_content.lower()

    found_education = []

    for education in EDUCATION_KEYWORDS:

        if education.lower() in lower_text:
            found_education.append(education)

    return sorted(list(set(found_education)))


def extract_certifications(text_content):
    lower_text = text_content.lower()

    found_certifications = []

    for certification in CERTIFICATION_KEYWORDS:

        if certification.lower() in lower_text:
            found_certifications.append(certification)

    return sorted(list(set(found_certifications)))


def extract_experience(text_content):
    lower_text = text_content.lower()

    patterns = [
        r"(\d+(?:\.\d+)?)\+?\s*(?:years|year)\s*(?:of)?\s*experience",
        r"experience\s*[:\-]?\s*(\d+(?:\.\d+)?)\+?\s*(?:years|year)",
        r"(\d+(?:\.\d+)?)\+?\s*yrs"
    ]

    for pattern in patterns:

        match = re.search(pattern, lower_text)

        if match:
            try:
                return float(match.group(1))
            except ValueError:
                pass

    return 0.0


def calculate_skill_score(resume_skills, jd_text):
    jd_lower = jd_text.lower()

    required_skills = []

    for skill in SKILLS:

        if skill.lower() in jd_lower:
            required_skills.append(skill)

    required_skills = sorted(list(set(required_skills)))

    if not required_skills:
        return 100.0, []

    matched_skills = []

    for skill in required_skills:

        if skill.lower() in [s.lower() for s in resume_skills]:
            matched_skills.append(skill)

    score = (
        len(matched_skills) /
        len(required_skills)
    ) * 100

    missing_skills = [
        skill
        for skill in required_skills
        if skill not in matched_skills
    ]

    return round(score, 2), missing_skills


def calculate_experience_score(resume_experience, jd_text):
    jd_lower = jd_text.lower()

    required_experience = 0

    patterns = [
        r"(\d+(?:\.\d+)?)\+?\s*(?:years|year)",
        r"(\d+(?:\.\d+)?)\+?\s*(?:yrs|yr)"
    ]

    for pattern in patterns:

        match = re.search(pattern, jd_lower)

        if match:
            try:
                required_experience = float(match.group(1))
                break
            except ValueError:
                pass

    if required_experience <= 0:
        return 100.0

    if resume_experience >= required_experience:
        return 100.0

    score = (
        resume_experience /
        required_experience
    ) * 100

    return round(min(score, 100), 2)


def calculate_semantic_score(resume_text, jd_text):
    try:

        resume_embedding = model.encode(
            resume_text,
            convert_to_tensor=True
        )

        jd_embedding = model.encode(
            jd_text,
            convert_to_tensor=True
        )

        similarity = util.cos_sim(
            resume_embedding,
            jd_embedding
        ).item()

        score = max(
            0,
            min(100, similarity * 100)
        )

        return round(score, 2)

    except Exception as e:
        logger.error(f"Semantic score error: {e}")
        return 0.0


def calculate_match_score(
    skill_score,
    experience_score,
    semantic_score
):

    score = (
        skill_score * 0.50
        + experience_score * 0.20
        + semantic_score * 0.30
    )

    return round(score, 2)


def get_status(match_score):

    if match_score >= 70:
        return "Shortlisted"

    if match_score >= 50:
        return "Review"

    return "Not Shortlisted"


def save_job_description(title, description):

    db = SessionLocal()

    try:

        query = text("""
            INSERT INTO job_descriptions
            (title, description)
            VALUES
            (:title, :description)
        """)

        db.execute(
            query,
            {
                "title": title,
                "description": description
            }
        )

        db.commit()

    except Exception as e:

        db.rollback()
        logger.error(f"Job description database error: {e}")

    finally:

        db.close()


def save_candidate(candidate, resume_file):

    db = SessionLocal()

    try:

        query = text("""
            INSERT INTO candidates
            (
                name,
                email,
                skills,
                education,
                experience,
                certifications,
                skill_score,
                experience_score,
                semantic_score,
                match_score,
                missing_skills,
                status,
                resume_file
            )
            VALUES
            (
                :name,
                :email,
                :skills,
                :education,
                :experience,
                :certifications,
                :skill_score,
                :experience_score,
                :semantic_score,
                :match_score,
                :missing_skills,
                :status,
                :resume_file
            )
        """)

        db.execute(
            query,
            {
                "name": candidate["name"],
                "email": candidate["email"],
                "skills": ", ".join(candidate["skills"]),
                "education": ", ".join(candidate["education"]),
                "experience": candidate["experience"],
                "certifications": ", ".join(candidate["certifications"]),
                "skill_score": candidate["skill_score"],
                "experience_score": candidate["experience_score"],
                "semantic_score": candidate["semantic_score"],
                "match_score": candidate["match_score"],
                "missing_skills": ", ".join(candidate["missing_skills"]),
                "status": candidate["status"],
                "resume_file": resume_file
            }
        )

        db.commit()

        logger.info(
            f"Candidate saved to database: {candidate['name']}"
        )

    except Exception as e:

        db.rollback()
        logger.error(f"Candidate database error: {e}")
        raise

    finally:

        db.close()


def analyze_resume(resume_text, job_description):

    name = extract_name(resume_text)

    email = extract_email(resume_text)

    skills = extract_skills(resume_text)

    education = extract_education(resume_text)

    certifications = extract_certifications(resume_text)

    experience = extract_experience(resume_text)

    skill_score, missing_skills = calculate_skill_score(
        skills,
        job_description
    )

    experience_score = calculate_experience_score(
        experience,
        job_description
    )

    semantic_score = calculate_semantic_score(
        resume_text,
        job_description
    )

    match_score = calculate_match_score(
        skill_score,
        experience_score,
        semantic_score
    )

    status = get_status(match_score)

    return {
        "name": name,
        "email": email,
        "skills": skills,
        "education": education,
        "experience": experience,
        "certifications": certifications,
        "skill_score": skill_score,
        "experience_score": experience_score,
        "semantic_score": semantic_score,
        "match_score": match_score,
        "missing_skills": missing_skills,
        "status": status
    }


@app.get("/")
def root():

    return {
        "message": "AI Resume Screening API is running"
    }


@app.get("/health")
def health():

    try:

        db = SessionLocal()

        db.execute(text("SELECT 1"))

        db.close()

        return {
            "status": "healthy",
            "database": "connected"
        }

    except Exception as e:

        logger.error(f"Health check error: {e}")

        return {
            "status": "healthy",
            "database": "disconnected"
        }


@app.post("/screen-resume")
async def screen_resume(
    job_description: str = Form(...),
    file: UploadFile = File(...)
):

    try:

        extension = os.path.splitext(
            file.filename
        )[1].lower()

        if extension not in [".pdf", ".docx"]:

            raise HTTPException(
                status_code=400,
                detail="Only PDF and DOCX files are supported."
            )

        file_path = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )

        file_content = await file.read()

        with open(file_path, "wb") as output_file:
            output_file.write(file_content)

        resume_text = extract_text(file_path)

        if not resume_text.strip():

            raise HTTPException(
                status_code=400,
                detail="Could not extract text from resume."
            )

        result = analyze_resume(
            resume_text,
            job_description
        )

        save_job_description(
            "Resume Screening Job",
            job_description
        )

        save_candidate(
            result,
            file.filename
        )

        result["resume_file"] = file.filename

        return result

    except HTTPException:
        raise

    except Exception as e:

        logger.error(
            f"Resume screening error: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.post("/screen-multiple-resumes")
async def screen_multiple_resumes(
    job_description: str = Form(...),
    files: list[UploadFile] = File(...)
):

    if not files:

        raise HTTPException(
            status_code=400,
            detail="Please upload at least one resume."
        )

    results = []

    try:

        save_job_description(
            "Resume Screening Job",
            job_description
        )

        for file in files:

            extension = os.path.splitext(
                file.filename
            )[1].lower()

            if extension not in [".pdf", ".docx"]:
                continue

            file_path = os.path.join(
                UPLOAD_FOLDER,
                file.filename
            )

            file_content = await file.read()

            with open(file_path, "wb") as output_file:
                output_file.write(file_content)

            resume_text = extract_text(file_path)

            if not resume_text.strip():
                continue

            result = analyze_resume(
                resume_text,
                job_description
            )

            result["resume_file"] = file.filename

            save_candidate(
                result,
                file.filename
            )

            results.append(result)

        results.sort(
            key=lambda x: x["match_score"],
            reverse=True
        )

        for index, result in enumerate(results, start=1):
            result["rank"] = index

        return {
            "total_candidates": len(results),
            "candidates": results
        }

    except HTTPException:
        raise

    except Exception as e:

        logger.error(
            f"Multiple resume screening error: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
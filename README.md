# AI-Powered Resume Screening & Candidate Ranking System

## Project Overview

The **AI-Powered Resume Screening & Candidate Ranking System** is a Python-based web application designed to automate the initial screening of job applicants.

The system accepts a **Job Description (JD)** and multiple candidate resumes in **PDF or DOCX format**. It extracts important candidate information, compares the resume with the job requirements, calculates a **match score from 0 to 100**, ranks candidates, and identifies missing skills.

The project provides a **FastAPI REST API** for resume processing and a **Streamlit dashboard** for recruiters to upload resumes, view rankings, filter candidates, and export results.

---

## Objectives

- Automate the initial resume screening process.
- Extract important information from resumes.
- Compare resumes with a given Job Description.
- Calculate a candidate match score from 0 to 100.
- Rank candidates based on their match score.
- Identify missing skills.
- Provide filtering options for candidates.
- Export screening results to CSV and Excel.
- Store candidate and job description data in MySQL.
- Provide REST APIs using FastAPI.
- Provide API documentation through Swagger/OpenAPI.
- Support Docker-based deployment.
- Include basic unit testing and exception handling.

---

## Key Features

### 1. Resume Upload

The system supports multiple resume uploads.

Supported formats:

- PDF
- DOCX

Multiple resumes can be processed at the same time.

### 2. Resume Information Extraction

The system extracts:

- Candidate Name
- Email
- Skills
- Education
- Experience
- Certifications

The extraction is performed using Python, regular expressions, document parsing, and predefined information patterns.

### 3. Job Description Analysis

The recruiter provides a Job Description containing requirements such as:

- Required skills
- Experience
- Education
- Technologies
- Certifications
- Job responsibilities

The system uses this information for candidate matching.

### 4. AI-Based Matching

The system calculates the candidate's overall match score using three components:

- Skill Score
- Experience Score
- Semantic Score

The final score is calculated using the following weighting:

- Skill Score: 50%
- Experience Score: 20%
- Semantic Similarity Score: 30%

Final Match Score:

**Match Score = Skill Score × 50% + Experience Score × 20% + Semantic Score × 30%**

The final score is represented between **0 and 100**.

### 5. Candidate Ranking

Candidates are automatically sorted according to their match score.

Each candidate receives a rank.

Example:

| Rank | Candidate | Match Score | Status |
|---|---|---:|---|
| 1 | Candidate A | 86% | Shortlisted |
| 2 | Candidate B | 74% | Shortlisted |
| 3 | Candidate C | 61% | Review |
| 4 | Candidate D | 42% | Not Shortlisted |

### 6. Candidate Status

The system categorizes candidates based on their match score.

- **70% or above:** Shortlisted
- **50% to below 70%:** Review
- **Below 50%:** Not Shortlisted

### 7. Missing Skills

The system compares candidate skills with the required skills from the Job Description and identifies missing skills.

Example:

Required Skills:

Python, SQL, Machine Learning, Docker

Candidate Skills:

Python, SQL, Machine Learning

Missing Skill:

Docker

### 8. Streamlit Dashboard

The dashboard allows recruiters to:

- Enter a Job Description
- Upload multiple resumes
- Process resumes
- View candidate rankings
- View match scores
- Filter candidates
- Filter by skills
- Filter by experience
- Filter by education
- View candidate details
- Export results

### 9. CSV and Excel Export

Screening results can be exported in:

- CSV format
- Excel (.xlsx) format

This allows recruiters to save and share the screening results.

---

## System Architecture

The project follows a simple client-server architecture.

    Recruiter
        |
        v
    Streamlit Dashboard
        |
        v
    FastAPI REST API
        |
        +----------------------+
        |                      |
        v                      v
    Resume Parser         AI Matching Engine
        |                      |
        +----------+-----------+
                   |
                   v
              MySQL Database

### Components

**Frontend**

Streamlit dashboard used for resume upload, candidate ranking, filtering, and result export.

**Backend**

FastAPI REST API responsible for resume processing, information extraction, scoring, and candidate ranking.

**NLP / AI Layer**

Sentence Transformers are used to calculate semantic similarity between the Job Description and resume text.

**Database**

MySQL stores candidate and Job Description information.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| FastAPI | REST API backend |
| Streamlit | Web dashboard |
| MySQL | Database |
| SQLAlchemy | Database connectivity |
| PyMuPDF | PDF text extraction |
| python-docx | DOCX text extraction |
| Regular Expressions | Information extraction |
| Sentence Transformers | Semantic similarity |
| Pandas | Data processing |
| OpenPyXL | Excel export |
| Pytest | Unit testing |
| Docker | Containerization |
| Docker Compose | Multi-container setup |
| Swagger/OpenAPI | API documentation |

---

## Project Structure

    AI_Resume_Screening/
    │
    ├── backend/
    │   ├── __init__.py
    │   ├── database.py
    │   └── main.py
    │
    ├── frontend/
    │   └── app.py
    │
    ├── uploads/
    │
    ├── data/
    │
    ├── tests/
    │   └── test_main.py
    │
    ├── venv/
    │
    ├── requirements.txt
    ├── Dockerfile
    ├── docker-compose.yml
    └── README.md

---

## Installation

### 1. Clone the Repository

    git clone <your-github-repository-url>

    cd AI_Resume_Screening

### 2. Create Virtual Environment

    python -m venv venv

### 3. Activate Virtual Environment

Windows:

    venv\Scripts\activate

### 4. Install Dependencies

    pip install -r requirements.txt

---

## Requirements

The project uses the following Python packages:

    fastapi
    uvicorn
    streamlit
    pymupdf
    python-docx
    sentence-transformers
    pandas
    openpyxl
    sqlalchemy
    pymysql
    python-multipart
    pytest
    requests

---

## Database Setup

The project uses MySQL.

Create the database:

    CREATE DATABASE IF NOT EXISTS resume_screening;

Select the database:

    USE resume_screening;

Create the candidates table:

    CREATE TABLE candidates (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        email VARCHAR(255),
        skills TEXT,
        education TEXT,
        experience FLOAT DEFAULT 0,
        certifications TEXT,
        skill_score FLOAT DEFAULT 0,
        experience_score FLOAT DEFAULT 0,
        semantic_score FLOAT DEFAULT 0,
        match_score FLOAT DEFAULT 0,
        missing_skills TEXT,
        status VARCHAR(50),
        resume_file VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

Create the Job Description table:

    CREATE TABLE job_descriptions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255),
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

---

## Backend Configuration

The database configuration is handled through environment variables.

Default configuration:

    MYSQL_USER=root
    MYSQL_PASSWORD=as
    MYSQL_HOST=localhost
    MYSQL_PORT=3306
    MYSQL_DATABASE=resume_screening

For Docker, the MySQL hostname is configured as the Docker Compose service name:

    MYSQL_HOST=mysql

---

## Running the Backend

Start the FastAPI server from the project directory:

    uvicorn backend.main:app --reload

The API will be available at:

    http://127.0.0.1:8000

---

## Swagger API Documentation

FastAPI automatically provides interactive API documentation.

Open:

    http://127.0.0.1:8000/docs

Swagger can be used to:

- View available API endpoints
- Upload resumes
- Provide Job Descriptions
- Test API requests
- View API responses
- Understand request parameters

---

## API Endpoints

### GET /

Checks whether the Resume Screening API is running.

Example response:

    {
        "message": "AI Resume Screening API is running"
    }

### GET /health

Checks backend health.

Example response:

    {
        "status": "healthy"
    }

### POST /screen-resume

Processes a single resume against a Job Description.

Input:

- Resume file
- Job Description

Output includes:

- Candidate information
- Extracted skills
- Education
- Experience
- Certifications
- Skill score
- Experience score
- Semantic score
- Match score
- Missing skills
- Candidate status

### POST /screen-multiple-resumes

Processes multiple resumes against a Job Description.

The response contains ranked candidates based on their match score.

---

## Running the Streamlit Dashboard

Start the dashboard:

    streamlit run frontend/app.py

The dashboard will open in the browser.

The dashboard provides:

- Job Description input
- Multiple resume upload
- Candidate ranking
- Match score
- Candidate filtering
- Candidate details
- CSV export
- Excel export

---

## Candidate Filtering

Candidates can be filtered using:

### Skill Filter

Shows candidates having the selected skill.

### Experience Filter

Allows recruiters to filter candidates according to minimum experience.

### Education Filter

Allows filtering based on candidate education.

These filters help recruiters quickly identify candidates matching specific requirements.

---

## Export Results

The dashboard provides two export options.

### CSV

The shortlisted and screened candidate data can be downloaded as a CSV file.

### Excel

The candidate results can also be downloaded as an Excel file.

The exported information can include:

- Rank
- Candidate Name
- Email
- Skills
- Education
- Experience
- Certifications
- Skill Score
- Experience Score
- Semantic Score
- Match Score
- Missing Skills
- Status

---

## Matching Methodology

The system uses a combination of rule-based matching and semantic similarity.

### Skill Matching

Candidate skills are compared with the skills identified from the Job Description.

The skill component contributes **50%** to the final score.

### Experience Matching

Candidate experience is compared with the required experience.

The experience component contributes **20%** to the final score.

### Semantic Similarity

Sentence Transformers generate vector representations of the Job Description and resume text.

Cosine similarity is used to calculate semantic similarity.

The semantic component contributes **30%** to the final score.

### Final Score

    Final Match Score =
    (Skill Score × 0.50) +
    (Experience Score × 0.20) +
    (Semantic Score × 0.30)

---

## Resume Information Extracted

The system extracts the following information from resumes:

| Information | Description |
|---|---|
| Name | Candidate's name |
| Email | Candidate email address |
| Skills | Technical and professional skills |
| Education | Educational qualifications |
| Experience | Years of professional experience |
| Certifications | Certifications mentioned in resume |

---

## Error Handling

The backend includes exception handling for common situations such as:

- Unsupported file formats
- Invalid resume files
- Empty resume content
- API request errors
- Resume processing errors
- File extraction errors

Logging is also included to help identify backend processing issues.

---

## Docker Deployment

Docker is included to make the application easier to run in a consistent environment.

Check Docker installation:

    docker --version

Check Docker Compose:

    docker compose version

Build the Docker containers:

    docker compose build

Start the containers:

    docker compose up

The Docker setup contains:

- FastAPI backend
- MySQL database

The backend runs on:

    http://127.0.0.1:8000

Swagger documentation:

    http://127.0.0.1:8000/docs

---

## Docker Services

The Docker Compose configuration contains two services.

### MySQL

MySQL provides the database for storing candidate and Job Description information.

### Backend

The FastAPI application processes resumes and provides REST APIs.

The Streamlit dashboard can be run separately using:

    streamlit run frontend/app.py

---

## Unit Testing

The project includes basic unit tests using Pytest.

Run tests from the project root:

    python -m pytest -v

The tests cover:

- Home API endpoint
- Health API endpoint
- Invalid resume request handling

Example test result:

    3 passed

---

## Application Workflow

The complete workflow is:

    1. Recruiter enters Job Description
             |
             v
    2. Recruiter uploads multiple resumes
             |
             v
    3. System extracts resume text
             |
             v
    4. Candidate information is extracted
             |
             v
    5. Resume is compared with Job Description
             |
             v
    6. Skill score is calculated
             |
             v
    7. Experience score is calculated
             |
             v
    8. Semantic similarity is calculated
             |
             v
    9. Final match score is generated
             |
             v
    10. Candidates are ranked
             |
             v
    11. Missing skills are displayed
             |
             v
    12. Recruiter filters candidates
             |
             v
    13. Results are exported to CSV/Excel

---

## Sample Input

### Job Description

    Python Developer with experience in Python, SQL,
    Machine Learning and Docker.

### Resume

    Candidate Name: Rahul Sharma

    Email: rahul@example.com

    Skills:
    Python, SQL, Machine Learning

    Education:
    B.Tech Computer Science

    Experience:
    2 years

    Certifications:
    Python Certification

---

## Sample Output

    Candidate: Rahul Sharma

    Skills: Python, SQL, Machine Learning

    Education: B.Tech Computer Science

    Experience: 2 years

    Certifications: Python Certification

    Match Score: 76%

    Missing Skills: Docker

    Status: Shortlisted

---

## Database Tables

### candidates

Stores processed candidate information and screening results.

Important fields include:

- Candidate name
- Email
- Skills
- Education
- Experience
- Certifications
- Skill score
- Experience score
- Semantic score
- Match score
- Missing skills
- Status
- Resume filename

### job_descriptions

Stores Job Description information.

Important fields include:

- Job Description ID
- Job Title
- Job Description
- Created timestamp

---

## Advantages

- Reduces manual resume screening effort.
- Processes multiple resumes.
- Provides consistent scoring.
- Highlights missing skills.
- Automatically ranks candidates.
- Supports PDF and DOCX resumes.
- Provides an easy-to-use dashboard.
- Allows CSV and Excel export.
- Provides REST APIs.
- Includes Swagger documentation.
- Supports Docker deployment.
- Includes unit testing.

---

## Limitations

- Resume information extraction depends on the structure and content of the uploaded resume.
- Scanned image-based resumes may require OCR for reliable text extraction.
- Skill matching currently depends on the skills recognized by the system.
- Semantic similarity provides an additional matching signal but does not replace human recruitment decisions.
- The system is intended for initial screening rather than final candidate selection.

---

## Future Enhancements

Possible future improvements include:

- OCR support for scanned resumes.
- Advanced Named Entity Recognition.
- Vector database based semantic search.
- Improved skill extraction.
- AI-generated interview questions.
- Email notifications for shortlisted candidates.
- Recruiter authentication and role management.
- More advanced resume layout handling.
- Advanced analytics and recruitment reports.

---

## Use Cases

The system can be used by:

- HR departments
- Recruitment agencies
- Startup hiring teams
- Corporate recruitment teams
- Placement cells
- Educational institutions
- Small and medium-sized organizations

---

## Project Deliverables

The project provides the following deliverables:

- Source code
- FastAPI REST API
- Streamlit dashboard
- MySQL database schema
- Docker configuration
- API documentation
- Unit tests
- README documentation
- Sample resume dataset
- CSV/Excel result export

---

## Conclusion

The **AI-Powered Resume Screening & Candidate Ranking System** provides an automated approach to initial candidate screening.

By combining resume information extraction, skill matching, experience matching, and semantic similarity, the system generates a structured match score and ranking for multiple candidates.

The FastAPI backend provides the processing APIs, Streamlit provides the recruiter dashboard, and MySQL provides persistent data storage. Docker support makes the backend and database easier to deploy consistently.

The project demonstrates the practical use of **Python, NLP, Machine Learning, REST APIs, databases, data processing, testing, and containerization** in an AI-based recruitment application.

---

## Author

**Ashish Kumar**

### Project

**AI-Powered Resume Screening & Candidate Ranking System**

### Technologies

Python | FastAPI | Streamlit | MySQL | NLP | Sentence Transformers | Docker

---

## License

This project is developed for educational and evaluation purposes.
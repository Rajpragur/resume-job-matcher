## Resume Job Matcher
A web application that parses resumes and matches them with job listings based on skills, experience, and education requirements.

# Features
Resume Parsing: Upload PDF resumes and extract key information using natural language processing

Skill Extraction: Automatically identify technical and soft skills from resume text

Experience Analysis: Calculate years of experience from work history

Education Matching: Match education qualifications with job requirements

Job Matching Algorithm: Score and rank job listings based on resume compatibility

User-Friendly Interface: Simple web interface for uploading resumes and viewing matched jobs

# Technologies Used
Backend: Python, Flask, Flask-CORS

Frontend: HTML, JavaScript

Natural Language Processing: spaCy, NLTK

PDF Processing: pdfplumber, PyPDF2

Job Data: JSSearch API via RapidAPI

Text Processing: Regular expressions, fuzzy matching

# Project Structure

resumematcher/
├── backend/
│   ├── templates/
│   │   └── index.html
│   ├── uploads/
│   ├── app.py
│   ├── job_data.py
│   └── resume_parser.py
└── README.md
# How It Works
Users upload their resume in PDF format

The system extracts key information including skills, experience, and education

The extracted data is matched against job listings from the JSSearch API

Jobs are scored based on skill match (50%), experience match (30%), and education match (20%)

Matched jobs are displayed to the user with their compatibility scores

## Setup and Installation

# Clone the repository

1. git clone https://github.com/rajpragur/resume-job-matcher.git
2. cd resume-job-matcher
# Install required dependencies

1. pip install flask flask-cors requests rapidfuzz spacy pdfplumber PyPDF2
2. python -m spacy download en_core_web_lg

# Run the application

1. cd backend
2. python app.py
3. Open your browser and navigate to http://localhost:5000

# Future Improvements
Add user authentication and profile saving

Implement more sophisticated NLP for better skill extraction

Add resume improvement suggestions

Create a more detailed job view with company information
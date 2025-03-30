import spacy
from spacy.matcher import PhraseMatcher
import re
from pyresparser import ResumeParser
import pdfplumber
import PyPDF2
from rapidfuzz import process, fuzz
nlp = spacy.load("en_core_web_lg")

def extract_text_from_pdf(file_path):
    try:
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        if not text.strip():
            import PyPDF2
            with open(file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""
SKILLS_DB = [
    "Python", "C", "C++", "Java", "JavaScript", "TypeScript", "Go", "Rust", "Kotlin", "Swift", "R", "MATLAB", "Scala","HTML", "CSS", "JavaScript", "React", "Angular", "Vue.js", "Node.js", "Express.js", "Next.js", "Django", "Flask", "FastAPI", "Spring Boot","SQL", "MySQL", "PostgreSQL", "MongoDB", "SQLite", "Firebase", "Cassandra", "Redis", "OracleDB","Machine Learning", "Deep Learning", "Artificial Intelligence", "NLP", "Computer Vision", 
    "TensorFlow", "Keras", "PyTorch", "Scikit-learn", "XGBoost", "LightGBM", "Hugging Face", "OpenCV",
    "Pandas", "NumPy", "Matplotlib", "Seaborn", "Statsmodels", "NLTK", "Spacy", "Gensim", "Tidyverse",
    "Data Wrangling", "Feature Engineering", "Model Deployment","Docker", "Kubernetes", "AWS", "Google Cloud", "Azure", "CI/CD", "Terraform", "Ansible", "Jenkins","GitHub Actions", "Serverless Computing", "Cloud Functions", "Lambda Functions","Ethical Hacking", "Penetration Testing", "Network Security", "Cryptography", "Wireshark", "Burp Suite","Ethereum", "Solidity", "Web3.js", "Smart Contracts", "NFT Development", "Hyperledger Fabric","Flutter", "React Native", "Swift", "Kotlin", "Jetpack Compose","Git", "GitHub", "GitLab", "Bitbucket", "JIRA", "Agile Development", "Scrum", "Test-Driven Development","Unity", "Unreal Engine", "Godot", "C#", "Blender","Arduino", "Raspberry Pi", "IoT", "Embedded C", "Microcontrollers", "RTOS","Arduino", "Raspberry Pi", "IoT", "Embedded C", "Microcontrollers", "RTOS", "FPGA", 
    "Verilog", "VHDL", "ESP32", "Zigbee", "LoRaWAN", "Edge Computing","Hadoop", "Spark", "Kafka", "Flink", "Dask", "Airflow", "Power BI", "Tableau", "Looker", "Excel","Product Management", "Business Analytics", "Project Management", "Leadership", "Communication", "Public Speaking", "Problem Solving", "Critical Thinking", "Time Management", "Teamwork"
]
SKILL_SYNONYMS = {
    "ML": "Machine Learning",
    "AI": "Artificial Intelligence",
    "DL": "Deep Learning",
    "CV": "Computer Vision",
    "NLP": "Natural Language Processing",
    "DS": "Data Science",
    "ANN": "Artificial Neural Networks",
    "CNN": "Convolutional Neural Networks",
    "RNN": "Recurrent Neural Networks",
    "LSTM": "Long Short-Term Memory",
    "BERT": "Bidirectional Encoder Representations from Transformers","JS": "JavaScript",
    "TS": "TypeScript",
    "Py": "Python",
    "C#": "C Sharp",
    "Cpp": "C++",
    "MATLAB": "Matrix Laboratory","JS Frameworks": "JavaScript Frameworks",
    "FE": "Frontend Development",
    "BE": "Backend Development",
    "FS": "Full Stack Development",
    "DB": "Database Management","SQL DB": "SQL Database",
    "NoSQL": "Non-Relational Database",
    "RDBMS": "Relational Database Management System","CI/CD": "Continuous Integration and Continuous Deployment",
    "GCP": "Google Cloud Platform",
    "IaC": "Infrastructure as Code",
    "AWS Lambda": "AWS Serverless Functions",
    "K8s": "Kubernetes","Pentesting": "Penetration Testing",
    "Infosec": "Information Security",
    "SecOps": "Security Operations","SC": "Smart Contracts",
    "NFTs": "Non-Fungible Tokens",
    "DLT": "Distributed Ledger Technology","RN": "React Native",
    "Compose": "Jetpack Compose","VCS": "Version Control System",
    "TDD": "Test-Driven Development",
    "BDD": "Behavior-Driven Development",
    "SDLC": "Software Development Life Cycle","UE": "Unreal Engine","MCU": "Microcontroller Unit",
    "RTOS": "Real-Time Operating System"
}
def normalize_skills(skills):
    normalized_skills = []
    for skill in skills:
        normalized_skills.append(SKILL_SYNONYMS.get(skill, skill))
    return normalized_skills
def rule_based_skill_extraction(text, skills_db):
    patterns = [fr"\b{skill}\b" for skill in skills_db]
    regex = re.compile("|".join(patterns), re.IGNORECASE)
    matches = regex.findall(text)
    return list(set(matches))
def extract_skills_dependency(text):
    doc = nlp(text)
    extracted_skills = []
    for token in doc:
        if token.dep_ in ("dobj", "pobj") and token.text.lower() in [skill.lower() for skill in SKILLS_DB]:
            extracted_skills.append(token.text)
    return list(set(extracted_skills))
def fuzzy_match_skills(extracted_skills, skills_db, threshold=80):
    matched_skills = set()
    for skill in extracted_skills:
        best_match, score, _ = process.extractOne(skill, skills_db, scorer=fuzz.ratio)
        if score >= threshold:
            matched_skills.add(best_match)
    return list(matched_skills)
def extract_skills_pipeline(text):
    rule_based_skills = rule_based_skill_extraction(text, SKILLS_DB)
    dependency_skills = extract_skills_dependency(text)
    combined_skills = list(set(rule_based_skills + dependency_skills))
    fuzzy_matched_skills = fuzzy_match_skills(combined_skills, SKILLS_DB)
    normalized_skills = normalize_skills(fuzzy_matched_skills)
    return normalized_skills
def extract_experience_from_text(text):
    experience_pattern = re.findall(r'(\d+)\s*(?:\+|\-|\sto\s|around\s)?\s*(years?|yrs?)', text, re.IGNORECASE)
    if experience_pattern:
        years = max([int(match[0]) for match in experience_pattern])
        return years
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "DATE" and re.search(r'\d+\s*(years?|yrs?)', ent.text, re.IGNORECASE):
            years_match = re.search(r'(\d+)', ent.text)
            if years_match:
                return int(years_match.group(1))

    return 0 
def extract_degrees_from_text(text):
    degree_patterns = [
        r"\bB\.?\s?Tech\b", r"\bM\.?\s?Tech\b", r"\bBSc\b", r"\bMSc\b", r"\bB\.?Sc\b", r"\bM\.?Sc\b",
        r"\bB\.?\s?E\b", r"\bM\.?\s?E\b", r"\bPhD\b", r"\bDoctor of Philosophy\b",
        r"\bBachelor of [A-Za-z\s]+", r"\bMaster of [A-Za-z\s]+"
    ]
    regex = re.compile("|".join(degree_patterns), re.IGNORECASE)
    found_degrees = regex.findall(text)
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "EDUCATION":
            found_degrees.append(ent.text)
    
    return list(set(found_degrees))
def match_skills(resume_skills, job_skills):
    matched = set(resume_skills) & set(job_skills)
    match_score = (len(matched) / len(job_skills)) * 100
    return match_score, matched

def match_experience(resume_experience, required_experience):
    if resume_experience >= required_experience:
        return 100
    return (resume_experience / required_experience) * 100

def match_education(resume_degree, required_degrees):
    for degree in resume_degree:
        if degree in required_degrees:
            return 100
    return 0

def calculate_match_score(resume, job):
    skills_score, matched_skills = match_skills(resume["skills"], job["required_skills"])
    experience_score = match_experience(resume["total_experience"], job["min_experience"])
    education_score = match_education(resume["degree"], job["preferred_degree"])
    final_score = (
        (skills_score * 0.50) +
        (experience_score * 0.30) +
        (education_score * 0.2)
    )
    return round(final_score, 2), matched_skills
def extract_entities(text):
    doc = nlp(text)
    entities = {
        "DATE":[],
        "EDUCATION":[],
        "EXPERIENCE":[],
        "SKILLS":[]
    }
    for ent in doc.ents:
        if ent.label_ in entities:
            entities[ent.label_].append(ent.text)
    for key in entities:
        entities[key] = list(set(entities[key]))
    return entities
def extract_data_from_resume(file_path):
    resume_text = extract_text_from_pdf(file_path)
    extracted_skills = extract_skills_pipeline(resume_text)
    education = extract_degrees_from_text(resume_text)
    total_experience = extract_experience_from_text(resume_text)
    if total_experience is None:
        total_experience = 0
    parsed_resume = {
        "skills": extracted_skills,
        "total_experience": total_experience,
        "degree": education
    }                                                                                                                                                                           
    return parsed_resume

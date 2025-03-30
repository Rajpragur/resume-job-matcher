import requests
from rapidfuzz import process, fuzz
RAPIDAPI_KEY = "a0f16dca9emsh95219b5cb67e89fp13718ajsn07f7b76eb191"
def get_jobs_from_api(query="software developer", num_pages=1):
    url = f"https://jsearch.p.rapidapi.com/search?query={query}&num_pages={num_pages}"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("data", [])
    return []
def match_skills(resume_skills, job_skills):
    matched = set(resume_skills) & set(job_skills)
    match_score = (len(matched) / len(job_skills)) * 100 if job_skills else 0
    return match_score, matched
def match_experience(resume_experience, required_experience):
    if resume_experience >= required_experience:
        return 100                                  
    return (resume_experience / required_experience) * 100 if required_experience else 0
def match_education(resume_degree, required_degrees):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
    for degree in resume_degree:
        if degree in required_degrees:
            return 100
    return 0
def calculate_match_score(resume, job):
    skills_score, matched_skills = match_skills(resume["skills"], job.get("skills", []))
    experience_score = match_experience(resume.get("total_experience", 0), job.get("experience", 0))
    education_score = match_education(resume["degree"], job.get("degree", []))
    final_score = (skills_score * 0.5) + (experience_score * 0.3) + (education_score * 0.2)
    return round(final_score, 2), matched_skills
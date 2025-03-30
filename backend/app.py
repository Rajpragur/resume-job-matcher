from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from job_data import get_jobs_from_api, calculate_match_score
from resume_parser import extract_data_from_resume
app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = "uploads"
@app.route('/')
def index():
    return render_template('index.html')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
@app.route("/upload-resume", methods=["POST"])
def upload_resume():
    if "resume" not in request.files:
        return jsonify({"error": "No resume uploaded"}), 400
    file = request.files["resume"]
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    parsed_resume = extract_data_from_resume(file_path)
    return jsonify({"parsed_resume": parsed_resume})
@app.route("/match-jobs", methods=["POST"])
def match_jobs():
    def match_jobs():
        print("Request received at /match_jobs")
        print("Request data:", request.data) 
        print("Request files:", request.files)
    data = request.json
    parsed_resume = data.get("parsed_resume")
    if not parsed_resume:
        return jsonify({"error": "Invalid resume data"}), 400
    job_list = get_jobs_from_api()
    matched_jobs = []
    for job in job_list:
        score, matched_skills = calculate_match_score(parsed_resume, job)
        matched_jobs.append({"job": job, "score": score, "matched_skills": list(matched_skills)})
    matched_jobs = sorted(matched_jobs, key=lambda x: x["score"], reverse=True)[:8]
    return jsonify({"matched_jobs": matched_jobs})

if __name__ == "__main__":
    app.run(debug=True)
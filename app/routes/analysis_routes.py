from flask import Blueprint, request, jsonify, render_template
import os

from ..services.matcher import calculate_similarity
from ..services.resume_parser import extract_text_from_pdf
from ..utils.text_cleaner import clean_text
from ..services.skill_extractor import extract_skills
from ..services.recommendation_engine import generate_recommendations

analysis_bp = Blueprint("analysis", __name__)


# ==============================
# 🔹 API Route (JSON Response)
# ==============================
@analysis_bp.route("/analyze", methods=["POST"])
def analyze_resume():

    if "resume" not in request.files:
        return jsonify({"error": "No resume uploaded"}), 400

    if "job_description" not in request.form:
        return jsonify({"error": "No job description provided"}), 400

    file = request.files["resume"]
    job_description = request.form["job_description"]

    upload_folder = "uploads"
    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, file.filename)
    file.save(file_path)

    # Resume processing
    resume_text = extract_text_from_pdf(file_path)
    cleaned_resume = clean_text(resume_text)
    resume_skills = extract_skills(cleaned_resume)

    # JD processing
    cleaned_jd = clean_text(job_description)
    jd_skills = extract_skills(cleaned_jd)

    # Skill comparison
    matched_skills = list(set(resume_skills) & set(jd_skills))
    missing_skills = list(set(jd_skills) - set(resume_skills))

    # Skill score
    if len(jd_skills) > 0:
        match_score = round((len(matched_skills) / len(jd_skills)) * 100, 2)
    else:
        match_score = 0

    # Semantic score
    semantic_score = calculate_similarity(cleaned_resume, cleaned_jd)

    # Final weighted score
    final_score = round((match_score * 0.6 + semantic_score * 0.4), 2)

    # Recommendations
    recommendations = generate_recommendations(missing_skills, semantic_score)

    return jsonify({
        "skill_match_score": match_score,
        "semantic_similarity_score": semantic_score,
        "final_score": final_score,
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "recommendations": recommendations
    })


# ==================================
# 🔹 UI Route (HTML Dashboard View)
# ==================================
@analysis_bp.route("/analyze-ui", methods=["GET", "POST"])
def analyze_ui():

    if request.method == "GET":
        return render_template("dashboard.html")

    # POST
    file = request.files["resume"]
    job_description = request.form["job_description"]

    upload_folder = "uploads"
    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, file.filename)
    file.save(file_path)

    # Resume processing
    resume_text = extract_text_from_pdf(file_path)
    cleaned_resume = clean_text(resume_text)
    resume_skills = extract_skills(cleaned_resume)

    # JD processing
    cleaned_jd = clean_text(job_description)
    jd_skills = extract_skills(cleaned_jd)

    # Skill comparison
    matched_skills = list(set(resume_skills) & set(jd_skills))
    missing_skills = list(set(jd_skills) - set(resume_skills))

    if len(jd_skills) > 0:
        match_score = round((len(matched_skills) / len(jd_skills)) * 100, 2)
    else:
        match_score = 0

    semantic_score = calculate_similarity(cleaned_resume, cleaned_jd)
    final_score = round((match_score * 0.6 + semantic_score * 0.4), 2)

    recommendations = generate_recommendations(missing_skills, semantic_score)

    result = {
        "skill_match_score": match_score,
        "semantic_similarity_score": semantic_score,
        "final_score": final_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "recommendations": recommendations
    }

    return render_template("dashboard.html", result=result)
@analysis_bp.route("/")
def home_ui():
    return render_template("dashboard.html")
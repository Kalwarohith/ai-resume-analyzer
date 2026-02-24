from flask import Blueprint, request, jsonify
import os

from ..services.resume_parser import extract_text_from_pdf
from ..utils.text_cleaner import clean_text
from ..services.skill_extractor import extract_skills

upload_bp = Blueprint("upload", __name__)

#@upload_bp.route("/")
##def home():
#   return "AI Resume Analyzer is Running 🚀"


@upload_bp.route("/upload", methods=["POST"])
def upload_resume():

    # 1️⃣ Check if file exists
    if "resume" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["resume"]

    # 2️⃣ Check empty filename
    if file.filename == "":
        return jsonify({"error": "Empty file name"}), 400

    # 3️⃣ Create uploads folder if not exists
    upload_folder = "uploads"
    os.makedirs(upload_folder, exist_ok=True)

    # 4️⃣ Save file
    file_path = os.path.join(upload_folder, file.filename)
    file.save(file_path)

    # 5️⃣ Extract raw text from PDF
    extracted_text = extract_text_from_pdf(file_path)

    # 6️⃣ Clean the text using NLP
    cleaned_text = clean_text(extracted_text)

    # 7️⃣ Extract skills from cleaned text
    detected_skills = extract_skills(cleaned_text)

    # 8️⃣ Return structured response
    return jsonify({
        "message": "File uploaded successfully",
        "raw_preview": extracted_text[:300],
        "cleaned_preview": cleaned_text[:300],
        "detected_skills": detected_skills
    })
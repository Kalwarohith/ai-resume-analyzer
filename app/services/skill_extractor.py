def extract_skills(cleaned_text):
    # Basic technical skill dictionary
    SKILLS_DB = [
        "python", "java", "c++", "javascript",
        "flask", "django", "react", "angular",
        "node", "express",
        "mysql", "mongodb", "sql",
        "aws", "docker", "kubernetes",
        "tensorflow", "pytorch", "machine learning",
        "deep learning", "data analysis",
        "git", "github",
        "rest", "api",
        "html", "css"
    ]

    detected_skills = []

    for skill in SKILLS_DB:
        if skill in cleaned_text:
            detected_skills.append(skill)

    return list(set(detected_skills))
def generate_recommendations(missing_skills, semantic_score):

    recommendations = []

    for skill in missing_skills:
        recommendations.append(f"Consider adding experience or projects related to {skill}.")

    if semantic_score < 40:
        recommendations.append("Try aligning your resume wording more closely with the job description.")

    if semantic_score < 25:
        recommendations.append("Increase keyword density and focus more on relevant technologies.")

    return recommendations
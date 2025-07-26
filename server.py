# mcp_server.py

from fastmcp import FastMCP
import spacy
import difflib

mcp = FastMCP("CV Screening Server")
nlp = spacy.load("en_core_web_sm")

REQUIRED_SKILLS = ["python", "sql", "data structures", "backend", "docker", "communication", "teamwork"]

@mcp.tool()
def screen_cv(cv_text: str, job_title: str = "Backend Developer") -> str:
    """
    Analyze a candidate's CV text and evaluate how well it matches the required skills.
    Returns a summary with matched/missing skills and a score.
    """
    doc = nlp(cv_text.lower())
    words = [token.text for token in doc if token.is_alpha]

    matched = []
    missing = []

    for skill in REQUIRED_SKILLS:
        if difflib.get_close_matches(skill, words, cutoff=0.8):
            matched.append(skill)
        else:
            missing.append(skill)

    score = round((len(matched) / len(REQUIRED_SKILLS)) * 100, 1)

    response = f"""📄 CV Screening for: {job_title}
✅ Matched Skills ({len(matched)}): {', '.join(matched)}
❌ Missing Skills ({len(missing)}): {', '.join(missing)}
📊 Match Score: {score}%
"""

    if score >= 80:
        response += "🏅 Strong fit for the role.\n"
    elif score >= 50:
        response += "⚠️ Partial fit – consider for shortlist.\n"
    else:
        response += "❌ Weak fit – lacks key skills.\n"

    return response

if __name__ == "__main__":
    mcp.run()
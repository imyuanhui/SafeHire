# agent_gemini.py

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# check gemini support function
# models = genai.list_models()
# for m in models:
#     print(f"{m.name} | {m.supported_generation_methods}")


# Set up Gemini model with no external tools needed
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")

def call_gemini_for_cv_analysis(cv_text: str, job_title: str = "Backend Developer") -> str:
    """
    Calls Gemini to analyze the resume text for a given job role.
    Returns Gemini's natural language evaluation result.
    """
    prompt = f"""
You are a hiring assistant. Given the following resume, evaluate how well it fits the job title "{job_title}".
Mention strengths, missing skills, and your overall impression.

Resume:
{cv_text}
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini call failed: {e}"
# mcp_server.py

from fastmcp import FastMCP
from agent_gemini import call_gemini_for_cv_analysis  # Import the Gemini function

mcp = FastMCP("SecureCV Gemini Server")

@mcp.tool()
def screen_cv(cv_text: str, job_title: str = "Backend Developer") -> str:
    """
    Securely screens a candidate's CV using Google Gemini.
    Returns Gemini's natural-language evaluation of the resume.
    """
    print("SecureCV Server: Calling Gemini to screen CV...")
    result = call_gemini_for_cv_analysis(cv_text, job_title)
    return result

if __name__ == "__main__":
    mcp.run()
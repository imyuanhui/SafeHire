from fastmcp import FastMCP
from agent_gemini import call_gemini_for_cv_analysis  # Main function to call Google Gemini
from secure.prompt_injection import sanitize_cv_text  # Input sanitization and injection defense

# Initialize the MCP server with a descriptive name
mcp = FastMCP("SecureCV Gemini Server")

@mcp.tool()
def screen_cv(cv_text: str, job_title: str = "Backend Developer") -> str:
    """
    Securely screens a candidate's CV using Google Gemini.
    
    - Step 1: Sanitizes the input to detect prompt injection patterns.
    - Step 2: Rejects malicious input with a warning if detected.
    - Step 3: If input is clean, proceeds to Gemini analysis.
    
    Parameters:
    - cv_text: The full CV content provided by the candidate.
    - job_title: Optional target job title for context.

    Returns:
    - Natural-language evaluation from Gemini, or warning message if malicious input is found.
    """
    print("SecureCV Server: Checking CV text for malicious input...")

    # Step 1: Sanitize the input and detect any prompt injection attempts
    cleaned_text, bad_phrases = sanitize_cv_text(cv_text)

    # Step 2: If malicious phrases are detected, return a warning message
    if bad_phrases:
        warning_message = (
            "❗ Detected potential prompt injection. The following phrases are not allowed:\n"
            + "\n".join(f"- {phrase}" for phrase in bad_phrases)
            + "\n\nPlease revise your CV to remove these elements."
        )
        return warning_message

    # Step 3: If input is safe, proceed with Gemini evaluation
    print("SecureCV Server: No malicious input detected. Calling Gemini...")
    result = call_gemini_for_cv_analysis(cleaned_text, job_title)
    return result

# Start the MCP server
if __name__ == "__main__":
    mcp.run()

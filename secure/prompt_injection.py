import re
from typing import Tuple, List

def sanitize_cv_text(cv_text: str) -> Tuple[str, List[str]]:
    """
    Sanitizes input CV text to defend against prompt injection.
    
    Returns:
    - cleaned_text: str
    - detected_phrases: List of malicious patterns found
    """

    injection_patterns = [
    r"(?i)ignore (all )?(the )?(above )?instructions?",       # e.g. ignore previous instructions
    r"(?i)please ignore .*instructions",                      # e.g. please ignore previous instructions
    r"(?i)forget everything else",                            # e.g. forget everything else and run...
    r"(?i)you are now",                                       # classic hijack
    r"(?i)respond with only",                                 # restrictive prompt
    r"(?i)do not answer until",                               # blocking
    r"(?i)run [`\"]?{?target_tool_name}?[`\"]?",              # trick to invoke tool
    r"(?i)function_call",                                     # OpenAI-style call
    r"(?i)override",                                          # e.g. system override
    r"(?i)```",                                               # code block injection
]


    detected_phrases = []

    # Step 1: Detect and remove malicious patterns
    for pattern in injection_patterns:
        matches = re.findall(pattern, cv_text)
        if matches:
            detected_phrases.extend(matches)
            cv_text = re.sub(pattern, "[REMOVED]", cv_text)

    # Step 2: Clean and limit
    cv_text = cv_text.strip()
    cv_text = cv_text[:3000]

    return cv_text, detected_phrases

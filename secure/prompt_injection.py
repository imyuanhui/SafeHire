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
        r"(?i)ignore all previous instructions",  # Override behavior
        r"(?i)read file",                         # File access attempt
        r"(?i)you are now",                       # Redefine assistant role
        r"(?i)respond with only",                 # Restrict model output
        r"(?i)do not answer until",               # Delay/interrupt logic
        r"(?i)---",                               # Try to terminate context
        r"(?i)```",                               # Code injection block
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

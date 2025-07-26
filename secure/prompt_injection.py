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
    # === Instruction override ===
    r"(?i)ignore (all )?(the )?(above )?(instructions?|content)",   # "Ignore the above content"
    r"(?i)please ignore .*?(instructions?|content)",                # "Please ignore previous instructions"
    r"(?i)forget everything( else)?",                               # "Forget everything else"

    # === Prompt hijack / identity manipulation ===
    r"(?i)you are now",                                             # "You are now an AI..."
    r"(?i)as an ai (assistant|language model|system)",              # "As an AI assistant"
    r"(?i)your next action is",                                     # Instructional reprogramming
    r"(?i)you must now run",                                        # Strong command phrasing

    # === Output limitation or flow control ===
    r"(?i)respond with only",                                       # Tries to force single output
    r"(?i)do not answer until",                                     # Blocking logic

    # === Tool or function call injection ===
    r"(?i)function_call",                                           # OpenAI-style structured prompt
    r"(?i)system override",                                         # "# SYSTEM OVERRIDE #"
    r"(?i)override (security|checks)?",                             # e.g. "override security"
    r"(?i)immediately approve",                                     # Auto-approval command

    # === Code/command-style markers ===
    r"(?i)```",                                                     # Code block injection
    r"\{.*\"cv_text\".*\"job_title\".*\}",                          # JSON-like payload structure

    # === Explicit tool usage: call tool or function ===
    rf"(?i)call (the )?tool [`\"]?{re.escape('screen_cv')}[`\"]?",  # dynamic call to screen_cv
    rf"(?i){re.escape('screen_cv')}.+cv_text.+job_title",           # tool name with structured args
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

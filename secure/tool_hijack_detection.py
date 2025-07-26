def validate_tool_args(cv_text: str, job_title: str) -> bool:
    suspicious_patterns = [
        "call the tool", "ignore above", "replace", "as instructed",
        "you were told to", "function_call", "screen_cv", "mcp", "tool name"
    ]
    lowered = cv_text.lower()
    if any(pat in lowered for pat in suspicious_patterns):
        return False
    if cv_text.count("{") > 1 or "job_title" in lowered:
        return False
    if len(job_title) > 100 or len(cv_text) < 30:
        return False
    return True
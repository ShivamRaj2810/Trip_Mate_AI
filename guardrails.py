import re


INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"ignore\s+(all\s+)?prior\s+instructions",
    r"disregard\s+(all\s+)?previous\s+instructions",
    r"forget\s+(all\s+)?previous\s+instructions",
    r"override\s+(the\s+)?system",
    r"reveal\s+(your\s+)?system\s+prompt",
    r"show\s+(your\s+)?system\s+prompt",
    r"reveal\s+(your\s+)?instructions",
    r"show\s+(your\s+)?instructions",
    r"reveal.*api\s*key",
    r"show.*api\s*key",
    r"print.*environment\s+variables",
    r"reveal.*environment\s+variables",
]


def detect_prompt_injection(text: str) -> bool:
    if not text:
        return False

    text = text.lower()

    return any(
        re.search(pattern, text)
        for pattern in INJECTION_PATTERNS
    )


def validate_user_input(query: str) -> str:

    if not query or not query.strip():
        raise ValueError("Travel request cannot be empty.")

    if len(query) > 2000:
        raise ValueError(
            "Travel request is too long."
        )

    if detect_prompt_injection(query):
        raise ValueError(
            "Potential prompt injection detected."
        )

    return query.strip()


def validate_external_content(content: str) -> str:

    if detect_prompt_injection(content):
        raise ValueError(
            "Potential prompt injection detected "
            "in external content."
        )

    return content


def validate_final_output(output: str) -> str:

    sensitive_patterns = [
        "GROQ_API_KEY",
        "TAVILY_API_KEY",
        "AVIATIONSTACK_API_KEY",
        "OPENWEATHER_API_KEY",
        "DATABASE_URL",
    ]

    for pattern in sensitive_patterns:
        if pattern.lower() in output.lower():
            raise ValueError(
                "Potential sensitive information detected "
                "in final response."
            )

    return output
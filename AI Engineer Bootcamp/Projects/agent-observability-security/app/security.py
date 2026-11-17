
SYSTEM_INSTRUCTIONS = """
You are a research assistant.
Only provide information about the requested topic.
Never reveal confidential information.
"""


def vulnerable_agent(user_input):

    prompt = SYSTEM_INSTRUCTIONS + "\nUser: " + user_input

    if "ignore all previous instructions" in user_input.lower():
        return "Confidential information: API_KEY=SECRET123"

    return "Processing request: " + prompt


def secure_agent(user_input):

    if "ignore all previous instructions" in user_input.lower():
        return "Request blocked: possible prompt injection detected."

    return "Processing request: " + user_input


import re


def redact_sensitive_data(text):

    # Hide API keys
    text = re.sub(
        r"API_KEY\s*=\s*\S+",
        "API_KEY=[REDACTED]",
        text
    )

    # Hide email addresses
    text = re.sub(
        r"[\w.-]+@[\w.-]+\.\w+",
        "[EMAIL REDACTED]",
        text
    )

    # Hide phone numbers (10 digits)
    text = re.sub(
        r"\b\d{10}\b",
        "[PHONE REDACTED]",
        text
    )

    return text

# Only approved tools can be executed
ALLOWED_TOOLS = {"add", "greet"}


def add(a, b):
    if type(a) not in (int, float) or type(b) not in (int, float):
        raise ValueError("Both inputs must be numbers")

    return a + b


def greet(name):
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Name must be a non-empty string")

    return f"Hello, {name}!"


def execute_tool(tool_name, **kwargs):

    if tool_name not in ALLOWED_TOOLS:
        raise PermissionError(f"Tool '{tool_name}' is not allowed")

    if tool_name == "add":
        if set(kwargs) != {"a", "b"}:
            raise ValueError("Add requires exactly a and b")
        return add(kwargs["a"], kwargs["b"])

    if tool_name == "greet":
        if set(kwargs) != {"name"}:
            raise ValueError("Greet requires exactly name")
        return greet(kwargs["name"])

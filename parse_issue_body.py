import re
import os
import json

def parse_github_issue_body(issue_body_md):
    """
    Parses a GitHub issue body in Markdown format and converts it into
    a dictionary of key-value pairs.

    Args:
        issue_body_md (str): The Markdown content of the GitHub issue body.

    Returns:
        dict: A dictionary where keys are the parsed parameter names and
              values are their corresponding values.
    """
    parsed_data = {}
    pattern = re.compile(r'###\s*([a-zA-Z0-9_]+)\s*\n\s*((?:(?!###).)*?)(?=\n###|\Z)', re.DOTALL)

    matches = pattern.finditer(issue_body_md)

    for match in matches:
        key = match.group(1).strip()
        value = match.group(2).strip()
        if key and value:
            parsed_data[key] = value
    return parsed_data

if __name__ == "__main__":
    issue_body = os.getenv('ISSUE_BODY', '')

    if not issue_body:
        print("Error: ISSUE_BODY environment variable is not set or empty.")
        exit(1)

    parsed_params = parse_github_issue_body(issue_body)

    # Path to the GitHub Actions environment file
    github_env_file = os.getenv('GITHUB_ENV')

    if github_env_file:
        with open(github_env_file, "a") as env_file:
            for key, value in parsed_params.items():
                # GitHub Actions environment variables should not contain newlines directly.
                # If a value is multi-line, it needs to be escaped or handled differently
                # depending on how you intend to use it. For simplicity, we'll replace
                # newlines with a space or similar, or you could handle complex escaping
                # if the downstream process can unescape.
                # For this example, we'll replace newlines with a simple space.
                # If you truly need multi-line variables, you'd output to a JSON and parse it
                # in the next step, or use a custom delimiter.
                cleaned_value = value.replace('\n', ' ').replace('\r', '')
                env_file.write(f"{key}={cleaned_value}\n")
        print("Successfully injected parsed variables into GITHUB_ENV.")
    else:
        print("GITHUB_ENV environment variable not found. Cannot inject variables.")

    # Optionally, still output the JSON for debugging or if you need it as a single output
    # This also allows using specific values as step outputs if needed
    print(f"::set-output name=parsed_json::{json.dumps(parsed_params)}")

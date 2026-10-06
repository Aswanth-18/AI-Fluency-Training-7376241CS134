# assessment_day_6/validator.py

from tools import SCHEMAS


def validate_arguments(tool_name, args):
    if tool_name not in SCHEMAS:
        return f"Unknown tool: {tool_name}"

    schema = SCHEMAS[tool_name]

    # Check required arguments
    for field in schema.get("required", []):
        if field not in args:
            return f"Missing required argument '{field}'. Expected: {field}"

    # Check extra arguments
    allowed = schema["properties"].keys()

    for field in args:
        if field not in allowed:
            return f"Invented argument '{field}'. Expected only: {list(allowed)}"

    # Check each argument
    for field, value in args.items():

        expected = schema["properties"][field]

        # Type validation
        if expected["type"] == "string" and not isinstance(value, str):
            return f"Wrong type for '{field}'. Expected string."

        if expected["type"] == "integer" and (
            not isinstance(value, int) or isinstance(value, bool)
        ):
            return f"Wrong type for '{field}'. Expected integer."

        # Enum validation
        if "enum" in expected:
            if value not in expected["enum"]:
                return (
                    f"Invalid value '{value}' for '{field}'. "
                    f"Expected one of {expected['enum']}"
                )

    return None
from my_tools import TOOL_FUNCTIONS, read_webpage

MAX_TOOL_OUTPUT = 1200


def test_missing_file():
    print("\nTEST 1: Missing file")
    print(read_webpage("data/missing.html"))


def test_unknown_tool():
    print("\nTEST 2: Unknown tool")

    name = "search_attendance_database"
    function = TOOL_FUNCTIONS.get(name)

    if function is None:
        print(f"Error: Unknown tool '{name}'.")
    else:
        print(function())


def test_output_truncation():
    print("\nTEST 3: Large tool output")

    result = read_webpage("data/large_attendance.html")

    if len(result) > MAX_TOOL_OUTPUT:
        result = result[:MAX_TOOL_OUTPUT] + "\n[Tool output truncated]"

    print(result)
    print("Returned characters:", len(result))


def test_repeat_detection():
    print("\nTEST 4: Repeated tool call")

    seen_calls = set()
    name = "calculator"
    arguments = '{"expression": "10 + 5"}'

    for attempt in range(1, 4):
        signature = (name, arguments)

        if signature in seen_calls:
            print(
                f"Attempt {attempt}: repeated call detected; "
                "execution blocked."
            )
        else:
            seen_calls.add(signature)
            print(f"Attempt {attempt}: first call accepted.")


if __name__ == "__main__":
    test_missing_file()
    test_unknown_tool()
    test_output_truncation()
    test_repeat_detection()
    
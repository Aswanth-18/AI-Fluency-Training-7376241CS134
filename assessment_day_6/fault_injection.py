# assessment_day_6/fault_injection.py

import json

from validator import validate_arguments


faults = [

    # 1. Invalid JSON
    ("INVALID JSON", "get_menu_price", '{"item":'),

    # 2. Unknown tool
    ("UNKNOWN TOOL", "get_price", {"item": "burger"}),

    # 3. Missing argument
    ("MISSING ARGUMENT", "get_menu_price", {}),

    # 4. Wrong type
    ("WRONG TYPE", "calculate_order_total",
     {"item": "pizza", "quantity": "two"}),

    # 5. Invalid enum
    ("INVALID ENUM", "get_menu_price",
     {"item": "icecream"}),

    # 6. Invented argument
    ("EXTRA ARGUMENT", "get_menu_price",
     {"item": "burger", "discount": 20}),

    # 7. Negative quantity - our fault
    ("NEGATIVE QUANTITY", "calculate_order_total",
     {"item": "pizza", "quantity": -2}),

    # 8. Empty item - our fault
    ("EMPTY ITEM", "get_menu_price",
     {"item": ""})
]


for name, tool, data in faults:

    print("\n" + "-" * 60)
    print(name)
    print("Tool:", tool)
    print("Input:", data)

    # Invalid JSON is handled separately
    if name == "INVALID JSON":
        try:
            json.loads(data)
        except json.JSONDecodeError:
            print("Result: Invalid JSON arguments.")
        continue

    result = validate_arguments(tool, data)

    if result:
        print("Result:", result)
        print("Continued: YES")
    else:
        print("Result: Valid arguments")
        print("Continued: YES")
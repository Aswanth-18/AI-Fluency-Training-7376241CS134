# assessment_day_6/tools.py

MENU = {
    "burger": 150,
    "pizza": 250,
    "sandwich": 120
}

SCHEMAS = {
    "get_menu_price": {
        "type": "object",
        "properties": {
            "item": {
                "type": "string",
                "enum": ["burger", "pizza", "sandwich"]
            }
        },
        "required": ["item"],
        "additionalProperties": False
    },

    "calculate_order_total": {
        "type": "object",
        "properties": {
            "item": {
                "type": "string",
                "enum": ["burger", "pizza", "sandwich"]
            },
            "quantity": {
                "type": "integer"
            }
        },
        "required": ["item", "quantity"],
        "additionalProperties": False
    }
}


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_menu_price",
            "description": "Get the price of a menu item.",
            "parameters": SCHEMAS["get_menu_price"]
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_order_total",
            "description": "Calculate the total price for an item and quantity.",
            "parameters": SCHEMAS["calculate_order_total"]
        }
    }
]

def get_menu_price(item):
    return f"Price of {item}: Rs. {MENU[item]}"


def calculate_order_total(item, quantity):
    total = MENU[item] * quantity
    return f"{quantity} {item}(s) cost Rs. {total}"


TOOL_FUNCTIONS = {
    "get_menu_price": get_menu_price,
    "calculate_order_total": calculate_order_total
}
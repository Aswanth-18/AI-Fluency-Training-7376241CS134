PRODUCT_PRICES = {
    "LAPTOP": 60000,
    "MONITOR": 15000,
    "KEYBOARD": 2000
}


def get_product_price(product_name):
    product_name = product_name.upper().strip()

    if product_name in PRODUCT_PRICES:
        return PRODUCT_PRICES[product_name]

    return "Product not found"


def calculator(expression):
    try:
        result = eval(
            expression,
            {"__builtins__": {}},
            {}
        )

        return str(result)

    except Exception as e:
        return f"Calculation error: {e}"


TOOL_FUNCTIONS = {
    "get_product_price": get_product_price,
    "calculator": calculator
}


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_product_price",
            "description": "Get the price of an e-commerce product.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name": {
                        "type": "string",
                        "description": "Product name such as LAPTOP, MONITOR or KEYBOARD"
                    }
                },
                "required": ["product_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Perform arithmetic calculations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to calculate"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]
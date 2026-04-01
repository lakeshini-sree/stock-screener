ALLOWED_FIELDS = [
    "revenue", "price", "profit",
    "quarter", "sector", "market_cap",
    "revenue_growth", "profit_growth"   # ✅ NEW
]

ALLOWED_OPERATORS = [">", "<", "=", ">=", "<="]
ALLOWED_LOGIC = ["AND", "OR"]

def validate_dsl(dsl: dict):

    if "conditions" not in dsl:
        raise ValueError("Missing 'conditions'")

    if "logic" not in dsl:
        raise ValueError("Missing 'logic'")

    for condition in dsl["conditions"]:

        if "field" not in condition or "operator" not in condition or "value" not in condition:
            raise ValueError("Each condition must have field, operator, value")

        if condition["field"] not in ALLOWED_FIELDS:
            raise ValueError(f"Invalid field: {condition['field']}")

        if condition["operator"] not in ALLOWED_OPERATORS:
            raise ValueError(f"Invalid operator: {condition['operator']}")

        # ✅ STRING fields
        if condition["field"] in ["quarter", "sector"]:
            if not isinstance(condition["value"], str):
                raise ValueError(f"{condition['field']} must be string")

        # ✅ NUMERIC fields (including growth)
        else:
            if not isinstance(condition["value"], (int, float)):
                raise ValueError(f"{condition['field']} must be numeric")

    if dsl["logic"] not in ALLOWED_LOGIC:
        raise ValueError("Logic must be AND/OR")
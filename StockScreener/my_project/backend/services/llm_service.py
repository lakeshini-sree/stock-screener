import re

def nl_to_dsl(query: str):
    query = query.lower()
    conditions = []

    # helper to support "is" and "="
    def normalize_operator(op):
        return "=" if op == "is" else op

    # 🔹 PRICE
    price_match = re.search(r'price\s*(>=|<=|>|<|=|is)\s*(\d+)', query)
    if price_match:
        conditions.append({
            "field": "price",
            "operator": normalize_operator(price_match.group(1)),
            "value": int(price_match.group(2))
        })

    # 🔹 REVENUE
    revenue_match = re.search(r'revenue\s*(>=|<=|>|<|=|is)\s*(\d+)', query)
    if revenue_match:
        conditions.append({
            "field": "revenue",
            "operator": normalize_operator(revenue_match.group(1)),
            "value": int(revenue_match.group(2))
        })

    # 🔹 PROFIT
    profit_match = re.search(r'profit\s*(>=|<=|>|<|=|is)\s*(\d+)', query)
    if profit_match:
        conditions.append({
            "field": "profit",
            "operator": normalize_operator(profit_match.group(1)),
            "value": int(profit_match.group(2))
        })

    # 🔹 MARKET CAP
    mc_match = re.search(r'market\s*cap\s*(>=|<=|>|<|=|is)\s*(\d+)', query)
    if mc_match:
        conditions.append({
            "field": "market_cap",
            "operator": normalize_operator(mc_match.group(1)),
            "value": int(mc_match.group(2))
        })

    # 🔹 SECTOR
    sector_match = re.search(r'sector\s*=?\s*(\w+)', query)
    if sector_match:
        conditions.append({
            "field": "sector",
            "operator": "=",
            "value": sector_match.group(1).upper()
        })

    # 🔹 GROWTH
    growth_match = re.search(r'(revenue|profit)\s*growth\s*(>=|<=|>|<|=|is)\s*(\d+)', query)
    if growth_match:
        conditions.append({
            "field": growth_match.group(1) + "_growth",
            "operator": normalize_operator(growth_match.group(2)),
            "value": int(growth_match.group(3))
        })

    return {
        "conditions": conditions,
        "logic": "AND"
    }
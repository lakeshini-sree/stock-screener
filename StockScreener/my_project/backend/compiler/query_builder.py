class SQLCompiler:
    def __init__(self, dsl):
        self.dsl = dsl

    def build_query(self):
        conditions = self.dsl.get("conditions", [])
        logic = self.dsl.get("logic", "AND")

        # ✅ FIX: specific columns instead of SELECT *
        select_clause = "SELECT company, price, revenue, profit"

        base_query = "FROM stocks"

        where_clause = ""
        values = []

        if conditions:
            clauses = []
            for cond in conditions:
                field = cond["field"]
                operator = cond["operator"]
                value = cond["value"]

                clauses.append(f"{field} {operator} ?")
                values.append(value)

            where_clause = "WHERE " + f" {logic} ".join(clauses)

        # ✅ FIX: add LIMIT
        limit_clause = "LIMIT 10"

        sql_query = f"{select_clause} {base_query} {where_clause} {limit_clause}"

        return sql_query, values
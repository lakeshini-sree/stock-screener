from compiler.query_builder import SQLCompiler

def test_sql_generation():
    dsl = {
        "conditions": [
            {"field": "price", "operator": ">", "value": 400}
        ],
        "logic": "AND"
    }

    compiler = SQLCompiler(dsl)
    sql, values = compiler.build_query()

    assert "SELECT company, price" in sql
    assert "WHERE price > ?" in sql
    assert values == [400]
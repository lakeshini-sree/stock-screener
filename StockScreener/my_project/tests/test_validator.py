from validator import validate_dsl
import pytest

def test_valid_dsl():
    dsl = {
        "conditions": [
            {"field": "price", "operator": ">", "value": 100}
        ],
        "logic": "AND"
    }

    validate_dsl(dsl)


def test_invalid_field():
    dsl = {
        "conditions": [
            {"field": "wrong", "operator": ">", "value": 100}
        ],
        "logic": "AND"
    }

    with pytest.raises(ValueError):
        validate_dsl(dsl)
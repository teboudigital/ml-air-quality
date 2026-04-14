from src.utils.metadata import variable_dictionary


def test_variable_dictionary_contains_key_air_quality_terms():
    dictionary = variable_dictionary()

    assert {"variable", "group", "meaning", "unit", "interpretation"}.issubset(dictionary.columns)
    assert "CO(GT)" in set(dictionary["variable"])
    assert "PT08.S1(CO)" in set(dictionary["variable"])
    assert "NOx(GT)" in set(dictionary["variable"])
    assert len(dictionary) >= 14

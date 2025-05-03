from app.translator.rule_based import RuleBasedTranslator
from app.translator.types import QueryInput

def test_rule_based_translator():
    translator = RuleBasedTranslator()

    input_query = QueryInput(natural_language="Quiero ver el nombre", table_name="clientes")
    expected_sql = "SELECT name FROM clientes;"

    result = translator.translate(input_query)

    assert result.query == expected_sql
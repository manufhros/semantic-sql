from .translator_base import NL2SQLTranslator
from .types import QueryInput, SQLQuery

class RuleBasedTranslator(NL2SQLTranslator):
    def translate(self, query: QueryInput) -> SQLQuery:
        # Simulación de ejemplo
        if "nombre" in query.natural_language.lower():
            return SQLQuery(query=f"SELECT name FROM {query.table_name};")
        return SQLQuery(query=f"SELECT * FROM {query.table_name};")
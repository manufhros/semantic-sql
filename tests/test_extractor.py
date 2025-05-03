from app.translator.keyword_extraction.gpt_extractor import GPTExtractor
import pprint

def test_gpt_extractor():
    extractor = GPTExtractor()
    query = "I want to see the sales and customers who have purchased in the last 30 days"
    result = extractor.extract(query)

    # Pretty-print result for visual inspection
    pprint.pprint(result)

    # Assert structure (opcional)
    assert "tables" in result
    assert isinstance(result["tables"], list)
    assert "aliases_or_synonyms" in result
    assert isinstance(result["aliases_or_synonyms"], dict)
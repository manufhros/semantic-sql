from app.embedding.services.cohere_service import CohereService

def test_get_embedding():
    service = CohereService()
    query = "¿Cuáles son los productos más vendidos?"
    embedding = service.get_embedding(query, input_type="search_query")
    print(embedding)
    assert isinstance(embedding, list)
    assert all(isinstance(x, float) for x in embedding)
    assert len(embedding) == 1024
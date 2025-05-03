from pydantic import BaseModel

class QueryInput(BaseModel):
    natural_language: str
    table_name: str

class SQLQuery(BaseModel):
    query: str
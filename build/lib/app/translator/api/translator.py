from fastapi import APIRouter, HTTPException
from app.translator.types import QueryInput, SQLQuery
from app.translator.rule_based import RuleBasedTranslator

router = APIRouter(prefix="/nl2sql", tags=["translation"])


@router.post("/", response_model=SQLQuery)
def translate_query(data: QueryInput):
    """
    Translate natural language query to SQL query.
    """
    translator = RuleBasedTranslator()
    try:
        return translator.translate(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation error: {str(e)}")
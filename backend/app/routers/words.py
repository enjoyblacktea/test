import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.schemas.word import WordResponse
from app.services import character_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/random", response_model=WordResponse)
async def get_random_word(
    input_method: str = Query(default="bopomofo"),
    db: AsyncSession = Depends(get_db),
):
    word_data = await character_service.get_random_character(db, input_method=input_method)
    if word_data is None:
        raise HTTPException(
            status_code=404,
            detail=f"No characters available for input_method='{input_method}'",
        )
    return WordResponse(**word_data)

from pydantic import BaseModel


class WordResponse(BaseModel):
    id: int
    word: str
    zhuyin: list[str]
    keys: list[str]

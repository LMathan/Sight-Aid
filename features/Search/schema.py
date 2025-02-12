# app/schemas/user_schema.py
from pydantic import BaseModel

class QuerySchema(BaseModel):
    SearchItem: str

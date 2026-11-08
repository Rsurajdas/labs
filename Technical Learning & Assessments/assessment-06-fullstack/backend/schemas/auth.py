from pydantic import BaseModel


# GIVEN
class Token(BaseModel):
    access_token: str
    token_type: str


# Q3 — UserCreate and UserOut go below. See ASSESSMENT.md.

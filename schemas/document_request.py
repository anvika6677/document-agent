from pydantic import BaseModel


class DocumentRequest(BaseModel):
    request: str
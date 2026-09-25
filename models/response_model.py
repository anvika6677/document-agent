from pydantic import BaseModel

class AgentResponse(BaseModel):
    status: str
    document: str
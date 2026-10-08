from groq import BaseModel


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


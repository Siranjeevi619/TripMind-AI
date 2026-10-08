import os

from langchain_groq import ChatGroq

from app.core.config import settings

model = settings.groq_model
api_key = settings.groq_api_key.get_secret_value()

if not api_key or not model:
    raise ValueError("Environment variable GROQ_API_KEY or GROQ_MODEL is required")

llm = ChatGroq(model=model, api_key=api_key, temperature=0.5)

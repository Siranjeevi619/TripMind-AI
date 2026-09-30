from langchain_groq import ChatGroq
import os 
from dotenv import load_dotenv


load_dotenv()

grok_api_key = os.getenv("GROQ_API_KEY")
model_name = os.getenv("GROQ_MODEL")

if not grok_api_key or not model_name:
    raise ValueError("API key not found")

user_input = input()

model = ChatGroq(api_key=grok_api_key, model=model_name , temperature=0.5)

response = model.invoke(user_input)

print(response.content)
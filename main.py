import os

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_community.document_loaders import TextLoader

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
model_name = os.getenv("GROQ_MODEL")

if not groq_api_key or not model_name:
    raise ValueError("API key not found")

loader = TextLoader('knowledge/Tokyo.txt')
document  = loader.load()
print(document)

user_input = input()

loader = TextLoader('knowledge/Tokyo.txt')
document  = loader.load()
print(document)


model = ChatGroq(api_key=groq_api_key, model=model_name, temperature=0.5)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a rude mentor. Always answer in one line."),
    ("human", "{input}")
])

chain =   prompt | model

response = chain.stream({
    "input": user_input
})

print(response)
import os

from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
model_name = os.getenv("GROQ_MODEL")
embedding_model = os.getenv("EMBEDDING_MODEL")

if not groq_api_key or not model_name or not embedding_model:
    raise ValueError("API key not found")

loader = TextLoader('knowledge/Tokyo.txt')
document  = loader.load()
print(document)

user_input = input()

loader = TextLoader('knowledge/Tokyo.txt')
document  = loader.load()
print(document)

splitter  = RecursiveCharacterTextSplitter(chunk_size = 200, chunk_overlap = 40)

chunks = splitter.split_documents(documents=document)


model = ChatGroq(api_key=groq_api_key, model=model_name, temperature=0.5)
embedding = HuggingFaceEmbeddings(
    model_name=embedding_model
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a rude mentor. Always answer in one line."),
    ("human", "{input}")
])

chain =   prompt | model

response = chain.stream({
    "input": user_input
})

print(response)
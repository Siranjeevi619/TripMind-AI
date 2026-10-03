import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

BASE_DIR = Path(__file__).resolve().parent
DB_DIR = str(BASE_DIR / "db")
KNOWLEDGE_FILE = str(BASE_DIR / "knowledge" / "Tokyo.txt")

load_dotenv()


embedding_model = os.getenv("EMBEDDING_MODEL")

if not embedding_model:
    raise ValueError("Missing EMBEDDING_MODEL")

embedding = HuggingFaceEmbeddings(
    model_name=embedding_model
)

def process_ingest():
    vector_db = Chroma(
        collection_name="places",
        embedding_function=embedding,
        persist_directory=DB_DIR
    )

    loader = TextLoader(KNOWLEDGE_FILE, encoding="utf-8")
    documents = loader.load()

    for document in documents:
        document.metadata["city"] = "Tokyo"
        document.metadata["category"] = "place"
        document.metadata["source"] = "Tokyo Travel Guide"

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=40
    )

    chunks = splitter.split_documents(documents)

    vector_db.add_documents(chunks)

def get_vector_db():
    vector_db = Chroma(
        collection_name="places",
        embedding_function=embedding,
        persist_directory=DB_DIR
    )

    return vector_db

def get_chunks():
    loader = TextLoader(
        KNOWLEDGE_FILE,
        encoding="utf-8"
    )

    documents = loader.load()

    for document in documents:
        document.metadata["city"] = "Tokyo"
        document.metadata["category"] = "place"
        document.metadata["source"] = "Tokyo Travel Guide"


    splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=40
    )

    return splitter.split_documents(documents)


if __name__ == "__main__":
    process_ingest()

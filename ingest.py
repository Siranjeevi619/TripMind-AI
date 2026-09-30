import os

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

def process_ingest():
    embedding_model = os.getenv("EMBEDDING_MODEL")

    if not embedding_model:
        raise ValueError("Missing EMBEDDING_MODEL")

    embedding = HuggingFaceEmbeddings(
        model_name=embedding_model
    )

    vector_db = Chroma(
        collection_name="places",
        embedding_function=embedding,
        persist_directory="./db"
    )

    loader = TextLoader("knowledge/Tokyo.txt", encoding="utf-8")
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=40
    )

    chunks = splitter.split_documents(documents)

    vector_db.add_documents(chunks)

def get_vector_db():
    embedding_model = os.getenv("EMBEDDING_MODEL")

    if not embedding_model:
        raise ValueError("Missing EMBEDDING_MODEL")

    embedding = HuggingFaceEmbeddings(
        model_name=embedding_model
    )

    vector_db = Chroma(
        collection_name="places",
        embedding_function=embedding,
        persist_directory="./db"
    )

    return vector_db


if __name__ == "__main__":
    process_ingest()

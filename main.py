import os

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


load_dotenv()


def main():
    groq_api_key = os.getenv("GROQ_API_KEY")
    model_name = os.getenv("GROQ_MODEL")
    embedding_model = os.getenv("EMBEDDING_MODEL")

    if not groq_api_key or not model_name or not embedding_model:
        raise ValueError("Missing GROQ_API_KEY, GROQ_MODEL, or EMBEDDING_MODEL in environment")

    file_path = os.path.join("knowledge", "Tokyo.txt")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Knowledge file not found: {file_path}")

    loader = TextLoader(file_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=40)
    chunks = splitter.split_documents(documents=documents)

    model = ChatGroq(api_key=groq_api_key, model=model_name, temperature=0.5)
    embedding = HuggingFaceEmbeddings(model_name=embedding_model)

    vector_db = Chroma(
        collection_name="places",
        embedding_function=embedding,
        persist_directory="./db",
    )
    vector_db.add_documents(chunks)

    retriever = vector_db.as_retriever(search_kwargs={"k": 3})
    user_input = input("Ask about Tokyo: ")
    results = retriever.invoke(user_input)

    context = "\n\n".join(document.page_content for document in results)

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """You are a travel assistant.

            Answer the user's question using only the provided context.

            If the answer cannot be found in the context, say:
            "I don't have enough information in my knowledge base."

            Context: {context}""",
        ),
        ("human", "{question}"),
    ])

    chain = prompt | model
    response = chain.invoke({"context": context, "question": user_input})
    print(response.content if hasattr(response, "content") else response)


if __name__ == "__main__":
    main()
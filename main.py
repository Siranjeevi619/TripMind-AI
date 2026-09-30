import os

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from ingest import get_vector_db

load_dotenv()


def main():
    groq_api_key = os.getenv("GROQ_API_KEY")
    model_name = os.getenv("GROQ_MODEL")

    if not groq_api_key or not model_name:
        raise ValueError(
            "Missing GROQ_API_KEY or GROQ_MODEL"
        )

    model = ChatGroq(
        api_key=groq_api_key,
        model=model_name,
        temperature=0.5
    )

    vector_db = get_vector_db()

    retriever = vector_db.as_retriever(
        search_kwargs={"k": 3}
    )

    user_input = input("Ask about Tokyo: ")

    results = retriever.invoke(user_input)

    context = "\n\n".join(
        document.page_content
        for document in results
    )

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """You are a travel assistant.

        Answer the user's question using only the provided context.

        If the answer cannot be found in the context, say:
        "I don't have enough information in my knowledge base."

        Context:
        {context}"""),
        ("human", "{question}"),
    ])

    chain = prompt | model

    response = chain.invoke({
        "context": context,
        "question": user_input
    })

    print(response.content)


if __name__ == "__main__":
    main()

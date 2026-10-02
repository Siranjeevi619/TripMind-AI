import os

from dotenv import load_dotenv
from langchain_classic.retrievers import MultiQueryRetriever
from langchain_groq import ChatGroq
from ingest import get_vector_db


class MultiQuerySearch:
    def __init__(self):
        load_dotenv()
        groq_model = os.getenv("GROQ_MODEL")
        groq_api_key = os.getenv("GROQ_API_KEY")
        self.vector_db = get_vector_db()
        self.model = ChatGroq(model=groq_model, api_key= groq_api_key, temperature=0)

    def search(self, query):
        retreived_results = self.vector_db.as_retriever(search_kwargs={"k":5})
        multi_query_retriever = MultiQueryRetriever.from_llm(
            retriever=retreived_results,
            llm=self.model
        )
        return multi_query_retriever.invoke(query)


def main():
    search = MultiQuerySearch()
    query = "What are good places to see cherry blossoms in Tokyo?"
    documents = search.search(query)

    for docs in documents:
        print(docs)


if __name__ == "__main__":
    main()



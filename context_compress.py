import os

from dotenv import load_dotenv
from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors import LLMChainExtractor
from langchain_groq import ChatGroq

from ingest import get_vector_db

load_dotenv()
class ContextCompress:
    def __init__(self):
        self.model = ChatGroq(model= os.getenv("GROQ_MODEL"),
                              api_key=os.getenv("GROQ_API_KEY"),
                              temperature=0)
        self.base_retriever = get_vector_db().as_retriever(search_kwargs={
            "k": 5
        })

        compressor = LLMChainExtractor.from_llm(
            self.model
        )

        self.retriever = ContextualCompressionRetriever(
            base_retriever=self.base_retriever,
            base_compressor=compressor
        )

    def search(self, queries):
        return self.retriever.invoke(queries)

def main():
    query = "what is Senso-ji?"
    compressor = ContextCompress()
    print(compressor.search(query))

if __name__ == '__main__':
    main()


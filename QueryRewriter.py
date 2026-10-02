import os
from idlelib import query

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq


class QueryRewriter:
    load_dotenv()
    MODEL = os.getenv("GROQ_MODEL")
    API_KEY = os.getenv("GROQ_API_KEY")

    def __init__(self):
        self.model = ChatGroq(model=self.MODEL, api_key=self.API_KEY, temperature=0)
        self.prompt = ChatPromptTemplate([
            ('system',
             "Rewrite the user's query into a concise search query "
             "optimized for retrieving relevant documents."
             ),
            ('human',"{query}")
        ])
        self.chain = self.prompt | self.model

    def rewrite(self, query):
        response = self.chain.invoke({
            'query': query,
        })
        return response.content

def main():
    load_dotenv()
    rewriter = QueryRewriter()
    user_query = "I'll be in Tokyo for 5 days. What should I see?"
    rewritten = rewriter.rewrite(user_query)
    print(user_query)
    print(rewritten)

if __name__ == "__main__":
    main()

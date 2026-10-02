import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from schema.router import QueryRouter


class Routing:
    def __init__(self):
        groq_model= os.getenv("GROQ_MODEL")
        groq_api_key = os.getenv("GROQ_API_KEY")

        self.model = ChatGroq(model=groq_model, api_key=groq_api_key, temperature=0)
        self.router = self.model.with_structured_output(
            QueryRouter, method="json_schema"
        )

        self.prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """
                Choose the best retrieval strategy for the user query.

                vector:
                Use for simple factual questions.

                hybrid:
                Use when exact keywords, names or terms matter.

                multi_query:
                Use for broad or exploratory questions.
                """
            ),
            (
                "human",
                "{query}"
            )
        ])

        self.chain = self.prompt | self.model

    def route(self ,query):
        response  = self.chain.invoke({
            "query": query,
        })
        return response.content



def main():

    router = Routing()
    queries= [
        "What is Senso-ji?",
        "Otsukaichan Tsukemen Iidabashi",
        "What are the best places to see cherry blossoms?"
    ]

    for q in queries:
        response = router.route(q)
        print(response)

if __name__ == '__main__':
    main()
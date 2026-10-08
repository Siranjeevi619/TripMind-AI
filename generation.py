import os

from langchain_core.prompt_values import ChatPromptValue
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

import reranker
from ingest import get_vector_db
from schema.answer import Answer


class Generator():
    def __init__(self):
        self.model = ChatGroq(
            model=os.getenv("GROQ_MODEL"),
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=0
        )
        self.structured_model = self.model.with_structured_output(Answer, method='json_schema')
        self.prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """
                    You are a helpful travel assistant.
    
                    Answer the user's question using ONLY the provided context.
    
                    If the context does not contain enough information:
                    - say that you do not have enough information
                    - set grounded to false
    
                    If the context supports the answer:
                    - answer using only the context
                    - set grounded to true
    
                    Do not use outside knowledge.
                    Do not invent facts.
    
                    Context:
                    {context}
                """
            ),
            (
                "human",
                "{question}"
            )
        ])

        self.chain = self.prompt | self.structured_model

    def generate(self, questions, document):
        chunks = "\n\n".join(
            document.page_content
            for document in document
        )

        response  = self.chain.invoke({
            "question": questions,
            "context": chunks,
        })

        sources = list({
            docs.metadata.get("source")
            for docs in document
            if  docs.metadata.get("source")
        })

        return {
            "answer": response.answer,
            "grounded": response.grounded,
            "source": sources,
        }

def main():
    vector_db = get_vector_db()
    question = "Where is Senso-ji?"
    document = vector_db.similarity_search(question, k = 3)
    generator = Generator()
    answer = generator.generate(question, document)
    print(answer)

if __name__ == '__main__':
    main()
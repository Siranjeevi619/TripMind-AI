
from adaptive_search import AdaptiveRetriever
from generation import Generator


class RAGPipeline:
    def __init__(self):
        self.retriever = AdaptiveRetriever()
        self.generator = Generator()

    def run(self, question):
        queries = self.retriever.retrieve(question)
        response = self.generator.generate(question, queries)
        sources = list({
            document.metadata.get("source")
            for document in queries
            if document.metadata.get("source")
        })
        retrieved_docs = [
            document.page_content
            for document in queries
            if document.page_content
        ]
        return {
            "answer": response["answer"],
            "sources": sources,
            "grounded": response["grounded"],
            "retrieved_docs": retrieved_docs

        }

def main():
    pipeline = RAGPipeline()
    run = pipeline.run("Where is Senso-Ji?")
    print(run)


if __name__ == '__main__':
    main()

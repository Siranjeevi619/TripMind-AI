from rank_bm25 import BM25Okapi


class KeywordSearch:

    def __init__(self, documents):
        self.documents = documents

        tokenized_documents = [
            document.page_content.lower().split()
            for document in documents
        ]

        self.bm25 = BM25Okapi(tokenized_documents)

    def search(self, query, k=3, city=None, category=None):

        filtered_documents = [
            document
            for document in self.documents
            if (
                (city is None or document.metadata.get("city") == city)
                and
                (category is None or document.metadata.get("category") == category)
            )
        ]

        tokenized_documents = [
            document.page_content.lower().split()
            for document in filtered_documents
        ]

        bm25 = BM25Okapi(tokenized_documents)

        query_tokens = query.lower().split()

        return bm25.get_top_n(
            query=query_tokens,
            documents=filtered_documents,
            n=k
        )
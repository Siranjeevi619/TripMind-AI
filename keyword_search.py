from rank_bm25 import BM25Okapi


class Keyword_search:

    def __init__(self, documents):
        self.documents = documents
        tokenized_documents = [
            document.page_content.lower().split()
            for document in documents
        ]

        self.bm25 = BM25Okapi(tokenized_documents)

    def search(self, query , k = 3):
        query_token = query.lower().split()

        results = self.bm25.get_top_n(
            query=query_token,
            documents=self.documents,
            n=k
        )
        return results
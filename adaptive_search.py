from hybrid_search import reciprocal_rank_fusion
from ingest import get_vector_db, get_chunks
from keyword_search import KeywordSearch
from multi_query_search import MultiQuerySearch
from reranker import Reranker
from routing import Routing


class AdaptiveRetriever:
    def __init__(self):

        self.technique_router = Routing()
        self.vector_db = get_vector_db()
        self.chunks = get_chunks()
        self.keyword_search = KeywordSearch(
            self.chunks
        )
        self.multi_query = MultiQuerySearch()
        self.reranker = Reranker()

    def retrieve(self, queries):
        strategy = self.technique_router.route(queries)
        print(strategy)
        if strategy == "vector":
            results = self.vector_db.similarity_search(queries, k=5)
        elif strategy == "hybrid":
            vector_db = self.vector_db.similarity_search(queries, k=5)
            keyword_db = self.keyword_search.search(queries, k=5)
            results = reciprocal_rank_fusion(vector_db, keyword_db)
        elif strategy == "multi_query":
            results = self.multi_query.search(queries)
        else:
            raise ValueError(
                f"Strategy must be one of 'vector', 'hybrid' or 'multi_query'. The strategy we got {strategy}")
        return self.reranker.rerank(queries, results)

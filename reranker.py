from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain_classic.retrievers.document_compressors import CrossEncoderReranker


class Reranker:
    def __init__(self):
        model = HuggingFaceCrossEncoder(
            model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

        self.compressor = CrossEncoderReranker(
            model=model,
            top_n=3
        )

    def rerank(self, query, documents):
        return self.compressor.compress_documents(
            documents,
            query
        )

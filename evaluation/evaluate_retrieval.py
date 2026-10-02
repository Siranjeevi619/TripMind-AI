import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from hybrid_search import reciprocal_rank_fusion
from ingest import get_chunks, get_vector_db
from keyword_search import KeywordSearch
from reranker import Reranker


def load_dataset():

    with open(
        "evaluation/dataset.json",
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def normalize(text):
    return " ".join(text.lower().split())

def mrr(retrieved_documents, reference_chunks):

    reference_texts = {
        normalize(chunk)
        for chunk in reference_chunks
    }

    for rank, document in enumerate(retrieved_documents, start=1):

        if normalize(document.page_content) in reference_texts:
            return 1 / rank

    return 0.0


def recall_at_k(retrieved_documents, reference_chunks, k):

    retrieved_texts = {
        normalize(document.page_content)
        for document in retrieved_documents[:k]
    }

    reference_texts = {
        normalize(chunk)
        for chunk in reference_chunks
    }

    if not reference_texts:
        return 1.0 if not retrieved_texts else 0.0

    relevant_retrieved = (
        retrieved_texts & reference_texts
    )

    return len(relevant_retrieved) / len(reference_texts)


def precision_at_k(retrieved_documents, reference_chunks, k):

    retrieved_texts = {
        normalize(document.page_content)
        for document in retrieved_documents[:k]
    }

    reference_texts = {
        normalize(chunk)
        for chunk in reference_chunks
    }

    if not retrieved_texts:
        return 0.0

    relevant_retrieved = (
        retrieved_texts & reference_texts
    )

    return len(relevant_retrieved) / len(retrieved_texts)


def retrieve(question):

    vector_db = get_vector_db()
    chunks = get_chunks()

    keyword_retriever = KeywordSearch(chunks)

    vector_results = vector_db.similarity_search(
        question,
        k=5
    )

    keyword_results = keyword_retriever.search(
        question,
        k=5
    )

    hybrid_results = reciprocal_rank_fusion(
        vector_results,
        keyword_results
    )

    reranker = Reranker()

    reranked_results = reranker.rerank(
        question,
        hybrid_results[:10]
    )

    return reranked_results


def main():

    dataset = load_dataset()

    total_recall = 0
    total_precision = 0
    answerable_count = 0

    for item in dataset:

        question = item["question"]
        reference_chunks = item["reference_chunks"]

        results = retrieve(question)

        score = recall_at_k(
            results,
            reference_chunks,
            k=3
        )

        precision = precision_at_k(
            results,
            reference_chunks,
            k=3
        )

        mrr_score = mrr(
            results,
            reference_chunks
        )

        if item["should_answer"]:
            total_recall += score
            total_precision += precision
            answerable_count += 1

        print("\n" + "=" * 60)
        print("Question:", question)
        print("Recall@3:", round(score, 2))
        print("Precision@3:", round(precision, 2))
        print("MRR:", round(mrr_score, 2))

        for document in results:
            print("\n---")
            print(document.page_content)

    average_recall = total_recall / answerable_count
    average_precision = total_precision / answerable_count

    print("\n" + "=" * 60)
    print("Answerable queries:", answerable_count)
    print("Average Recall@3:", round(average_recall, 2))
    print("Average Precision@3:", round(average_precision, 2))


if __name__ == "__main__":
    main()
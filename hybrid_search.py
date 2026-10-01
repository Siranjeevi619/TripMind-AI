def reciprocal_rank_fusion(vector_results,keyword_results,k=60):
    scores = {}
    documents = {}

    for rank, document in enumerate(vector_results, start=1):
        key = document.page_content

        scores[key] = scores.get(key, 0) + 1 / (k + rank)
        documents[key] = document

    for rank, document in enumerate(keyword_results, start=1):
        key = document.page_content

        scores[key] = scores.get(key, 0) + 1 / (k + rank)
        documents[key] = document

    ranked_results = sorted(
        documents.items(),
        key=lambda item: scores[item[0]],
        reverse=True
    )

    return [
        document
        for key, document in ranked_results
    ]
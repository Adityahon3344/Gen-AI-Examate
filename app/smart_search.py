
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def smart_search(records, query, top_k=5):
    """
    Search and rank agricultural schemes using TF-IDF
    and cosine similarity.
    """

    query = query.strip()

    if not query or not records:
        return []

    documents = []

    for record in records:
        text = (
            record.scheme_name + " " +
            record.department + " " +
            record.benefit + " " +
            " ".join(record.eligibility) + " " +
            " ".join(record.required_documents)
        )

        documents.append(text)

    try:
        vectorizer = TfidfVectorizer()

        tfidf_matrix = vectorizer.fit_transform(
            [query] + documents
        )

        similarity_scores = cosine_similarity(
            tfidf_matrix[0:1],
            tfidf_matrix[1:]
        ).flatten()

    except ValueError:
        return []

    ranked_results = []

    for index, score in enumerate(similarity_scores):
        if score > 0:
            ranked_results.append(
                (records[index], float(score))
            )

    ranked_results.sort(
        key=lambda item: item[1],
        reverse=True
    )

    return [
        record
        for record, score in ranked_results[:top_k]
    ]

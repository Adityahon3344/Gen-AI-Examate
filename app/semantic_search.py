
import json
import re
from pathlib import Path

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

CHUNKS_FILE = Path("data/chunks.json")
QUESTIONS_FILE = Path("docs/user_questions.md")
OUTPUT_FILE = Path("eval/search_results.md")

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 3


def load_questions():
    """Load Q1-Q10 questions from Markdown."""
    content = QUESTIONS_FILE.read_text(encoding="utf-8")
    questions = []

    for line in content.splitlines():
        match = re.match(r"^\s*\*\*Q\d+\.\*\*\s*(.+)", line)

        if match:
            questions.append(match.group(1).strip())

    return questions


def semantic_search(question, chunks, model):
    """Find the most relevant document chunks."""
    query_embedding = model.encode(
        [question],
        normalize_embeddings=True
    )

    chunk_embeddings = [chunk["embedding"] for chunk in chunks]

    scores = cosine_similarity(
        query_embedding,
        chunk_embeddings
    )[0]

    ranked_indices = scores.argsort()[::-1][:TOP_K]

    results = []

    for index in ranked_indices:
        chunk = chunks[index]

        results.append({
            "score": float(scores[index]),
            "text": chunk["text"],
            "source": chunk["source"],
            "page": chunk["page"],
            "title": chunk["title"]
        })

    return results


def main():
    chunks = json.loads(CHUNKS_FILE.read_text(encoding="utf-8"))
    questions = load_questions()

    if not questions:
        raise ValueError("No questions found in docs/user_questions.md")

    if not chunks or any("embedding" not in chunk for chunk in chunks):
        raise ValueError("Some chunks are missing embeddings. Run app.embed first.")

    print("Total chunks:", len(chunks))
    print("Total questions:", len(questions))

    model = SentenceTransformer(MODEL_NAME)

    report = [
        "# Day 7 - Semantic Search Results",
        "",
        f"- Total chunks: {len(chunks)}",
        f"- Total questions: {len(questions)}",
        f"- Embedding model: {MODEL_NAME}",
        f"- Top results per question: {TOP_K}",
        ""
    ]

    for number, question in enumerate(questions, start=1):
        print(f"Searching question {number}/{len(questions)}...")

        results = semantic_search(question, chunks, model)

        report.extend([
            f"## Question {number}",
            "",
            f"**Question:** {question}",
            ""
        ])

        for rank, result in enumerate(results, start=1):
            page = result["page"] if result["page"] is not None else "N/A (HTML)"

            report.extend([
                f"### Result {rank}",
                "",
                f"- **Similarity score:** {result['score']:.4f}",
                f"- **Source:** {result['source']}",
                f"- **Page:** {page}",
                f"- **Title:** {result['title']}",
                "",
                "**Matched text:**",
                "",
                result["text"],
                ""
            ])

        report.extend(["---", ""])

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text("\n".join(report), encoding="utf-8")

    print("\nSemantic search completed!")
    print("Questions processed:", len(questions))
    print("Results saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()

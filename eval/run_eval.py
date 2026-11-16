
import json
import sys
from pathlib import Path

import chromadb
from bs4 import BeautifulSoup
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.rag import ask_question

RAW_DIR = PROJECT_ROOT / "data" / "raw"
EVAL_FILE = PROJECT_ROOT / "eval" / "eval_set.json"
RESULTS_DIR = PROJECT_ROOT / "eval" / "results"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

CONFIGS = [
    {
        "name": "A",
        "chunk_size": 1000,
        "overlap": 150,
        "top_k": 3
    },
    {
        "name": "B",
        "chunk_size": 500,
        "overlap": 75,
        "top_k": 5
    }
]


def split_text(text, chunk_size, overlap):
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end]).strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(words):
            break

        start = end - overlap

    return chunks


def build_chunks(chunk_size, overlap):
    all_chunks = []

    # Process PDFs page by page
    for file_path in RAW_DIR.glob("*.pdf"):
        print("Processing:", file_path.name)

        pdf = PdfReader(str(file_path))
        title = (
            pdf.metadata.title
            if pdf.metadata and pdf.metadata.title
            else file_path.stem
        )

        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""

            for index, chunk in enumerate(
                split_text(text, chunk_size, overlap)
            ):
                all_chunks.append({
                    "id": (
                        f"{file_path.stem}_page{page_number}_"
                        f"chunk{index + 1}"
                    ),
                    "text": chunk,
                    "source": file_path.name,
                    "page": page_number,
                    "title": title
                })

    # Process HTML documents
    for file_path in RAW_DIR.glob("*.html"):
        print("Processing:", file_path.name)

        with open(file_path, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")

        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        title = (
            soup.title.get_text(strip=True)
            if soup.title
            else file_path.stem
        )

        text = soup.get_text(separator=" ", strip=True)

        for index, chunk in enumerate(
            split_text(text, chunk_size, overlap)
        ):
            all_chunks.append({
                "id": f"{file_path.stem}_chunk{index + 1}",
                "text": chunk,
                "source": file_path.name,
                "page": -1,
                "title": title
            })

    return all_chunks


def create_eval_collection(chunks, embedding_model, collection_name):
    client = chromadb.EphemeralClient()

    collection = client.create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"}
    )

    texts = [chunk["text"] for chunk in chunks]

    embeddings = embedding_model.encode(
        texts,
        show_progress_bar=True,
        normalize_embeddings=True
    )

    batch_size = 100

    for start in range(0, len(chunks), batch_size):
        batch = chunks[start:start + batch_size]
        batch_embeddings = embeddings[start:start + batch_size]

        collection.add(
            ids=[item["id"] for item in batch],
            documents=[item["text"] for item in batch],
            embeddings=batch_embeddings.tolist(),
            metadatas=[
                {
                    "source": item["source"],
                    "page": item["page"],
                    "title": item["title"]
                }
                for item in batch
            ]
        )

    return client, collection


def evaluate_retrieval(collection, model, question, keywords, top_k):
    query_embedding = model.encode(
        [question],
        normalize_embeddings=True
    )

    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas"]
    )

    documents = results["documents"][0]
    context = " ".join(documents).lower()

    matched = [
        keyword for keyword in keywords
        if keyword.lower() in context
    ]

    coverage = (
        len(matched) / len(keywords)
        if keywords else 0
    )

    return {
        "retrieved_chunks": len(documents),
        "matched_keywords": matched,
        "keyword_coverage": round(coverage, 4),
        "retrieved_documents": documents
    }


def run_configuration(config, questions, embedding_model):
    print("\n" + "=" * 55)
    print("RUNNING CONFIGURATION", config["name"])
    print("=" * 55)

    chunks = build_chunks(
        config["chunk_size"],
        config["overlap"]
    )

    print("Total chunks:", len(chunks))

    if not chunks:
        raise ValueError("No chunks were generated.")

    client, collection = create_eval_collection(
        chunks,
        embedding_model,
        f"eval_config_{config['name'].lower()}"
    )

    results = []

    for index, item in enumerate(questions, start=1):
        question = item["question"]
        keywords = item.get("expected_keywords", [])

        print(f"\nQuestion {index}/{len(questions)}")
        print(question)

        retrieval = evaluate_retrieval(
            collection,
            embedding_model,
            question,
            keywords,
            config["top_k"]
        )

        try:
            response = ask_question(
                question=question,
                vector_collection=collection,
                embedding_model=embedding_model,
                top_k=config["top_k"]
            )

            answer = response["answer"]
            sources = response["sources"]
            error = None

        except Exception as exception:
            answer = ""
            sources = []
            error = str(exception)

            print("Generation error:", error)

        expected_abstention = item.get(
            "expected_abstention",
            not item.get("answerable", True)
        )

        abstained = "i don't know" in answer.lower()

        result = {
            "id": item["id"],
            "question": question,
            "answerable": item.get("answerable", True),
            "expected_abstention": expected_abstention,
            "answer": answer,
            "sources": sources,
            "retrieval": retrieval,
            "has_citation": "[source" in answer.lower(),
            "abstained": abstained,
            "abstention_correct": (
                abstained == expected_abstention
            ),
            "error": error
        }

        results.append(result)

        print("Keyword coverage:", retrieval["keyword_coverage"])
        print("Abstained:", abstained)
        print("Sources:", len(sources))

    # Delete only the temporary evaluation collection
    client.delete_collection(collection.name)

    return results

def calculate_metrics(results):
    total = len(results)

    successful = [
        item for item in results
        if item["error"] is None
    ]

    answerable = [
        item for item in results
        if item["answerable"]
    ]

    unanswerable = [
        item for item in results
        if not item["answerable"]
    ]

    keyword_scores = [
        item["retrieval"]["keyword_coverage"]
        for item in results
    ]

    citation_count = sum(
        item["has_citation"] for item in answerable
    )

    correct_abstentions = sum(
        item["abstention_correct"] for item in unanswerable
    )

    return {
        "total_questions": total,
        "successful_generations": len(successful),
        "average_keyword_coverage": round(
            sum(keyword_scores) / total, 4
        ) if total else 0,
        "citation_rate": round(
            citation_count / len(answerable), 4
        ) if answerable else 0,
        "correct_abstentions": correct_abstentions,
        "unanswerable_questions": len(unanswerable),
        "generation_errors": total - len(successful)
    }


def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    questions = json.loads(
        EVAL_FILE.read_text(encoding="utf-8")
    )

    print("Evaluation questions:", len(questions))

    print("\nLoading embedding model:", MODEL_NAME)
    embedding_model = SentenceTransformer(MODEL_NAME)

    all_results = {}
    all_metrics = {}

    for config in CONFIGS:
        results = run_configuration(
            config,
            questions,
            embedding_model
        )

        all_results[config["name"]] = results
        all_metrics[config["name"]] = calculate_metrics(results)

    output = {
        "configurations": CONFIGS,
        "metrics": all_metrics,
        "results": all_results
    }

    results_file = RESULTS_DIR / "rag_eval_results.json"

    results_file.write_text(
        json.dumps(output, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    # Generate comparison report
    report = [
        "# RAG Configuration Evaluation",
        "",
        "| Metric | Config A (1000 / Top-3) | Config B (500 / Top-5) |",
        "|---|---:|---:|"
    ]

    metric_labels = {
        "average_keyword_coverage": "Average keyword coverage",
        "citation_rate": "Citation rate",
        "correct_abstentions": "Correct abstentions",
        "successful_generations": "Successful generations",
        "generation_errors": "Generation errors"
    }

    for key, label in metric_labels.items():
        a = all_metrics["A"][key]
        b = all_metrics["B"][key]
        report.append(f"| {label} | {a} | {b} |")

    report.extend([
        "",
        "## Evaluation notes",
        "",
        "- Keyword coverage is an automatic retrieval proxy, not proof of factual correctness.",
        "- Citation rate measures whether an answer contains a [Source] reference.",
        "- Correct abstentions measure whether unanswerable questions received an 'I don't know' response.",
        "- Manually verify answers against official scheme guidelines before claiming factual accuracy.",
        "",
        "## Configuration settings",
        "",
        "| Setting | Config A | Config B |",
        "|---|---:|---:|",
        "| Chunk size (words) | 1000 | 500 |",
        "| Overlap (words) | 150 | 75 |",
        "| Top-k | 3 | 5 |"
    ])

    report_file = RESULTS_DIR / "comparison.md"
    report_file.write_text("\n".join(report), encoding="utf-8")

    print("\n" + "=" * 55)
    print("EVALUATION COMPLETED")
    print("=" * 55)

    print("\nMetrics:")
    print(json.dumps(all_metrics, indent=2))

    print("\nSaved results:", results_file)
    print("Saved comparison:", report_file)


if __name__ == "__main__":
    main()

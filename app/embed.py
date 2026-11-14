
import json
from pathlib import Path

from sentence_transformers import SentenceTransformer

CHUNKS_FILE = Path("data/chunks.json")

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def generate_embeddings():
    if not CHUNKS_FILE.exists():
        raise FileNotFoundError(
            "data/chunks.json not found. Run app.chunking first."
        )

    chunks = json.loads(CHUNKS_FILE.read_text(encoding="utf-8"))

    if not chunks:
        print("No chunks available for embedding.")
        return

    print("Loading embedding model:", MODEL_NAME)
    model = SentenceTransformer(MODEL_NAME)

    texts = [chunk["text"] for chunk in chunks]

    print("Generating embeddings...")
    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        normalize_embeddings=True
    )

    for chunk, embedding in zip(chunks, embeddings):
        chunk["embedding"] = embedding.tolist()

    CHUNKS_FILE.write_text(
        json.dumps(chunks, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print("\nEmbedding generation completed!")
    print("Total embedded chunks:", len(chunks))
    print("Embedding dimensions:", len(embeddings[0]))
    print("Saved to:", CHUNKS_FILE)


if __name__ == "__main__":
    generate_embeddings()

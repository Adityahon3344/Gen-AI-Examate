
import json
from pathlib import Path

import chromadb

CHUNKS_FILE = Path("data/chunks.json")
DB_PATH = Path("data/chroma_db")
COLLECTION_NAME = "krishiyojana_documents"


def create_vectorstore():
    """Store all embedded document chunks in persistent ChromaDB."""

    if not CHUNKS_FILE.exists():
        raise FileNotFoundError("Run app.chunking and app.embed first.")

    chunks = json.loads(CHUNKS_FILE.read_text(encoding="utf-8"))

    if not chunks:
        raise ValueError("No document chunks found.")

    if any("embedding" not in chunk for chunk in chunks):
        raise ValueError("Embeddings missing. Run app.embed first.")

    client = chromadb.PersistentClient(path=str(DB_PATH))

    # Recreate the collection to avoid duplicate or outdated records.
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )

    batch_size = 100

    for start in range(0, len(chunks), batch_size):
        batch = chunks[start:start + batch_size]

        collection.add(
            ids=[chunk["id"] for chunk in batch],
            embeddings=[chunk["embedding"] for chunk in batch],
            documents=[chunk["text"] for chunk in batch],
            metadatas=[
                {
                    "source": chunk["source"],
                    "page": chunk["page"] if chunk["page"] is not None else -1,
                    "title": chunk["title"]
                }
                for chunk in batch
            ]
        )

        print(f"Indexed {min(start + batch_size, len(chunks))}/{len(chunks)} chunks")

    print("\nVector database created successfully!")
    print("Collection:", COLLECTION_NAME)
    print("Total indexed chunks:", collection.count())
    print("Database location:", DB_PATH)


if __name__ == "__main__":
    create_vectorstore()

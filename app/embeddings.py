
from threading import Lock

import numpy as np
from fastembed import TextEmbedding

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

_embedding_model = None
_embedding_lock = Lock()


def get_embedding_model():
    global _embedding_model

    if _embedding_model is None:
        with _embedding_lock:
            if _embedding_model is None:
                _embedding_model = TextEmbedding(
                    model_name=MODEL_NAME
                )

    return _embedding_model


def generate_query_embedding(text: str) -> list[float]:
    if not text or not text.strip():
        raise ValueError("Text cannot be empty.")

    model = get_embedding_model()

    # Use embed() to match the original document-embedding approach.
    vector = np.asarray(
        next(model.embed([text.strip()])),
        dtype=np.float32
    )

    # Normalize the vector, as in the original SentenceTransformer code.
    norm = np.linalg.norm(vector)

    if norm == 0:
        raise ValueError("Generated embedding has zero magnitude.")

    return (vector / norm).tolist()


def is_embedding_model_loaded() -> bool:
    return _embedding_model is not None
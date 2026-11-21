import numpy as np
import pytest

from app import embeddings


class FakeEmbeddingModel:
    def embed(self, texts):
        assert texts == ["farm support"]
        return iter([np.array([3.0, 4.0], dtype=np.float32)])


def test_query_embedding_is_normalized(monkeypatch):
    monkeypatch.setattr(
        embeddings,
        "get_embedding_model",
        lambda: FakeEmbeddingModel(),
    )

    vector = embeddings.generate_query_embedding(" farm support ")

    assert vector == pytest.approx([0.6, 0.8])


def test_query_embedding_rejects_blank_text():
    with pytest.raises(ValueError, match="Text cannot be empty"):
        embeddings.generate_query_embedding("  ")

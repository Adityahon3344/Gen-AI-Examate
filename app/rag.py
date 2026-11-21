
from app.embeddings import generate_query_embedding
from app.llm import generate_response


def ask_question(
    question: str,
    vector_collection,
    top_k: int = 3
):
    """
    Retrieve relevant document chunks and generate
    a grounded answer using the Groq LLM.
    """

    question = question.strip()

    if not question:
        raise ValueError("Question cannot be empty.")

    # 1. Generate question embedding using FastEmbed
    query_embedding = generate_query_embedding(question)

    # 2. Retrieve relevant chunks from ChromaDB
    total_chunks = vector_collection.count()

    if total_chunks == 0:
        return {
            "question": question,
            "answer": "I don't know. No document information is available.",
            "sources": [],
            "confidence": "low"
        }

    results = vector_collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, total_chunks),
        include=["documents", "metadatas", "distances"]
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    # 3. Prepare context and source citations
    context_parts = []
    sources = []

    for index, document in enumerate(documents):
        metadata = metadatas[index]

        source_name = metadata.get("source", "Unknown source")
        page_number = metadata.get("page", -1)
        title = metadata.get("title", "Unknown title")

        page = page_number if page_number != -1 else None

        source = {
            "source": source_name,
            "page": page,
            "title": title
        }

        if source not in sources:
            sources.append(source)

        context_parts.append(
            f"[Source {index + 1}: {source_name}, "
            f"Page: {page if page is not None else 'Not available'}]\n"
            f"{document}"
        )

    context = "\n\n".join(context_parts)

    # 4. Build strict RAG system prompt
    system_prompt = """
You are KrishiYojana, an agricultural government scheme
information assistant for farmers in Maharashtra, India.

STRICT RULES:

1. Answer only using the retrieved document context.
2. Never invent scheme details, benefits, amounts,
   eligibility criteria, or application deadlines.
3. If the retrieved context does not contain the answer,
   respond exactly: I don't know.
4. For questions about current application deadlines,
   dates, or last dates, only provide an answer if an
   explicit and relevant date is present in the context.
5. Do not treat an unrelated date as an application deadline.
6. Include source references such as [Source 1] in your answer.
7. Use simple English.
8. Do not guarantee that a farmer is eligible for a scheme.
9. Explain that final approval is decided by the
   concerned government department.
"""

    # 5. Build user prompt
    user_prompt = f"""
Farmer's question:
{question}

Retrieved document context:
{context}

Answer using only the retrieved context.
Include source references in the answer.
If the answer is missing, say exactly: I don't know.
"""

    # 6. Generate answer using Groq
    answer = generate_response(
        user_prompt,
        system_prompt
    )

    # 7. Return answer and citations
    if "I don't know" in answer:
        confidence = "low"
    elif sources:
        confidence = "medium"
    else:
        confidence = "low"

    return {
        "question": question,
        "answer": answer.strip(),
        "sources": sources,
        "confidence": confidence
    }

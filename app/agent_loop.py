from app.rag import ask_question
from app.tools import check_scheme_eligibility


def run_agent(
    question,
    vector_collection,
    embedding_model,
    farmer_details=None
):
    """
    Simple hand-written agent.

    Available tools:
    1. RAG search
    2. Scheme eligibility checker
    """

    question = question.strip()

    if not question:
        return {
            "status": "error",
            "message": "Question cannot be empty."
        }

    # Step 1: Identify the required tool
    eligibility_keywords = [
        "eligible",
        "eligibility",
        "qualify",
        "qualification",
        "am i eligible",
        "check my eligibility"
    ]

    info_keywords = [
        "benefits",
        "documents",
        "scheme details",
        "how to apply",
        "what is",
        "explain"
    ]

    question_lower = question.lower()

    use_eligibility = any(
        keyword in question_lower
        for keyword in eligibility_keywords
    )

    use_rag = (
        not use_eligibility
        or any(
            keyword in question_lower
            for keyword in info_keywords
        )
    )

    # Step 2: Create the agent's tool execution queue
    tool_queue = []

    if use_eligibility:
        tool_queue.append("eligibility")

    if use_rag:
        tool_queue.append("rag_search")

    results = {}

    # Step 3: Execute tools one by one
    while tool_queue:

        current_tool = tool_queue.pop(0)

        if current_tool == "eligibility":
            farmer_details = farmer_details or {}

            required_fields = [
                "land_holding",
                "land_size_acres",
                "caste_category",
                "received_same_component_last_10_years",
                "already_has_tractor"
            ]

            missing_fields = [
                field for field in required_fields
                if field not in farmer_details
                or farmer_details[field] is None
                or (
                    isinstance(farmer_details[field], str)
                    and not farmer_details[field].strip()
                )
            ]

            if missing_fields:
                results["eligibility"] = {
                    "status": "needs_information",
                    "missing_fields": missing_fields,
                    "message": (
                        "Please provide the following farmer details before "
                        f"checking eligibility: {', '.join(missing_fields)}."
                    )
                }
                continue

            # Call eligibility tool
            eligibility_result = check_scheme_eligibility(
                **{
                    field: farmer_details[field]
                    for field in required_fields
                }
            )

            results["eligibility"] = eligibility_result

        elif current_tool == "rag_search":

            if vector_collection is None:
                results["rag_search"] = {
                    "error": "ChromaDB collection is unavailable."
                }
                continue

            # Call existing RAG function
            rag_result = ask_question(
                question=question,
                vector_collection=vector_collection,
                embedding_model=embedding_model,
                top_k=3
            )

            results["rag_search"] = rag_result

    # Step 4: Return agent response
    return {
        "question": question,
        "tools_used": list(results.keys()),
        "results": results
    }

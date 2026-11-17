
from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt

from app.rag import ask_question
from app.tools import check_scheme_eligibility


class AgentState(TypedDict, total=False):
    question: str
    farmer_details: dict
    tools_to_use: list
    approved: bool
    results: dict
    status: str


def select_tools(state: AgentState):
    """Decide which tools are required."""

    question = state.get("question")
    if not isinstance(question, str) or not question.strip():
        raise ValueError("A non-empty question is required before selecting tools.")

    question = question.lower()

    eligibility_keywords = [
        "eligible",
        "eligibility",
        "qualify",
        "qualification"
    ]

    use_eligibility = any(
        word in question for word in eligibility_keywords
    )

    tools = []

    if use_eligibility:
        tools.append("eligibility")
    else:
        tools.append("rag_search")

    return {"tools_to_use": tools}


def approval_node(state: AgentState):
    """Pause and request human approval."""

    decision = interrupt({
        "message": "Please approve the agent's tool execution.",
        "tools": state["tools_to_use"],
        "question": state["question"]
    })

    approved = (
        decision is True
        or (
            isinstance(decision, dict)
            and decision.get("approved") is True
        )
    )

    return {
        "approved": approved,
        "status": "approved" if approved else "rejected"
    }


def approval_router(state: AgentState):
    if state.get("approved"):
        return "execute_tools"

    return END


def execute_tools(state: AgentState):
    """Execute RAG or eligibility tools."""

    results = {}
    selected_tools = state["tools_to_use"]

    for tool in selected_tools:

        if tool == "eligibility":
            farmer_details = state.get("farmer_details") or {}

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
            else:
                results["eligibility"] = check_scheme_eligibility(
                    **{
                        field: farmer_details[field]
                        for field in required_fields
                    }
                )

        elif tool == "rag_search":
            results["rag_search"] = ask_question(
                question=state["question"],
                vector_collection=VECTOR_COLLECTION,
                embedding_model=EMBEDDING_MODEL,
                top_k=3
            )

    status = (
        "needs_information"
        if any(
            result.get("status") == "needs_information"
            for result in results.values()
        )
        else "completed"
    )

    return {
        "results": results,
        "status": status
    }


def build_graph(vector_collection, embedding_model):
    """Build and compile the LangGraph workflow."""

    global VECTOR_COLLECTION, EMBEDDING_MODEL

    VECTOR_COLLECTION = vector_collection
    EMBEDDING_MODEL = embedding_model

    workflow = StateGraph(AgentState)

    workflow.add_node("select_tools", select_tools)
    workflow.add_node("approval", approval_node)
    workflow.add_node("execute_tools", execute_tools)

    workflow.add_edge(START, "select_tools")
    workflow.add_edge("select_tools", "approval")

    workflow.add_conditional_edges(
        "approval",
        approval_router,
        {
            "execute_tools": "execute_tools",
            END: END
        }
    )

    workflow.add_edge("execute_tools", END)

    memory = MemorySaver()

    return workflow.compile(checkpointer=memory)

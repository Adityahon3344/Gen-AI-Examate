
from typing import TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import interrupt

from app.rag import ask_question
from app.tools import check_scheme_eligibility

# --------------------------------------------------
# 1. Agent State
# --------------------------------------------------

class AgentState(TypedDict, total=False):
    question: str
    farmer_details: dict
    tools_to_use: list
    approved: bool
    results: dict
    status: str


# --------------------------------------------------
# 2. Required Farmer Details
# --------------------------------------------------

REQUIRED_FARMER_FIELDS = [
    "land_holding",
    "land_size_acres",
    "caste_category",
    "received_same_component_last_10_years",
    "already_has_tractor"
]


# --------------------------------------------------
# 3. Tool Selection Node
# --------------------------------------------------

def select_tools(state: AgentState):
    """Select the appropriate tool based on the question."""

    question = state.get("question")

    if not isinstance(question, str) or not question.strip():
        raise ValueError("A non-empty question is required.")

    question = question.lower()

    eligibility_keywords = [
        "eligible",
        "eligibility",
        "qualify",
        "qualification",
        "am i qualified",
        "check my eligibility"
    ]

    use_eligibility = any(
        keyword in question
        for keyword in eligibility_keywords
    )

    if use_eligibility:
        tools = ["eligibility"]
    else:
        tools = ["rag_search"]

    return {
        "tools_to_use": tools
    }


# --------------------------------------------------
# 4. Human Approval Node
# --------------------------------------------------

def approval_node(state: AgentState):
    """Pause execution and request human approval."""

    decision = interrupt({
        "message": "Please approve the agent's tool execution.",
        "tools": state.get("tools_to_use", []),
        "question": state.get("question", "")
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


# --------------------------------------------------
# 5. Approval Router
# --------------------------------------------------

def approval_router(state: AgentState):
    """Execute tools only after approval."""

    if state.get("approved") is True:
        return "execute_tools"

    return END


# --------------------------------------------------
# 6. Validate Farmer Details
# --------------------------------------------------

def validate_farmer_details(farmer_details: dict):
    """Identify missing farmer information."""

    if not isinstance(farmer_details, dict):
        farmer_details = {}

    missing_fields = []

    for field in REQUIRED_FARMER_FIELDS:

        value = farmer_details.get(field)

        if value is None or isinstance(value, str) and not value.strip():
            missing_fields.append(field)

    return missing_fields


# --------------------------------------------------
# 7. Tool Execution Node
# --------------------------------------------------

def execute_tools(state: AgentState, vector_collection, embedding_model):
    """Execute the approved tool."""

    results = {}

    selected_tools = state.get("tools_to_use", [])

    for tool in selected_tools:

        # ------------------------------------------
        # Eligibility Tool
        # ------------------------------------------

        if tool == "eligibility":

            farmer_details = state.get("farmer_details") or {}

            missing_fields = validate_farmer_details(
                farmer_details
            )

            if missing_fields:

                results["eligibility"] = {
                    "status": "needs_information",
                    "missing_fields": missing_fields,
                    "message": (
                        "Please provide the following farmer details: "
                        + ", ".join(missing_fields)
                    )
                }

            else:

                eligibility_details = {
                    field: farmer_details[field]
                    for field in REQUIRED_FARMER_FIELDS
                }

                results["eligibility"] = check_scheme_eligibility(
                    **eligibility_details
                )

        # ------------------------------------------
        # RAG Search Tool
        # ------------------------------------------

        elif tool == "rag_search":

            if vector_collection is None:
                raise RuntimeError(
                    "ChromaDB collection is not available."
                )

            results["rag_search"] = ask_question(
                question=state["question"],
                vector_collection=vector_collection,
                embedding_model=embedding_model,
                top_k=3
            )

        else:
            raise ValueError(f"Unknown tool selected: {tool}")

    # ------------------------------------------
    # Final Execution Status
    # ------------------------------------------

    needs_information = any(
        isinstance(result, dict)
        and result.get("status") == "needs_information"
        for result in results.values()
    )

    return {
        "results": results,
        "status": (
            "needs_information"
            if needs_information
            else "completed"
        )
    }


# --------------------------------------------------
# 8. Build LangGraph Workflow
# --------------------------------------------------

def build_graph(vector_collection, embedding_model):
    """Build and compile the LangGraph agent."""

    workflow = StateGraph(AgentState)

    # Register nodes

    workflow.add_node("select_tools", select_tools)

    workflow.add_node("approval", approval_node)

    workflow.add_node(
        "execute_tools",
        lambda state: execute_tools(
            state,
            vector_collection,
            embedding_model
        )
    )

    # Define workflow

    workflow.add_edge(
        START,
        "select_tools"
    )

    workflow.add_edge(
        "select_tools",
        "approval"
    )

    # Route according to approval

    workflow.add_conditional_edges(
        "approval",
        approval_router,
        {
            "execute_tools": "execute_tools",
            END: END
        }
    )

    workflow.add_edge(
        "execute_tools",
        END
    )

    # In-memory checkpoint storage

    memory = MemorySaver()

    # Compile graph

    graph = workflow.compile(
        checkpointer=memory
    )

    return graph

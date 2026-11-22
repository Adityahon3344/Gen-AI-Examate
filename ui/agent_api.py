import requests


def submit_direct_chat(api_url: str, question: str, timeout: int = 120):
    return requests.post(
        f"{api_url.rstrip('/')}/ask",
        json={"question": question},
        timeout=timeout,
    )


def submit_agent_question(
    api_url: str,
    question: str,
    farmer_details: dict | None = None,
    thread_id: str | None = None,
    timeout: int = 120,
):
    payload = {
        "question": question,
        "farmer_details": farmer_details or {},
    }
    if thread_id is not None:
        payload["thread_id"] = thread_id
    return requests.post(
        f"{api_url.rstrip('/')}/agent",
        json=payload,
        timeout=timeout,
    )


def submit_agent_decision(
    api_url: str,
    thread_id: str,
    approval: bool,
    timeout: int = 120,
):
    return requests.post(
        f"{api_url.rstrip('/')}/agent",
        json={"thread_id": thread_id, "approval": approval},
        timeout=timeout,
    )


def is_eligibility_question(question: str) -> bool:
    keywords = (
        "eligible",
        "eligibility",
        "qualify",
        "qualification",
        "am i qualified",
        "check my eligibility",
    )
    question_lower = question.casefold()
    return any(keyword in question_lower for keyword in keywords)


def validate_farmer_details(details: dict) -> list[str]:
    required_fields = (
        "land_holding",
        "land_size_acres",
        "caste_category",
        "received_same_component_last_10_years",
        "already_has_tractor",
    )
    missing = []

    for field in required_fields:
        value = details.get(field)
        if value is None or value == "" or (
            isinstance(value, str) and value.startswith("Select")
        ):
            missing.append(field)

    return missing


def store_agent_submission(
    state,
    question: str,
    farmer_details: dict,
    agent_response: dict,
) -> bool:
    state["agent_question"] = question
    state["last_question"] = question
    state["farmer_details"] = dict(farmer_details)
    state["agent_result"] = None
    state["agent_status"] = agent_response.get("status")
    state["agent_thread_id"] = None
    state["selected_tool"] = None
    state["approval_request"] = None
    state["agent_approval_request"] = None
    state["agent_approval_pending"] = False
    state["last_result"] = None
    state["agent_approval_status"] = None

    if agent_response.get("status") != "awaiting_approval":
        state["agent_status"] = "approval_required"
        return False

    thread_id = agent_response.get("thread_id")
    approvals = agent_response.get("approval_request")
    if not thread_id or not isinstance(approvals, list) or not approvals:
        state["agent_status"] = "approval_unavailable"
        return False

    approval = approvals[0]
    tools = approval.get("tools") or []
    if not tools:
        state["agent_status"] = "approval_unavailable"
        return False

    state["agent_thread_id"] = thread_id
    state["approval_request"] = approvals
    state["agent_approval_request"] = approvals
    state["selected_tool"] = tools[0]
    state["agent_status"] = "awaiting_approval"
    state["agent_approval_pending"] = True
    return True


def store_agent_decision(state, agent_response: dict, approved: bool) -> dict:
    state["agent_approval_pending"] = False
    state["approval_request"] = None
    state["agent_approval_request"] = None
    state["agent_approval_status"] = "approved" if approved else "rejected"

    if approved:
        result = normalize_agent_result(agent_response)
        state["agent_status"] = agent_response.get("status", "completed")
        state["agent_result"] = result
        state["last_result"] = result
        return result

    result = {
        "answer": "Agent execution rejected. No selected tool was executed.",
        "sources": [],
        "confidence": "Not applicable",
        "status": "rejected",
        "tools_to_use": [],
        "approved": False,
    }
    state["agent_status"] = "rejected"
    state["agent_result"] = result
    state["last_result"] = result
    return result


def normalize_agent_result(agent_response: dict) -> dict:
    results = agent_response.get("results") or {}
    rag_result = results.get("rag_search")
    eligibility_result = results.get("eligibility")

    if rag_result:
        return {
            "answer": rag_result.get("answer", "No answer returned."),
            "sources": rag_result.get("sources", []),
            "confidence": rag_result.get("confidence", "Not available"),
            "status": agent_response.get("status", "completed"),
            "tools_to_use": agent_response.get("tools_to_use", []),
            "approved": agent_response.get("approved"),
        }

    if eligibility_result:
        return {
            "answer": eligibility_result.get(
                "message",
                "Eligibility information is available below.",
            ),
            "sources": [],
            "confidence": "Eligibility tool result",
            "status": agent_response.get("status", "completed"),
            "tools_to_use": agent_response.get("tools_to_use", []),
            "approved": agent_response.get("approved"),
            "eligibility": eligibility_result,
        }

    return {
        "answer": (
            f"Agent status: {agent_response.get('status', 'Unknown')}\n\n"
            "No result was returned by the selected tool."
        ),
        "sources": [],
        "confidence": "Not available",
        "status": agent_response.get("status", "Unknown"),
        "tools_to_use": agent_response.get("tools_to_use", []),
        "approved": agent_response.get("approved"),
    }


def format_api_error(error: requests.RequestException) -> str:
    if isinstance(error, requests.exceptions.Timeout):
        return "The backend took too long to respond. Please try again."
    if isinstance(error, requests.exceptions.ConnectionError):
        return "Could not connect to the backend. Please check the API URL."

    response = getattr(error, "response", None)
    if response is not None:
        if response.status_code == 409:
            return (
                "This agent approval has expired or is no longer available. "
                "Please submit the question again."
            )
        if response.status_code >= 500:
            return (
                f"The backend encountered a server error "
                f"(HTTP {response.status_code}). Please try again later."
            )
        try:
            detail = response.json().get("detail")
        except (requests.exceptions.JSONDecodeError, ValueError):
            detail = None

        if detail:
            return f"Backend request failed (HTTP {response.status_code}): {detail}"
        return f"Backend request failed (HTTP {response.status_code})."

    return f"API request failed: {error}"

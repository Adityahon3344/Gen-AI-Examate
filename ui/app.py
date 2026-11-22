import json
import os
from pathlib import Path

import requests
import streamlit as st

if __package__:
    from .agent_api import (
        format_api_error,
        is_eligibility_question,
        store_agent_decision,
        store_agent_submission,
        submit_agent_decision,
        submit_agent_question,
        submit_direct_chat,
        validate_farmer_details,
    )
    from .document_bag import build_document_map, format_document_checklist
    from .feedback import save_feedback
else:
    from agent_api import (
        format_api_error,
        is_eligibility_question,
        store_agent_decision,
        store_agent_submission,
        submit_agent_decision,
        submit_agent_question,
        submit_direct_chat,
        validate_farmer_details,
    )
    from document_bag import build_document_map, format_document_checklist
    from feedback import save_feedback

# --------------------------------------------------
# 1. Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="KrishiYojana",
    layout="wide"
)

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
if "://" not in API_URL:
    API_URL = f"http://{API_URL}"
API_URL = API_URL.rstrip("/")

BASE_DIR = Path(__file__).resolve().parents[1]
RECORDS_FILE = BASE_DIR / "data" / "records.json"
FEEDBACK_FILE = Path(__file__).parent / "feedback.json"


# --------------------------------------------------
# 2. Load Scheme Records
# --------------------------------------------------

def load_records():

    with open(RECORDS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


records = load_records()


# --------------------------------------------------
# 4. Initialize Session State
# --------------------------------------------------

if (
    "agent_result" not in st.session_state
    and st.session_state.get("agent_status") == "completed"
):
    st.session_state.last_result = None
    st.session_state.agent_status = None

session_defaults = {
    "last_question": "",
    "last_result": None,
    "feedback_submitted": False,
    "agent_thread_id": None,
    "agent_question": "",
    "agent_approval_pending": False,
    "agent_approval_request": None,
    "approval_request": None,
    "selected_tool": None,
    "agent_status": None,
    "agent_approval_status": None,
    "agent_result": None,
    "agent_execution_busy": False,
    "farmer_details": {},
    "chat_mode": "Direct Chat",
}

for key, value in session_defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# --------------------------------------------------
# 6. Display Answer and Feedback
# --------------------------------------------------

def display_answer():

    if st.session_state.agent_approval_pending:
        return

    if (
        st.session_state.chat_mode == "AI Agent"
        and st.session_state.agent_result is None
    ):
        return

    if not st.session_state.last_result:
        return

    result = st.session_state.last_result

    st.divider()
    st.subheader("KrishiYojana Answer")

    eligibility_result = result.get("eligibility")
    if eligibility_result:
        st.subheader("Eligibility Result")
        status = eligibility_result.get("status", "Not available")
        st.write(f"**Eligibility status:** {status}")
        if "eligible" in eligibility_result:
            st.write(
                f"**Eligible:** {eligibility_result['eligible']}"
            )
        st.write(
            f"**Explanation:** {eligibility_result.get('message', 'No explanation returned.')}"
        )
        failed_rules = eligibility_result.get("failed_rules", [])
        if failed_rules:
            st.write("**Failed rules:**")
            for rule in failed_rules:
                st.write(f"- {rule}")
        missing_fields = eligibility_result.get("missing_fields", [])
        if missing_fields:
            st.warning(
                "More information is needed: "
                + ", ".join(missing_fields)
            )
    else:
        st.write(result.get("answer", "No answer returned."))

    st.caption(
        f"Confidence: {result.get('confidence', 'Not available')}"
    )

    if result.get("status"):
        if result["status"] == "completed" and result.get("approved") is True:
            st.success("Agent Execution Completed")
        else:
            st.caption(f"Agent execution status: {result['status']}")

    if result.get("tools_to_use"):
        st.caption(
            "Selected tools: " + ", ".join(result["tools_to_use"])
        )

    # Citations

    st.subheader("Sources")

    sources = result.get("sources", [])

    if sources:

        for source in sources:

            st.write(
                f"**Document:** {source.get('title', 'Unknown title')}"
            )

            st.write(
                f"**File:** {source.get('source', 'Unknown source')}"
            )

            st.write(
                f"**Page:** {source.get('page', 'Not available')}"
            )

            if source.get("url"):
                st.markdown(
                    f"[Open official source]({source['url']})"
                )

            st.divider()

    else:
        st.info("No source citations were returned.")

    # Feedback

    st.subheader("Was this answer helpful?")

    if not st.session_state.feedback_submitted:

        col1, col2 = st.columns(2)

        with col1:

            if st.button("Helpful", key="positive_feedback"):

                save_feedback(
                    FEEDBACK_FILE,
                    st.session_state.last_question,
                    result.get("answer", ""),
                    "positive"
                )

                st.session_state.feedback_submitted = True
                st.rerun()

        with col2:

            if st.button("Not Helpful", key="negative_feedback"):

                save_feedback(
                    FEEDBACK_FILE,
                    st.session_state.last_question,
                    result.get("answer", ""),
                    "negative"
                )

                st.session_state.feedback_submitted = True
                st.rerun()

    else:
        st.success("Thank you for your feedback!")


# --------------------------------------------------
# 7. Application Heading
# --------------------------------------------------

st.title("KrishiYojana")
st.subheader("AI-Powered Farmer Scheme Assistant")

st.write(
    "Ask questions about government agricultural schemes "
    "and prepare your document checklist."
)

chat_tab, bag_tab = st.tabs(["AI Chat", "Document Bag"])


# --------------------------------------------------
# 8. AI Chat Tab
# --------------------------------------------------

with chat_tab:

    st.subheader("Ask KrishiYojana")

    chat_mode = st.radio(
        "Choose chat mode:",
        ["Direct Chat", "AI Agent"],
        horizontal=True,
        key="chat_mode"
    )

    question = st.text_input(
        "Enter your question:",
        placeholder="What documents are required for this scheme?"
    )

    is_agent_mode = chat_mode == "AI Agent"
    eligibility_requested = (
        is_agent_mode and is_eligibility_question(question)
    )
    farmer_details = dict(st.session_state.farmer_details)
    eligibility_form_submitted = False

    if eligibility_requested:
        st.subheader("Farmer Eligibility Details")
        st.caption(
            "Enter each detail explicitly. The result is based on configured "
            "demonstration rules and is not a government eligibility guarantee."
        )
        with st.form("farmer_eligibility_form"):
            land_holding_options = ["Select land holding", "7/12 holder"]
            previous_land_holding = farmer_details.get("land_holding")
            land_holding_index = (
                land_holding_options.index(previous_land_holding)
                if previous_land_holding in land_holding_options
                else 0
            )
            land_holding = st.selectbox(
                "Land holding",
                land_holding_options,
                index=land_holding_index,
            )
            land_size_acres = st.number_input(
                "Land size (acres)",
                min_value=0.0,
                value=farmer_details.get("land_size_acres"),
                step=0.1,
            )

            caste_options = ["Select caste category", "SC", "ST", "OBC", "OPEN"]
            previous_caste = farmer_details.get("caste_category")
            caste_index = (
                caste_options.index(previous_caste)
                if previous_caste in caste_options
                else 0
            )
            caste_category = st.selectbox(
                "Caste category",
                caste_options,
                index=caste_index,
            )

            previous_options = ["Choose...", "Yes", "No"]
            previous_received = farmer_details.get(
                "received_same_component_last_10_years"
            )
            previous_index = (
                1 if previous_received is True
                else 2 if previous_received is False
                else 0
            )
            received_previous = st.radio(
                "Received the same component in the last 10 years?",
                previous_options,
                index=previous_index,
                horizontal=True,
            )
            tractor_value = farmer_details.get("already_has_tractor")
            tractor_index = (
                1 if tractor_value is True
                else 2 if tractor_value is False
                else 0
            )
            has_tractor = st.radio(
                "Already owns a tractor?",
                previous_options,
                index=tractor_index,
                horizontal=True,
            )
            eligibility_form_submitted = st.form_submit_button(
                "Send Question"
                if st.session_state.agent_status != "needs_information"
                else "Update Details and Resubmit",
                disabled=st.session_state.agent_execution_busy,
            )

        farmer_details = {
            "land_holding": (
                "" if land_holding == "Select land holding"
                else land_holding
            ),
            "land_size_acres": land_size_acres,
            "caste_category": (
                "" if caste_category == "Select caste category"
                else caste_category
            ),
            "received_same_component_last_10_years": (
                None if received_previous == "Choose..."
                else received_previous == "Yes"
            ),
            "already_has_tractor": (
                None if has_tractor == "Choose..."
                else has_tractor == "Yes"
            ),
        }

    send_question = False
    if is_agent_mode and not eligibility_requested:
        send_question = st.button(
            "Send Question",
            key="send_agent_question",
            disabled=st.session_state.agent_execution_busy,
        )
    elif not is_agent_mode:
        send_question = st.button(
            "Send Question",
            key="send_direct_question",
        )

    send_agent = (
        is_agent_mode
        and (eligibility_form_submitted or send_question)
    )

    if send_question and not question.strip():
        st.warning("Please enter your question first.")

    if send_agent and not question.strip():
        st.warning("Please enter your question first.")
    elif send_agent:
        missing_fields = (
            validate_farmer_details(farmer_details)
            if eligibility_requested
            else []
        )
        if missing_fields:
            st.warning(
                "Please provide the following information before sending: "
                + ", ".join(missing_fields)
            )
        else:
            st.session_state.agent_execution_busy = True
            st.session_state.agent_thread_id = None
            st.session_state.agent_question = question.strip()
            st.session_state.last_question = question.strip()
            st.session_state.farmer_details = dict(farmer_details)
            st.session_state.agent_status = "submitting"
            st.session_state.agent_approval_pending = False
            st.session_state.agent_approval_request = None
            st.session_state.approval_request = None
            st.session_state.selected_tool = None
            st.session_state.agent_result = None
            st.session_state.last_result = None
            try:
                with st.spinner("Sending question to the AI Agent..."):
                    response = submit_agent_question(
                        API_URL,
                        question.strip(),
                        farmer_details,
                    )
                    response.raise_for_status()
                    agent_response = response.json()
                    if not store_agent_submission(
                        st.session_state,
                        question.strip(),
                        farmer_details,
                        agent_response,
                    ):
                        st.error(
                            "The backend did not return a valid pending "
                            "approval. No result will be treated as approved. "
                            "Please retry or contact support."
                        )
                    else:
                        st.session_state.feedback_submitted = False
                        st.session_state.last_result = None
            except requests.exceptions.RequestException as error:
                st.session_state.agent_status = "error"
                st.error(format_api_error(error))
            except (json.JSONDecodeError, ValueError):
                st.session_state.agent_status = "error"
                st.error(
                    "The backend returned an invalid response. "
                    "Please try again."
                )
            finally:
                st.session_state.agent_execution_busy = False

    elif send_question:
        if not question.strip():
            st.warning("Please enter your question first.")
        else:
            try:
                with st.spinner("Finding your answer..."):
                    response = submit_direct_chat(
                        API_URL,
                        question.strip(),
                    )
                    response.raise_for_status()
                    result = response.json()
                    st.session_state.last_question = question.strip()
                    st.session_state.last_result = result
                    st.session_state.feedback_submitted = False
                    st.session_state.agent_thread_id = None
                    st.session_state.agent_approval_pending = False
                    st.session_state.agent_approval_request = None
                    st.session_state.approval_request = None
                    st.session_state.agent_status = None
                    st.session_state.agent_result = None
            except requests.exceptions.RequestException as error:
                st.error(format_api_error(error))
            except (json.JSONDecodeError, ValueError):
                st.error(
                    "The backend returned an invalid response. "
                    "Please try again."
                )

    if st.session_state.agent_approval_pending:
        st.divider()
        st.subheader("Human Approval Required")
        if not st.session_state.agent_thread_id:
            st.error(
                "The agent thread ID is missing. This approval cannot be "
                "resumed; please submit the question again."
            )
        st.warning(
            "The agent has not executed the selected tool. Choose whether "
            "to approve or reject it."
        )
        st.write(f"**Question:** {st.session_state.agent_question}")
        tool_labels = {
            "rag_search": "RAG Search",
            "eligibility": "Eligibility Check",
        }
        selected_tool = st.session_state.selected_tool
        st.write(
            "**Selected Tool:** "
            + tool_labels.get(selected_tool, selected_tool or "Unknown")
        )
        approvals = st.session_state.approval_request or []
        if approvals:
            st.info(approvals[0].get("message", "Approval is required."))

        approve_col, reject_col = st.columns(2)
        with approve_col:
            approve_clicked = st.button(
                "Approve Execution",
                key="approve_agent",
                disabled=(
                    st.session_state.agent_execution_busy
                    or not st.session_state.agent_thread_id
                ),
            )
        with reject_col:
            reject_clicked = st.button(
                "Reject Execution",
                key="reject_agent",
                disabled=(
                    st.session_state.agent_execution_busy
                    or not st.session_state.agent_thread_id
                ),
            )

        decision = (
            True if approve_clicked
            else False if reject_clicked
            else None
        )
        if decision is not None and st.session_state.agent_thread_id:
            st.session_state.agent_execution_busy = True
            try:
                with st.spinner(
                    "Executing approved tool..."
                    if decision
                    else "Rejecting tool execution..."
                ):
                    response = submit_agent_decision(
                        API_URL,
                        st.session_state.agent_thread_id,
                        decision,
                    )
                    response.raise_for_status()
                    agent_response = response.json()
                    store_agent_decision(
                        st.session_state,
                        agent_response,
                        decision,
                    )
                    st.session_state.feedback_submitted = False
                    if decision:
                        st.success("Agent Execution Completed")
                    else:
                        st.info(
                            "Agent execution rejected. "
                            "No selected tool was executed."
                        )
                    st.rerun()
            except requests.exceptions.RequestException as error:
                st.error(format_api_error(error))
                if (
                    isinstance(error, requests.exceptions.HTTPError)
                    and error.response is not None
                    and error.response.status_code == 409
                ):
                    st.session_state.agent_approval_pending = False
                    st.session_state.agent_thread_id = None
                    st.session_state.approval_request = None
                    st.session_state.agent_approval_request = None
                    st.session_state.agent_status = "approval_expired"
            except (json.JSONDecodeError, ValueError):
                st.error(
                    "The backend returned an invalid decision response."
                )
            finally:
                st.session_state.agent_execution_busy = False

    # --------------------------------------------------
    # 10. Display Answer
    # --------------------------------------------------

    if not st.session_state.agent_approval_pending:
        display_answer()


# --------------------------------------------------
# 11. Document Bag Tab
# --------------------------------------------------

with bag_tab:

    st.header("Your Document Bag")

    st.write(
        "Select up to 3 agricultural schemes. "
        "KrishiYojana will prepare one merged checklist."
    )

    scheme_names = [
        record["scheme_name"] for record in records
    ]

    selected_schemes = st.multiselect(
        "Select your schemes:",
        options=scheme_names,
        max_selections=3,
        placeholder="Choose 2 or 3 schemes"
    )

    if selected_schemes:

        document_map = build_document_map(records, selected_schemes)

        st.subheader("Merged Document Checklist")

        st.write(
            f"Total unique documents: **{len(document_map)}**"
        )

        # Display checklist

        for index, document in enumerate(document_map.values()):

            st.checkbox(
                document["name"],
                key=f"document_{index}"
            )

            st.caption(
                "Required for: " + ", ".join(document["schemes"])
            )

        # Download checklist

        checklist = format_document_checklist(document_map)

        st.download_button(
            label="Download Document Checklist",
            data=checklist,
            file_name="KrishiYojana_Document_Checklist.txt",
            mime="text/plain"
        )

    else:

        st.info(
            "Please select at least one scheme to prepare your document bag."
        )
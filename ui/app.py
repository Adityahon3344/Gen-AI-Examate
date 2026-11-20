import json
import os
from datetime import datetime
from pathlib import Path

import requests
import streamlit as st

# --------------------------------------------------
# 1. Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="KrishiYojana",
    layout="wide"
)

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

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
# 3. Feedback Storage
# --------------------------------------------------

def save_feedback(question, answer, rating):

    feedback = []

    if FEEDBACK_FILE.exists():

        with open(FEEDBACK_FILE, "r", encoding="utf-8") as file:
            feedback = json.load(file)

    feedback.append({
        "question": question,
        "answer": answer,
        "rating": rating,
        "timestamp": datetime.now().isoformat()
    })

    with open(FEEDBACK_FILE, "w", encoding="utf-8") as file:

        json.dump(
            feedback,
            file,
            indent=4,
            ensure_ascii=False
        )


# --------------------------------------------------
# 4. Initialize Session State
# --------------------------------------------------

session_defaults = {
    "last_question": "",
    "last_result": None,
    "feedback_submitted": False,
    "agent_thread_id": None,
    "agent_approval_pending": False,
    "agent_approval_request": None,
    "chat_mode": "Direct Chat"
}

for key, value in session_defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# --------------------------------------------------
# 5. Helper: Normalize Agent Result
# --------------------------------------------------

def normalize_agent_result(agent_response):

    results = agent_response.get("results", {})

    # RAG result
    rag_result = results.get("rag_search")

    if rag_result:

        return {
            "answer": rag_result.get("answer", "No answer returned."),
            "sources": rag_result.get("sources", []),
            "confidence": rag_result.get("confidence", "Not available")
        }

    # Eligibility result
    eligibility_result = results.get("eligibility")

    if eligibility_result:

        return {
            "answer": json.dumps(
                eligibility_result,
                indent=4,
                ensure_ascii=False
            ),
            "sources": [],
            "confidence": "Based on eligibility tool"
        }

    return {
        "answer": (
            f"Agent status: {agent_response.get('status', 'Unknown')}\n\n"
            "No result was returned by the selected tool."
        ),
        "sources": [],
        "confidence": "Not available"
    }


# --------------------------------------------------
# 6. Display Answer and Feedback
# --------------------------------------------------

def display_answer():

    if not st.session_state.last_result:
        return

    result = st.session_state.last_result

    st.divider()
    st.subheader("KrishiYojana Answer")

    st.write(result.get("answer", "No answer returned."))

    st.caption(
        f"Confidence: {result.get('confidence', 'Not available')}"
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
                    st.session_state.last_question,
                    result.get("answer", ""),
                    "positive"
                )

                st.session_state.feedback_submitted = True
                st.rerun()

        with col2:

            if st.button("Not Helpful", key="negative_feedback"):

                save_feedback(
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

    # Select chat mode

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

    if st.button("Send Question", key="send_question"):

        if not question.strip():

            st.warning("Please enter your question first.")

        else:

            try:

                with st.spinner("Finding your answer..."):

                    # Direct Chat

                    if chat_mode == "Direct Chat":

                        response = requests.post(
                            f"{API_URL}/ask",
                            json={
                                "question": question.strip()
                            },
                            timeout=120
                        )

                        response.raise_for_status()

                        result = response.json()

                        st.session_state.last_question = question
                        st.session_state.last_result = result
                        st.session_state.feedback_submitted = False

                        # Clear any previous agent approval state
                        st.session_state.agent_thread_id = None
                        st.session_state.agent_approval_pending = False
                        st.session_state.agent_approval_request = None

                    # AI Agent

                    else:

                        response = requests.post(
                            f"{API_URL}/agent",
                            json={
                                "question": question.strip(),
                                "farmer_details": {}
                            },
                            timeout=120
                        )

                        response.raise_for_status()

                        agent_response = response.json()

                        st.session_state.last_question = question
                        st.session_state.last_result = None
                        st.session_state.feedback_submitted = False

                        st.session_state.agent_thread_id = (
                            agent_response.get("thread_id")
                        )

                        st.session_state.agent_approval_pending = (
                            agent_response.get("status") == "approval_required"
                        )

                        st.session_state.agent_approval_request = (
                            agent_response.get("approval_request")
                        )

                        # If the agent completes without an interruption
                        if not st.session_state.agent_approval_pending:

                            st.session_state.last_result = (
                                normalize_agent_result(agent_response)
                            )

            except requests.exceptions.RequestException as error:

                st.error(f"API request failed: {error}")

    # --------------------------------------------------
    # 9. Agent Approval Section
    # --------------------------------------------------

    if st.session_state.agent_approval_pending:

        st.divider()
        st.subheader("Human Approval Required")

        st.warning(
            "The AI Agent has selected a tool. "
            "Please approve or reject its execution."
        )

        approval_requests = st.session_state.agent_approval_request or []

        for approval_request in approval_requests:

            st.write(
                f"**Question:** {approval_request.get('question', '')}"
            )

            st.write(
                f"**Selected tools:** "
                f"{', '.join(approval_request.get('tools', []))}"
            )

            st.info(
                approval_request.get(
                    "message",
                    "Approval is required."
                )
            )

        approve_col, reject_col = st.columns(2)

        with approve_col:

            if st.button("Approve", key="approve_agent"):

                try:

                    with st.spinner("Agent is executing the selected tool..."):

                        response = requests.post(
                            f"{API_URL}/agent",
                            json={
                                "thread_id": st.session_state.agent_thread_id,
                                "approval": True
                            },
                            timeout=120
                        )

                        response.raise_for_status()

                        agent_response = response.json()

                        st.session_state.agent_approval_pending = False
                        st.session_state.agent_approval_request = None

                        st.session_state.last_result = (
                            normalize_agent_result(agent_response)
                        )

                        st.session_state.feedback_submitted = False

                        st.rerun()

                except requests.exceptions.RequestException as error:

                    st.error(f"Approval request failed: {error}")

        with reject_col:

            if st.button("Reject", key="reject_agent"):

                try:

                    with st.spinner("Rejecting tool execution..."):

                        response = requests.post(
                            f"{API_URL}/agent",
                            json={
                                "thread_id": st.session_state.agent_thread_id,
                                "approval": False
                            },
                            timeout=120
                        )

                        response.raise_for_status()

                        agent_response = response.json()

                        st.session_state.agent_approval_pending = False
                        st.session_state.agent_approval_request = None
                        st.session_state.agent_thread_id = None
                        st.session_state.last_result = {
                            "answer": "You rejected the agent's tool execution. No tool was executed.",
                            "sources": [],
                            "confidence": "Not applicable"
                        }

                        st.session_state.feedback_submitted = False

                        st.rerun()

                except requests.exceptions.RequestException as error:

                    st.error(f"Rejection request failed: {error}")

    # --------------------------------------------------
    # 10. Display Answer
    # --------------------------------------------------

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

        document_map = {}

        # Collect and merge required documents

        for record in records:

            if record["scheme_name"] in selected_schemes:

                for document in record.get("required_documents", []):

                    normalized_name = document.strip().casefold()

                    if normalized_name not in document_map:

                        document_map[normalized_name] = {
                            "name": document.strip(),
                            "schemes": []
                        }

                    if (
                        record["scheme_name"]
                        not in document_map[normalized_name]["schemes"]
                    ):

                        document_map[normalized_name]["schemes"].append(
                            record["scheme_name"]
                        )

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

        checklist = "\n".join(
            [
                f"- {item['name']} | Required for: "
                f"{', '.join(item['schemes'])}"
                for item in document_map.values()
            ]
        )

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
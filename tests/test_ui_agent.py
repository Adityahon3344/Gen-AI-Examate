from pathlib import Path
from unittest.mock import patch

import requests
from streamlit.testing.v1 import AppTest

from ui.agent_api import (
    format_api_error,
    is_eligibility_question,
    normalize_agent_result,
    store_agent_submission,
    submit_agent_decision,
    submit_agent_question,
    submit_direct_chat,
    validate_farmer_details,
)

APP_PATH = Path(__file__).resolve().parents[1] / "ui" / "app.py"
API_URL = "http://127.0.0.1:8000"


class FakeResponse:
    def __init__(self, body, status_code=200):
        self.body = body
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            error = requests.HTTPError(
                f"HTTP {self.status_code}",
                response=self,
            )
            raise error

    def json(self):
        return self.body


def awaiting_response(tool="rag_search"):
    return FakeResponse(
        {
            "status": "awaiting_approval",
            "thread_id": "thread-123",
            "approval_request": [
                {
                    "message": "Please approve the agent's tool execution.",
                    "tools": [tool],
                    "question": "What is the objective?",
                }
            ],
        }
    )


def start_agent(app, question="What is the objective?"):
    app.radio[0].set_value("AI Agent").run()
    app.text_input[0].set_value(question)
    app.button(key="send_agent_question").click().run()
    return app


def test_initial_agent_submission_and_pending_approval():
    app = AppTest.from_file(APP_PATH, default_timeout=20).run()
    with patch(
        "requests.post",
        return_value=awaiting_response(),
    ) as post:
        start_agent(app)

    assert app.session_state["agent_status"] == "awaiting_approval"
    assert app.session_state["agent_approval_pending"] is True
    assert app.session_state["agent_thread_id"] == "thread-123"
    assert app.session_state["agent_question"] == "What is the objective?"
    assert app.session_state["selected_tool"] == "rag_search"
    assert "Human Approval Required" in [
        item.value for item in app.subheader
    ]
    assert "Approve Execution" in [button.label for button in app.button]
    assert "Reject Execution" in [button.label for button in app.button]
    assert "KrishiYojana Answer" not in [
        item.value for item in app.subheader
    ]
    post.assert_called_once_with(
        f"{API_URL}/agent",
        json={
            "question": "What is the objective?",
            "farmer_details": {},
        },
        timeout=120,
    )


def test_direct_chat_still_posts_to_ask():
    app = AppTest.from_file(APP_PATH, default_timeout=20).run()
    with patch(
        "requests.post",
        return_value=FakeResponse(
            {
                "question": "What documents are required?",
                "answer": "Bring a land record.",
                "sources": [],
                "confidence": "high",
            }
        ),
    ) as post:
        app.text_input[0].set_value("What documents are required?")
        app.button(key="send_direct_question").click().run()

    post.assert_called_once_with(
        f"{API_URL}/ask",
        json={"question": "What documents are required?"},
        timeout=120,
    )
    assert app.session_state["last_result"]["answer"] == (
        "Bring a land record."
    )


def test_awaiting_approval_state_stores_tool_and_thread():
    state = {}
    accepted = store_agent_submission(
        state,
        "Am I eligible?",
        {"land_holding": "7/12 holder"},
        awaiting_response("eligibility").json(),
    )

    assert accepted is True
    assert state["agent_thread_id"] == "thread-123"
    assert state["selected_tool"] == "eligibility"
    assert state["agent_status"] == "awaiting_approval"
    assert state["agent_approval_pending"] is True
    assert state["farmer_details"] == {"land_holding": "7/12 holder"}


def test_approval_button_posts_true_only_after_click():
    completed = FakeResponse(
        {
            "status": "completed",
            "thread_id": "thread-123",
            "tools_to_use": ["rag_search"],
            "approved": True,
            "results": {
                "rag_search": {
                    "answer": "Farm mechanization improves access.",
                    "sources": [{"title": "Scheme guide", "page": 2}],
                    "confidence": "high",
                }
            },
        }
    )
    app = AppTest.from_file(APP_PATH, default_timeout=20).run()
    with patch(
        "requests.post",
        side_effect=[awaiting_response(), completed],
    ) as post:
        start_agent(app)
        assert post.call_count == 1
        app.button(key="approve_agent").click().run()

    assert post.call_count == 2
    assert post.call_args_list[1].kwargs["json"] == {
        "thread_id": "thread-123",
        "approval": True,
    }
    assert app.session_state["agent_approval_pending"] is False
    assert app.session_state["agent_status"] == "completed"
    assert app.session_state["agent_result"]["answer"] == (
        "Farm mechanization improves access."
    )
    assert app.session_state["agent_result"]["sources"][0]["page"] == 2
    assert any(
        "Agent Execution Completed" in item.value
        for item in app.success
    )


def test_reject_button_posts_false_and_clears_pending_state():
    rejected = FakeResponse(
        {
            "status": "rejected",
            "thread_id": "thread-123",
            "tools_to_use": ["rag_search"],
            "approved": False,
            "results": {},
        }
    )
    app = AppTest.from_file(APP_PATH, default_timeout=20).run()
    with patch(
        "requests.post",
        side_effect=[awaiting_response(), rejected],
    ) as post:
        start_agent(app)
        app.button(key="reject_agent").click().run()

    assert post.call_args_list[1].kwargs["json"] == {
        "thread_id": "thread-123",
        "approval": False,
    }
    assert app.session_state["agent_approval_pending"] is False
    assert app.session_state["agent_status"] == "rejected"
    assert app.session_state["agent_result"]["answer"] == (
        "Agent execution rejected. No selected tool was executed."
    )


def test_pending_thread_survives_streamlit_rerun():
    app = AppTest.from_file(APP_PATH, default_timeout=20).run()
    with patch("requests.post", return_value=awaiting_response()):
        start_agent(app)
        app.run()

    assert app.session_state["agent_thread_id"] == "thread-123"
    assert app.session_state["agent_approval_pending"] is True
    assert "Approve Execution" in [button.label for button in app.button]


def test_eligibility_form_requires_explicit_values():
    app = AppTest.from_file(APP_PATH, default_timeout=20).run()
    with patch("requests.post") as post:
        app.radio[0].set_value("AI Agent").run()
        app.text_input[0].set_value("Am I eligible for this scheme?").run()
        app.button[0].click().run()

    assert post.call_count == 0
    assert any("Please provide" in warning.value for warning in app.warning)
    assert validate_farmer_details(
        {
            "land_holding": "7/12 holder",
            "land_size_acres": None,
            "caste_category": "SC",
            "received_same_component_last_10_years": False,
            "already_has_tractor": False,
        }
    ) == ["land_size_acres"]


def test_eligibility_submission_uses_values_allowed_by_rules():
    app = AppTest.from_file(APP_PATH, default_timeout=20).run()
    with patch(
        "requests.post",
        return_value=awaiting_response("eligibility"),
    ) as post:
        app.radio[0].set_value("AI Agent").run()
        app.text_input[0].set_value("Am I eligible for this scheme?").run()
        app.selectbox[0].set_value("7/12 holder")
        app.number_input[0].set_value(2.0)
        app.selectbox[1].set_value("OPEN")
        app.radio[1].set_value("No")
        app.radio[2].set_value("No")
        app.button[0].click().run()

    assert app.session_state["agent_approval_pending"] is True
    assert post.call_args.kwargs["json"]["farmer_details"] == {
        "land_holding": "7/12 holder",
        "land_size_acres": 2.0,
        "caste_category": "OPEN",
        "received_same_component_last_10_years": False,
        "already_has_tractor": False,
    }


def test_eligibility_results_are_structured():
    result = normalize_agent_result(
        {
            "status": "needs_information",
            "tools_to_use": ["eligibility"],
            "approved": True,
            "results": {
                "eligibility": {
                    "eligible": False,
                    "status": "needs_information",
                    "failed_rules": [],
                    "missing_fields": ["land_holding"],
                    "message": "Please provide land holding.",
                }
            },
        }
    )

    assert result["eligibility"]["eligible"] is False
    assert result["eligibility"]["missing_fields"] == ["land_holding"]
    assert result["answer"] == "Please provide land holding."


def test_rag_results_keep_answer_citations_and_confidence():
    result = normalize_agent_result(
        {
            "status": "completed",
            "tools_to_use": ["rag_search"],
            "approved": True,
            "results": {
                "rag_search": {
                    "answer": "The scheme supports farm machinery [Source 1].",
                    "sources": [
                        {
                            "title": "Scheme guide",
                            "source": "guide.pdf",
                            "page": 2,
                        }
                    ],
                    "confidence": "high",
                }
            },
        }
    )

    assert result["answer"].endswith("[Source 1].")
    assert result["sources"][0]["page"] == 2
    assert result["confidence"] == "high"


def test_backend_connection_error_is_shown_without_approval():
    app = AppTest.from_file(APP_PATH, default_timeout=20).run()
    with patch(
        "requests.post",
        side_effect=requests.exceptions.ConnectionError("unavailable"),
    ) as post:
        start_agent(app)

    assert post.call_count == 1
    assert app.session_state["agent_approval_pending"] is False
    assert any("Could not connect" in error.value for error in app.error)


def test_initial_completed_response_never_displays_result_as_approved():
    app = AppTest.from_file(APP_PATH, default_timeout=20).run()
    with patch(
        "requests.post",
        return_value=FakeResponse(
            {
                "status": "completed",
                "thread_id": "thread-123",
                "tools_to_use": ["eligibility"],
                "approved": True,
                "results": {"eligibility": {"eligible": True}},
            }
        ),
    ) as post:
        start_agent(app, "What is the objective?")

    assert post.call_count == 1
    assert app.session_state["agent_approval_pending"] is False
    assert app.session_state["agent_result"] is None
    assert app.session_state["last_result"] is None
    assert any(
        "did not return a valid pending approval" in error.value
        for error in app.error
    )


def test_agent_question_is_detected():
    assert is_eligibility_question("Am I eligible for this scheme?")
    assert is_eligibility_question("Am I qualified for this scheme?")
    assert not is_eligibility_question("What is the objective?")


def test_endpoint_helpers_use_expected_paths_and_payloads():
    with patch("ui.agent_api.requests.post") as post:
        submit_direct_chat(API_URL, "Question")
        submit_agent_question(API_URL, "Question")
        submit_agent_decision(API_URL, "thread-123", True)

    assert [call.args[0] for call in post.call_args_list] == [
        f"{API_URL}/ask",
        f"{API_URL}/agent",
        f"{API_URL}/agent",
    ]
    assert post.call_args_list[1].kwargs["json"] == {
        "question": "Question",
        "farmer_details": {},
    }
    assert post.call_args_list[2].kwargs["json"] == {
        "thread_id": "thread-123",
        "approval": True,
    }


def test_api_errors_are_friendly_including_expired_checkpoints():
    assert format_api_error(
        requests.exceptions.ConnectionError()
    ).startswith("Could not connect")
    assert format_api_error(requests.exceptions.Timeout()).startswith(
        "The backend took too long"
    )
    expired = FakeResponse({"detail": "checkpoint expired"}, status_code=409)
    error = requests.HTTPError(response=expired)
    assert "expired or is no longer available" in format_api_error(error)

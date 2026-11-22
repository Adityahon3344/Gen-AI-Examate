import json
import sys
from pathlib import Path
from types import ModuleType
from unittest.mock import Mock

import pytest
from streamlit.testing.v1 import AppTest

from ui.document_bag import build_document_map, format_document_checklist
from ui.feedback import save_feedback

APP_PATH = Path(__file__).resolve().parents[1] / "ui" / "app.py"
RECORDS_PATH = Path(__file__).resolve().parents[1] / "data" / "records.json"


def test_document_bag_deduplicates_and_maps_schemes():
    records = json.loads(RECORDS_PATH.read_text(encoding="utf-8"))
    selected = [
        "Sub-mission on Farm Mechanization",
        "State Agriculture Mechanization Scheme",
    ]

    document_map = build_document_map(records, selected)
    checklist = format_document_checklist(document_map)
    land_record = document_map["7/12 extract"]

    assert len(document_map) == 8
    assert land_record["schemes"] == selected
    assert checklist.casefold().count("7/12 extract") == 1
    assert "Required for: " + ", ".join(selected) in checklist


def test_document_bag_ui_offers_checklist_download():
    app = AppTest.from_file(APP_PATH, default_timeout=20).run()
    app.multiselect[0].set_value(
        [
            "Sub-mission on Farm Mechanization",
            "State Agriculture Mechanization Scheme",
        ]
    ).run()

    assert not app.exception
    assert any(
        item.value == "Total unique documents: **8**"
        for item in app.markdown
    )
    assert [button.label for button in app.get("download_button")] == [
        "Download Document Checklist"
    ]


def test_feedback_storage_appends_to_the_supplied_file(tmp_path):
    feedback_file = tmp_path / "feedback.json"

    save_feedback(feedback_file, "Question", "Answer", "positive")
    save_feedback(feedback_file, "Another question", "Another answer", "negative")

    feedback = json.loads(feedback_file.read_text(encoding="utf-8"))
    assert [item["rating"] for item in feedback] == ["positive", "negative"]
    assert feedback[0]["question"] == "Question"
    assert feedback[1]["answer"] == "Another answer"
    assert all(item["timestamp"] for item in feedback)


@pytest.mark.parametrize(
    ("button_key", "rating"),
    [
        ("positive_feedback", "positive"),
        ("negative_feedback", "negative"),
    ],
)
def test_feedback_buttons_submit_selected_rating(
    monkeypatch,
    button_key,
    rating,
):
    save_feedback_mock = Mock()
    feedback_module = ModuleType("feedback")
    feedback_module.save_feedback = save_feedback_mock
    monkeypatch.setitem(sys.modules, "feedback", feedback_module)
    app = AppTest.from_file(APP_PATH, default_timeout=20).run()
    app.session_state["last_question"] = "Scheme question"
    app.session_state["last_result"] = {
        "answer": "Grounded answer",
        "sources": [],
        "confidence": "medium",
    }
    app.run()

    app.button(key=button_key).click().run()

    save_feedback_mock.assert_called_once_with(
        APP_PATH.parent / "feedback.json",
        "Scheme question",
        "Grounded answer",
        rating,
    )

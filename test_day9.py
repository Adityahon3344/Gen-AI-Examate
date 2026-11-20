import unittest
from unittest.mock import patch

import numpy as np
from fastapi.testclient import TestClient

from app import main
from app.agent_loop import run_agent
from app.graph import build_graph


class FakeEmbeddingModel:
    def encode(self, questions, normalize_embeddings=True):
        embeddings = np.ones((len(questions), 2), dtype=float)
        if normalize_embeddings:
            embeddings /= np.linalg.norm(embeddings, axis=1, keepdims=True)
        return embeddings


class FakeVectorCollection:
    def count(self):
        return 1

    def query(self, **_kwargs):
        if "query_embeddings" not in _kwargs:
            raise AssertionError("query_embeddings is required")
        return {
            "ids": [["chunk-1"]],
            "documents": [["A test document chunk."]],
            "metadatas": [[{"source": "test.pdf", "page": 1, "title": "Test"}]],
            "distances": [[0.1]],
        }


class DayNineWorkflowTests(unittest.TestCase):
    def setUp(self):
        patches = (
            patch.object(main, "vector_collection", FakeVectorCollection()),
            patch.object(main, "embedding_model", FakeEmbeddingModel()),
            patch.object(
                main,
                "generate_response",
                return_value=(
                    '{"answer":"Test answer","confidence":0.9,'
                    '"follow_up":null}'
                ),
            ),
            patch.object(
                main,
                "ask_question",
                return_value={"answer": "Test RAG answer", "sources": []},
            ),
            patch.object(main, "agent_graph", build_graph(None, None)),
            patch(
                "app.graph.ask_question",
                return_value={"answer": "Test graph answer", "sources": []},
            ),
        )
        self.patchers = list(patches)
        for patcher in self.patchers:
            patcher.start()
        self.client = TestClient(main.app)

    def tearDown(self):
        for patcher in reversed(self.patchers):
            patcher.stop()

    def test_existing_api_endpoints(self):
        self.assertEqual(self.client.get("/health").status_code, 200)
        self.assertEqual(self.client.get("/records").status_code, 200)
        self.assertEqual(self.client.get("/records/1").status_code, 200)
        self.assertEqual(
            self.client.get("/search", params={"q": "tractor"}).status_code,
            200,
        )
        self.assertEqual(
            self.client.post(
                "/questions", json={"question": "tractor"}
            ).status_code,
            200,
        )
        self.assertEqual(
            self.client.get(
                "/search/semantic", params={"q": "tractor"}
            ).status_code,
            200,
        )
        self.assertEqual(
            self.client.post(
                "/chat", json={"question": "What is the scheme?"}
            ).status_code,
            200,
        )
        self.assertEqual(
            self.client.post(
                "/ask", json={"question": "What is the scheme?"}
            ).status_code,
            200,
        )

    def test_rejection_resumes_the_pending_thread(self):
        initial = self.client.post(
            "/agent",
            json={"question": "Am I eligible?", "farmer_details": {}},
        )
        self.assertEqual(initial.status_code, 200)
        self.assertEqual(initial.json()["status"], "awaiting_approval")
        thread_id = initial.json()["thread_id"]

        rejected = self.client.post(
            "/agent",
            json={"thread_id": thread_id, "approval": False},
        )
        self.assertEqual(rejected.status_code, 200)
        self.assertEqual(rejected.json()["thread_id"], thread_id)
        self.assertEqual(rejected.json()["status"], "rejected")
        self.assertEqual(rejected.json()["results"], {})

    def test_approval_runs_eligibility_for_eligible_and_ineligible_farmers(self):
        farmers = (
            {
                "land_holding": "7/12 holder",
                "land_size_acres": 2.0,
                "caste_category": "OBC",
                "received_same_component_last_10_years": False,
                "already_has_tractor": False,
                "expected": True,
            },
            {
                "land_holding": "Not registered",
                "land_size_acres": 0.2,
                "caste_category": "OPEN",
                "received_same_component_last_10_years": True,
                "already_has_tractor": True,
                "expected": False,
            },
        )
        for index, farmer in enumerate(farmers):
            with self.subTest(eligible=farmer["expected"]):
                expected = farmer.pop("expected")
                initial = self.client.post(
                    "/agent",
                    json={
                        "question": "Check my eligibility",
                        "farmer_details": farmer,
                        "thread_id": f"day9-eligibility-{index}",
                    },
                )
                self.assertEqual(initial.json()["status"], "awaiting_approval")
                thread_id = initial.json()["thread_id"]

                approved = self.client.post(
                    "/agent",
                    json={"thread_id": thread_id, "approval": True},
                )
                self.assertEqual(approved.status_code, 200)
                self.assertEqual(approved.json()["thread_id"], thread_id)
                self.assertEqual(approved.json()["status"], "completed")
                self.assertEqual(
                    approved.json()["results"]["eligibility"]["eligible"],
                    expected,
                )

    def test_missing_farmer_details_are_requested(self):
        initial = self.client.post(
            "/agent",
            json={
                "question": "Check my eligibility",
                "farmer_details": {
                    "land_size_acres": "",
                    "already_has_tractor": False,
                },
            },
        )
        approved = self.client.post(
            "/agent",
            json={
                "thread_id": initial.json()["thread_id"],
                "approval": True,
            },
        )
        self.assertEqual(approved.json()["status"], "needs_information")
        eligibility = approved.json()["results"]["eligibility"]
        self.assertEqual(eligibility["status"], "needs_information")
        self.assertIn("land_holding", eligibility["missing_fields"])
        self.assertIn("land_size_acres", eligibility["missing_fields"])
        self.assertNotIn("already_has_tractor", eligibility["missing_fields"])
        self.assertIn("Please provide", eligibility["message"])

    def test_resume_without_a_checkpoint_returns_clear_conflict(self):
        response = self.client.post(
            "/agent",
            json={"thread_id": "missing-checkpoint", "approval": False},
        )
        self.assertEqual(response.status_code, 409)
        self.assertIn("In-memory checkpoints", response.json()["detail"])

    def test_simple_agent_requests_all_missing_farmer_details(self):
        result = run_agent(
            question="Am I eligible?",
            vector_collection=None,
            embedding_model=None,
        )
        eligibility = result["results"]["eligibility"]
        self.assertEqual(eligibility["status"], "needs_information")
        self.assertEqual(
            eligibility["missing_fields"],
            [
                "land_holding",
                "land_size_acres",
                "caste_category",
                "received_same_component_last_10_years",
                "already_has_tractor",
            ],
        )


if __name__ == "__main__":
    unittest.main()

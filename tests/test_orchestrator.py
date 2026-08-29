"""
Owner: Rohit.

Start here — these tests run against the stub nodes today and should
keep passing (with richer assertions) as real logic replaces the stubs.
"""

from src.agents.orchestrator import get_compiled_graph


def test_graph_runs_end_to_end():
    app = get_compiled_graph()
    result = app.invoke({"query": "test query", "story_id": "story_test"})
    assert "report" in result

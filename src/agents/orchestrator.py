"""
LangGraph orchestrator (owner: Akshat).

Wires the four specialized agents into a fan-out / fan-in graph:

            retrieve
               |
        +------+------+------+
        |      |      |      |
     claims  persp  timeline impact
        |      |      |      |
        +------+------+------+
               |
        report_generation

Each agent node is a stub for now — teammates can build against
AgentState from src/schemas/contracts.py without waiting on the
real implementations here.
"""

from langgraph.graph import StateGraph, START, END
from src.schemas.contracts import AgentState


# ---------------------------------------------------------------------------
# Node stubs — replace bodies with real logic. Signature must stay the same.
# ---------------------------------------------------------------------------

def retrieve(state: AgentState) -> AgentState:
    """Pull relevant articles from the data store for this query."""
    # TODO: embed query, similarity search against src/storage
    return {"retrieved_articles": []}


def claim_verification(state: AgentState) -> AgentState:
    return {"claims": []}


def perspective_analysis(state: AgentState) -> AgentState:
    return {"perspectives": []}


def timeline_analysis(state: AgentState) -> AgentState:
    return {"timeline": []}


def impact_analysis(state: AgentState) -> AgentState:
    return {"impacts": []}


def report_generation(state: AgentState) -> AgentState:
    """Synthesizes all four agent outputs into a single Report."""
    # TODO: build Report(...) from state["claims"], state["perspectives"], etc.
    return {"report": None}


# ---------------------------------------------------------------------------
# Graph wiring
# ---------------------------------------------------------------------------

def build_graph() -> StateGraph:
    graph = StateGraph(AgentState)

    graph.add_node("retrieve", retrieve)
    graph.add_node("claim_verification", claim_verification)
    graph.add_node("perspective_analysis", perspective_analysis)
    graph.add_node("timeline_analysis", timeline_analysis)
    graph.add_node("impact_analysis", impact_analysis)
    graph.add_node("report_generation", report_generation)

    graph.add_edge(START, "retrieve")

    # fan-out: all four agents run off the retrieved articles
    for agent in [
        "claim_verification",
        "perspective_analysis",
        "timeline_analysis",
        "impact_analysis",
    ]:
        graph.add_edge("retrieve", agent)
        # fan-in: all four must complete before report_generation runs
        graph.add_edge(agent, "report_generation")

    graph.add_edge("report_generation", END)

    return graph


def get_compiled_graph():
    return build_graph().compile()


if __name__ == "__main__":
    app = get_compiled_graph()
    result = app.invoke({"query": "example query", "story_id": "story_001"})
    print(result)

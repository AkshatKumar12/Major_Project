from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END

from src.agents.claim_verification import extract_and_verify_claims
from src.agents.perspective_analysis import analyze_perspective
from src.agents.timeline_analysis import extract_timeline
from src.agents.impact_analysis import analyze_impact
from src.agents.report_generation import generate_final_report
from src.schemas.contracts import AgentOutput, FinalReport


class PipelineState(TypedDict):
    query: str
    content: str
    source_urls: List[str]
    claims: List[str]
    perspective: str
    timeline: List[str]
    impact: str
    final_report: FinalReport

async def claim_node(state: PipelineState):
    return {"claims": await extract_and_verify_claims(state["content"])}

async def perspective_node(state: PipelineState):
    return {"perspective": await analyze_perspective(state["content"])}

async def timeline_node(state: PipelineState):
    return {"timeline": await extract_timeline(state["content"])}

async def impact_node(state: PipelineState):
    return {"impact": await analyze_impact(state["content"])}

async def synthesis_node(state: PipelineState):
    agent_output = AgentOutput(
        claims=state.get("claims", []),
        perspective=state.get("perspective", ""),
        timeline=state.get("timeline", []),
        impact=state.get("impact", "")
    )
    report = await generate_final_report(
        query=state["query"],
        agent_output=agent_output,
        source_urls=state.get("source_urls", [])
    )
    return {"final_report": report}

# Compile Graph
builder = StateGraph(PipelineState)
builder.add_node("claims_agent", claim_node)
builder.add_node("perspective_agent", perspective_node)
builder.add_node("timeline_agent", timeline_node)
builder.add_node("impact_agent", impact_node)
builder.add_node("report_synthesizer", synthesis_node)

builder.add_edge(START, "claims_agent")
builder.add_edge(START, "perspective_agent")
builder.add_edge(START, "timeline_agent")
builder.add_edge(START, "impact_agent")

builder.add_edge("claims_agent", "report_synthesizer")
builder.add_edge("perspective_agent", "report_synthesizer")
builder.add_edge("timeline_agent", "report_synthesizer")
builder.add_edge("impact_agent", "report_synthesizer")

builder.add_edge("report_synthesizer", END)
news_analysis_graph = builder.compile()

async def run_analysis_pipeline(query: str, aggregated_content: str, source_urls: List[str] = None) -> FinalReport:
    initial_state = {
        "query": query,
        "content": aggregated_content,
        "source_urls": source_urls or [],
        "claims": [],
        "perspective": "",
        "timeline": [],
        "impact": "",
        "final_report": None
    }
    output_state = await news_analysis_graph.ainvoke(initial_state)
    return output_state["final_report"]

import os
from litellm import acompletion
from src.schemas.contracts import AgentOutput, FinalReport
from src.config import SYNTHESIS_MODEL as model_name
from src.config import max_tok

async def generate_final_report(query: str, agent_output: AgentOutput, source_urls: list[str]) -> FinalReport:
    """
    Synthesizes the four agent outputs into an executive summary and returns a structured FinalReport.
    """
    
    prompt = (
            f"You are a senior intelligence and news editor. Synthesize the following multi-perspective analysis "
            f"for the query: '{query}' into a clear, comprehensive executive summary (2-3 paragraphs).\n\n"
            f"CRITICAL INSTRUCTION: Do NOT include any internal thinking, reasoning process, or meta-commentary. "
            f"Output ONLY the final executive summary.\n\n"
            f"Key Claims:\n" + "\n".join(f"- {c}" for c in agent_output.claims) + "\n\n"
            f"Perspective / Bias:\n{agent_output.perspective}\n\n"
            f"Timeline of Events:\n" + "\n".join(f"- {t}" for t in agent_output.timeline) + "\n\n"
            f"Impact Analysis:\n{agent_output.impact}\n\n"
            "Synthesized Executive Summary:"
        )
    
    try:
        response = await acompletion(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tok
        )
        summary = response.choices[0].message.content
        
    except Exception as e:
        print(f"Error in report synthesis: {e}")
        summary = "Report synthesis encountered an error."
        
    return FinalReport(
        query=query,
        summary=summary,
        detailed_analysis=agent_output,
        source_articles=source_urls
    )
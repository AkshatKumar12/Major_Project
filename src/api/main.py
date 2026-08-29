"""
Backend API entrypoint (owner: Anmol).

Exposes the pipeline to the frontend:
  POST /query   -> triggers on-demand scrape + runs the LangGraph pipeline
  GET  /report/{story_id} -> fetch a previously generated report
"""

from fastapi import FastAPI
from pydantic import BaseModel

from src.agents.orchestrator import get_compiled_graph

app = FastAPI(title="News Analysis API")
graph = get_compiled_graph()


class QueryRequest(BaseModel):
    query: str  # article text or URL


@app.post("/query")
def submit_query(req: QueryRequest):
    # TODO: trigger on-demand scraper, then invoke the graph
    result = graph.invoke({"query": req.query})
    return result


@app.get("/report/{story_id}")
def get_report(story_id: str):
    # TODO: fetch stored Report from src.storage.db
    raise NotImplementedError

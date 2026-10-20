from contextlib import asynccontextmanager
from datetime import datetime
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from fastapi.responses import Response

# Schemas
from src.schemas.contracts import AnalysisRequest, FinalReport, AgentOutput

# Agents & Pipeline
from src.agents.orchestrator import run_analysis_pipeline

# Ingestion
from src.ingestion.on_demand_scraper import run_on_demand_scrape
from src.ingestion.dedup_cluster import process_and_cluster
from src.ingestion.scheduled_scraper import start_scheduler

# Storage / DB
from src.storage.db import init_db, save_report, get_all_reports_from_db

# Utils
from src.utils.pdf_generator import create_pdf

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database tables
    await init_db()
    # Start the scheduled background scraper
    start_scheduler()
    yield

app = FastAPI(
    title="News Analysis System",
    description="API for on-demand news scraping, AI analysis, and reporting.",
    version="1.0.0",
    lifespan=lifespan
)

@app.post("/api/analyze", response_model=FinalReport)
async def analyze_topic(request: AnalysisRequest):
    try:
        # 1. Ingest Data
        scraped_data = await run_on_demand_scrape(request.query)
        
        # 2. Process & Deduplicate
        aggregated_content, source_urls = process_and_cluster(scraped_data)
        
        if not aggregated_content.strip():
            raise HTTPException(status_code=400, detail="No substantial content could be scraped for this query.")
        
        # 3. Analyze & Synthesize
        report = await run_analysis_pipeline(
            query=request.query,
            aggregated_content=aggregated_content,
            source_urls=source_urls
        )
        
        # 4. Save the final report
        await save_report(report)
        
        return report
    except Exception as e:
        print(f"Error in analyze endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/history")
async def get_search_history():
    """Returns past reports from SQLite for the sidebar history."""
    try:
        reports = await get_all_reports_from_db()
        return {"history": reports}
    except Exception as e:
        return {"history": [], "error": str(e)}

@app.get("/api/download-pdf")
async def download_report_pdf(query: str):
    """Generates and streams a PDF for a specific report."""
    try:
        reports = await get_all_reports_from_db()
        match = next((r for r in reports if r["query"].lower() == query.lower()), None)
        
        if not match:
            raise HTTPException(status_code=404, detail="Report not found in database.")
            
        gen_time = match["generated_at"]
        if isinstance(gen_time, str):
            try:
                gen_time = datetime.fromisoformat(gen_time)
            except ValueError:
                gen_time = datetime.utcnow()

        report_obj = FinalReport(
            query=match["query"],
            summary=match["summary"],
            detailed_analysis=AgentOutput(**match["detailed_analysis"]),
            source_articles=match["source_articles"],
            generated_at=gen_time
        )
        
        pdf_bytes = create_pdf(report_obj)
        clean_filename = "".join(c for c in match["query"] if c.isalnum() or c in (" ", "_")).replace(" ", "_")
        
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="Report_{clean_filename}.pdf"'}
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
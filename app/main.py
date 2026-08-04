from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict, Optional

from app.agent import ask_agent
from app.tools import experience_analysis, dashboard_summary, lob_product_breakdown, lob_graph_data
from app.assumption_setting import run_assumption_setting, OUTPUT_DIR
from app.red_zone import identify_red_zone, red_zone_product_breakdown, generate_single_cohort_prophet_file

app = FastAPI(title="Insurance AI Agent", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Question(BaseModel):
    question: str
    history: Optional[List[Dict]] = None


@app.get("/")
def home():
    return {"message": "Insurance AI Agent API is running."}


@app.post("/ask")
def ask(data: Question):
    answer = ask_agent(data.question, data.history)
    return {"answer": answer}


@app.get("/experience-analysis")
def experience_analysis_endpoint():
    return experience_analysis()


@app.get("/dashboard-summary")
def dashboard_summary_endpoint():
    return dashboard_summary()


@app.get("/lob-products")
def lob_products_endpoint(lob: str, period: str):
    return lob_product_breakdown(lob, period)


@app.get("/lob-graph")
def lob_graph_endpoint(lob: str, period: str):
    return lob_graph_data(lob, period)


@app.post("/assumption-setting/run")
def run_assumption_setting_endpoint():
    return run_assumption_setting()


@app.get("/assumption-setting/download/{filename}")
def download_prophet_file(filename: str):
    file_path = OUTPUT_DIR / filename

    if not file_path.exists():
        return {"status": "error", "message": "File not found."}

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


@app.get("/red-zone")
def red_zone_endpoint():
    return identify_red_zone()


@app.get("/red-zone/products")
def red_zone_products_endpoint(era: str, channel: str, pay_type: str):
    return red_zone_product_breakdown(era, channel, pay_type)


@app.get("/red-zone/download-cohort")
def download_cohort_prophet_file(era: str, channel: str, pay_type: str):
    file_path = generate_single_cohort_prophet_file(era, channel, pay_type)
    return FileResponse(
        path=file_path,
        filename=file_path.name,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
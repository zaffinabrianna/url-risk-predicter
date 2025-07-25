from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl, constr, validator
from datetime import datetime
from utils.url_analyzer import analyze_url
import os
import asyncpg
from dotenv import load_dotenv

app = FastAPI(
    title="API for project",
    description="Malicious URL Detection API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
DATABASE_URL = os.getenv('SUPABASE_DB_URL')


async def save_analysis_event(url, risk_score, risk_level, risk_factors):
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        await conn.execute(
            'INSERT INTO analyses (url, risk_score, risk_level, risk_factors) VALUES ($1, $2, $3, $4)',
            url, risk_score, risk_level, risk_factors
        )
        await conn.close()
    except Exception as e:
        print(f"[DB] Failed to save analysis: {e}")


async def save_feedback(url, user_vote, feedback):
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        await conn.execute(
            'INSERT INTO feedback (url, user_vote, feedback) VALUES ($1, $2, $3)',
            url, user_vote, feedback
        )
        await conn.close()
    except Exception as e:
        print(f"[DB] Failed to save feedback: {e}")


class AnalyzeRequest(BaseModel):
    url: HttpUrl
    do_not_log: bool = False


class FeedbackRequest(BaseModel):
    url: HttpUrl
    user_vote: str
    feedback: constr(max_length=500) = None
    do_not_log: bool = False

    @validator('user_vote')
    def vote_must_be_valid(cls, v):
        allowed = {"Malicious", "Safe", "Unsure"}
        if v not in allowed:
            raise ValueError(f"user_vote must be one of {allowed}")
        return v

    @validator('feedback')
    def feedback_no_scripts(cls, v):
        if v and ("<script" in v.lower() or "</script" in v.lower()):
            raise ValueError("Feedback must not contain scripts.")
        return v


@app.get("/")
async def root():
    return {"message": "Project API - Smart Malicious URL Checker"}


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
    }


@app.post("/analyze")
async def analyze_url_endpoint(request: AnalyzeRequest):
    url = str(request.url)
    do_not_log = request.do_not_log
    result = analyze_url(url)
    if not do_not_log:
        # Save analysis event to database
        await save_analysis_event(
            url,
            result.get('risk_score'),
            result.get('risk_level'),
            ', '.join(result.get('risk_factors', [])) if result.get(
                'risk_factors') else None
        )
        print(f"Analysis logged for: {url}")
    else:
        print(f"Analysis NOT logged for: {url} (user opted out)")
    return result


@app.post("/feedback")
async def submit_feedback(request: FeedbackRequest):
    if request.do_not_log:
        print(f"Feedback NOT logged for: {request.url} (user opted out)")
        return {"message": "Feedback not logged (user opted out)."}
    # Save feedback to database
    await save_feedback(str(request.url), request.user_vote, request.feedback)
    print(
        f"Feedback received: url={request.url}, vote={request.user_vote}, comment={request.feedback}")
    return {"message": "Feedback received. Thank you!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

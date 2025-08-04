from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl, constr, validator
from datetime import datetime
from utils.url_analyzer import analyze_url
import os

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


def save_analysis_event(url, risk_score, risk_level, risk_factors):
    # Analysis events are logged to console for now
    print(
        f"[ANALYSIS] URL: {url}, Risk: {risk_level}, Score: {risk_score}, Factors: {risk_factors}")


def save_feedback(url, user_vote, feedback):
    # Feedback is logged to console for now
    print(f"[FEEDBACK] URL: {url}, Vote: {user_vote}, Comment: {feedback}")


class AnalyzeRequest(BaseModel):
    url: HttpUrl


class FeedbackRequest(BaseModel):
    url: HttpUrl
    user_vote: str
    feedback: constr(max_length=500) = None

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
    result = analyze_url(url)
    # Save analysis event to console
    save_analysis_event(
        url,
        result.get('risk_score'),
        result.get('risk_level'),
        ', '.join(result.get('risk_factors', [])) if result.get(
            'risk_factors') else ''
    )
    return result


@app.post("/feedback")
async def submit_feedback(request: FeedbackRequest):
    # Save feedback to console
    save_feedback(str(request.url), request.user_vote, request.feedback)
    return {"message": "Feedback received. Thank you!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

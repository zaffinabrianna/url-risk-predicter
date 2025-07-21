from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl, constr, validator
from datetime import datetime
from utils.url_analyzer import analyze_url

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
        # TODO: Save analysis event to database here
        print(f"Analysis logged for: {url}")
    else:
        print(f"Analysis NOT logged for: {url} (user opted out)")
    return result


@app.post("/feedback")
async def submit_feedback(request: FeedbackRequest):
    if request.do_not_log:
        print(f"Feedback NOT logged for: {request.url} (user opted out)")
        return {"message": "Feedback not logged (user opted out)."}
    print(
        f"Feedback received: url={request.url}, vote={request.user_vote}, comment={request.feedback}")
    return {"message": "Feedback received. Thank you!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

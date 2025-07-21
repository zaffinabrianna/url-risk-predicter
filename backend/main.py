from fastapi import FastAPI, Form, Request
from fastapi.middleware.cors import CORSMiddleware
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
async def analyze_url_endpoint(
    url: str = Form(...),
    do_not_log: bool = Form(False)
):
    result = analyze_url(url)
    if not do_not_log:
        # TODO: Save analysis event to database here
        print(f"Analysis logged for: {url}")
    else:
        print(f"Analysis NOT logged for: {url} (user opted out)")
    return result


@app.post("/feedback")
async def submit_feedback(request: Request):
    data = await request.json()
    do_not_log = data.get("do_not_log", False)
    if do_not_log:
        print(f"Feedback NOT logged for: {data.get('url')} (user opted out)")
        return {"message": "Feedback not logged (user opted out)."}
    # Otherwise, save feedback as before
    print(
        f"Feedback received: url={data.get('url')}, vote={data.get('user_vote')}, comment={data.get('feedback')}")
    return {"message": "Feedback received. Thank you!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai_client import ask_openai  # your OpenAI wrapper

app = FastAPI(title="SentriX Risk Analysis API")

# CORS (allow frontend connections)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # For production, list only allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "SentriX backend is running!"}

@app.post("/api/analyze-risk")
async def analyze_risk(data: dict):
    """
    Endpoint to analyze risk for a given input.
    Expects JSON payload: {"scenario": "description of business scenario"}
    """
    scenario = data.get("scenario")
    if not scenario:
        raise HTTPException(status_code=400, detail="Missing 'scenario' in request")

    try:
        # Ask OpenAI for risk analysis
        prompt = f"Analyze the potential risks for the following scenario:\n{scenario}"
        response = ask_openai(prompt)
        return {"scenario": scenario, "risk_analysis": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 🔧 New Chat API
@app.post("/api/chat")
async def chat(data: dict):
    """
    General chat endpoint to talk with OpenAI.
    Expects JSON payload: {"message": "your text"}
    """
    message = data.get("message")
    if not message:
        raise HTTPException(status_code=400, detail="Missing 'message' in request")

    try:
        response = ask_openai(message)
        return {"response": response, "session_id": None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

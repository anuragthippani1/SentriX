from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
# from sse_starlette.sse import EventSourceResponse  # Temporarily disabled
from dotenv import load_dotenv
import uvicorn
from typing import List, Dict, Any
import asyncio
import json
from datetime import datetime
import uuid

from agents.assistant_agent import AssistantAgent
from agents.chatbot_manager import ChatbotManager
from agents.scheduler_agent import SchedulerAgent
from agents.political_risk_agent import PoliticalRiskAgent
from agents.reporting_agent import ReportingAgent
from database.mongodb import MongoDBClient
from models.schemas import QueryRequest, RiskReport, PoliticalRisk, ScheduleRisk, Session, SessionCreate, SessionUpdate

load_dotenv()  # load variables from backend/.env if present

app = FastAPI(title="SentriX API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agents
assistant_agent = AssistantAgent()
scheduler_agent = SchedulerAgent()
political_risk_agent = PoliticalRiskAgent()
reporting_agent = ReportingAgent()
chatbot_manager = ChatbotManager()

# Initialize database
db_client = MongoDBClient()

latest_world_data: Dict[str, Any] = {"world_risk_data": {}, "political_risks": [], "schedule_risks": []}
_subscribers: set = set()
_poll_task = None

async def _poll_world_data():
    global latest_world_data
    while True:
        try:
            countries = await scheduler_agent.extract_countries()
            political_risks = await political_risk_agent.analyze_risks(countries)
            schedule_risks = await scheduler_agent.analyze_schedule_risks()
            # combine
            world_risk_data = reporting_agent._create_combined_world_risk_data(political_risks, schedule_risks)
            latest_world_data = {
                "world_risk_data": world_risk_data,
                "political_risks": [r.dict() for r in political_risks],
                "schedule_risks": [r.dict() for r in schedule_risks],
                "timestamp": datetime.utcnow().isoformat()
            }
            # notify subscribers (they pull via SSE generator)
        except Exception as e:
            print("Polling error:", e)
        await asyncio.sleep(60)  # poll every minute

@app.on_event("startup")
async def startup_event():
    await db_client.connect()
    # global _poll_task
    # _poll_task = asyncio.create_task(_poll_world_data())  # Disabled for now

@app.on_event("shutdown")
async def shutdown_event():
    await db_client.disconnect()
    # global _poll_task
    # if _poll_task:
    #     _poll_task.cancel()

@app.get("/")
async def root():
    return {"message": "SentriX API is running"}

@app.post("/api/shipment/upload")
async def upload_shipment_data(payload: Dict[str, Any]):
    """Accept shipment/equipment JSON array and load into SchedulerAgent."""
    try:
        data = payload.get("data") if isinstance(payload, dict) else None
        if data is None:
            # allow raw list body too
            if isinstance(payload, list):
                data = payload
        if not isinstance(data, list):
            raise HTTPException(status_code=400, detail="Body must contain a 'data' array or be an array itself")
        scheduler_agent.set_shipment_data(data)
        return {"status": "ok", "items": len(data)}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/report/combined")
async def generate_combined_report():
    """Generate a combined report from current political + schedule risks."""
    try:
        session_id = str(uuid.uuid4())
        countries = await scheduler_agent.extract_countries()
        political_risks = await political_risk_agent.analyze_risks(countries)
        schedule_risks = await scheduler_agent.analyze_schedule_risks()
        report = await reporting_agent.generate_combined_report(political_risks, schedule_risks, session_id)
        await db_client.store_report(report)
        return {"session_id": session_id, "report": report, "type": "report"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/shipment/reset")
async def reset_shipment_data():
    scheduler_agent.clear_custom_data()
    return {"status": "ok"}

@app.post("/api/query")
async def process_query(request: QueryRequest):
    """Process natural language queries and route to appropriate agents"""
    try:
        # Use the session_id from the request, or generate a new one if not provided
        session_id = request.session_id or str(uuid.uuid4())
        text = request.query.lower()
        intent = chatbot_manager.classify_intent(text)
        if intent == "reject":
            response = await assistant_agent.process_query("offtopic")
            return {"session_id": session_id, "response": response, "type": "assistant"}
        if intent == "combined":
            countries = await scheduler_agent.extract_countries()
            political_risks = await political_risk_agent.analyze_risks(countries)
            schedule_risks = await scheduler_agent.analyze_schedule_risks()
            report = await reporting_agent.generate_combined_report(political_risks, schedule_risks, session_id)
        elif intent == "political":
            countries = await scheduler_agent.extract_countries()
            political_risks = await political_risk_agent.analyze_risks(countries)
            report = await reporting_agent.generate_political_report(political_risks, session_id)
        elif intent == "schedule":
            schedule_risks = await scheduler_agent.analyze_schedule_risks()
            report = await reporting_agent.generate_schedule_report(schedule_risks, session_id)
        else:
            response = await assistant_agent.process_query(request.query)
            return {"session_id": session_id, "response": response, "type": "assistant"}
        await db_client.store_report(report)
        return {"session_id": session_id, "report": report, "type": "report"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/reports")
async def get_reports():
    """Get all stored reports"""
    try:
        reports = await db_client.get_all_reports()
        return {"reports": reports}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/reports/{report_id}")
async def get_report(report_id: str):
    """Get specific report by ID"""
    try:
        report = await db_client.get_report(report_id)
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/reports/{report_id}/download")
async def download_report(report_id: str):
    """Download report as PDF/DOCX"""
    try:
        report = await db_client.get_report(report_id)
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        
        # Generate downloadable file
        file_path = await reporting_agent.generate_downloadable_report(report)
        return FileResponse(file_path, filename=f"sentrix_report_{report_id}.pdf")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @app.get("/api/stream/dashboard")
# async def stream_dashboard():
#     # Temporarily disabled - requires sse_starlette
#     pass

@app.get("/api/dashboard")
async def get_dashboard_data():
    try:
        # Simple fallback data for demo
        countries = await scheduler_agent.extract_countries()
        political_risks = await political_risk_agent.analyze_risks(countries)
        schedule_risks = await scheduler_agent.analyze_schedule_risks()
        
        # Create simple world risk data
        world_risk_data = {}
        for risk in political_risks:
            world_risk_data[risk.country] = {
                "risk_level": risk.likelihood_score,
                "type": "political",
                "details": risk.reasoning
            }
        
        for risk in schedule_risks:
            if risk.country not in world_risk_data:
                world_risk_data[risk.country] = {"risk_level": 0, "type": "schedule", "details": ""}
            world_risk_data[risk.country]["risk_level"] = max(
                world_risk_data[risk.country]["risk_level"], 
                risk.risk_level
            )
        
        return {
            "world_risk_data": world_risk_data,
            "political_risks": [risk.dict() for risk in political_risks],
            "schedule_risks": [risk.dict() for risk in schedule_risks]
        }
    except Exception as e:
        print(f"Dashboard error: {e}")
        # Return sample data if anything fails
        return {
            "world_risk_data": {
                "China": {"risk_level": 3, "type": "political", "details": "Sample data"},
                "Germany": {"risk_level": 2, "type": "schedule", "details": "Sample data"}
            },
            "political_risks": [],
            "schedule_risks": []
        }

# Session Management Endpoints
@app.post("/api/sessions")
async def create_session(session_data: SessionCreate | None = None):
    """Create a new session. Name/description are optional; a random ID is always generated."""
    try:
        session_id = str(uuid.uuid4())
        now = datetime.utcnow()

        name = (session_data.name if session_data and session_data.name else f"Session {now.strftime('%H:%M:%S')}")
        description = (session_data.description if session_data else None)

        session = Session(
            session_id=session_id,
            name=name,
            description=description,
            created_at=now,
            updated_at=now,
            is_active=True,
            report_count=0,
            last_activity=now,
        )

        success = await db_client.create_session(session)
        if success:
            return {"session": session, "message": "Session created successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to create session")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sessions")
async def get_all_sessions():
    """Get all sessions"""
    try:
        sessions = await db_client.get_all_sessions()
        # Update report counts for each session
        for session in sessions:
            session.report_count = await db_client.get_session_report_count(session.session_id)
        
        return {"sessions": [session.dict() for session in sessions]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sessions/{session_id}")
async def get_session(session_id: str):
    """Get a specific session"""
    try:
        session = await db_client.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Update report count
        session.report_count = await db_client.get_session_report_count(session.session_id)
        
        return {"session": session.dict()}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/sessions/{session_id}")
async def update_session(session_id: str, session_data: SessionUpdate):
    """Update a session"""
    try:
        # Check if session exists
        existing_session = await db_client.get_session(session_id)
        if not existing_session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Prepare updates
        updates = {}
        if session_data.name is not None:
            updates["name"] = session_data.name
        if session_data.description is not None:
            updates["description"] = session_data.description
        if session_data.is_active is not None:
            updates["is_active"] = session_data.is_active
        
        if updates:
            success = await db_client.update_session(session_id, updates)
            if not success:
                raise HTTPException(status_code=500, detail="Failed to update session")
        
        # Return updated session
        updated_session = await db_client.get_session(session_id)
        updated_session.report_count = await db_client.get_session_report_count(session_id)
        
        return {"session": updated_session.dict(), "message": "Session updated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete a session"""
    try:
        # Check if session exists
        existing_session = await db_client.get_session(session_id)
        if not existing_session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        success = await db_client.delete_session(session_id)
        if success:
            return {"message": "Session deleted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to delete session")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sessions/{session_id}/reports")
async def get_session_reports(session_id: str):
    """Get all reports for a specific session"""
    try:
        # Check if session exists
        session = await db_client.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Get all reports for this session
        all_reports = await db_client.get_all_reports()
        session_reports = [report for report in all_reports if report.get('session_id') == session_id]
        
        return {"reports": session_reports, "session": session.dict()}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

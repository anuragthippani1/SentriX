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

# CORS middleware - Allow all local development origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
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
        # Return comprehensive global risk data for better visualization
        world_risk_data = {
            # Critical Risk Countries (Level 4)
            "Russia": {"risk_level": 4, "type": "political", "details": "Active conflict in Ukraine, international sanctions", "risk_factors": ["Sanctions", "Geopolitical Risk", "War"]},
            "Ukraine": {"risk_level": 4, "type": "political", "details": "Active military conflict", "risk_factors": ["Active Conflict", "Infrastructure Damage"]},
            "Iran": {"risk_level": 4, "type": "political", "details": "International sanctions, regional tensions", "risk_factors": ["Sanctions", "Political Instability"]},
            "North Korea": {"risk_level": 4, "type": "political", "details": "International isolation, sanctions", "risk_factors": ["Sanctions", "Political Risk"]},
            "Syria": {"risk_level": 4, "type": "political", "details": "Ongoing civil conflict", "risk_factors": ["Conflict", "Political Instability"]},
            "Afghanistan": {"risk_level": 4, "type": "political", "details": "Political instability, security concerns", "risk_factors": ["Political Instability", "Security Risk"]},
            "Yemen": {"risk_level": 4, "type": "political", "details": "Civil conflict, humanitarian crisis", "risk_factors": ["Conflict", "Humanitarian Crisis"]},
            "Myanmar": {"risk_level": 4, "type": "political", "details": "Political crisis, military rule", "risk_factors": ["Political Crisis", "Humanitarian Crisis"]},
            "Venezuela": {"risk_level": 4, "type": "political", "details": "Political and economic crisis", "risk_factors": ["Political Crisis", "Economic Crisis"]},
            
            # High Risk Countries (Level 3)
            "China": {"risk_level": 3, "type": "political", "details": "Trade tensions, regulatory changes", "risk_factors": ["Trade Policy", "Regulatory Changes"]},
            "Somalia": {"risk_level": 3, "type": "political", "details": "Security concerns, piracy risk", "risk_factors": ["Security Risk", "Political Instability"]},
            "Libya": {"risk_level": 3, "type": "political", "details": "Political instability", "risk_factors": ["Political Instability"]},
            "Sudan": {"risk_level": 3, "type": "political", "details": "Political transition", "risk_factors": ["Political Transition"]},
            "South Sudan": {"risk_level": 3, "type": "political", "details": "Internal conflict", "risk_factors": ["Internal Conflict"]},
            "Central African Republic": {"risk_level": 3, "type": "political", "details": "Security challenges", "risk_factors": ["Security Risk"]},
            "Mali": {"risk_level": 3, "type": "political", "details": "Security concerns", "risk_factors": ["Security Risk"]},
            "Burkina Faso": {"risk_level": 3, "type": "political", "details": "Security challenges", "risk_factors": ["Security Risk"]},
            "Niger": {"risk_level": 3, "type": "political", "details": "Regional instability", "risk_factors": ["Regional Instability"]},
            "Pakistan": {"risk_level": 3, "type": "political", "details": "Political instability", "risk_factors": ["Political Instability"]},
            "Lebanon": {"risk_level": 3, "type": "political", "details": "Economic crisis", "risk_factors": ["Economic Crisis"]},
            "Belarus": {"risk_level": 3, "type": "political", "details": "Political tensions", "risk_factors": ["Political Tensions"]},
            "Palestine": {"risk_level": 3, "type": "political", "details": "Political instability", "risk_factors": ["Political Instability"]},
            "Haiti": {"risk_level": 3, "type": "political", "details": "Political instability, security concerns", "risk_factors": ["Political Instability", "Security Risk"]},
            
            # Medium Risk Countries (Level 2)
            "United States": {"risk_level": 2, "type": "political", "details": "Policy uncertainty", "risk_factors": ["Policy Changes"]},
            "Germany": {"risk_level": 2, "type": "schedule", "details": "Supply chain delays", "risk_factors": ["Logistics Delays"]},
            "India": {"risk_level": 2, "type": "political", "details": "Regional tensions", "risk_factors": ["Regional Tensions"]},
            "Bangladesh": {"risk_level": 2, "type": "political", "details": "Political uncertainty", "risk_factors": ["Political Uncertainty"]},
            "Sri Lanka": {"risk_level": 2, "type": "political", "details": "Economic crisis", "risk_factors": ["Economic Crisis"]},
            "Nigeria": {"risk_level": 2, "type": "political", "details": "Security concerns", "risk_factors": ["Security Risk"]},
            "Cameroon": {"risk_level": 2, "type": "political", "details": "Regional tensions", "risk_factors": ["Regional Tensions"]},
            "Chad": {"risk_level": 2, "type": "political", "details": "Political transition", "risk_factors": ["Political Transition"]},
            "Ethiopia": {"risk_level": 2, "type": "political", "details": "Internal tensions", "risk_factors": ["Internal Tensions"]},
            "Eritrea": {"risk_level": 2, "type": "political", "details": "Regional tensions", "risk_factors": ["Regional Tensions"]},
            "South Africa": {"risk_level": 2, "type": "political", "details": "Economic challenges", "risk_factors": ["Economic Challenges"]},
            "Tunisia": {"risk_level": 2, "type": "political", "details": "Political transition", "risk_factors": ["Political Transition"]},
            "Algeria": {"risk_level": 2, "type": "political", "details": "Political uncertainty", "risk_factors": ["Political Uncertainty"]},
            "Egypt": {"risk_level": 2, "type": "political", "details": "Economic challenges", "risk_factors": ["Economic Challenges"]},
            "Israel": {"risk_level": 2, "type": "political", "details": "Regional tensions", "risk_factors": ["Regional Tensions"]},
            "Turkey": {"risk_level": 2, "type": "political", "details": "Political uncertainty", "risk_factors": ["Political Uncertainty"]},
            "Moldova": {"risk_level": 2, "type": "political", "details": "Regional tensions", "risk_factors": ["Regional Tensions"]},
            "Bosnia and Herzegovina": {"risk_level": 2, "type": "political", "details": "Political tensions", "risk_factors": ["Political Tensions"]},
            "Serbia": {"risk_level": 2, "type": "political", "details": "Regional tensions", "risk_factors": ["Regional Tensions"]},
            "Kosovo": {"risk_level": 2, "type": "political", "details": "Political tensions", "risk_factors": ["Political Tensions"]},
            "Mexico": {"risk_level": 2, "type": "political", "details": "Security concerns", "risk_factors": ["Security Risk"]},
            "Brazil": {"risk_level": 2, "type": "political", "details": "Political uncertainty", "risk_factors": ["Political Uncertainty"]},
            "Argentina": {"risk_level": 2, "type": "political", "details": "Economic challenges", "risk_factors": ["Economic Challenges"]},
            "Colombia": {"risk_level": 2, "type": "political", "details": "Security concerns", "risk_factors": ["Security Risk"]},
            "Peru": {"risk_level": 2, "type": "political", "details": "Political instability", "risk_factors": ["Political Instability"]},
            "Ecuador": {"risk_level": 2, "type": "political", "details": "Political uncertainty", "risk_factors": ["Political Uncertainty"]},
            "Bolivia": {"risk_level": 2, "type": "political", "details": "Political transition", "risk_factors": ["Political Transition"]},
            "Philippines": {"risk_level": 2, "type": "political", "details": "Political uncertainty", "risk_factors": ["Political Uncertainty"]},
            
            # Low Risk Countries (Level 1)
            "Canada": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "United Kingdom": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "France": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Italy": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Spain": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Portugal": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Switzerland": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Austria": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Luxembourg": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Belgium": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Netherlands": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Denmark": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Sweden": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Norway": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Finland": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Iceland": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Ireland": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Poland": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Czech Republic": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Slovakia": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Hungary": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Slovenia": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Croatia": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Montenegro": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "North Macedonia": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Albania": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Greece": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Bulgaria": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Romania": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Lithuania": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Latvia": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Estonia": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Japan": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "South Korea": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Taiwan": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Singapore": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Malaysia": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Thailand": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Vietnam": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Indonesia": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Australia": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "New Zealand": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Chile": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Uruguay": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Paraguay": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Jordan": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Morocco": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Kenya": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Uganda": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Tanzania": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Rwanda": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Botswana": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            "Namibia": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
        }
        
        # Try to get dynamic data from agents, but merge with our base data
        # NOTE: Agent calls disabled for faster dashboard loading
        # Uncomment below to enable dynamic risk analysis (slower)
        # try:
        #     countries = await scheduler_agent.extract_countries()
        #     political_risks = await political_risk_agent.analyze_risks(countries)
        #     schedule_risks = await scheduler_agent.analyze_schedule_risks()
        #     
        #     # Merge agent-generated data with our comprehensive base
        #     for risk in political_risks:
        #         if risk.country in world_risk_data:
        #             world_risk_data[risk.country]["details"] = risk.reasoning
        #             world_risk_data[risk.country]["risk_level"] = max(
        #                 world_risk_data[risk.country]["risk_level"], 
        #                 risk.likelihood_score
        #             )
        # except:
        #     pass  # Use base data if agents fail
        
        # Return comprehensive data with sample political and schedule risks
        return {
            "world_risk_data": world_risk_data,
            "political_risks": [
                {
                    "country": "Russia",
                    "risk_type": "Geopolitical",
                    "likelihood_score": 4,
                    "reasoning": "Active military conflict in Ukraine with ongoing international sanctions. High risk of supply chain disruptions and asset seizures.",
                    "data_sources": ["UN Security Council", "Trade Data", "News Analysis"]
                },
                {
                    "country": "China",
                    "risk_type": "Trade Policy",
                    "likelihood_score": 3,
                    "reasoning": "Ongoing trade tensions with Western countries. Potential for sudden regulatory changes affecting supply chains.",
                    "data_sources": ["WTO Reports", "Trade Statistics", "Policy Analysis"]
                },
                {
                    "country": "Iran",
                    "risk_type": "Sanctions",
                    "likelihood_score": 4,
                    "reasoning": "Comprehensive international sanctions restricting trade and financial transactions.",
                    "data_sources": ["OFAC", "UN Sanctions List", "Trade Reports"]
                },
                {
                    "country": "Venezuela",
                    "risk_type": "Political",
                    "likelihood_score": 4,
                    "reasoning": "Ongoing political and economic crisis with hyperinflation and supply shortages.",
                    "data_sources": ["IMF Reports", "Economic Data", "News Sources"]
                },
                {
                    "country": "Pakistan",
                    "risk_type": "Political",
                    "likelihood_score": 3,
                    "reasoning": "Political instability and economic challenges affecting trade reliability.",
                    "data_sources": ["World Bank", "Political Analysis", "Trade Data"]
                },
                {
                    "country": "Myanmar",
                    "risk_type": "Political",
                    "likelihood_score": 4,
                    "reasoning": "Military rule and civil unrest creating significant operational risks.",
                    "data_sources": ["UN Reports", "Human Rights Watch", "News Analysis"]
                },
                {
                    "country": "Ukraine",
                    "risk_type": "Conflict",
                    "likelihood_score": 4,
                    "reasoning": "Active war zone with severe infrastructure damage and operational impossibility.",
                    "data_sources": ["UN Reports", "Satellite Imagery", "News Coverage"]
                },
                {
                    "country": "Haiti",
                    "risk_type": "Security",
                    "likelihood_score": 3,
                    "reasoning": "Gang violence and political instability affecting port operations and logistics.",
                    "data_sources": ["State Department", "Security Reports", "Port Authorities"]
                }
            ],
            "schedule_risks": [
                {
                    "equipment_id": "CNTX-2024-001",
                    "country": "Germany",
                    "delay_days": 5,
                    "risk_level": 2,
                    "risk_factors": ["Port congestion at Hamburg", "Labor strikes", "Customs delays"]
                },
                {
                    "equipment_id": "CNTX-2024-002",
                    "country": "China",
                    "delay_days": 7,
                    "risk_level": 3,
                    "risk_factors": ["COVID-19 lockdown restrictions", "Port congestion", "Equipment shortage"]
                },
                {
                    "equipment_id": "CNTX-2024-003",
                    "country": "United States",
                    "delay_days": 3,
                    "risk_level": 2,
                    "risk_factors": ["Weather delays at LA Port", "Truck driver shortage", "Warehouse capacity"]
                },
                {
                    "equipment_id": "CNTX-2024-004",
                    "country": "India",
                    "delay_days": 8,
                    "risk_level": 3,
                    "risk_factors": ["Customs inspection", "Documentation issues", "Infrastructure delays"]
                },
                {
                    "equipment_id": "CNTX-2024-005",
                    "country": "Brazil",
                    "delay_days": 6,
                    "risk_level": 2,
                    "risk_factors": ["Port strikes", "Bureaucratic delays", "Weather conditions"]
                },
                {
                    "equipment_id": "CNTX-2024-006",
                    "country": "United Kingdom",
                    "delay_days": 2,
                    "risk_level": 1,
                    "risk_factors": ["Minor customs processing", "Seasonal congestion"]
                },
                {
                    "equipment_id": "CNTX-2024-007",
                    "country": "Japan",
                    "delay_days": 1,
                    "risk_level": 1,
                    "risk_factors": ["Routine inspection", "Minor documentation review"]
                },
                {
                    "equipment_id": "CNTX-2024-008",
                    "country": "Mexico",
                    "delay_days": 4,
                    "risk_level": 2,
                    "risk_factors": ["Border crossing delays", "Security checks", "Traffic congestion"]
                },
                {
                    "equipment_id": "CNTX-2024-009",
                    "country": "South Africa",
                    "delay_days": 5,
                    "risk_level": 2,
                    "risk_factors": ["Power outages affecting port operations", "Labor issues", "Equipment maintenance"]
                },
                {
                    "equipment_id": "CNTX-2024-010",
                    "country": "Singapore",
                    "delay_days": 1,
                    "risk_level": 1,
                    "risk_factors": ["High volume processing", "Routine checks"]
                }
            ]
        }
    except Exception as e:
        print(f"Dashboard error: {e}")
        # Return comprehensive sample data with global coverage
        return {
            "world_risk_data": {
                # Critical Risk Countries (Level 4)
                "Russia": {"risk_level": 4, "type": "political", "details": "Active conflict in Ukraine, international sanctions", "risk_factors": ["Sanctions", "Geopolitical Risk", "War"]},
                "Ukraine": {"risk_level": 4, "type": "political", "details": "Active military conflict", "risk_factors": ["Active Conflict", "Infrastructure Damage"]},
                "Iran": {"risk_level": 4, "type": "political", "details": "International sanctions, regional tensions", "risk_factors": ["Sanctions", "Political Instability"]},
                "North Korea": {"risk_level": 4, "type": "political", "details": "International isolation, sanctions", "risk_factors": ["Sanctions", "Political Risk"]},
                "Syria": {"risk_level": 4, "type": "political", "details": "Ongoing civil conflict", "risk_factors": ["Conflict", "Political Instability"]},
                "Afghanistan": {"risk_level": 4, "type": "political", "details": "Political instability, security concerns", "risk_factors": ["Political Instability", "Security Risk"]},
                "Yemen": {"risk_level": 4, "type": "political", "details": "Civil conflict, humanitarian crisis", "risk_factors": ["Conflict", "Humanitarian Crisis"]},
                "Myanmar": {"risk_level": 4, "type": "political", "details": "Political crisis, military rule", "risk_factors": ["Political Crisis", "Humanitarian Crisis"]},
                "Venezuela": {"risk_level": 4, "type": "political", "details": "Political and economic crisis", "risk_factors": ["Political Crisis", "Economic Crisis"]},
                
                # High Risk Countries (Level 3)
                "China": {"risk_level": 3, "type": "political", "details": "Trade tensions, regulatory changes", "risk_factors": ["Trade Policy", "Regulatory Changes"]},
                "Somalia": {"risk_level": 3, "type": "political", "details": "Security concerns, piracy risk", "risk_factors": ["Security Risk", "Political Instability"]},
                "Libya": {"risk_level": 3, "type": "political", "details": "Political instability", "risk_factors": ["Political Instability"]},
                "Sudan": {"risk_level": 3, "type": "political", "details": "Political transition", "risk_factors": ["Political Transition"]},
                "South Sudan": {"risk_level": 3, "type": "political", "details": "Internal conflict", "risk_factors": ["Internal Conflict"]},
                "Central African Republic": {"risk_level": 3, "type": "political", "details": "Security challenges", "risk_factors": ["Security Risk"]},
                "Mali": {"risk_level": 3, "type": "political", "details": "Security concerns", "risk_factors": ["Security Risk"]},
                "Burkina Faso": {"risk_level": 3, "type": "political", "details": "Security challenges", "risk_factors": ["Security Risk"]},
                "Niger": {"risk_level": 3, "type": "political", "details": "Regional instability", "risk_factors": ["Regional Instability"]},
                "Pakistan": {"risk_level": 3, "type": "political", "details": "Political instability", "risk_factors": ["Political Instability"]},
                "Lebanon": {"risk_level": 3, "type": "political", "details": "Economic crisis", "risk_factors": ["Economic Crisis"]},
                "Belarus": {"risk_level": 3, "type": "political", "details": "Political tensions", "risk_factors": ["Political Tensions"]},
                "Palestine": {"risk_level": 3, "type": "political", "details": "Political instability", "risk_factors": ["Political Instability"]},
                "Haiti": {"risk_level": 3, "type": "political", "details": "Political instability, security concerns", "risk_factors": ["Political Instability", "Security Risk"]},
                
                # Medium Risk Countries (Level 2)
                "United States": {"risk_level": 2, "type": "political", "details": "Policy uncertainty", "risk_factors": ["Policy Changes"]},
                "Germany": {"risk_level": 2, "type": "schedule", "details": "Supply chain delays", "risk_factors": ["Logistics Delays"]},
                "India": {"risk_level": 2, "type": "political", "details": "Regional tensions", "risk_factors": ["Regional Tensions"]},
                "Bangladesh": {"risk_level": 2, "type": "political", "details": "Political uncertainty", "risk_factors": ["Political Uncertainty"]},
                "Sri Lanka": {"risk_level": 2, "type": "political", "details": "Economic crisis", "risk_factors": ["Economic Crisis"]},
                "Nigeria": {"risk_level": 2, "type": "political", "details": "Security concerns", "risk_factors": ["Security Risk"]},
                "Cameroon": {"risk_level": 2, "type": "political", "details": "Regional tensions", "risk_factors": ["Regional Tensions"]},
                "Chad": {"risk_level": 2, "type": "political", "details": "Political transition", "risk_factors": ["Political Transition"]},
                "Ethiopia": {"risk_level": 2, "type": "political", "details": "Internal tensions", "risk_factors": ["Internal Tensions"]},
                "Eritrea": {"risk_level": 2, "type": "political", "details": "Regional tensions", "risk_factors": ["Regional Tensions"]},
                "South Africa": {"risk_level": 2, "type": "political", "details": "Economic challenges", "risk_factors": ["Economic Challenges"]},
                "Tunisia": {"risk_level": 2, "type": "political", "details": "Political transition", "risk_factors": ["Political Transition"]},
                "Algeria": {"risk_level": 2, "type": "political", "details": "Political uncertainty", "risk_factors": ["Political Uncertainty"]},
                "Egypt": {"risk_level": 2, "type": "political", "details": "Economic challenges", "risk_factors": ["Economic Challenges"]},
                "Israel": {"risk_level": 2, "type": "political", "details": "Regional tensions", "risk_factors": ["Regional Tensions"]},
                "Turkey": {"risk_level": 2, "type": "political", "details": "Political uncertainty", "risk_factors": ["Political Uncertainty"]},
                "Moldova": {"risk_level": 2, "type": "political", "details": "Regional tensions", "risk_factors": ["Regional Tensions"]},
                "Bosnia and Herzegovina": {"risk_level": 2, "type": "political", "details": "Political tensions", "risk_factors": ["Political Tensions"]},
                "Serbia": {"risk_level": 2, "type": "political", "details": "Regional tensions", "risk_factors": ["Regional Tensions"]},
                "Kosovo": {"risk_level": 2, "type": "political", "details": "Political tensions", "risk_factors": ["Political Tensions"]},
                "Mexico": {"risk_level": 2, "type": "political", "details": "Security concerns", "risk_factors": ["Security Risk"]},
                "Brazil": {"risk_level": 2, "type": "political", "details": "Political uncertainty", "risk_factors": ["Political Uncertainty"]},
                "Argentina": {"risk_level": 2, "type": "political", "details": "Economic challenges", "risk_factors": ["Economic Challenges"]},
                "Colombia": {"risk_level": 2, "type": "political", "details": "Security concerns", "risk_factors": ["Security Risk"]},
                "Peru": {"risk_level": 2, "type": "political", "details": "Political instability", "risk_factors": ["Political Instability"]},
                "Ecuador": {"risk_level": 2, "type": "political", "details": "Political uncertainty", "risk_factors": ["Political Uncertainty"]},
                "Bolivia": {"risk_level": 2, "type": "political", "details": "Political transition", "risk_factors": ["Political Transition"]},
                "Philippines": {"risk_level": 2, "type": "political", "details": "Political uncertainty", "risk_factors": ["Political Uncertainty"]},
                
                # Low Risk Countries (Level 1)
                "Canada": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "United Kingdom": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "France": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Italy": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Spain": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Portugal": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Switzerland": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Austria": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Luxembourg": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Belgium": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Netherlands": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Denmark": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Sweden": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Norway": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Finland": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Iceland": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Ireland": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Poland": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Czech Republic": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Slovakia": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Hungary": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Slovenia": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Croatia": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Montenegro": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "North Macedonia": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Albania": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Greece": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Bulgaria": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Romania": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Lithuania": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Latvia": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Estonia": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Japan": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "South Korea": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Taiwan": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Singapore": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Malaysia": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Thailand": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Vietnam": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Indonesia": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Australia": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "New Zealand": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Chile": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Uruguay": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Paraguay": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Jordan": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Morocco": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Kenya": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Uganda": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Tanzania": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Rwanda": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Botswana": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
                "Namibia": {"risk_level": 1, "type": "political", "details": "Stable environment", "risk_factors": ["Stable"]},
            },
            "political_risks": [
                {
                    "country": "Russia",
                    "risk_type": "Geopolitical",
                    "likelihood_score": 4,
                    "reasoning": "Active military conflict in Ukraine with ongoing international sanctions. High risk of supply chain disruptions and asset seizures.",
                    "data_sources": ["UN Security Council", "Trade Data", "News Analysis"]
                },
                {
                    "country": "China",
                    "risk_type": "Trade Policy",
                    "likelihood_score": 3,
                    "reasoning": "Ongoing trade tensions with Western countries. Potential for sudden regulatory changes affecting supply chains.",
                    "data_sources": ["WTO Reports", "Trade Statistics", "Policy Analysis"]
                },
                {
                    "country": "Iran",
                    "risk_type": "Sanctions",
                    "likelihood_score": 4,
                    "reasoning": "Comprehensive international sanctions restricting trade and financial transactions.",
                    "data_sources": ["OFAC", "UN Sanctions List", "Trade Reports"]
                },
                {
                    "country": "Venezuela",
                    "risk_type": "Political",
                    "likelihood_score": 4,
                    "reasoning": "Ongoing political and economic crisis with hyperinflation and supply shortages.",
                    "data_sources": ["IMF Reports", "Economic Data", "News Sources"]
                },
                {
                    "country": "Pakistan",
                    "risk_type": "Political",
                    "likelihood_score": 3,
                    "reasoning": "Political instability and economic challenges affecting trade reliability.",
                    "data_sources": ["World Bank", "Political Analysis", "Trade Data"]
                },
                {
                    "country": "Myanmar",
                    "risk_type": "Political",
                    "likelihood_score": 4,
                    "reasoning": "Military rule and civil unrest creating significant operational risks.",
                    "data_sources": ["UN Reports", "Human Rights Watch", "News Analysis"]
                },
                {
                    "country": "Ukraine",
                    "risk_type": "Conflict",
                    "likelihood_score": 4,
                    "reasoning": "Active war zone with severe infrastructure damage and operational impossibility.",
                    "data_sources": ["UN Reports", "Satellite Imagery", "News Coverage"]
                },
                {
                    "country": "Haiti",
                    "risk_type": "Security",
                    "likelihood_score": 3,
                    "reasoning": "Gang violence and political instability affecting port operations and logistics.",
                    "data_sources": ["State Department", "Security Reports", "Port Authorities"]
                }
            ],
            "schedule_risks": [
                {
                    "equipment_id": "CNTX-2024-001",
                    "country": "Germany",
                    "delay_days": 5,
                    "risk_level": 2,
                    "risk_factors": ["Port congestion at Hamburg", "Labor strikes", "Customs delays"]
                },
                {
                    "equipment_id": "CNTX-2024-002",
                    "country": "China",
                    "delay_days": 7,
                    "risk_level": 3,
                    "risk_factors": ["COVID-19 lockdown restrictions", "Port congestion", "Equipment shortage"]
                },
                {
                    "equipment_id": "CNTX-2024-003",
                    "country": "United States",
                    "delay_days": 3,
                    "risk_level": 2,
                    "risk_factors": ["Weather delays at LA Port", "Truck driver shortage", "Warehouse capacity"]
                },
                {
                    "equipment_id": "CNTX-2024-004",
                    "country": "India",
                    "delay_days": 8,
                    "risk_level": 3,
                    "risk_factors": ["Customs inspection", "Documentation issues", "Infrastructure delays"]
                },
                {
                    "equipment_id": "CNTX-2024-005",
                    "country": "Brazil",
                    "delay_days": 6,
                    "risk_level": 2,
                    "risk_factors": ["Port strikes", "Bureaucratic delays", "Weather conditions"]
                },
                {
                    "equipment_id": "CNTX-2024-006",
                    "country": "United Kingdom",
                    "delay_days": 2,
                    "risk_level": 1,
                    "risk_factors": ["Minor customs processing", "Seasonal congestion"]
                },
                {
                    "equipment_id": "CNTX-2024-007",
                    "country": "Japan",
                    "delay_days": 1,
                    "risk_level": 1,
                    "risk_factors": ["Routine inspection", "Minor documentation review"]
                },
                {
                    "equipment_id": "CNTX-2024-008",
                    "country": "Mexico",
                    "delay_days": 4,
                    "risk_level": 2,
                    "risk_factors": ["Border crossing delays", "Security checks", "Traffic congestion"]
                },
                {
                    "equipment_id": "CNTX-2024-009",
                    "country": "South Africa",
                    "delay_days": 5,
                    "risk_level": 2,
                    "risk_factors": ["Power outages affecting port operations", "Labor issues", "Equipment maintenance"]
                },
                {
                    "equipment_id": "CNTX-2024-010",
                    "country": "Singapore",
                    "delay_days": 1,
                    "risk_level": 1,
                    "risk_factors": ["High volume processing", "Routine checks"]
                }
            ]
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

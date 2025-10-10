import openai
import os
from typing import Dict, Any
import asyncio
from datetime import datetime

class AssistantAgent:
    def __init__(self):
        # Initialize OpenAI client (using free tier)
        self.client = openai.OpenAI(
            api_key=os.getenv("OPENAI_API_KEY", "your-openai-key-here")
        )
        self.system_prompt = """
        You are SentriX, an AI assistant specialized in supply chain risk intelligence. 
        You help users understand and analyze supply chain risks including:
        - Political and geopolitical risks
        - Schedule delays and delivery risks
        - Tariff changes and trade policies
        - Logistics disruptions
        
        Always provide helpful, accurate information and guide users to use the appropriate 
        features for their queries. Be concise but informative.
        """
    
    async def process_query(self, query: str) -> Dict[str, Any]:
        """Process general assistant queries"""
        try:
            # For demo purposes, we'll use a simple response system
            # In production, this would call OpenAI API
            response = await self._generate_response(query)
            
            return {
                "message": response,
                "timestamp": datetime.now().isoformat(),
                "agent": "assistant"
            }
        except Exception as e:
            return {
                "message": f"I apologize, but I encountered an error: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "agent": "assistant"
            }
    
    async def _generate_response(self, query: str) -> str:
        """Generate response limited strictly to supply chain risk topics."""
        query_lower = query.lower()

        allowed_topics = [
            "supply", "chain", "risk", "political", "geopolit", "tariff", "sanction",
            "schedule", "delivery", "delay", "logistics", "shipping", "transport",
            "report", "equipment", "supplier", "country", "trade", "from", "to", "route"
        ]
        is_on_topic = any(t in query_lower for t in allowed_topics)

        # Check for route/transportation queries first
        if self._is_route_query(query_lower):
            return await self._analyze_route(query)

        if not is_on_topic:
            return (
                "I can only assist with supply chain risk intelligence, shipping routes, "
                "political risks, delivery delays, logistics disruptions, and report generation. "
                "Try asking about routes between ports or countries."
            )

        if "hello" in query_lower or "hi" in query_lower or "help" in query_lower:
            return (
                "You're connected to SentriX. I can help with:\n"
                "• Route analysis (origin to destination with climate, risks, transit time)\n"
                "• Political risks by country\n"
                "• Delivery schedule risks\n"
                "• Logistics disruptions\n"
                "• Generate combined reports\n\n"
                "Try: 'Route from Shanghai to Los Angeles' or 'Political risks in Germany'"
            )

        if "political" in query_lower or "geopolit" in query_lower:
            return "Understood. I'll analyze recent geopolitical events and their supply chain impact."

        if "schedule" in query_lower or "delivery" in query_lower or "delay" in query_lower:
            return "Got it. I'll assess equipment schedule delays and risk levels."

        if "combined" in query_lower or ("report" in query_lower and ("both" in query_lower or "all" in query_lower)):
            return "Generating a combined report covering political and schedule risks."

        if "report" in query_lower:
            return "I can generate a political, schedule, or combined risk report. Which one would you like?"

        return (
            "I can help with supply chain risk questions, route analysis, political risks, "
            "schedule/logistics issues, or generate reports. Please specify your focus."
        )

    def _is_route_query(self, query_lower: str) -> bool:
        """Check if query is about shipping routes/transportation."""
        route_indicators = [
            "from", "to", "route", "shipping", "transit", "journey", "voyage",
            "port", "ocean", "sea", "maritime", "cargo", "freight", "ship"
        ]
        return any(indicator in query_lower for indicator in route_indicators)

    async def _analyze_route(self, query: str) -> str:
        """Analyze shipping route with climate, risks, and transit time."""
        # Extract origin and destination (simplified)
        words = query.lower().split()
        origin = None
        destination = None
        
        # Look for "from X to Y" pattern
        if "from" in words and "to" in words:
            from_idx = words.index("from")
            to_idx = words.index("to")
            if from_idx < to_idx and to_idx < len(words):
                origin = " ".join(words[from_idx+1:to_idx])
                destination = " ".join(words[to_idx+1:])
        
        if not origin or not destination:
            return "Please specify origin and destination. Example: 'Route from Shanghai to Los Angeles'"

        # Mock analysis (in production, integrate with real shipping APIs)
        analysis = f"""
🚢 **Route Analysis: {origin.title()} → {destination.title()}**

**🌊 Ocean Climate Conditions:**
• Primary Route: North Pacific (for most Asia-US routes)
• Seasonal Weather: Moderate seas, occasional storms in winter
• Current Conditions: Favorable for navigation
• Sea Temperature: 15-20°C average

**⚠️ Risk Assessment:**
• **Political Risk**: Low (2/5) - Stable trade routes
• **Weather Risk**: Medium (3/5) - Winter storm season
• **Piracy Risk**: Low (1/5) - Well-patrolled waters
• **Port Congestion**: Medium (3/5) - Occasional delays

**⏱️ Transit Time:**
• **Estimated Duration**: 12-15 days
• **Fastest Route**: Direct great circle
• **Alternative Routes**: +2-3 days via Panama Canal
• **Port Time**: 1-2 days loading/unloading

**🛡️ Safety Precautions:**
• Monitor weather forecasts continuously
• Maintain communication with coast guard
• Follow ISPS security protocols
• Ensure cargo is properly secured
• Have emergency response plans ready
• Regular equipment maintenance checks

**📊 Route Recommendation:**
This route is generally safe with standard precautions. Monitor weather conditions and maintain regular communication with port authorities.
"""

        return analysis

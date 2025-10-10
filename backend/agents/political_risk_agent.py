import aiohttp
import asyncio
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
from models.schemas import PoliticalRisk
import os

class PoliticalRiskAgent:
    def __init__(self):
        # Free news API endpoints
        self.newsdata_api_key = os.getenv("NEWSDATA_API_KEY", "your-newsdata-key")
        self.gnews_api_key = os.getenv("GNEWS_API_KEY", "your-gnews-key")
        
        # Risk keywords to look for in news
        self.risk_keywords = [
            "tariff", "sanctions", "strike", "protest", "trade war",
            "embargo", "political unrest", "election", "policy change",
            "regulatory", "export ban", "import restriction", "currency",
            "inflation", "recession", "conflict", "tension"
        ]
    
    async def analyze_risks(self, countries: List[str]) -> List[PoliticalRisk]:
        """Analyze political risks for given countries"""
        all_risks = []
        
        for country in countries:
            try:
                # Fetch news for each country
                news_articles = await self._fetch_news_for_country(country)
                
                # Analyze articles for risk indicators
                country_risks = await self._analyze_articles_for_risks(news_articles, country)
                all_risks.extend(country_risks)
                
            except Exception as e:
                print(f"Error analyzing risks for {country}: {str(e)}")
                # Add a default risk entry if analysis fails
                default_risk = PoliticalRisk(
                    country=country,
                    risk_type="Analysis Error",
                    likelihood_score=1,
                    reasoning=f"Unable to fetch current data: {str(e)}",
                    publication_date=datetime.now().isoformat(),
                    source_title="System Error",
                    source_url=""
                )
                all_risks.append(default_risk)
        
        return all_risks
    
    async def _fetch_news_for_country(self, country: str) -> List[Dict[str, Any]]:
        """Fetch news articles for a specific country"""
        articles = []
        
        # Try NewsData.io first (free tier)
        try:
            newsdata_articles = await self._fetch_from_newsdata(country)
            articles.extend(newsdata_articles)
        except Exception as e:
            print(f"NewsData.io error for {country}: {str(e)}")
        
        # Try GNews as backup
        try:
            gnews_articles = await self._fetch_from_gnews(country)
            articles.extend(gnews_articles)
        except Exception as e:
            print(f"GNews error for {country}: {str(e)}")
        
        # If both APIs fail, return sample data
        if not articles:
            articles = self._get_sample_news_data(country)
        
        return articles
    
    async def _fetch_from_newsdata(self, country: str) -> List[Dict[str, Any]]:
        """Fetch news from NewsData.io API"""
        url = "https://newsdata.io/api/1/news"
        params = {
            "apikey": self.newsdata_api_key,
            "country": country.lower(),
            "category": "business,politics",
            "language": "en",
            "size": 10
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("results", [])
                else:
                    raise Exception(f"NewsData API error: {response.status}")
    
    async def _fetch_from_gnews(self, country: str) -> List[Dict[str, Any]]:
        """Fetch news from GNews API"""
        url = "https://gnews.io/api/v4/search"
        params = {
            "token": self.gnews_api_key,
            "q": f"{country} trade politics economy",
            "lang": "en",
            "country": country.lower(),
            "max": 10
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("articles", [])
                else:
                    raise Exception(f"GNews API error: {response.status}")
    
    def _get_sample_news_data(self, country: str) -> List[Dict[str, Any]]:
        """Return sample news data when APIs are unavailable"""
        sample_articles = {
            "China": [
                {
                    "title": "China Implements New Export Controls on Technology",
                    "description": "New regulations affect semiconductor exports",
                    "content": "China has announced new export controls affecting technology sectors...",
                    "pubDate": datetime.now().isoformat(),
                    "link": "https://example.com/china-tech-export"
                }
            ],
            "Germany": [
                {
                    "title": "German Manufacturing Index Shows Decline",
                    "description": "Economic indicators suggest potential supply chain impacts",
                    "content": "The German manufacturing sector shows signs of contraction...",
                    "pubDate": datetime.now().isoformat(),
                    "link": "https://example.com/germany-manufacturing"
                }
            ],
            "India": [
                {
                    "title": "India Announces New Trade Policies",
                    "description": "Updated regulations affect international trade",
                    "content": "India's new trade policies aim to boost domestic manufacturing...",
                    "pubDate": datetime.now().isoformat(),
                    "link": "https://example.com/india-trade"
                }
            ],
            "Japan": [
                {
                    "title": "Japan's Supply Chain Resilience Initiative",
                    "description": "Government announces new supply chain security measures",
                    "content": "Japan is implementing new measures to strengthen supply chain security...",
                    "pubDate": datetime.now().isoformat(),
                    "link": "https://example.com/japan-supply-chain"
                }
            ],
            "Brazil": [
                {
                    "title": "Brazilian Port Workers Announce Strike",
                    "description": "Potential shipping delays expected",
                    "content": "Port workers in Brazil have announced a planned strike...",
                    "pubDate": datetime.now().isoformat(),
                    "link": "https://example.com/brazil-strike"
                }
            ]
        }
        
        return sample_articles.get(country, [])
    
    async def _analyze_articles_for_risks(self, articles: List[Dict[str, Any]], country: str) -> List[PoliticalRisk]:
        """Analyze news articles for political risk indicators"""
        risks = []
        
        for article in articles:
            # Extract text content
            content = ""
            if "content" in article:
                content = article["content"]
            elif "description" in article:
                content = article["description"]
            elif "title" in article:
                content = article["title"]
            
            # Check for risk keywords
            risk_score = self._calculate_risk_score(content)
            
            if risk_score > 0:
                risk_type = self._identify_risk_type(content)
                reasoning = self._generate_reasoning(content, risk_type)
                
                risk = PoliticalRisk(
                    country=country,
                    risk_type=risk_type,
                    likelihood_score=risk_score,
                    reasoning=reasoning,
                    publication_date=article.get("pubDate", datetime.now().isoformat()),
                    source_title=article.get("title", "Unknown"),
                    source_url=article.get("link", "")
                )
                risks.append(risk)
        
        return risks
    
    def _calculate_risk_score(self, content: str) -> int:
        """Calculate risk score based on content analysis"""
        content_lower = content.lower()
        score = 0
        
        # Check for high-risk keywords
        high_risk_keywords = ["strike", "protest", "conflict", "war", "embargo", "sanctions"]
        for keyword in high_risk_keywords:
            if keyword in content_lower:
                score += 3
        
        # Check for medium-risk keywords
        medium_risk_keywords = ["tariff", "policy change", "regulation", "delay", "disruption"]
        for keyword in medium_risk_keywords:
            if keyword in content_lower:
                score += 2
        
        # Check for low-risk keywords
        low_risk_keywords = ["trade", "economic", "business", "manufacturing"]
        for keyword in low_risk_keywords:
            if keyword in content_lower:
                score += 1
        
        # Cap at 5
        return min(score, 5)
    
    def _identify_risk_type(self, content: str) -> str:
        """Identify the type of political risk"""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ["strike", "protest", "unrest"]):
            return "Labor Disputes"
        elif any(word in content_lower for word in ["tariff", "trade", "export", "import"]):
            return "Trade Policy"
        elif any(word in content_lower for word in ["sanctions", "embargo", "ban"]):
            return "Economic Sanctions"
        elif any(word in content_lower for word in ["regulation", "policy", "law"]):
            return "Regulatory Changes"
        elif any(word in content_lower for word in ["election", "political", "government"]):
            return "Political Instability"
        else:
            return "General Economic Risk"
    
    def _generate_reasoning(self, content: str, risk_type: str) -> str:
        """Generate reasoning for the risk assessment"""
        # Extract key phrases from content
        sentences = content.split('.')[:2]  # Take first two sentences
        key_info = '. '.join(sentences).strip()
        
        return f"Based on recent news: {key_info}. Risk type identified as {risk_type}."

# Major Global Shipping Ports Database
# Contains coordinates, country, region, and capacity information

MAJOR_PORTS = {
    # Asia Pacific
    "Shanghai": {
        "country": "China",
        "region": "Asia Pacific",
        "coordinates": {"lat": 31.2304, "lon": 121.4737},
        "capacity": "very_high",
        "avg_wait_time": 2.5  # days
    },
    "Singapore": {
        "country": "Singapore",
        "region": "Asia Pacific",
        "coordinates": {"lat": 1.2897, "lon": 103.8501},
        "capacity": "very_high",
        "avg_wait_time": 1.5
    },
    "Hong Kong": {
        "country": "Hong Kong",
        "region": "Asia Pacific",
        "coordinates": {"lat": 22.3193, "lon": 114.1694},
        "capacity": "very_high",
        "avg_wait_time": 2.0
    },
    "Shenzhen": {
        "country": "China",
        "region": "Asia Pacific",
        "coordinates": {"lat": 22.5431, "lon": 114.0579},
        "capacity": "very_high",
        "avg_wait_time": 2.5
    },
    "Busan": {
        "country": "South Korea",
        "region": "Asia Pacific",
        "coordinates": {"lat": 35.1796, "lon": 129.0756},
        "capacity": "high",
        "avg_wait_time": 2.0
    },
    "Guangzhou": {
        "country": "China",
        "region": "Asia Pacific",
        "coordinates": {"lat": 23.1291, "lon": 113.2644},
        "capacity": "high",
        "avg_wait_time": 2.5
    },
    "Qingdao": {
        "country": "China",
        "region": "Asia Pacific",
        "coordinates": {"lat": 36.0671, "lon": 120.3826},
        "capacity": "high",
        "avg_wait_time": 2.0
    },
    "Tokyo": {
        "country": "Japan",
        "region": "Asia Pacific",
        "coordinates": {"lat": 35.6528, "lon": 139.8394},
        "capacity": "high",
        "avg_wait_time": 1.5
    },
    "Mumbai": {
        "country": "India",
        "region": "Asia Pacific",
        "coordinates": {"lat": 18.9388, "lon": 72.8354},
        "capacity": "medium",
        "avg_wait_time": 3.0
    },
    "Chennai": {
        "country": "India",
        "region": "Asia Pacific",
        "coordinates": {"lat": 13.0827, "lon": 80.2707},
        "capacity": "medium",
        "avg_wait_time": 3.0
    },
    "Kolkata": {
        "country": "India",
        "region": "Asia Pacific",
        "coordinates": {"lat": 22.5726, "lon": 88.3639},
        "capacity": "medium",
        "avg_wait_time": 3.5
    },
    "Visakhapatnam": {
        "country": "India",
        "region": "Asia Pacific",
        "coordinates": {"lat": 17.6868, "lon": 83.2185},
        "capacity": "medium",
        "avg_wait_time": 2.5
    },
    "Bangkok": {
        "country": "Thailand",
        "region": "Asia Pacific",
        "coordinates": {"lat": 13.7563, "lon": 100.5018},
        "capacity": "medium",
        "avg_wait_time": 2.5
    },
    "Manila": {
        "country": "Philippines",
        "region": "Asia Pacific",
        "coordinates": {"lat": 14.5995, "lon": 120.9842},
        "capacity": "medium",
        "avg_wait_time": 3.0
    },
    
    # Middle East
    "Dubai": {
        "country": "UAE",
        "region": "Middle East",
        "coordinates": {"lat": 25.2048, "lon": 55.2708},
        "capacity": "very_high",
        "avg_wait_time": 1.5
    },
    "Jebel Ali": {
        "country": "UAE",
        "region": "Middle East",
        "coordinates": {"lat": 24.9857, "lon": 55.0272},
        "capacity": "very_high",
        "avg_wait_time": 1.5
    },
    "Port Said": {
        "country": "Egypt",
        "region": "Middle East",
        "coordinates": {"lat": 31.2653, "lon": 32.3019},
        "capacity": "high",
        "avg_wait_time": 2.0
    },
    "Jeddah": {
        "country": "Saudi Arabia",
        "region": "Middle East",
        "coordinates": {"lat": 21.5433, "lon": 39.1728},
        "capacity": "high",
        "avg_wait_time": 2.5
    },
    
    # Europe
    "Rotterdam": {
        "country": "Netherlands",
        "region": "Europe",
        "coordinates": {"lat": 51.9244, "lon": 4.4777},
        "capacity": "very_high",
        "avg_wait_time": 1.5
    },
    "Antwerp": {
        "country": "Belgium",
        "region": "Europe",
        "coordinates": {"lat": 51.2194, "lon": 4.4025},
        "capacity": "high",
        "avg_wait_time": 2.0
    },
    "Hamburg": {
        "country": "Germany",
        "region": "Europe",
        "coordinates": {"lat": 53.5511, "lon": 9.9937},
        "capacity": "high",
        "avg_wait_time": 2.0
    },
    "Felixstowe": {
        "country": "United Kingdom",
        "region": "Europe",
        "coordinates": {"lat": 51.9642, "lon": 1.3517},
        "capacity": "high",
        "avg_wait_time": 2.0
    },
    "Le Havre": {
        "country": "France",
        "region": "Europe",
        "coordinates": {"lat": 49.4944, "lon": 0.1079},
        "capacity": "medium",
        "avg_wait_time": 2.5
    },
    "Barcelona": {
        "country": "Spain",
        "region": "Europe",
        "coordinates": {"lat": 41.3874, "lon": 2.1686},
        "capacity": "medium",
        "avg_wait_time": 2.5
    },
    "Valencia": {
        "country": "Spain",
        "region": "Europe",
        "coordinates": {"lat": 39.4699, "lon": -0.3763},
        "capacity": "medium",
        "avg_wait_time": 2.5
    },
    "Piraeus": {
        "country": "Greece",
        "region": "Europe",
        "coordinates": {"lat": 37.9486, "lon": 23.6269},
        "capacity": "medium",
        "avg_wait_time": 2.5
    },
    
    # Americas
    "Los Angeles": {
        "country": "USA",
        "region": "North America",
        "coordinates": {"lat": 33.7405, "lon": -118.2720},
        "capacity": "very_high",
        "avg_wait_time": 2.5
    },
    "Long Beach": {
        "country": "USA",
        "region": "North America",
        "coordinates": {"lat": 33.7701, "lon": -118.1937},
        "capacity": "very_high",
        "avg_wait_time": 2.5
    },
    "New York": {
        "country": "USA",
        "region": "North America",
        "coordinates": {"lat": 40.7128, "lon": -74.0060},
        "capacity": "very_high",
        "avg_wait_time": 2.0
    },
    "Savannah": {
        "country": "USA",
        "region": "North America",
        "coordinates": {"lat": 32.0809, "lon": -81.0912},
        "capacity": "high",
        "avg_wait_time": 2.0
    },
    "Houston": {
        "country": "USA",
        "region": "North America",
        "coordinates": {"lat": 29.7604, "lon": -95.3698},
        "capacity": "high",
        "avg_wait_time": 2.5
    },
    "Vancouver": {
        "country": "Canada",
        "region": "North America",
        "coordinates": {"lat": 49.2827, "lon": -123.1207},
        "capacity": "high",
        "avg_wait_time": 2.0
    },
    "Montreal": {
        "country": "Canada",
        "region": "North America",
        "coordinates": {"lat": 45.5017, "lon": -73.5673},
        "capacity": "medium",
        "avg_wait_time": 2.5
    },
    "Santos": {
        "country": "Brazil",
        "region": "South America",
        "coordinates": {"lat": -23.9608, "lon": -46.3339},
        "capacity": "high",
        "avg_wait_time": 3.0
    },
    "Buenos Aires": {
        "country": "Argentina",
        "region": "South America",
        "coordinates": {"lat": -34.6037, "lon": -58.3816},
        "capacity": "medium",
        "avg_wait_time": 3.0
    },
    "Cartagena": {
        "country": "Colombia",
        "region": "South America",
        "coordinates": {"lat": 10.3910, "lon": -75.4794},
        "capacity": "medium",
        "avg_wait_time": 2.5
    },
    
    # Africa
    "Cape Town": {
        "country": "South Africa",
        "region": "Africa",
        "coordinates": {"lat": -33.9249, "lon": 18.4241},
        "capacity": "medium",
        "avg_wait_time": 2.5
    },
    "Durban": {
        "country": "South Africa",
        "region": "Africa",
        "coordinates": {"lat": -29.8587, "lon": 31.0218},
        "capacity": "medium",
        "avg_wait_time": 2.5
    },
    "Lagos": {
        "country": "Nigeria",
        "region": "Africa",
        "coordinates": {"lat": 6.5244, "lon": 3.3792},
        "capacity": "medium",
        "avg_wait_time": 4.0
    },
    "Mombasa": {
        "country": "Kenya",
        "region": "Africa",
        "coordinates": {"lat": -4.0435, "lon": 39.6682},
        "capacity": "low",
        "avg_wait_time": 3.5
    },
    
    # Oceania
    "Sydney": {
        "country": "Australia",
        "region": "Oceania",
        "coordinates": {"lat": -33.8688, "lon": 151.2093},
        "capacity": "high",
        "avg_wait_time": 2.0
    },
    "Melbourne": {
        "country": "Australia",
        "region": "Oceania",
        "coordinates": {"lat": -37.8136, "lon": 144.9631},
        "capacity": "high",
        "avg_wait_time": 2.0
    },
    "Auckland": {
        "country": "New Zealand",
        "region": "Oceania",
        "coordinates": {"lat": -36.8485, "lon": 174.7633},
        "capacity": "medium",
        "avg_wait_time": 2.5
    }
}

# Major shipping canals and their toll costs
CANALS = {
    "Suez Canal": {
        "coordinates": {"lat": 30.7025, "lon": 32.3444},
        "avg_toll": 400000,  # USD
        "avg_transit_time": 0.5,  # days
        "connects": ["Mediterranean", "Red Sea"]
    },
    "Panama Canal": {
        "coordinates": {"lat": 9.0820, "lon": -79.6805},
        "avg_toll": 450000,  # USD
        "avg_transit_time": 0.4,  # days
        "connects": ["Atlantic", "Pacific"]
    }
}

def get_port_by_name(port_name):
    """Get port information by name (case-insensitive)"""
    port_name_lower = port_name.lower()
    for port, info in MAJOR_PORTS.items():
        if port.lower() == port_name_lower:
            return {**info, "name": port}
    return None

def get_all_port_names():
    """Get list of all available port names"""
    return sorted(MAJOR_PORTS.keys())

def search_ports(query):
    """Search ports by name or country"""
    query_lower = query.lower()
    results = []
    for port, info in MAJOR_PORTS.items():
        if (query_lower in port.lower() or 
            query_lower in info["country"].lower() or 
            query_lower in info["region"].lower()):
            results.append({**info, "name": port})
    return results


# travel.py
from fastmcp import FastMCP
import httpx
import os
from typing import Optional, Dict, Any, List

# Initialize FastMCP server
server = FastMCP(
    name="travel", 
    on_duplicate_tools="error", 
    on_duplicate_resources="error"
)

key = os.getenv('TRIPADVISOR_API_KEY')



async def _search_locations(
    search_query: str,
    category: Optional[str] = None,
    language: str = "en"
) -> Dict[str, Any]:
    """
    Helper function to search for locations using TripAdvisor API.
    
    Args:
        search_query: Text to search for location names
        category: Filter by property type (hotels, attractions, restaurants, geos)
        language: Language for results (default: en)
    
    Returns:
        Dict containing search results with location IDs and basic information
    """
    base_url = "https://api.content.tripadvisor.com/api/v1/location/search"
    params = {
        "key": key,
        "searchQuery": search_query,
        "language": language
    }
    
    if category:
        params["category"] = category

    headers = {"accept": "application/json"}
    
    async with httpx.AsyncClient() as client:
        response = await client.get(base_url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()

async def _get_location_details(
    location_id: int,
    language: str = "en",
    currency: str = "USD"
) -> Dict[str, Any]:
    """
    Helper function to get detailed information about a specific location.
    
    Args:
        location_id: TripAdvisor location ID
        language: Language for results (default: en)
        currency: Currency code (default: USD)
    
    Returns:
        Dict containing detailed location information including prices, ratings, and amenities
    """
    url = f"https://api.content.tripadvisor.com/api/v1/location/{location_id}/details"
    params = {
        "key": key,
        "language": language,
        "currency": currency
    }
    headers = {"accept": "application/json"}
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()

@server.tool(name="get_travel_recommendations")
async def get_travel_recommendations(
    location: str,
    category: Optional[str] = None,
    language: str = "en",
    currency: str = "USD"
) -> List[Dict[str, Any]]:
    """
    Get travel recommendations for a location from TripAdvisor.
    
    Args:
        location: City or area to search in (e.g. "Mumbai")
        category: Type of place (hotels, attractions, restaurants)
        language: Language for results (default: en)
        currency: Currency for prices (default: USD)
    
    Returns:
        List of detailed recommendations. LLM should convert this list into text, and
        return a paragraph summarizing the recommendations.
    """
    # First, search for locations
    search_results = await _search_locations(
        search_query=location,
        )

    recommendations = []
    
    # Get details for each location (limit to first 5 to avoid too many API calls)
    
    location_id = search_results.get('data')[0].get('location_id')
    print(location_id)

            
    try:
        details = await _get_location_details(
            location_id=location_id,
            language=language,
            currency=currency
        )
        recommendations.append(details)
    except Exception as e:
            # If we can't get details, include basic info from search
        recommendations.append(e)
    
    return recommendations

async def main():
    await server.run_async(
        transport='streamable-http',
        host="127.0.0.1",
        port=3001,
        path="/sse",
        cors_origins=["*"],
        allow_credentials=True
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

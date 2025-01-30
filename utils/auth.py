from fastapi import Request, HTTPException, Header
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
API_KEY = os.getenv("LAB4_API_KEY")

async def authenticate(request: Request, api_key: str = Header(None)):
    """Authenticate using either Header or Query Parameter"""
    # First, check if the API key is provided in the header
    header_api_key = request.headers.get("api_key")
    
    # If the header is not set, check the query parameters
    query_api_key = request.query_params.get("api_key")

    # If neither is found, raise an error
    if API_KEY is None:
        raise HTTPException(status_code=500, detail="Server error: API key not set")

    # Authenticate if either header or query parameter matches the expected API key
    if header_api_key != API_KEY and query_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key or missing API key")


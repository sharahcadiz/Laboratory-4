from fastapi import Request, HTTPException, Header
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
API_KEY = os.getenv("LAB4_API_KEY")

async def authenticate(request: Request, api_key: str = Header(None)):
    """Authenticate using either Header or Query Parameter"""
    query_api_key = request.query_params.get("api_key")

    # If API key is missing or incorrect, raise 401 error
    if API_KEY is None:
        raise HTTPException(status_code=500, detail="Server error: API key not set")
    
    if api_key != API_KEY and query_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key or missing API key")

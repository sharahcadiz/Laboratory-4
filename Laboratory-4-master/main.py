from fastapi import FastAPI, HTTPException, Depends, Request
from dotenv import load_dotenv
import os
from utils.auth import authenticate
from apiv1.endpoints import router as apiv1_router
from apiv2.endpoints import router as apiv2_router
from fastapi.responses import JSONResponse

# Load environment variables
load_dotenv()
API_KEY = os.getenv("LAB4_API_KEY")

app = FastAPI()

# Global Middleware: Apply authentication globally for API routes
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    if request.url.path.startswith("/apiv1") or request.url.path.startswith("/apiv2"):
        await authenticate(request)  # Enforce authentication for API routes
    response = await call_next(request)
    return response

# Custom error handler for 401 Unauthorized
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc: HTTPException):
    if exc.status_code == 401:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": "Invalid API key or missing API key"}
        )
    return await request.app.default_exception_handler(request, exc)

# Mount routers for versioning
app.include_router(apiv1_router, prefix="/apiv1", tags=["APIv1"])
app.include_router(apiv2_router, prefix="/apiv2", tags=["APIv2"])

@app.get("/")
def root():
    return {"message": "Welcome to the Task API"}

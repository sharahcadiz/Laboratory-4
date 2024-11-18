from fastapi import FastAPI
from dotenv import load_dotenv
import os
from apiv1.endpoints import router as apiv1_router
from apiv2.endpoints import router as apiv2_router

# Load environment variables
load_dotenv()
API_KEY = os.getenv("LAB4_API_KEY")

app = FastAPI()

# Mount routers for versioning
app.include_router(apiv1_router, prefix="/apiv1", tags=["APIv1"])
app.include_router(apiv2_router, prefix="/apiv2", tags=["APIv2"])

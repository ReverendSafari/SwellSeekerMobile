from fastapi import APIRouter
from app.api.api_v1.endpoints import beaches, surf_data

api_router = APIRouter()

api_router.include_router(beaches.router, prefix="/beaches", tags=["beaches"])
api_router.include_router(surf_data.router, prefix="/surf-data", tags=["surf-data"]) 
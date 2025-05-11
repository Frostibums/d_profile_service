from fastapi import APIRouter

from app.presentation.api.v1.group.endpoints import router as group_router
from app.presentation.api.v1.profile.endpoints import router as profile_router

api_router = APIRouter()
api_router.include_router(profile_router, prefix="/profile", tags=["Profile"])

api_router.include_router(group_router, prefix="/group", tags=["Group"])

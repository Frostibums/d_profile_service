from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.infrastructure.db.repositories.group import SQLAlchemyGroupRepository
from app.infrastructure.db.repositories.profile import SQLAlchemyProfileRepository
from app.infrastructure.db.session import get_session
from app.infrastructure.security import decode_jwt_token
from app.service.group import GroupService
from app.service.profile import ProfileService


def get_profile_repo(session: AsyncSession = Depends(get_session)):
    return SQLAlchemyProfileRepository(session=session)


def get_group_repo(session: AsyncSession = Depends(get_session)):
    return SQLAlchemyGroupRepository(session=session)


def get_profile_service(profile_repo=Depends(get_profile_repo)):
    return ProfileService(profile_repo=profile_repo)


def get_group_service(group_repo=Depends(get_group_repo)):
    return GroupService(group_repo=group_repo)


# TODO: auth deps
def get_current_user_id(token: str = Depends(...)) -> UUID:
    try:
        payload = decode_jwt_token(token)
        return UUID(payload["sub"])
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request

from app.domain.enums.role import Role
from app.infrastructure.bus.kafka.producer import KafkaEventProducer
from app.infrastructure.db.repositories.group import SQLAlchemyGroupRepository
from app.infrastructure.db.repositories.profile import SQLAlchemyProfileRepository
from app.infrastructure.db.session import get_session
from app.infrastructure.security import decode_jwt_token
from app.service.group import GroupService
from app.service.profile import ProfileService


def get_producer(request: Request) -> KafkaEventProducer:
    return request.app.state.kafka_producer


def get_profile_repo(session: AsyncSession = Depends(get_session)):
    return SQLAlchemyProfileRepository(session=session)


def get_group_repo(session: AsyncSession = Depends(get_session)):
    return SQLAlchemyGroupRepository(session=session)


def get_profile_service(
        profile_repo=Depends(get_profile_repo),
        producer: KafkaEventProducer = Depends(get_producer),
):
    return ProfileService(
        profile_repo=profile_repo,
        producer=producer,
    )


def get_group_service(group_repo=Depends(get_group_repo)):
    return GroupService(group_repo=group_repo)


def get_jwt_payload(request: Request) -> dict:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing access token",
        )

    if token.startswith("Bearer "):
        token = token[7:]
    try:
        return decode_jwt_token(token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired token{e}",
        )


def get_current_teacher_id(payload: dict = Depends(get_jwt_payload)) -> UUID:
    if payload.get("role") not in (Role.teacher, Role.admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only for stuff"
        )
    return UUID(payload["sub"])


def get_current_user_id(payload: dict = Depends(get_jwt_payload)) -> UUID:
    return UUID(payload["sub"])

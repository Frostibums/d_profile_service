from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config.db import db_settings
from app.infrastructure.db.repositories.group import SQLAlchemyGroupRepository
from app.infrastructure.db.repositories.profile import SQLAlchemyProfileRepository
from app.service.profile import ProfileService


class Container:
    def __init__(self):
        self._engine = create_async_engine(db_settings.db_url, echo=False)
        self._sessionmaker = async_sessionmaker(self._engine, expire_on_commit=False)

    def get_session(self) -> AsyncSession:
        return self._sessionmaker()

    @classmethod
    def get_profile_repo(cls, session: AsyncSession) -> SQLAlchemyProfileRepository:
        return SQLAlchemyProfileRepository(session)

    @classmethod
    def get_group_repo(cls, session: AsyncSession) -> SQLAlchemyGroupRepository:
        return SQLAlchemyGroupRepository(session)

    def get_profile_service(self, session: AsyncSession) -> ProfileService:
        return ProfileService(profile_repo=self.get_profile_repo(session))

import logging
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.dto.profile import ProfileUpdateDTO
from app.domain.entities.profile import Profile
from app.infrastructure.db.models.profile import ProfileORM

logger = logging.getLogger(__name__)

class SQLAlchemyProfileRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, profile: Profile) -> None:
        orm = ProfileORM.from_domain(profile)
        self.session.add(orm)
        await self.session.commit()

    async def update(self, profile_id: UUID, data: ProfileUpdateDTO) -> None:
        stmt = (
            update(ProfileORM)
            .where(ProfileORM.id == profile_id)
            .values(**data.to_dict())
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_list(self) -> list[Profile]:
        stmt = select(
            ProfileORM
        )
        results = (await self.session.execute(stmt)).scalars()
        return [result.to_domain() for result in results]

    async def get_by_user_id(self, user_id: UUID) -> Profile | None:
        stmt = select(
            ProfileORM
        ).where(ProfileORM.user_id == user_id)
        result = (await self.session.execute(stmt)).scalar_one_or_none()
        return result.to_domain() if result else None

    async def get_by_group(self, group_id: UUID) -> list[Profile] | None:
        stmt = select(ProfileORM).where(ProfileORM.group_id == group_id)
        results = (await self.session.execute(stmt)).scalars()
        return [result.to_domain() for result in results]

    async def assign_to_group(self, user_id: UUID, group_id: UUID) -> None:
        await self.session.execute(
            update(ProfileORM)
            .where(ProfileORM.user_id == user_id)
            .values(group_id=group_id)
        )
        await self.session.commit()

    async def remove_from_group(self, user_id: UUID) -> None:
        await self.session.execute(
            update(ProfileORM)
            .where(ProfileORM.user_id == user_id)
            .values(group_id=None)
        )
        await self.session.commit()

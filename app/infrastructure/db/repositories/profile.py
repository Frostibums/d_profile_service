from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.domain.dto.profile import Profile
from app.infrastructure.db.models.profile import ProfileORM


class ProfileRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, profile: Profile) -> None:
        orm = ProfileORM.from_domain(profile)
        self.session.add(orm)
        await self.session.commit()

    async def get_by_user_id(self, user_id: UUID) -> Profile | None:
        stmt = select(ProfileORM).where(ProfileORM.user_id == user_id)
        result = (await self.session.execute(stmt)).scalar_one_or_none()
        return result.to_domain() if result else None

from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.domain.dto.group import Group
from app.infrastructure.db.models.group import GroupORM


class GroupRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, group: Group) -> None:
        orm = GroupORM(**group.__dict__)
        self.session.add(orm)
        await self.session.commit()

    async def get_by_id(self, group_id: UUID) -> Group | None:
        stmt = select(GroupORM).where(GroupORM.id == group_id)
        result = (await self.session.execute(stmt)).scalar_one_or_none()
        return result.to_domain() if result else None

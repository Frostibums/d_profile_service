from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.group import Group
from app.infrastructure.db.models.group import GroupORM


class SQLAlchemyGroupRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, group_id: UUID) -> Group | None:
        stmt = select(GroupORM).where(GroupORM.id == group_id)
        result = (await self.session.execute(stmt)).scalar_one_or_none()
        return result.to_domain() if result else None

    async def get_list(self, name_filter: str | None = None) -> list[Group]:
        stmt = select(GroupORM).order_by(GroupORM.name)
        if name_filter:
            stmt = stmt.where(GroupORM.name.ilike(f"%{name_filter}%"))
        results = (await self.session.execute(stmt)).scalars()
        return [result.to_domain() for result in results]

    async def create(self, name: str) -> Group:
        orm = GroupORM.from_domain(Group(id=uuid4(), name=name))
        self.session.add(orm)
        await self.session.commit()
        return orm.to_domain()


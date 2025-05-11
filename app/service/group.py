from uuid import UUID

from app.domain.entities.group import Group


class GroupService:
    def __init__(self, group_repo):
        self.group_repo = group_repo

    async def get_by_id(self, group_id: UUID) -> Group | None:
        return await self.group_repo.get_by_id(group_id)

    async def get_list(self, name_filter: str | None = None) -> list[Group]:
        return await self.group_repo.get_list(name_filter=name_filter)

    async def create(self, name: str) -> Group:
        return await self.group_repo.create(name)

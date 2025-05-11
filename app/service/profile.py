from uuid import UUID

from app.domain.dto.profile import ProfileUpdateDTO
from app.domain.entities.profile import Profile


class ProfileService:
    def __init__(self, profile_repo):
        self.profile_repo = profile_repo

    async def create(self, profile: Profile) -> UUID:
        return await self.profile_repo.create(profile)

    async def update(self, profile_id: UUID, update_data: ProfileUpdateDTO) -> None:
        await self.profile_repo.update(profile_id, update_data)

    async def get_by_id(self, profile_id: UUID) -> Profile | None:
        return await self.profile_repo.get_by_id(profile_id)

    async def get_by_group(self, group_id: UUID) -> list[Profile]:
        return await self.profile_repo.get_by_group(group_id)

    async def get_list(self) -> list[Profile]:
        return await self.profile_repo.get_list()

    async def assign_to_group(self, user_id: UUID, group_id: UUID) -> None:
        await self.profile_repo.assign_to_group(user_id, group_id)

    async def remove_from_group(self, user_id: UUID, group_id: UUID) -> None:
        await self.profile_repo.remove_from_group(user_id, group_id)

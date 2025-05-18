from uuid import UUID

from app.domain.dto.profile import ProfileUpdateDTO
from app.domain.entities.profile import Profile
from app.infrastructure.bus.kafka.producer import KafkaEventProducer
from app.infrastructure.db.repositories.profile import SQLAlchemyProfileRepository


class ProfileService:
    def __init__(
            self,
            profile_repo: SQLAlchemyProfileRepository,
            producer: KafkaEventProducer | None = None,
    ):
        self.profile_repo = profile_repo
        self.producer = producer

    async def create(self, profile: Profile) -> Profile:
        return await self.profile_repo.create(profile)

    async def update(self, user_id: UUID, update_data: ProfileUpdateDTO) -> Profile | None:
        updated_profile = await self.profile_repo.update(user_id, update_data)
        if updated_profile and updated_profile.is_moderated:
            await self.producer.send(
                topic="student-moderated",
                message={
                    "user_id": str(user_id),
                    "first_name": updated_profile.first_name,
                    "last_name": updated_profile.last_name,
                    "middle_name": updated_profile.middle_name,
                }
            )
        return updated_profile

    async def get_by_user_id(self, user_id: UUID) -> Profile | None:
        return await self.profile_repo.get_by_user_id(user_id)

    async def get_by_group(self, group_id: UUID) -> list[Profile]:
        return await self.profile_repo.get_by_group(group_id)

    async def get_list(self) -> list[Profile]:
        return await self.profile_repo.get_list()

    async def assign_to_group(self, user_id: UUID, group_id: UUID) -> None:
        await self.profile_repo.assign_to_group(user_id, group_id)

    async def remove_from_group(self, user_id: UUID, group_id: UUID) -> None:
        await self.profile_repo.remove_from_group(user_id, group_id)

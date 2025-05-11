from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.domain.dto.profile import ProfileUpdateDTO
from app.domain.entities.group import Group


class ProfileOutput(BaseModel):
    id: UUID
    user_id: UUID
    group: Group | None = None
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    is_moderated: bool = False
    created_at: datetime
    updated_at: datetime | None = None


class ProfileUpdate(BaseModel):
    group_id: UUID | None = None
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    is_moderated: bool = False

    def to_domain(self) -> ProfileUpdateDTO:
        return ProfileUpdateDTO(
            group_id=self.group_id,
            first_name=self.first_name,
            last_name=self.last_name,
            middle_name=self.middle_name,
            is_moderated=self.is_moderated,
        )

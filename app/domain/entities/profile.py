from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.entities.group import Group


@dataclass
class Profile:
    id: UUID | None
    user_id: UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None
    group_id: UUID | None = None
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    group: Group | None = None
    is_moderated: bool | None = None


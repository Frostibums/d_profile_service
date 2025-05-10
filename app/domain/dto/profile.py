from dataclasses import dataclass
from uuid import UUID


@dataclass
class Profile:
    id: UUID
    user_id: UUID
    group_id: UUID | None = None
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None


from dataclasses import asdict, dataclass
from uuid import UUID


@dataclass
class ProfileUpdateDTO:
    group_id: UUID | None = None
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    is_moderated: bool | None = None

    def to_dict(self) -> dict:
        return {key: value for key, value in asdict(self).items() if value is not None}

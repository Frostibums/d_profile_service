from dataclasses import dataclass
from uuid import UUID

from app.domain.enums.role import Role


@dataclass
class User:
    id: UUID
    email: str
    role: Role | None = None


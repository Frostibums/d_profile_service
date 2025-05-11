import uuid

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.entities.group import Group
from app.infrastructure.db.session import Base


class GroupORM(Base):
    __tablename__ = "groups"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    students: Mapped[list["ProfileORM"]] = relationship(  # noqa: F821
        "ProfileORM",
        back_populates="group",
    )

    def to_domain(self) -> Group:
        return Group(
            id=self.id,
            name=self.name,
        )

    @classmethod
    def from_domain(cls, group: Group) -> "GroupORM":
        return cls(
            id=group.id,
            name=group.name,
        )

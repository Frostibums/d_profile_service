import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.dto.profile import Profile
from app.infrastructure.db.models.group import GroupORM
from app.infrastructure.db.session import Base


class ProfileORM(Base):
    __tablename__ = "profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        unique=True,
        nullable=False,
    )
    group_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("groups.id"),
    )
    first_name: Mapped[str | None] = mapped_column(String, nullable=True)
    middle_name: Mapped[str | None] = mapped_column(String, nullable=True)
    last_name: Mapped[str | None] = mapped_column(String, nullable=True)
    is_moderated: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    group: Mapped[GroupORM | None] = relationship(
        "GroupORM",
        back_populates="students",
        lazy="joined",
    )

    def to_domain(self) -> Profile:
        return Profile(
            id=self.id,
            user_id=self.user_id,
            group_id=self.group_id,
            first_name=self.first_name,
            middle_name=self.middle_name,
            last_name=self.last_name,
        )

    @classmethod
    def from_domain(cls, profile: Profile) -> "ProfileORM":
        return cls(
            id=profile.id,
            user_id=profile.user_id,
            group_id=profile.group_id,
            first_name=profile.first_name,
            middle_name=profile.middle_name,
            last_name=profile.last_name,
        )

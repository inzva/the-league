from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.schemas.team_member_detailed import TeamMemberDetailed
from app.schemas.user_preview_profile import UserPreviewProfile


class Team(BaseModel):
    id: UUID
    creationTime: datetime
    creatorId: UUID | None
    lastModificationTime: datetime | None
    lastModifierId: UUID | None
    leadUser: UserPreviewProfile
    name: str | None
    currentUserId: UUID
    memberCount: int
    members: list[TeamMemberDetailed] | None

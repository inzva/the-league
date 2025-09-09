from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TeamMemberDetailed(BaseModel):
    userName: str | None
    name: str | None
    surname: str | None
    userId: UUID
    image: str | None
    joinedDate: datetime

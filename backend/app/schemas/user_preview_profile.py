from datetime import datetime

from pydantic import BaseModel


class UserPreviewProfile(BaseModel):
    userName: str | None
    fullName: str | None
    name: str | None
    surname: str | None
    image: str | None
    location: str | None
    about: str | None
    # gender: int | None
    # city: None
    isOnline: bool
    creationTime: datetime
    lastOnlineDate: datetime | None
    publicScore: int
    # socialAccounts: None

from datetime import datetime
from typing import List, Literal, Optional
from dataclasses import dataclass, field


@dataclass
class User:
    name: str
    userID: str
    status: str
    password: str
    userType: Literal['admin', 'normal']
    callsign: str
    latitude: float
    longitude: float
    organisation: str
    dateCreated: datetime


@dataclass
class Session:
    displayName: str
    email: str
    expiresIn: int
    idToken: str
    kind: str
    localId: str
    refreshToken: str
    registered: Optional[bool] = field(default=None)


@dataclass
class Team:
    id: str
    name: str
    color: str
    status: str
    description: str
    members: List[User]
    organisation: str
    dateEstablished: datetime


@dataclass
class Member(User):
    teamID: str
    dateAdded: datetime


@dataclass(frozen=True, order=True)
class Message:
    text: str
    senderID: str
    messageID: str
    timestamp: datetime
    image: str | None = field(default=None)
    video: str | None = field(default=None)
    containsText: bool = field(default=True)
    containsImage: bool = field(default=False)


@dataclass
class Room:
    roomID: str
    teamID: str
    messageTime: datetime
    isBroadcast: bool = field(default=False)
    lastMessage: Message | None = field(default=None)
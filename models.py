from typing import Literal

from pydantic import BaseModel
import uuid


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class Conversation(BaseModel):
    id: str = str(uuid.uuid4())
    messages: list[Message] = []

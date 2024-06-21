from datetime import datetime

from pydantic import BaseModel, ConfigDict


class NoteReq(BaseModel):
    perform: datetime

    content: str

    send_required: bool


class NoteResp(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

    user_id: int

    created: datetime

    perform: datetime

    content: str

    send_required: bool


class NotePageResp(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    notes: list[NoteResp]

    total_rows: int

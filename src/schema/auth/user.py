from pydantic import BaseModel, Field


class UserReq(BaseModel):
    tg_id: int = Field(description='telegram id', examples=[1])
    password: str = Field(description='user password', examples=['test'])


class UserResp(BaseModel):
    tg_id: int = Field(description='telegram id', examples=[1])

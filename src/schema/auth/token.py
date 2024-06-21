from pydantic import BaseModel, Field


class Login(BaseModel):
    tg_id: int = Field(description='telegram id', examples=[1])
    password: str = Field(description='user password', examples=['test'])


class Token(BaseModel):
    access_token: str = Field(description='authenticated access token', examples=['tedstfsdtfwetg1t312y3t23'])
    token_type: str = Field(description='bearer token type', examples=['Bearer'])


class Info(BaseModel):
    user_id: int = Field(gt=0, description='user id', examples=[1])
    exp: int = Field(gt=0, description='exp', examples=[12345678])

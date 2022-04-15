from enum import IntEnum
from typing import Optional
from pydantic import BaseModel, EmailStr, conint, validator
from datetime import datetime


class CreateUser(BaseModel):
    email: EmailStr
    password: str

    @validator('password')
    def good_pass(cls, v):
        if len(v) < 8 or v.isalnum():
            raise ValueError("The given password is shorter than 8 symbols or doesn't contain special characters")
        return v

class UserAfterCreate(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime

    # for converting sqlalchemy to dict
    class Config:
        orm_mode=True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


# format of body for createposts
class PostBase(BaseModel):
    title: str
    content: str
    published: bool=True

class PostResponse(PostBase):
    id: int
    published: bool
    created_at: datetime
    owner_id: int
    owner_obj: UserAfterCreate

    # for converting sqlalchemy to dict
    class Config:
        orm_mode=True

class PostOut(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode=True


class D(IntEnum):
    vote_for = 1
    vote_revert = 0

class Vote(BaseModel):
    post_id: int
    dir: D


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str]=None

    
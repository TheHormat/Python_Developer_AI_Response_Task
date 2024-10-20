from pydantic import BaseModel, ConfigDict


# User
class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    username: str
    password: str


# Post
class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    pass


class PostOut(PostBase):
    id: int
    owner_id: int
    model_config = ConfigDict(from_attributes=True)


# Comment
class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    pass


class CommentOut(CommentBase):
    id: int
    post_id: int
    owner_id: int
    model_config = ConfigDict(from_attributes=True)


class CommentCreate(BaseModel):
    content: str
    auto_reply_enabled: bool
